
# MCP Security Gateway Proxy

## Overview
A lightweight HTTP/JSON-RPC reverse proxy that acts as a security gateway between an AI agent client and a downstream MCP server.

## Architecture

AI Agent Client → Security Gateway → Mock MCP Server

## Technologies Used
- Python 3
- FastAPI
- Uvicorn
- HTTPX
- JSON-RPC 2.0

## Features
- Bearer token authentication
- Admin and viewer role identification
- Transparent forwarding of tools/list requests
- Tool-level authorization for tools/call
- Admin-only tool protection using the admin_ prefix
- JSON-RPC error handling (-32001)
- HTTP reverse proxy forwarding

## Mock Credentials

| Token | Role |
|---|---|
| admin-secret | admin |
| viewer-secret | viewer |

These credentials are for local assessment testing only.

## Running the Application

Start the Mock MCP Server:

```bash
python -m uvicorn mock_mcp_server:app --host 127.0.0.1 --port 8001
```

Start the Security Gateway:

```bash
python -m uvicorn gateway:app --host 127.0.0.1 --port 8000
```

## Authorization Rules

| Method | Admin | Viewer |
|---|---|---|
| tools/list | Allowed | Allowed |
| Normal tools/call | Allowed | Allowed |
| admin_ tools/call | Allowed | Denied |

## Unauthorized Response

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32001,
    "message": "Unauthorized Tool Call"
  }
}
```

## Test Results

- Viewer blocked from admin_reset_key
- Admin successfully executed admin_reset_key
- Viewer successfully executed get_customer_data
- Viewer successfully listed available tools

## Project Structure

```text
task2-security-proxy/
├── gateway.py
├── mock_mcp_server.py
├── requirements.txt
├── README.md
└── venv/
```
