
from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/mcp")
async def handle_mcp_request(request: Request):
    payload = await request.json()

    method = payload.get("method")
    request_id = payload.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "get_customer_data",
                        "description": "Get customer data"
                    },
                    {
                        "name": "admin_reset_key",
                        "description": "Reset an admin key"
                    }
                ]
            }
        }

    if method == "tools/call":
        tool_name = payload.get("params", {}).get("name")

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": f"Successfully executed {tool_name}"
                    }
                ]
            }
        }

    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": -32601,
            "message": "Method not found"
        }
    }
