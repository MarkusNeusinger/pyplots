import { render, type RenderOptions } from '@testing-library/react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { MemoryRouter } from 'react-router-dom';
import type { ReactElement, ReactNode } from 'react';

const theme = createTheme();

function AllProviders({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider theme={theme}>
      <MemoryRouter>{children}</MemoryRouter>
    </ThemeProvider>
  );
}

function customRender(ui: ReactElement, options?: Omit<RenderOptions, 'wrapper'>) {
  return render(ui, { wrapper: AllProviders, ...options });
}

export { customRender as render };
export { screen, within, waitFor, act } from '@testing-library/react';
export { default as userEvent } from '@testing-library/user-event';
