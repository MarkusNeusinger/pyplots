const LANG_PREFIX = '/python';

export function specPath(specId: string, library?: string): string {
  return library ? `${LANG_PREFIX}/${specId}/${library}` : `${LANG_PREFIX}/${specId}`;
}

export function interactivePath(specId: string, library: string): string {
  return `${LANG_PREFIX}/interactive/${specId}/${library}`;
}

export function langPrefix(): string {
  return LANG_PREFIX;
}
