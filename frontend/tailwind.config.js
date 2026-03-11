/** @type {import('tailwindcss').Config} */
export const content = [
  './App.{js,jsx,ts,tsx}',
  './app/**/*.{js,jsx,ts,tsx}',
  './components/**/*.{js,jsx,ts,tsx}',
  './screens/**/*.{js,jsx,ts,tsx}',
];
export const presets = [import('nativewind/preset')];
export const theme = {
  extend: {},
};
export const plugins = [];
