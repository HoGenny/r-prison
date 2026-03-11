# Frontend Lint & Format Guide
*TypeScript, ESLint, Prettier*를 사용하여 코드 품질을 관리합니다.

## ✅ 필수 설정
- VS Code Extension: ESLint, Prettier - Code formatter 설치 필수.

- Auto Fix: 파일을 저장(Ctrl+S)하면 타입 오류를 제외한 스타일 및 문법 오류가 자동 수정됩니다.

## 🛠 명령어

### Lint 체크
```bash
npx eslint .
```

### Style 수정
```bash
npx prettier --write .
```