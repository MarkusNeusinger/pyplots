"""SEO endpoints (sitemap)."""

import html

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.cache import cache_key, get_cache, set_cache
from api.dependencies import optional_db
from core.database import SpecRepository


router = APIRouter(tags=["seo"])


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
