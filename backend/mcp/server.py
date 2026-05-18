import sys
import os
import json
import logging
import asyncio
from pathlib import Path

# Add the backend root to Python path so we can import app modules
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Ensure environment is loaded (dotenv) if not already
from dotenv import load_dotenv
load_dotenv(backend_dir / ".env")

import mcp.server.stdio
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.types as types

from app.services.ga4_service import ga4_service

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_server")

server = Server("ga4-analytics-mcp")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available GA4 tools."""
    return [
        types.Tool(
            name="get_analytics_overview",
            description="Get high-level analytics overview metrics like total users, sessions, page views, bounce rate.",
            inputSchema={
                "type": "object",
                "properties": {
                    "date_range": {
                        "type": "string",
                        "description": "Date range to query (e.g., '7d', '28d', '90d', '12m'). Default is '28d'."
                    }
                }
            }
        ),
        types.Tool(
            name="get_traffic_data",
            description="Get daily traffic data points for time-series analysis.",
            inputSchema={
                "type": "object",
                "properties": {
                    "date_range": {
                        "type": "string",
                        "description": "Date range to query (e.g., '7d', '28d'). Default is '28d'."
                    }
                }
            }
        ),
        types.Tool(
            name="get_device_breakdown",
            description="Get visitor breakdown by device category (Desktop, Mobile, etc.).",
            inputSchema={
                "type": "object",
                "properties": {
                    "date_range": {
                        "type": "string",
                        "description": "Date range to query (e.g., '7d', '28d'). Default is '28d'."
                    }
                }
            }
        ),
        types.Tool(
            name="get_top_pages",
            description="Get the most viewed pages on the website.",
            inputSchema={
                "type": "object",
                "properties": {
                    "date_range": {
                        "type": "string",
                        "description": "Date range to query (e.g., '7d', '28d'). Default is '28d'."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of pages to return. Default is 10."
                    }
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    if not arguments:
        arguments = {}

    date_range = arguments.get("date_range", "28d")

    try:
        if name == "get_analytics_overview":
            data = ga4_service.get_overview(date_range)
            # data is a Pydantic model
            return [types.TextContent(type="text", text=data.model_dump_json(indent=2))]
            
        elif name == "get_traffic_data":
            data = ga4_service.get_traffic(date_range)
            result = json.dumps([d.model_dump() for d in data], indent=2)
            return [types.TextContent(type="text", text=result)]
            
        elif name == "get_device_breakdown":
            data = ga4_service.get_devices(date_range)
            result = json.dumps([d.model_dump() for d in data], indent=2)
            return [types.TextContent(type="text", text=result)]
            
        elif name == "get_top_pages":
            limit = arguments.get("limit", 10)
            data = ga4_service.get_top_pages(date_range, limit)
            result = json.dumps([d.model_dump() for d in data], indent=2)
            return [types.TextContent(type="text", text=result)]
            
        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    if not ga4_service.is_connected():
        logger.error("GA4 Service is not connected. Make sure credentials are set up.")
        
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ga4-analytics-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
