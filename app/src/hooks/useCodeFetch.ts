/**
 * Hook for fetching plot code on-demand.
 *
 * Code is excluded from /plots/filter to reduce payload size (~2MB savings).
 * This hook fetches code from /specs/{spec_id} when needed.
 */

import { useState, useCallback, useRef } from 'react';
import { API_URL } from '../constants';

interface CodeCache {
  [key: string]: string | null; // key: `${spec_id}:${library}`
}

interface UseCodeFetchReturn {
  fetchCode: (specId: string, library: string) => Promise<string | null>;
  getCode: (specId: string, library: string) => string | null;
  isLoading: boolean;
}

export function useCodeFetch(): UseCodeFetchReturn {
  const [isLoading, setIsLoading] = useState(false);
  const cacheRef = useRef<CodeCache>({});
  const pendingRef = useRef<Map<string, Promise<string | null>>>(new Map());

  const getCode = useCallback((specId: string, library: string): string | null => {
    const key = `${specId}:${library}`;
    return cacheRef.current[key] ?? null;
  }, []);

  const fetchCode = useCallback(async (specId: string, library: string): Promise<string | null> => {
    const key = `${specId}:${library}`;

    // Check cache first
    if (key in cacheRef.current) {
      return cacheRef.current[key];
    }

    // Check if already fetching
    const pending = pendingRef.current.get(key);
    if (pending) {
      return pending;
    }

    // Fetch from API
    setIsLoading(true);
    const promise = (async () => {
      try {
        const response = await fetch(`${API_URL}/specs/${specId}`);
        if (!response.ok) {
          cacheRef.current[key] = null;
          return null;
        }

        const data = await response.json();
        const impl = data.implementations?.find(
          (i: { library_id: string }) => i.library_id === library
        );
        const code = impl?.code ?? null;
        cacheRef.current[key] = code;
        return code;
      } catch {
        cacheRef.current[key] = null;
        return null;
      } finally {
        pendingRef.current.delete(key);
        setIsLoading(false);
      }
    })();

    pendingRef.current.set(key, promise);
    return promise;
  }, []);

  return { fetchCode, getCode, isLoading };
}
