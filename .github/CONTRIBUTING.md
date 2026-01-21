# Contributing Guide (팀 협업 표준)

이 문서는 **Git으로 협업할 때의 규칙**을 정의합니다.  
목표는 다음 3가지입니다.

- ✅ main 브랜치 안정성 유지
- ✅ 충돌(conflict) 최소화
- ✅ 누구나 이해 가능한 히스토리(커밋/PR) 유지

---

## 0. 우리 팀 원칙

- **main에는 직접 push 금지**
- **모든 작업은 브랜치에서**
- **PR → 리뷰 승인 → Merge**

---

## 1. 브랜치 전략 규칙

### ✅ 핵심 규칙
1. **main 브랜치에는 절대 직접 push 하지 않는다.**
2. 모든 작업은 **main에서 새 브랜치를 따서 진행한다.**
3. 작업이 끝나면 **PR(Pull Request) 생성 → 팀원 승인 후 Merge**한다.

### ✅ Merge 방식
- **Squash and merge**
  - PR 안의 여러 커밋을 **하나로 합쳐서** main에 반영

---

## 2. 브랜치 이름 규칙

### ✅ 기본 형식 (필수)
- `feature/기능이름`
- 영어 소문자 + 하이픈(-) 사용

### ✅ 예시
- `feature/login`
- `feature/map-view`
- `feature/user-profile`

### ❌ 금지 예시
- `feature/Login` (대문자)
- `login-feature` (형식 불일치)
- `feature_map` (언더바 사용)

### 🟨 확장 가능한 접두어
> 원칙적으로는 `feature/`만 써도 됩니다.  
> 기능이 명확히 다르면 아래 접두어를 써도 됩니다.

- `fix/` : 버그 수정
- `docs/` : 문서 작업
- `refactor/` : 리팩토링
- `chore/` : 설정/잡일

예시:
- `fix/login-redirect`
- `docs/api-spec`

---

## 3. 작업 시작

### ✅ 1) main 최신화
```bash
git checkout main
git pull origin main
```

### ✅ 2) 브랜치 생성
```bash
git checkout -b feature/기능이름
```

### ✅ 3) 작업 → 커밋
```bash
git add .
git commit -m "Feat: 로그인 UI 추가"
```

### ✅ 4) 원격 저장소로 푸시
```bash
git push origin feature/기능이름
```

### ✅ 5) PR 생성
- GitHub에서 PR 생성
- 리뷰 요청(Reviewers) 지정
- 승인 받은 뒤 Merge

---

## 4. PR(Pull Request) 규칙

### ✅ PR 원칙
- PR 하나는 **목적 하나(기능 하나)** 를 담는다.
- PR은 **짧을수록 리뷰가 쉽다.**
  - 권장: 300줄 이하(가능하면)

### ✅ 승인 규칙
- PR은 **최소 1명 이상 승인** 후 Merge
- Merge 전 반드시 **충돌(conflict) 여부 확인**
- Merge 후 브랜치는 **삭제(Delete branch)** 권장

### ✅ PR 제목 규칙
PR 제목은 “무슨 작업인지” 한 줄로 명확히 작성

예시:
- `Login 기능 구현`
- `지도 화면 UI 추가`
- `프로필 수정 API 연결`

---

## 5. PR 템플릿 사용 규칙

PR을 만들면 자동으로 템플릿이 뜹니다.  
**작업 내용/테스트 방법은 필수로 작성**합니다.

---

## 6. 커밋 메시지 규칙

### ✅ 커밋 메시지 작성 규칙
1. 제목과 본문을 **빈 줄로 구분**
2. 제목은 **50글자 이내**
3. 제목 첫 글자는 **대문자**
4. 제목 끝에 **마침표 금지**
5. 제목은 **명령문**, 과거형 금지
6. 본문 각 줄은 **72글자 이내**
7. “어떻게”보다 **무엇/왜**를 설명

---

## 7. 커밋 메시지 구조

```text
타입(스코프): 주제(제목)

본문

바닥글
```

- Body는 Header로 부족할 때만 작성
- Footer는 이슈 참조가 필요할 때만 작성

---

## 8. 커밋 타입 정의

| 타입 | 의미 |
|------|------|
| Feat | 새로운 기능 추가 |
| Fix | 버그 수정 |
| Build | 빌드/의존성 관련 수정 |
| Chore | 자잘한 수정 |
| Ci | CI 설정 변경 |
| Docs | 문서 수정 |
| Style | 코드 스타일/포맷 변경 |
| Refactor | 기능 변화 없는 구조 개선 |
| Test | 테스트 코드 수정 |
| Perf | 성능 개선 |

### 🟨 (선택) 스코프(scope) 사용 규칙
> 스코프는 “어떤 영역인지” 표시합니다.

예시:
- `Feat(auth): 로그인 API 요청 기능 추가`
- `Fix(map): 마커 중복 노출 방지`
- `Refactor(ui): 모달 컴포넌트 로직 간소화`

---

## 9. 커밋 예시

### ✅ Header만 작성하는 경우 (추천)
```text
Feat: 로그인 API 요청 기능 추가
```

### ✅ Body 포함 예시
```text
Fix: 토큰 응답값 null 처리 로직 수정

로그인 API에서 토큰이 null로 반환될 때 앱이 강제 종료되는 문제 방지.
실패 시 에러 메시지를 띄우고 로그인 페이지로 이동하도록 변경함.
```

### ✅ Footer 포함 예시
```text
Feat: 지도 마커 렌더링 기능 추가

서버에서 받아온 위도/경도 데이터를 사용하여 지도 위에 마커(핀)을 표시함.

Closes #12
```

---

## 10. 협업 운영 규칙

### ✅ 코어 타임 정하기
- 팀원 모두 겹치는 시간을 정해서 소통한다.
- 예시) 주 3회 1시간
  - `월/수/금 21:00 ~ 22:00`

코어타임에서 하는 것:
- 오늘 작업 목표 공유 (각자 1분)
- 막힌 부분 요청 (서로 10분 디버깅)
- PR 리뷰/머지 처리

### ✅ 작업 공유 최소 단위
- “오늘 할 일”을 이슈/노션/디스코드에 1줄로 남긴다.
- 예: `로그인 버튼 클릭 시 API 연결하고 토큰 저장까지`

---

## 11. 주석 규칙

### ✅ 주석은 “의도 설명”
복잡한 로직 위에는 “왜 이 코드가 필요한지” 한글로 작성

✅ 좋은 예시:
```js
// 여기서 위도/경도 좌표를 받아서 지도에 마커를 생성함
```

❌ 나쁜 예시:
```js
// marker 생성
```

---

## 12. PR 올리기 전 체크리스트 ✅

PR 생성 전 반드시 확인:

- [ ] `git pull origin main` 반영했는가?
- [ ] 충돌(conflict)이 없는가?
- [ ] 프로젝트 실행/빌드가 정상인가?
- [ ] 불필요한 console.log / print 제거했는가?
- [ ] 커밋 메시지 규칙을 지켰는가?
- [ ] PR 설명/테스트 방법을 적었는가?

---

## 13. 충돌(conflict) 발생 시 해결 흐름

> 가급적 rebase보다 **merge로 해결**

### ✅ 1) main 최신화
```bash
git checkout main
git pull origin main
```

### ✅ 2) 내 브랜치로 이동
```bash
git checkout feature/기능이름
```

### ✅ 3) main을 내 브랜치로 merge
```bash
git merge main
```

### ✅ 4) 충돌 해결 후 커밋/푸시
```bash
git add .
git commit -m "Chore: 머지 충돌 해결"
git push origin feature/기능이름
```

---

## 14. Definition of Done (완료 기준)

작업이 “끝났다”고 말하려면 아래를 만족해야 합니다.

- [ ] 기능이 요구사항대로 동작한다
- [ ] 에러 상황을 최소 1개 이상 처리했다
- [ ] 관련 UI/로직이 깨지지 않는다
- [ ] PR 설명 + 테스트 방법이 있다
- [ ] 팀원이 봐도 이해 가능한 코드/주석이다

---

## 15. 금지 사항 🚫 (실수 방지용)

- main에 직접 push 금지
- 여러 기능을 한 PR에 섞지 않기
- 의미 없는 커밋 금지 (`update`, `fix`, `asdf` 등)
- 남의 브랜치에서 직접 작업하지 않기
- 승인 없이 Merge 하지 않기

---

## 16. (권장) GitHub Repository 설정

- main 브랜치 보호(Branch protection)
  - ✅ Require pull request before merging
  - ✅ Require approvals (1명 이상)
  - ✅ Restrict who can push to main
  - ✅ Require status checks (선택)

---

## 17. 도움이 되는 습관

- 작은 단위로 자주 커밋하기
- PR 하나 = 목적 하나
- PR 설명은 “공유 문서”라고 생각하기
