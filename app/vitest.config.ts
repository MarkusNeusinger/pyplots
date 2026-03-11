import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    include: ['src/**/*.test.ts', 'src/**/*.test.tsx'],
    setupFiles: ['./src/setupTests.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      include: [
        'src/utils/**/*.ts',
        'src/hooks/**/*.ts',
        'src/components/**/*.tsx',
        'src/pages/**/*.tsx',
        'src/constants/**/*.ts',
        'src/theme/**/*.ts',
        'src/types/**/*.ts',
      ],
      exclude: ['src/**/*.test.ts', 'src/**/*.test.tsx', 'src/setupTests.ts', 'src/test-utils.tsx'],
    },
  },
});
