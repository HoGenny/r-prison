# Git 협업 규칙

> 자세한 규칙은 [CONTRIBUTING.md](./.github/CONTRIBUTING.md)를 참고하세요.

## 브랜치 정책
- main 브랜치에는 직접 push 하지 않습니다.
- 모든 작업은 `feature/기능이름` 브랜치에서 수행합니다.
- 작업 완료 후 PR 생성 → 리뷰 승인 후 Merge 합니다.

## 커밋 메시지 예시
- `Feat: 로그인 API 요청 기능 추가`
- `Fix: 토큰 응답값 null 처리 로직 수정`
- `Docs: API 엔드포인트 목록 업데이트`

## PR 규칙
- PR 하나는 목적 하나(기능 하나)
- 최소 1명 승인 후 Merge
- Squash and merge 권장
