
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

# Mock Bearer tokens for testing
TOKENS = {
    "admin-secret": "admin",
    "viewer-secret": "viewer"
}

# Downstream MCP server URL
DOWNSTREAM_URL = "http://127.0.0.1:8001/mcp"


@app.post("/mcp")
async def security_gateway(request: Request):

    # Step 1: Read Bearer token
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"detail": "Missing or invalid Bearer token"}
        )

    token = auth_header.split(" ", 1)[1]
    role = TOKENS.get(token)

    if role is None:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid token"}
        )

    # Step 2: Read JSON-RPC request
    payload = await request.json()

    method = payload.get("method")
    request_id = payload.get("id")

    # Step 3: Check tool-level authorization
    if method == "tools/call":
        tool_name = payload.get("params", {}).get("name", "")

        if tool_name.startswith("admin_") and role != "admin":
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32001,
                        "message": "Unauthorized Tool Call"
                    }
                }
            )

    # Step 4: Forward authorized requests
    async with httpx.AsyncClient() as client:
        response = await client.post(
            DOWNSTREAM_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

    # Step 5: Return downstream response
    return JSONResponse(
        content=response.json(),
        status_code=response.status_code
    )
