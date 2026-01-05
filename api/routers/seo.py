"""SEO endpoints (sitemap, bot-optimized pages)."""

import html

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.cache import cache_key, get_cache, set_cache
from api.dependencies import optional_db
from core.database import SpecRepository


router = APIRouter(tags=["seo"])


# Minimal HTML template for social media bots (meta tags are what matters)
BOT_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>{title}</title>
    <meta name="description" content="{description}" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:image" content="{image}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="pyplots.ai" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />
    <meta name="twitter:image" content="{image}" />
    <link rel="canonical" href="{url}" />
</head>
<body><h1>{title}</h1><p>{description}</p></body>
</html>"""

DEFAULT_IMAGE = "https://pyplots.ai/og-image.png"
DEFAULT_DESCRIPTION = "Library-agnostic, AI-powered Python plotting examples. Automatically generated, tested, and maintained."


@router.get("/sitemap.xml")
async def get_sitemap(db: AsyncSession | None = Depends(optional_db)):
    """
    Generate dynamic XML sitemap for SEO.

    Includes root, catalog page, and all specs with implementations.
    """
    key = cache_key("sitemap_xml")
    cached = get_cache(key)
    if cached:
        return Response(content=cached, media_type="application/xml")

    # Build XML lines
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        "  <url><loc>https://pyplots.ai/</loc></url>",
        "  <url><loc>https://pyplots.ai/catalog</loc></url>",
    ]

    # Add spec URLs (overview + all implementations)
    if db is not None:
        repo = SpecRepository(db)
        specs = await repo.get_all()
        for spec in specs:
            if spec.impls:  # Only include specs with implementations
                spec_id = html.escape(spec.id)
                # Overview page
                xml_lines.append(f"  <url><loc>https://pyplots.ai/{spec_id}</loc></url>")
                # Individual implementation pages
                for impl in spec.impls:
                    library_id = html.escape(impl.library_id)
                    xml_lines.append(f"  <url><loc>https://pyplots.ai/{spec_id}/{library_id}</loc></url>")

    xml_lines.append("</urlset>")
    xml = "\n".join(xml_lines)

    set_cache(key, xml)
    return Response(content=xml, media_type="application/xml")


# =============================================================================
# Bot SEO Proxy Endpoints
# These endpoints serve HTML with correct meta tags for social media bots.
# nginx proxies bot requests here based on User-Agent detection.
# =============================================================================


@router.get("/seo-proxy/")
async def seo_home():
    """Bot-optimized home page with correct og:tags."""
    return HTMLResponse(
        BOT_HTML_TEMPLATE.format(
            title="pyplots.ai",
            description=DEFAULT_DESCRIPTION,
            image=DEFAULT_IMAGE,
            url="https://pyplots.ai/",
        )
    )


@router.get("/seo-proxy/catalog")
async def seo_catalog():
    """Bot-optimized catalog page with correct og:tags."""
    return HTMLResponse(
        BOT_HTML_TEMPLATE.format(
            title="Catalog | pyplots.ai",
            description="Browse all Python plotting specifications alphabetically. Find matplotlib, seaborn, plotly, bokeh, altair examples.",
            image=DEFAULT_IMAGE,
            url="https://pyplots.ai/catalog",
        )
    )


@router.get("/seo-proxy/{spec_id}")
async def seo_spec_overview(spec_id: str, db: AsyncSession | None = Depends(optional_db)):
    """Bot-optimized spec overview page with correct og:tags."""
    if db is None:
        # Fallback when DB unavailable
        return HTMLResponse(
            BOT_HTML_TEMPLATE.format(
                title=f"{spec_id} | pyplots.ai",
                description=DEFAULT_DESCRIPTION,
                image=DEFAULT_IMAGE,
                url=f"https://pyplots.ai/{html.escape(spec_id)}",
            )
        )

    repo = SpecRepository(db)
    spec = await repo.get_by_id(spec_id)
    if not spec:
        raise HTTPException(status_code=404, detail="Spec not found")

    return HTMLResponse(
        BOT_HTML_TEMPLATE.format(
            title=f"{html.escape(spec.title)} | pyplots.ai",
            description=html.escape(spec.description or DEFAULT_DESCRIPTION),
            image=DEFAULT_IMAGE,
            url=f"https://pyplots.ai/{html.escape(spec_id)}",
        )
    )


@router.get("/seo-proxy/{spec_id}/{library}")
async def seo_spec_implementation(
    spec_id: str,
    library: str,
    db: AsyncSession | None = Depends(optional_db),
):
    """Bot-optimized spec implementation page with dynamic og:image from preview_url."""
    if db is None:
        # Fallback when DB unavailable
        return HTMLResponse(
            BOT_HTML_TEMPLATE.format(
                title=f"{spec_id} - {library} | pyplots.ai",
                description=DEFAULT_DESCRIPTION,
                image=DEFAULT_IMAGE,
                url=f"https://pyplots.ai/{html.escape(spec_id)}/{html.escape(library)}",
            )
        )

    repo = SpecRepository(db)
    spec = await repo.get_by_id(spec_id)
    if not spec:
        raise HTTPException(status_code=404, detail="Spec not found")

    # Find the implementation for this library
    impl = next((i for i in spec.impls if i.library_id == library), None)
    image = impl.preview_url if impl and impl.preview_url else DEFAULT_IMAGE

    return HTMLResponse(
        BOT_HTML_TEMPLATE.format(
            title=f"{html.escape(spec.title)} - {html.escape(library)} | pyplots.ai",
            description=html.escape(spec.description or DEFAULT_DESCRIPTION),
            image=image,
            url=f"https://pyplots.ai/{html.escape(spec_id)}/{html.escape(library)}",
        )
    )
