import { useEffect, useState } from 'react';

const API_URL = 'https://api.github.com/repos/MarkusNeusinger/anyplot/releases/latest';
const CACHE_KEY = 'anyplot:latest-release';
const TTL_MS = 24 * 60 * 60 * 1000;

type Cached = { tag: string; ts: number };

function readCache(): string | null {
  try {
    const raw = localStorage.getItem(CACHE_KEY);
    if (!raw) return null;
    const parsed: Cached = JSON.parse(raw);
    if (parsed?.tag && Date.now() - parsed.ts < TTL_MS) return parsed.tag;
  } catch {
    /* ignore */
  }
  return null;
}

export function useLatestRelease(): string | null {
  const [tag, setTag] = useState<string | null>(readCache);

  useEffect(() => {
    if (readCache()) return;
    let cancelled = false;
    fetch(API_URL)
      .then((r) => (r.ok ? r.json() : null))
      .then((data) => {
        if (cancelled) return;
        const name: string | undefined = data?.tag_name;
        if (!name) return;
        setTag(name);
        try {
          localStorage.setItem(CACHE_KEY, JSON.stringify({ tag: name, ts: Date.now() } satisfies Cached));
        } catch {
          /* ignore */
        }
      })
      .catch(() => {
        /* offline / rate-limited — fallback stays */
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return tag;
}
