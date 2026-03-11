import js from '@eslint/js';
import globals from 'globals';
import tseslint from 'typescript-eslint';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import reactNative from 'eslint-plugin-react-native';
import prettierConfig from 'eslint-config-prettier';

export default tseslint.config(
  // 1. 검사 제외 대상
  {
    ignores: ['node_modules', 'dist', '.expo', 'ios', 'android', 'web-build'],
  },
  js.configs.recommended,
  ...tseslint.configs.recommended, // TS 권장 규칙 적용
  {
    files: ['**/*.{ts,tsx}'],
    plugins: {
      react,
      'react-hooks': reactHooks,
      'react-native': reactNative,
    },
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        ecmaFeatures: { jsx: true },
      },
      globals: {
        ...globals.node,
        ...reactNative.environments['react-native'].globals,
      },
    },
    settings: {
      react: { version: 'detect' },
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      // [TypeScript 전용 규칙]
      '@typescript-eslint/no-explicit-any': 'warn', // any 사용 자제 유도
      '@typescript-eslint/no-unused-vars': [
        'error',
        {
          // 미사용 변수 에러 (대문자/언더바 제외)
          varsIgnorePattern: '^[A-Z_]',
          argsIgnorePattern: '^_',
        },
      ],

      // [React Native 전용 규칙]
      'react-native/no-unused-styles': 'error', // 안 쓰는 StyleSheet 정리
      'react-native/no-inline-styles': 'warn', // 인라인 스타일 지양 (StyleSheet 권장)
      'react-native/no-raw-text': 'off', // Text 컴포넌트 외 텍스트 허용 여부

      'react/prop-types': 'off', // TS가 타입을 잡으므로 필요 없음
    },
  },
  prettierConfig, // 마지막에 배치하여 스타일 충돌 방지
);
