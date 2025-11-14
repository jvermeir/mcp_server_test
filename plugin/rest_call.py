from typing import Any, Dict, Optional
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("rest_call")

host = "http://localhost:3000/"

@mcp.tool()
async def call_api(method: str, url: str, json_body: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout_seconds: float = 10.0) -> Dict[str, Any]:
    """
    Perform an HTTP request. call a rest service that his hosted locally on port 3000. the url parameter is the part that follows after localhost:3000/

    Args:
        method: HTTP method (GET, POST, PUT, PATCH, DELETE).
        url: Target URL.
        json_body: JSON payload for methods with a body.
        headers: Optional request headers.
        timeout_seconds: Request timeout in seconds.
    """
    allowed = {"GET", "POST", "PUT", "PATCH", "DELETE"}
    m = method.upper()
    if m not in allowed:
        return {"error": f"Unsupported method {m}", "allowed_methods": sorted(list(allowed))}
    try:
        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            resp = await client.request(m, host + url, json=json_body, headers=headers)
        content_type = resp.headers.get("content-type", "")
        try:
            parsed = resp.json() if "application/json" in content_type else resp.text
        except ValueError:
            parsed = resp.text
        return {
            "status": resp.status_code,
            "reason": resp.reason_phrase,
            "headers": dict(resp.headers),
            "body": parsed
        }
    except httpx.RequestError as e:
        return {"error": str(e), "url": url}

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
