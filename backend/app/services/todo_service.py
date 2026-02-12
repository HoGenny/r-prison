from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta

from app.schemas.todo import TodoCreate, TodoUpdate
from app.models.todo import Todo
from app.core.errors import AppError
from app.models.rp import RPTransaction # rp 획득 로그
from app.models.user import User # User 모델
from app.models.stats import DailyStat # 한 User의 하루 활동량

class TodoService:
    async def list_todos(self, session: AsyncSession, user_id: int) -> list[Todo]: # 유저의 todo list 목록 조회
        stmt = (
          select(Todo)
          .where(
            Todo.user_id == user_id,
            Todo.deleted_at.is_(None),
          )
          .order_by(Todo.scheduled_for.asc())
        )

        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def get_todo(self, session: AsyncSession, user_id: int, todo_id: int) -> Todo: # todo 1건 상세 검색
        stmt = (
            select(Todo)
            .where(
                Todo.id == todo_id,
                Todo.user_id == user_id,
                Todo.deleted_at.is_(None),
            )
        )

        result = await session.execute(stmt)
        todo = result.scalar_one_or_none()

        if todo is None :
            raise AppError("Todo 조회 불가", status_code=404, code="not found")
        
        return todo
      

    async def create_todo(self, session: AsyncSession, user_id: int, data: TodoCreate) -> Todo: # todo 생성 
        content = data.content.strip()
        if not content:
            raise AppError("제목 필수", status_code=422, code="invalid_request")

        async with session.begin():
            todo = Todo(
                user_id = user_id,
                content = content,
                description = data.description,
                scheduled_for = data.scheduled_for,
                due_at = data.due_at,
                difficulty = data.difficulty if data.difficulty is not None else 1,
                category = data.category if data.category is not None else "general",
                reward_rp = data.reward_rp if data.reward_rp is not None else 0,
            )

            session.add(todo)
            await session.flush() 

            return todo
    
    async def update_todo(self, session: AsyncSession, user_id: int, todo_id: int, data: TodoUpdate) -> Todo: # todo 수정
        todo = await self.get_todo(session, user_id, todo_id)

        async with session.begin():
            if data.content is not None:
                todo.content = data.content.strip()
            
            if data.description is not None:
                todo.description = data.description

            if data.scheduled_for is not None:
                todo.scheduled_for = data.scheduled_for

            if data.due_at is not None:
                todo.due_at = data.due_at
            
            if data.category is not None:
                todo.category = data.category
            
            await session.flush()
        
        return todo
    
    async def delete_todo(self, session: AsyncSession, user_id: int, todo_id: int) -> None: # todo 삭제(soft delete)
        todo = await self.get_todo(session, user_id, todo_id)

        async with session.begin():
            todo.deleted_at = datetime.now(timezone.utc)

            await session.flush()


    # todo 완료 처리 로직
    # 0. 이미 완료된 todo 인지 확인(그럴 시 409)
    # 1. 완료 처리
    # 2. rp 로그에 기록
    # 3. User 테이블 rp, rp_blance에 추가 
    # 4. stats(하루 활동량 기록 로그)에 추가
    async def complete_todo(self, session: AsyncSession, user_id: int, todo_id: int) -> None: # todo 완료 처리  
        todo = await self.get_todo(session, user_id, todo_id)

        if todo.completed_at is not None :
            raise AppError("이미 완료된 항목", status_code=409, code="already_completed")

        async with session.begin():
            now = datetime.now(timezone.utc)

            # 1. 완료처리
            todo.completed_at = now

            # 2. rp 기록
            session.add(
                RPTransaction(
                    user_id = user_id,
                    delta = todo.reward_rp,
                    reason = "todo_complete",
                    ref_type = "todo",
                    ref_id = todo.id,
                )
            )

            # 3. User 조회 및 잔액 증가
            result = await session.execute(
                select(User).where(User.id == user_id)
            )

            user = result.scalar_one()

            user.rp_balance += todo.reward_rp # 유저가 모은 총 rp
            user.rp += todo.reward_rp # 유저가 현재 들고있는 rp

            # 4. stats(하루 단위 활동량 로그) 기존에 있으면 추가, 없으면 새로 생성성
            stmt = select(DailyStat).where(
                DailyStat.user_id == user_id,
                DailyStat.date == todo.scheduled_for,
            )

            result = await session.execute(stmt)
            stat = result.scalar_one_or_none()

            if stat is None:
                yesterday = todo.scheduled_for - timedelta(days=1) # 연속도전 계산을 위한 어제 연속일 계산
            
                y_stmt = select(DailyStat).where(
                    DailyStat.user_id == user_id,
                    DailyStat.date == yesterday,
                )

                y_result = await session.execute(y_stmt)
                yesterday_stat = y_result.scalar_one_or_none()

                if yesterday_stat:
                    streak = yesterday_stat.streak_day + 1
                else:
                    streak = 1

                stat = DailyStat(
                    user_id = user_id,
                    date = todo.scheduled_for,
                    todos_completed=1,
                    rp_earned=todo.reward_rp,
                    streak_day=streak,
                )

                session.add(stat)
            
            else :
                stat.todos_completed += 1
                stat.rp_earned += todo.reward_rp

    # todo 완료 취소 처리 로직
    # 0. 이미 미완료(todo.completed_at is None)면 409
    # 1. completed_at = None
    # 2. rp 로그에 기록 (delta = -reward_rp)
    # 3. User 테이블 rp, rp_balance 감소
    # 4. stats(하루 활동량 기록 로그) 감소
    async def uncomplete_todo(self, session: AsyncSession, user_id: int, todo_id: int) -> None:
        todo = await self.get_todo(session, user_id, todo_id)

        if todo.completed_at is None:
            raise AppError("이미 미완료된 항목", status_code=409, code="already_uncompleted")

        async with session.begin():

            # 1. 완료 취소
            todo.completed_at = None

            # 2. RP 회수 로그 (음수)
            session.add(
                RPTransaction(
                    user_id=user_id,
                    delta=-todo.reward_rp,
                    reason="todo_uncomplete",
                    ref_type="todo",
                    ref_id=todo.id,
                )
            )

            # 3. User 조회 및 잔액 감소
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one()

            # 잔액 음수 방지 정책
            if user.rp_balance < todo.reward_rp:
                raise AppError("RP 잔액이 부족하여 완료 취소할 수 없음", status_code=400, code="insufficient_rp")

            user.rp_balance -= todo.reward_rp
            
            if user.rp < todo.reward_rp:
                user.rp = 0
            else:
                user.rp -= todo.reward_rp

            # 4. daily_stats 감소
            stmt = select(DailyStat).where(
                DailyStat.user_id == user_id,
                DailyStat.date == todo.scheduled_for,
            )
            result = await session.execute(stmt)
            stat = result.scalar_one_or_none()

            if stat is None:
                # complete 했던 기록이 있는데 stat이 없다면 데이터가 깨진 상태
                raise AppError("DailyStat not found for uncomplete", status_code=400, code="stat_missing")

            # 감소
            if stat.todos_completed <= 0 or stat.rp_earned < todo.reward_rp:
                raise AppError("DailyStat underflow", status_code=400, code="stat_underflow")

            stat.todos_completed -= 1
            stat.rp_earned -= todo.reward_rp


todo_service = TodoService()
