/**
 * Pure helpers for the /map page: tag flattening, IDF weighting,
 * weighted Jaccard similarity, and sparse KNN edge construction.
 *
 * Kept side-effect-free so the math is exhaustively unit-testable
 * in MapPage.helpers.test.ts. The page component imports these and
 * feeds the result into react-force-graph-2d.
 */

import { selectPreviewUrl } from '../utils/themedPreview';


/** Backend response shape from GET /api/specs/map. Mirrors api/schemas.py::SpecMapItem. */
export interface SpecMapItem {
  id: string;
  title: string;
  preview_url_light: string | null;
  preview_url_dark: string | null;
  quality_score: number | null;
  tags: Record<string, string[]> | null;
  impl_tags: Record<string, string[]> | null;
}

/** Resolution tiers baked by the responsive-image pipeline (responsiveImage.ts). */
export const RESOLUTION_TIERS = [400, 800, 1200] as const;
export type ResolutionTier = (typeof RESOLUTION_TIERS)[number];

/**
 * Node shape passed to ForceGraph2D. Holds a lazy collection of image variants
 * keyed by resolution tier (400/800/1200). The page populates the 400 tier
 * eagerly on load and progressively upgrades on zoom-in.
 */
export interface MapNode {
  id: string;
  title: string;
  tags: string[];
  thumbUrl: string | null;                       // base theme-aware .png URL
  imgs: Map<ResolutionTier, HTMLImageElement>;   // loaded variants
  pendingTiers: Set<ResolutionTier>;             // tiers with an in-flight fetch
  // colorBucket = primary plot_type for nodes that fall into the top-N most
  // frequent plot types; null otherwise. Drives the per-cluster border color
  // without imposing any spatial bias on the layout.
  colorBucket: string | null;
}

/** Link shape passed to ForceGraph2D. `weight` = weighted-Jaccard sim ∈ (0, 1]. */
export interface MapLink {
  source: string;
  target: string;
  weight: number;
}

/**
 * Flatten a spec's nested tag dicts to a single `category:value` string set.
 * Prefixing prevents collisions like `numeric` appearing in both `data_type`
 * and `dataprep` and gives the IDF/Jaccard math distinct tokens to weigh.
 */
export function flattenTags(spec: SpecMapItem, includeImpl = true): string[] {
  const out: string[] = [];
  const push = (dict: Record<string, string[]> | null | undefined) => {
    if (!dict) return;
    for (const [category, values] of Object.entries(dict)) {
      if (!Array.isArray(values)) continue;
      for (const v of values) {
        if (typeof v === 'string' && v.length > 0) out.push(`${category}:${v}`);
      }
    }
  };
  push(spec.tags);
  if (includeImpl) push(spec.impl_tags);
  return Array.from(new Set(out));
}

/**
 * Inverse-document-frequency weights: w_t = log(N / df_t).
 * Down-weights ubiquitous tags (`data_type:numeric` is in nearly every spec)
 * and amplifies rare ones. Returns weight ≥ 0; tags absent from the corpus
 * default to 0 when looked up.
 */
export function computeIDF(specs: SpecMapItem[]): Map<string, number> {
  const N = specs.length || 1;
  const df = new Map<string, number>();
  for (const spec of specs) {
    for (const tag of flattenTags(spec)) {
      df.set(tag, (df.get(tag) ?? 0) + 1);
    }
  }
  const idf = new Map<string, number>();
  for (const [tag, count] of df) {
    idf.set(tag, Math.log(N / count));
  }
  return idf;
}

/**
 * Per-category multiplier on top of IDF weighting. Lets us privilege some
 * tag categories over others when measuring similarity — e.g. sharing the
 * same `plot_type` should pull two specs together harder than sharing a
 * common `styling` token. Categories not listed here default to 1.0.
 */
export const CATEGORY_WEIGHT: Record<string, number> = {
  plot_type: 3,
  features: 1.5,
  data_type: 1,
  domain: 1,
  dependencies: 0.8,
  patterns: 1,
  dataprep: 1,
  techniques: 0.7,
  styling: 0.5,
};

function categoryOf(prefixedTag: string): string {
  const idx = prefixedTag.indexOf(':');
  return idx >= 0 ? prefixedTag.slice(0, idx) : '';
}

function tagWeight(tag: string, idf: Map<string, number>): number {
  return (idf.get(tag) ?? 0) * (CATEGORY_WEIGHT[categoryOf(tag)] ?? 1);
}

/**
 * Weighted Jaccard similarity over two tag sets.
 *   sim = Σ w_t for t∈a∩b / Σ w_t for t∈a∪b
 * Per-tag weight = IDF × CATEGORY_WEIGHT[category prefix], so the contribution
 * of a shared tag depends both on its rarity in the corpus and on which
 * category it belongs to. Returns 0 when either set is empty or denominator
 * collapses to zero.
 */
export function weightedJaccard(a: string[], b: string[], idf: Map<string, number>): number {
  if (a.length === 0 || b.length === 0) return 0;
  const setA = new Set(a);
  const setB = new Set(b);
  let num = 0;
  let denom = 0;
  const seen = new Set<string>();
  for (const t of setA) {
    seen.add(t);
    const w = tagWeight(t, idf);
    denom += w;
    if (setB.has(t)) num += w;
  }
  for (const t of setB) {
    if (seen.has(t)) continue;
    denom += tagWeight(t, idf);
  }
  return denom > 0 ? num / denom : 0;
}

/**
 * Build a sparse KNN link list: each spec keeps its top-K most similar
 * neighbors above `minSim`. Output is deduplicated (no A→B + B→A pair) and
 * symmetric — the link with the higher weight wins on tie.
 *
 * With ~327 specs × K=5 the result is ~1.6k edges: dense enough for
 * cohesive clustering, sparse enough to avoid hairball rendering.
 */
export function buildKNNLinks(
  specs: SpecMapItem[],
  idf: Map<string, number>,
  k = 5,
  minSim = 0.05
): MapLink[] {
  const tagsByIdx = specs.map(s => flattenTags(s));
  const linkSet = new Map<string, MapLink>();
  for (let i = 0; i < specs.length; i++) {
    const sims: { j: number; sim: number }[] = [];
    for (let j = 0; j < specs.length; j++) {
      if (i === j) continue;
      const sim = weightedJaccard(tagsByIdx[i], tagsByIdx[j], idf);
      // sim > 0 drops zero-weight links (no shared tags or all-zero IDF) — pure visual noise.
      if (sim > 0 && sim >= minSim) sims.push({ j, sim });
    }
    sims.sort((x, y) => y.sim - x.sim);
    for (const { j, sim } of sims.slice(0, k)) {
      const a = specs[i].id;
      const b = specs[j].id;
      const key = a < b ? `${a}|${b}` : `${b}|${a}`;
      const existing = linkSet.get(key);
      if (!existing || sim > existing.weight) {
        linkSet.set(key, { source: a < b ? a : b, target: a < b ? b : a, weight: sim });
      }
    }
  }
  return Array.from(linkSet.values());
}

/**
 * Pick the theme-aware base preview URL (the original `.png`). Variant
 * selection happens at draw time via {@link buildVariantUrl} + {@link pickTier}
 * so we only fetch higher-resolution thumbnails for nodes the user actually
 * zooms into.
 */
export function selectMapThumbUrl(spec: SpecMapItem, isDark: boolean): string | null {
  return selectPreviewUrl(spec, isDark);
}

/**
 * Derive the URL of a specific resolution variant from the base `.png` URL.
 * `.../plot-light.png` + 800 → `.../plot-light_800.webp`. Returns the original
 * URL unchanged if it doesn't end in `.png` (no variants available).
 */
export function buildVariantUrl(baseUrl: string, tier: ResolutionTier): string {
  if (!baseUrl.endsWith('.png')) return baseUrl;
  return baseUrl.replace(/\.png$/, `_${tier}.webp`);
}

/**
 * Pick the smallest pipeline tier whose source resolution comfortably covers
 * the requested device-pixel size. Source needs to be ≥ device pixels for
 * crisp rendering — we add a small headroom factor so a tiny zoom-in nudge
 * doesn't immediately re-fetch the next tier.
 */
export function pickTier(devicePxSize: number): ResolutionTier {
  const HEADROOM = 1.25;
  const target = devicePxSize * HEADROOM;
  if (target <= 400) return 400;
  if (target <= 800) return 800;
  return 1200;
}

/**
 * Return the highest-resolution tier that's already loaded and at least as
 * big as `desired`. Falls back to a smaller tier if nothing larger is loaded
 * yet (better than blank during the lazy upgrade).
 */
export function pickBestLoadedTier(
  imgs: Map<ResolutionTier, HTMLImageElement>,
  desired: ResolutionTier
): HTMLImageElement | null {
  for (const t of RESOLUTION_TIERS) {
    if (t >= desired && imgs.has(t)) return imgs.get(t)!;
  }
  for (let i = RESOLUTION_TIERS.length - 1; i >= 0; i--) {
    const t = RESOLUTION_TIERS[i];
    if (imgs.has(t)) return imgs.get(t)!;
  }
  return null;
}

/**
 * Pick a spec's primary plot type. We use the first entry of the spec-level
 * `plot_type` tag list — that's the canonical type the spec is filed under.
 * Specs without any plot_type fall into a synthetic "other" cluster.
 */
export function primaryPlotType(spec: SpecMapItem): string {
  return spec.tags?.plot_type?.[0] ?? 'other';
}

/**
 * Return the top-N most frequent primary plot types in the corpus, sorted by
 * count descending (alphabetic name as tiebreaker for determinism). Used to
 * decide which buckets earn a distinct color border in the map.
 *
 * Excludes the synthetic `other` bucket (which only appears when a spec has
 * no plot_type tag at all) so it never wastes a color slot.
 */
export function topPlotTypes(specs: SpecMapItem[], n: number): string[] {
  const counts = new Map<string, number>();
  for (const s of specs) {
    const pt = primaryPlotType(s);
    if (pt === 'other') continue;
    counts.set(pt, (counts.get(pt) ?? 0) + 1);
  }
  return Array.from(counts.entries())
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, n)
    .map(([t]) => t);
}

/**
 * Read a node's intrinsic aspect ratio (width/height) from any already-loaded
 * thumbnail variant. Defaults to 1 when nothing is loaded yet (and the page
 * draws a square fallback rect anyway). Most plots are 16:9 (figsize=(16,9)),
 * so the typical return value is ~1.78.
 */
export function nodeAspectRatio(node: MapNode): number {
  for (const t of RESOLUTION_TIERS) {
    const img = node.imgs.get(t);
    if (img && img.naturalWidth > 0 && img.naturalHeight > 0) {
      return img.naturalWidth / img.naturalHeight;
    }
  }
  return 1;
}

/**
 * Given a target box size and an aspect ratio, return the (width, height) that
 * fits inside the box without distortion (longer side = boxSize). Used for both
 * canvas drawing and hit-area painting so they always agree.
 */
export function fitToBox(boxSize: number, aspectRatio: number): { w: number; h: number } {
  if (!isFinite(aspectRatio) || aspectRatio <= 0) return { w: boxSize, h: boxSize };
  if (aspectRatio >= 1) return { w: boxSize, h: boxSize / aspectRatio };
  return { w: boxSize * aspectRatio, h: boxSize };
}

/**
 * Lazily fetch the requested tier for a node and call `onLoad` when it lands.
 * Idempotent — safe to call repeatedly from `nodeCanvasObject` on every paint.
 * force-graph only invokes that callback for visible nodes, so off-screen
 * specs never trigger a higher-tier fetch.
 */
export function ensureNodeTier(
  node: MapNode,
  tier: ResolutionTier,
  onLoad: () => void
): void {
  if (!node.thumbUrl) return;
  if (node.imgs.has(tier) || node.pendingTiers.has(tier)) return;
  node.pendingTiers.add(tier);
  const img = document.createElement('img');
  img.onload = () => {
    node.imgs.set(tier, img);
    node.pendingTiers.delete(tier);
    onLoad();
  };
  img.onerror = () => {
    node.pendingTiers.delete(tier);
  };
  img.src = buildVariantUrl(node.thumbUrl, tier);
}

/**
 * Eager-preload every node's thumbnail at the smallest tier (400 px wide ≈ 6 KB
 * webp). Resolves once all images either loaded or errored — failures are
 * swallowed (the node renders as a plain dot in the fallback path).
 *
 * `onLoad` fires per-image so the page can call fgRef.refresh() to re-paint
 * without re-running the simulation, producing the "thumbnails pop in
 * organically" UX rather than a blocking wait. Higher-resolution tiers are
 * lazy-loaded on demand by {@link ensureNodeTier} from `nodeCanvasObject`
 * when the user zooms in.
 */
export async function preloadImages(
  items: { id: string; thumbUrl: string | null }[],
  onLoad?: (id: string, tier: ResolutionTier, img: HTMLImageElement) => void
): Promise<Map<string, HTMLImageElement>> {
  const out = new Map<string, HTMLImageElement>();
  const tier: ResolutionTier = 400;
  await Promise.all(
    items.map(({ id, thumbUrl }) => {
      if (!thumbUrl) return Promise.resolve();
      return new Promise<void>(resolve => {
        // document.createElement is preferred over `new Image()` here only because
        // some lint configs don't surface browser globals on plain .ts files.
        const img = document.createElement('img');
        // Intentionally NOT setting img.crossOrigin: the GCS bucket has no CORS
        // headers, and adding crossOrigin='anonymous' triggers a preflight that
        // fails. We only ever drawImage() these onto the canvas (the canvas
        // becomes "tainted", which is fine — we never read it back).
        img.onload = () => {
          out.set(id, img);
          onLoad?.(id, tier, img);
          resolve();
        };
        img.onerror = () => resolve();
        img.src = buildVariantUrl(thumbUrl, tier);
      });
    })
  );
  return out;
}
