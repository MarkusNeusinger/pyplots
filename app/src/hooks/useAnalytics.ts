import { useCallback, useRef, useMemo } from 'react';

interface EventProps {
  [key: string]: string | undefined;
}

function debounce<T extends (...args: unknown[]) => void>(fn: T, delay: number) {
  let timeoutId: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

// Konvertiert Query-Params zu Pfad-Segmenten für Plausible
// /?spec=scatter&tag=finance → /spec/scatter/tag/finance
function buildPlausibleUrl(): string {
  const params = new URLSearchParams(window.location.search);
  const segments: string[] = [];

  // Definierte Reihenfolge der Params (spec/library zuerst, dann alphabetisch)
  const orderedKeys = ['spec', 'library'];
  const otherKeys = Array.from(params.keys())
    .filter((k) => !orderedKeys.includes(k))
    .sort();

  for (const key of [...orderedKeys, ...otherKeys]) {
    const value = params.get(key);
    if (value) {
      segments.push(key, value);
    }
  }

  return segments.length > 0 ? `https://pyplots.ai/${segments.join('/')}` : 'https://pyplots.ai/';
}

export function useAnalytics() {
  const lastPageviewRef = useRef<string>('');
  const isProduction = typeof window !== 'undefined' && window.location.hostname === 'pyplots.ai';

  const sendPageview = useCallback(() => {
    if (!isProduction) return;

    const url = buildPlausibleUrl();
    if (url === lastPageviewRef.current) return;
    lastPageviewRef.current = url;

    window.plausible?.('pageview', { url });
  }, [isProduction]);

  const trackPageview = useMemo(() => debounce(sendPageview, 300), [sendPageview]);

  const trackEvent = useCallback(
    (name: string, props?: EventProps) => {
      if (!isProduction) return;
      const cleanProps = props
        ? Object.fromEntries(Object.entries(props).filter(([, v]) => v !== undefined))
        : undefined;
      window.plausible?.(name, cleanProps ? { props: cleanProps as Record<string, string> } : undefined);
    },
    [isProduction]
  );

  return { trackPageview, trackEvent };
}
