import { useEffect, useMemo, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import Typography from '@mui/material/Typography';
import ForceGraph2D from 'react-force-graph-2d';

import { API_URL } from '../constants';
import { useAnalytics } from '../hooks';
import { useTheme } from '../hooks/useLayoutContext';
import { specPath } from '../utils/paths';
import { colors, fontSize, typography } from '../theme';
import {
  buildKNNLinks,
  computeIDF,
  flattenTags,
  preloadImages,
  selectMapThumbUrl,
  type MapLink,
  type MapNode,
  type SpecMapItem,
} from './MapPage.helpers';


const NODE_SIZE = 22;            // px in graph space — ImageCard thumbnails feel right around this size
const HOVER_SCALE = 1.6;          // hovered + neighbor node bump
const COOLDOWN_TICKS = 200;       // simulation stops after settling
const KNN_K = 5;                  // edges per node in the sparse KNN graph
const KNN_MIN_SIM = 0.05;         // drop near-zero noise links

// visually-hidden style — keeps the spec list readable for screen readers
// even though the canvas is the primary interface.
const visuallyHiddenSx = {
  position: 'absolute' as const,
  width: '1px',
  height: '1px',
  padding: 0,
  margin: '-1px',
  overflow: 'hidden',
  clip: 'rect(0, 0, 0, 0)',
  whiteSpace: 'nowrap' as const,
  border: 0,
};

// Hairline border around a thumbnail node, theme-aware.
function strokeFor(isDark: boolean, isHover: boolean): string {
  if (isHover) return colors.primary;
  return isDark ? 'rgba(240,239,232,0.18)' : 'rgba(26,26,23,0.18)';
}


export function MapPage() {
  const { trackPageview, trackEvent } = useAnalytics();
  const { isDark } = useTheme();
  const navigate = useNavigate();

  // refs
  // ForceGraph2D's TypeScript surface for the imperative ref is non-trivial; the
  // generated types live in dist and aren't worth re-typing here. Treat as opaque.
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const fgRef = useRef<any>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // data state
  const [specs, setSpecs] = useState<SpecMapItem[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [size, setSize] = useState<{ w: number; h: number }>({ w: 0, h: 0 });
  const [hoverId, setHoverId] = useState<string | null>(null);

  // 1. fetch + page view
  useEffect(() => {
    trackPageview('/map');
  }, [trackPageview]);

  useEffect(() => {
    const ctrl = new AbortController();
    fetch(`${API_URL}/specs/map`, { signal: ctrl.signal })
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json() as Promise<SpecMapItem[]>;
      })
      .then(setSpecs)
      .catch(err => {
        if (err.name !== 'AbortError') setError(err.message ?? 'Failed to load map data');
      });
    return () => ctrl.abort();
  }, []);

  // 2. resize observer
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const obs = new ResizeObserver(entries => {
      const r = entries[0]?.contentRect;
      if (r) setSize({ w: r.width, h: r.height });
    });
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  // 3. derive graph data from specs/theme (pure — no setState in effect)
  const graphData = useMemo<{ nodes: MapNode[]; links: MapLink[] }>(() => {
    if (!specs) return { nodes: [], links: [] };
    const idf = computeIDF(specs);
    const nodes: MapNode[] = specs.map(s => ({
      id: s.id,
      title: s.title,
      tags: flattenTags(s),
      thumbUrl: selectMapThumbUrl(s, isDark),
    }));
    const links = buildKNNLinks(specs, idf, KNN_K, KNN_MIN_SIM);
    return { nodes, links };
  }, [specs, isDark]);

  // Preload thumbnails as a side effect; attach to nodes by reference and
  // ask force-graph to repaint without restarting the physics simulation.
  useEffect(() => {
    if (graphData.nodes.length === 0) return;
    const nodeById = new Map(graphData.nodes.map(n => [n.id, n]));
    let cancelled = false;
    preloadImages(
      graphData.nodes.map(n => ({ id: n.id, thumbUrl: n.thumbUrl })),
      (id, img) => {
        if (cancelled) return;
        const n = nodeById.get(id);
        if (n) n.img = img;
        fgRef.current?.refresh?.();
      }
    );
    return () => {
      cancelled = true;
    };
  }, [graphData]);

  // 4. neighbor lookup for hover highlight (built once per links change)
  const neighbors = useMemo(() => {
    const map = new Map<string, Set<string>>();
    for (const l of graphData.links) {
      if (!map.has(l.source)) map.set(l.source, new Set());
      if (!map.has(l.target)) map.set(l.target, new Set());
      map.get(l.source)!.add(l.target);
      map.get(l.target)!.add(l.source);
    }
    return map;
  }, [graphData.links]);

  // 5. ForceGraph2D callbacks. Types for ctx come from the wrapper's prop signature
  // when these are passed inline below — extracting them out would force us to spell
  // CanvasRenderingContext2D explicitly, which our eslint config doesn't recognize.
  type WithCoords = MapNode & { x?: number; y?: number };

  const onNodeClick = (node: MapNode) => {
    trackEvent('map_node_click', { spec_id: node.id });
    navigate(specPath(node.id));
  };

  const ready = graphData.nodes.length > 0 && size.w > 0 && size.h > 0;

  return (
    <>
      <Helmet>
        <title>map() — anyplot</title>
        <meta name="description" content="Interactive map of all anyplot specifications, clustered by tag similarity." />
      </Helmet>
      <Box
        ref={containerRef}
        // Negative margins cancel RootLayout's container px so the canvas goes full-bleed.
        // TODO: replace with a router-level layout switch (analog to mastheadSticks) once we
        // have more full-bleed pages — see issue tracking the /map rollout.
        sx={{
          mx: { xs: -2, sm: -4, md: -8, lg: -12 },
          height: { xs: 'calc(100svh - 200px)', sm: 'calc(100svh - 180px)' },
          minHeight: 480,
          position: 'relative',
          bgcolor: 'var(--bg-page)',
          overflow: 'hidden',
        }}
        role="region"
        aria-label="Force-directed map of anyplot specifications, clustered by tag similarity"
      >
        {/* Header overlay with tiny meta */}
        <Box sx={{
          position: 'absolute',
          top: { xs: 8, sm: 16 },
          left: { xs: 16, sm: 32 },
          zIndex: 2,
          fontFamily: typography.mono,
          fontSize: fontSize.xs,
          color: 'var(--ink-soft)',
          pointerEvents: 'none',
        }}>
          {specs ? `${specs.length} specs · ${graphData.links.length} edges` : ' '}
          {hoverId && (
            <Box component="span" sx={{ ml: 1.5, color: 'var(--ink)', pointerEvents: 'auto' }}>
              ❯ {graphData.nodes.find(n => n.id === hoverId)?.title}
            </Box>
          )}
        </Box>

        {/* Loading / error states */}
        {!specs && !error && (
          <Box sx={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <CircularProgress size={28} />
          </Box>
        )}
        {error && (
          <Box sx={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--ink-soft)', fontFamily: typography.mono }}>
            <Typography sx={{ fontFamily: typography.mono, fontSize: fontSize.sm }}>
              Failed to load map: {error}
            </Typography>
          </Box>
        )}

        {/* Canvas */}
        {ready && (
          <ForceGraph2D
            ref={fgRef}
            graphData={graphData}
            width={size.w}
            height={size.h}
            backgroundColor={'transparent'}
            nodeCanvasObject={(node, ctx) => {
              const n = node as WithCoords;
              if (n.x == null || n.y == null) return;
              const isHover = hoverId === n.id;
              const isNeighbor = !isHover && hoverId != null && neighbors.get(hoverId)?.has(n.id);
              const dim = hoverId != null && !isHover && !isNeighbor;
              const baseSize = NODE_SIZE * (isHover ? HOVER_SCALE : isNeighbor ? 1.15 : 1);
              const x = n.x - baseSize / 2;
              const y = n.y - baseSize / 2;

              ctx.save();
              if (dim) ctx.globalAlpha = 0.18;
              if (n.img) {
                ctx.drawImage(n.img, x, y, baseSize, baseSize);
              } else {
                ctx.fillStyle = isDark ? '#242420' : '#FFFDF6';
                ctx.fillRect(x, y, baseSize, baseSize);
              }
              ctx.lineWidth = isHover ? 2 : 1;
              ctx.strokeStyle = strokeFor(isDark, !!isHover);
              ctx.strokeRect(x, y, baseSize, baseSize);
              ctx.restore();
            }}
            nodePointerAreaPaint={(node, color, ctx) => {
              const n = node as WithCoords;
              if (n.x == null || n.y == null) return;
              ctx.fillStyle = color;
              ctx.fillRect(n.x - NODE_SIZE / 2, n.y - NODE_SIZE / 2, NODE_SIZE, NODE_SIZE);
            }}
            linkColor={(l: MapLink) => {
              const involved = hoverId && (l.source === hoverId || l.target === hoverId);
              if (involved) return colors.primary;
              if (hoverId) return isDark ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.04)';
              return isDark ? 'rgba(255,255,255,0.10)' : 'rgba(0,0,0,0.12)';
            }}
            linkWidth={(l: MapLink) => Math.max(0.5, (l.weight ?? 0.3) * 2.5)}
            onNodeClick={onNodeClick}
            onNodeHover={(n: MapNode | null) => setHoverId(n?.id ?? null)}
            cooldownTicks={COOLDOWN_TICKS}
            onEngineStop={() => fgRef.current?.zoomToFit?.(400, 40)}
          />
        )}

        {/* a11y fallback: visually-hidden list so screen readers + keyboard users
            can still reach every spec from this page. */}
        <Box component="ul" sx={visuallyHiddenSx}>
          {(specs ?? []).map(s => (
            <li key={s.id}>
              <a href={specPath(s.id)}>{s.title}</a>
            </li>
          ))}
        </Box>
      </Box>
    </>
  );
}
