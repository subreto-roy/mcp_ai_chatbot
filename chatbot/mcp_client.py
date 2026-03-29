"""
mcp_client.py
─────────────
Helper that the Django chat view uses to call MCP server tools
and build a product context string for Claude.

Since the MCP server runs as a subprocess (stdio transport),
we call it directly via Python import when running in the same process.
This keeps things simple for a local dev / portfolio setup.
"""

import os
import sys

# Make sure Django is set up before importing models
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcp_ai_chatbot.settings')


def get_product_context_via_mcp() -> str:
    """
    Calls the MCP server's get_all_products tool directly
    and returns a formatted string for use as AI context.

    In a real production setup you would call the MCP server
    over stdio/SSE transport; here we import directly so the
    whole stack runs locally without extra processes.
    """
    try:
        # Import MCP server tools directly (same process, local dev)
        from chatbot.models import Product

        products = Product.objects.filter(in_stock=True)
        if not products.exists():
            return "No products currently in the database."

        lines = ["=== MCP AI CHATBOT — LIVE PRODUCT CATALOG ===\n"]
        for p in products:
            specs_str = "\n".join(f"    {k}: {v}" for k, v in p.specs.items())
            highlights_str = ", ".join(p.highlights)
            lines.append(
                f"## {p.name}\n"
                f"  Category : {p.get_category_display()}\n"
                f"  Price    : {p.price_display()}\n"
                f"  Desc     : {p.description}\n"
                f"  Specs    :\n{specs_str}\n"
                f"  Features : {highlights_str}\n"
            )

        return "\n".join(lines)

    except Exception as e:
        return f"[MCP Error] Could not fetch products: {e}"