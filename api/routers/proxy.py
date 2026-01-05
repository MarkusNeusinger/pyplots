"""HTML proxy endpoint for interactive plots with size reporting."""

from urllib.parse import urlparse

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse


router = APIRouter(tags=["proxy"])

# Script injected to report content size to parent window
# Uses specific origin (pyplots.ai) for postMessage security
SIZE_REPORTER_SCRIPT = """
<script>
(function() {
  function reportSize() {
    try {
      // Find the main content element (try common patterns for different libraries)
      var content = document.querySelector(
        '.bk-root, .vega-embed, .plotly, .chart-container, #container, .lp-plot, svg, canvas'
      ) || document.body.firstElementChild || document.body;

      // Get actual rendered size
      var rect = content.getBoundingClientRect();
      var width = Math.max(rect.width, content.scrollWidth || 0, document.body.scrollWidth || 0);
      var height = Math.max(rect.height, content.scrollHeight || 0, document.body.scrollHeight || 0);

      // Add padding to account for action buttons, toolbars, and other UI elements
      var padding = 40;
      width += padding;
      height += padding;

      // Send to parent with specific origin for security
      if (width > 0 && height > 0 && window.parent !== window) {
        window.parent.postMessage({
          type: 'pyplots-size',
          width: Math.ceil(width),
          height: Math.ceil(height)
        }, 'https://pyplots.ai');
      }
    } catch (e) {
      // Silently fail if postMessage is blocked
    }
  }

  // Report after load and after delays (for async rendering libraries)
  if (document.readyState === 'complete') {
    setTimeout(reportSize, 100);
    setTimeout(reportSize, 500);
    setTimeout(reportSize, 1000);
  } else {
    window.addEventListener('load', function() {
      setTimeout(reportSize, 100);
      setTimeout(reportSize, 500);
      setTimeout(reportSize, 1000);
    });
  }
})();
</script>
"""

# Allowed GCS bucket for security
ALLOWED_HOST = "storage.googleapis.com"
ALLOWED_BUCKET = "pyplots-images"


def validate_gcs_url(url: str) -> bool:
    """Validate that URL is from allowed GCS bucket with no path traversal."""
    try:
        parsed = urlparse(url)
        # Must be HTTPS
        if parsed.scheme != "https":
            return False
        # Must be exact host (no subdomains)
        if parsed.netloc != ALLOWED_HOST:
            return False
        # Path must start with bucket name and not contain traversal
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) < 2:
            return False
        if path_parts[0] != ALLOWED_BUCKET:
            return False
        # Check for path traversal attempts
        if ".." in parsed.path:
            return False
        return True
    except Exception:
        return False


@router.get("/proxy/html", response_class=HTMLResponse)
async def proxy_html(url: str):
    """
    Proxy an HTML file and inject size reporting script.

    This endpoint fetches HTML from GCS, injects a script that reports
    the content's actual dimensions via postMessage, and returns the
    modified HTML. This allows the frontend to dynamically scale the
    iframe based on actual content size.

    Args:
        url: The GCS URL to fetch (must be from allowed bucket)

    Returns:
        Modified HTML with size reporting script injected
    """
    # Security: Validate URL strictly to prevent SSRF and path traversal
    if not validate_gcs_url(url):
        raise HTTPException(status_code=400, detail=f"Only URLs from {ALLOWED_HOST}/{ALLOWED_BUCKET} are allowed")

    # Fetch the HTML with shorter timeout
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Failed to fetch HTML") from e
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail="Failed to connect to storage") from e

    html_content = response.text

    # Inject the size reporter script before </body>
    if "</body>" in html_content:
        html_content = html_content.replace("</body>", f"{SIZE_REPORTER_SCRIPT}</body>")
    elif "</html>" in html_content:
        html_content = html_content.replace("</html>", f"{SIZE_REPORTER_SCRIPT}</html>")
    else:
        # Fallback: append to end
        html_content += SIZE_REPORTER_SCRIPT

    return HTMLResponse(content=html_content)
