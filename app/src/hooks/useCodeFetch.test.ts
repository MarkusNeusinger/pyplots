import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useCodeFetch } from './useCodeFetch';

describe('useCodeFetch', () => {
  beforeEach(() => {
    vi.spyOn(globalThis, 'fetch');
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  function mockFetchResponse(data: unknown, ok = true) {
    (globalThis.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok,
      json: () => Promise.resolve(data),
    });
  }

  const apiResponse = {
    implementations: [
      { library_id: 'matplotlib', code: 'import matplotlib\nfig, ax = plt.subplots()' },
      { library_id: 'seaborn', code: 'import seaborn as sns\nsns.heatmap(data)' },
    ],
  };

  describe('getCode', () => {
    it('returns null for uncached entries', () => {
      const { result } = renderHook(() => useCodeFetch());
      expect(result.current.getCode('scatter-basic', 'matplotlib')).toBeNull();
    });

    it('returns cached code after successful fetch', async () => {
      mockFetchResponse(apiResponse);
      const { result } = renderHook(() => useCodeFetch());

      await act(async () => {
        await result.current.fetchCode('scatter-basic', 'matplotlib');
      });

      expect(result.current.getCode('scatter-basic', 'matplotlib')).toBe(
        'import matplotlib\nfig, ax = plt.subplots()'
      );
    });
  });

  describe('fetchCode', () => {
    it('fetches code from API and returns it', async () => {
      mockFetchResponse(apiResponse);
      const { result } = renderHook(() => useCodeFetch());

      let code: string | null = null;
      await act(async () => {
        code = await result.current.fetchCode('scatter-basic', 'matplotlib');
      });

      expect(code).toBe('import matplotlib\nfig, ax = plt.subplots()');
      expect(globalThis.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/specs/scatter-basic')
      );
    });

    it('returns cached result on second call without re-fetching', async () => {
      mockFetchResponse(apiResponse);
      const { result } = renderHook(() => useCodeFetch());

      await act(async () => {
        await result.current.fetchCode('scatter-basic', 'matplotlib');
      });

      let code: string | null = null;
      await act(async () => {
        code = await result.current.fetchCode('scatter-basic', 'matplotlib');
      });

      expect(code).toBe('import matplotlib\nfig, ax = plt.subplots()');
      expect(globalThis.fetch).toHaveBeenCalledTimes(1);
    });

    it('deduplicates concurrent requests for the same key', async () => {
      mockFetchResponse(apiResponse);
      const { result } = renderHook(() => useCodeFetch());

      await act(async () => {
        const [code1, code2] = await Promise.all([
          result.current.fetchCode('scatter-basic', 'matplotlib'),
          result.current.fetchCode('scatter-basic', 'matplotlib'),
        ]);
        expect(code1).toBe(code2);
      });

      expect(globalThis.fetch).toHaveBeenCalledTimes(1);
    });

    it('returns null when API responds with non-ok status', async () => {
      mockFetchResponse(null, false);
      const { result } = renderHook(() => useCodeFetch());

      let code: string | null = 'initial';
      await act(async () => {
        code = await result.current.fetchCode('missing-spec', 'matplotlib');
      });

      expect(code).toBeNull();
    });

    it('returns null when implementation is not found for library', async () => {
      mockFetchResponse({ implementations: [{ library_id: 'plotly', code: 'plotly code' }] });
      const { result } = renderHook(() => useCodeFetch());

      let code: string | null = 'initial';
      await act(async () => {
        code = await result.current.fetchCode('scatter-basic', 'matplotlib');
      });

      expect(code).toBeNull();
    });

    it('returns null and caches on network error', async () => {
      (globalThis.fetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(new Error('Network error'));
      const { result } = renderHook(() => useCodeFetch());

      let code: string | null = 'initial';
      await act(async () => {
        code = await result.current.fetchCode('scatter-basic', 'matplotlib');
      });

      expect(code).toBeNull();
      // Subsequent call should return cached null without fetching
      await act(async () => {
        code = await result.current.fetchCode('scatter-basic', 'matplotlib');
      });
      expect(globalThis.fetch).toHaveBeenCalledTimes(1);
    });

    it('manages isLoading state during fetch', async () => {
      mockFetchResponse(apiResponse);
      const { result } = renderHook(() => useCodeFetch());

      expect(result.current.isLoading).toBe(false);

      await act(async () => {
        await result.current.fetchCode('scatter-basic', 'matplotlib');
      });

      expect(result.current.isLoading).toBe(false);
    });

    it('fetches different libraries independently', async () => {
      mockFetchResponse(apiResponse);
      mockFetchResponse(apiResponse);
      const { result } = renderHook(() => useCodeFetch());

      let mplCode: string | null = null;
      let snsCode: string | null = null;
      await act(async () => {
        mplCode = await result.current.fetchCode('scatter-basic', 'matplotlib');
      });
      await act(async () => {
        snsCode = await result.current.fetchCode('scatter-basic', 'seaborn');
      });

      expect(mplCode).toContain('matplotlib');
      expect(snsCode).toContain('seaborn');
      expect(globalThis.fetch).toHaveBeenCalledTimes(2);
    });
  });
});
