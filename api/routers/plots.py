"""Filter endpoint for plots."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.cache import get_cache, set_cache
from api.dependencies import require_db
from api.schemas import FilteredPlotsResponse
from core.database import SpecRepository


router = APIRouter(tags=["plots"])


def _image_matches_groups(spec_id: str, library: str, groups: list[dict], spec_lookup: dict) -> bool:
    """Check if an image matches a set of filter groups."""
    if spec_id not in spec_lookup:
        return False
    spec_tags = spec_lookup[spec_id]["tags"]

    for group in groups:
        category = group["category"]
        values = group["values"]

        if category == "lib":
            if library not in values:
                return False
        elif category == "spec":
            if spec_id not in values:
                return False
        elif category == "plot":
            spec_plot_types = spec_tags.get("plot_type", [])
            if not any(v in spec_plot_types for v in values):
                return False
        elif category == "data":
            spec_data_types = spec_tags.get("data_type", [])
            if not any(v in spec_data_types for v in values):
                return False
        elif category == "dom":
            spec_domains = spec_tags.get("domain", [])
            if not any(v in spec_domains for v in values):
                return False
        elif category == "feat":
            spec_features = spec_tags.get("features", [])
            if not any(v in spec_features for v in values):
                return False
    return True


def _calculate_global_counts(all_specs: list) -> dict:
    """Calculate global counts for all filter categories."""
    global_counts: dict = {"lib": {}, "spec": {}, "plot": {}, "data": {}, "dom": {}, "feat": {}}

    for spec_obj in all_specs:
        if not spec_obj.impls:
            continue
        spec_tags = spec_obj.tags or {}

        for impl in spec_obj.impls:
            if not impl.preview_url:
                continue

            # Count library
            global_counts["lib"][impl.library_id] = global_counts["lib"].get(impl.library_id, 0) + 1

            # Count spec ID
            global_counts["spec"][spec_obj.id] = global_counts["spec"].get(spec_obj.id, 0) + 1

            # Count tags
            for plot_type in spec_tags.get("plot_type", []):
                global_counts["plot"][plot_type] = global_counts["plot"].get(plot_type, 0) + 1

            for data_type in spec_tags.get("data_type", []):
                global_counts["data"][data_type] = global_counts["data"].get(data_type, 0) + 1

            for domain in spec_tags.get("domain", []):
                global_counts["dom"][domain] = global_counts["dom"].get(domain, 0) + 1

            for feature in spec_tags.get("features", []):
                global_counts["feat"][feature] = global_counts["feat"].get(feature, 0) + 1

    # Sort counts
    for category in global_counts:
        global_counts[category] = dict(sorted(global_counts[category].items(), key=lambda x: (-x[1], x[0])))

    return global_counts


def _calculate_contextual_counts(filtered_images: list[dict], spec_id_to_tags: dict) -> dict:
    """Calculate contextual counts from filtered images."""
    counts: dict = {"lib": {}, "spec": {}, "plot": {}, "data": {}, "dom": {}, "feat": {}}

    for img in filtered_images:
        spec_id = img["spec_id"]
        library = img["library"]
        spec_tags = spec_id_to_tags.get(spec_id, {})

        # Count library
        counts["lib"][library] = counts["lib"].get(library, 0) + 1

        # Count spec ID
        counts["spec"][spec_id] = counts["spec"].get(spec_id, 0) + 1

        # Count tags
        for plot_type in spec_tags.get("plot_type", []):
            counts["plot"][plot_type] = counts["plot"].get(plot_type, 0) + 1

        for data_type in spec_tags.get("data_type", []):
            counts["data"][data_type] = counts["data"].get(data_type, 0) + 1

        for domain in spec_tags.get("domain", []):
            counts["dom"][domain] = counts["dom"].get(domain, 0) + 1

        for feature in spec_tags.get("features", []):
            counts["feat"][feature] = counts["feat"].get(feature, 0) + 1

    # Sort counts
    for category in counts:
        counts[category] = dict(sorted(counts[category].items(), key=lambda x: (-x[1], x[0])))

    return counts


def _calculate_or_counts(
    filter_groups: list[dict], all_images: list[dict], spec_id_to_tags: dict, spec_lookup: dict
) -> list[dict]:
    """Calculate OR preview counts for each filter group."""
    or_counts: list[dict] = []

    for group_idx, group in enumerate(filter_groups):
        # Get all other groups (excluding this one)
        other_groups = [g for i, g in enumerate(filter_groups) if i != group_idx]

        # Filter images with only the other groups' filters
        images_with_other_filters = [
            img
            for img in all_images
            if _image_matches_groups(img["spec_id"], img["library"], other_groups, spec_lookup)
        ]

        # Count each value for this group's category
        category = group["category"]
        group_counts: dict[str, int] = {}

        for img in images_with_other_filters:
            spec_id = img["spec_id"]
            library = img["library"]
            spec_tags = spec_id_to_tags.get(spec_id, {})

            if category == "lib":
                group_counts[library] = group_counts.get(library, 0) + 1
            elif category == "spec":
                group_counts[spec_id] = group_counts.get(spec_id, 0) + 1
            elif category == "plot":
                for v in spec_tags.get("plot_type", []):
                    group_counts[v] = group_counts.get(v, 0) + 1
            elif category == "data":
                for v in spec_tags.get("data_type", []):
                    group_counts[v] = group_counts.get(v, 0) + 1
            elif category == "dom":
                for v in spec_tags.get("domain", []):
                    group_counts[v] = group_counts.get(v, 0) + 1
            elif category == "feat":
                for v in spec_tags.get("features", []):
                    group_counts[v] = group_counts.get(v, 0) + 1

        # Sort by count descending
        group_counts = dict(sorted(group_counts.items(), key=lambda x: (-x[1], x[0])))
        or_counts.append(group_counts)

    return or_counts


def _parse_filter_groups(request: Request) -> list[dict]:
    """
    Parse query parameters into filter groups.

    Args:
        request: FastAPI request object

    Returns:
        List of filter group dicts with category and values
    """
    filter_groups: list[dict] = []
    query_params = request.query_params.multi_items()

    for key, value in query_params:
        if key in ("lib", "spec", "plot", "data", "dom", "feat") and value:
            values = [v.strip() for v in value.split(",") if v.strip()]
            if values:
                filter_groups.append({"category": key, "values": values})

    return filter_groups


def _build_cache_key(filter_groups: list[dict]) -> str:
    """
    Build cache key from filter groups.

    Args:
        filter_groups: List of filter group dicts

    Returns:
        Cache key string
    """
    if not filter_groups:
        return "filter:all"

    cache_parts = [f"{g['category']}={','.join(sorted(g['values']))}" for g in filter_groups]
    return f"filter:{':'.join(cache_parts)}"


def _build_spec_lookup(all_specs: list) -> dict:
    """
    Build lookup dictionary of spec_id -> (spec_obj, tags).

    Args:
        all_specs: List of Spec objects

    Returns:
        Dict mapping spec_id to spec object and tags
    """
    spec_lookup: dict = {}
    for spec_obj in all_specs:
        if spec_obj.impls:
            spec_lookup[spec_obj.id] = {"spec": spec_obj, "tags": spec_obj.tags or {}}
    return spec_lookup


def _collect_all_images(all_specs: list) -> list[dict]:
    """
    Collect all plot images from specs with implementations.

    Args:
        all_specs: List of Spec objects

    Returns:
        List of image dicts with spec_id, library, quality, url, thumb, and html
    """
    all_images: list[dict] = []
    for spec_obj in all_specs:
        if not spec_obj.impls:
            continue
        for impl in spec_obj.impls:
            if impl.preview_url:
                all_images.append(
                    {
                        "spec_id": spec_obj.id,
                        "library": impl.library_id,
                        "quality": impl.quality_score,
                        "url": impl.preview_url,
                        "thumb": impl.preview_thumb,
                        "html": impl.preview_html,
                    }
                )
    return all_images


def _filter_images(all_images: list[dict], filter_groups: list[dict], spec_lookup: dict) -> list[dict]:
    """
    Filter images based on filter groups.

    Args:
        all_images: List of all image dicts
        filter_groups: List of filter group dicts
        spec_lookup: Spec lookup dictionary

    Returns:
        Filtered list of image dicts
    """
    return [
        img for img in all_images if _image_matches_groups(img["spec_id"], img["library"], filter_groups, spec_lookup)
    ]


@router.get("/plots/filter", response_model=FilteredPlotsResponse)
async def get_filtered_plots(request: Request, db: AsyncSession = Depends(require_db)):
    """
    Get filtered plot images with counts for all filter categories.

    Filter logic:
    - Multiple values in same param: OR (lib=matplotlib,seaborn)
    - Multiple params with same name: AND (lib=matplotlib&lib=seaborn)
    - Different categories: AND (lib=matplotlib&plot=scatter)

    Query params (comma-separated for OR, multiple params for AND):
    - lib: Library filter (matplotlib, seaborn, etc.)
    - spec: Spec ID filter (scatter-basic, etc.)
    - plot: Plot type tag (scatter, bar, line, etc.)
    - data: Data type tag (numeric, categorical, etc.)
    - dom: Domain tag (statistics, finance, etc.)
    - feat: Features tag (basic, 3d, interactive, etc.)

    Returns:
        FilteredPlotsResponse with images, counts, and orCounts per group
    """
    # Parse query parameters
    filter_groups = _parse_filter_groups(request)

    # Check cache
    cache_key = _build_cache_key(filter_groups)
    cached = get_cache(cache_key)
    if cached:
        return cached

    # Fetch data from database
    repo = SpecRepository(db)
    all_specs = await repo.get_all()

    # Build data structures
    spec_lookup = _build_spec_lookup(all_specs)
    all_images = _collect_all_images(all_specs)
    spec_id_to_tags = {spec_id: spec_data["tags"] for spec_id, spec_data in spec_lookup.items()}

    # Filter images
    filtered_images = _filter_images(all_images, filter_groups, spec_lookup)

    # Calculate counts
    global_counts = _calculate_global_counts(all_specs)
    counts = _calculate_contextual_counts(filtered_images, spec_id_to_tags)
    or_counts = _calculate_or_counts(filter_groups, all_images, spec_id_to_tags, spec_lookup)

    # Build and cache response
    result = FilteredPlotsResponse(
        total=len(filtered_images),
        images=filtered_images,
        counts=counts,
        globalCounts=global_counts,
        orCounts=or_counts,
    )
    set_cache(cache_key, result)
    return result
