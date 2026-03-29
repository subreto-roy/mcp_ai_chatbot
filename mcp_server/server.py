"""
MCP AI Chatbot MCP Server
─────────────────
An MCP (Model Context Protocol) server that exposes product database
tools so that AI models can query live product data.

Run standalone:
    python mcp_server/server.py
"""

import os
import sys
import django
import json

# ── Bootstrap Django so we can use ORM outside of manage.py ──────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcp_ai_chatbot.settings')
django.setup()

from mcp.server.fastmcp import FastMCP
from chatbot.models import Product

mcp = FastMCP("shopassist-ai")


# ─── Tool 1: list all products ────────────────────────────────────────────────

@mcp.tool()
def get_all_products() -> str:
    """
    Retrieve all available products from the MCP AI Chatbot store database.
    Returns a structured summary of every product including name,
    category, price, description, specs, and highlights.
    """
    products = Product.objects.filter(in_stock=True)
    if not products.exists():
        return "No products currently available."

    lines = []
    for p in products:
        specs_str = "\n".join(f"  {k}: {v}" for k, v in p.specs.items())
        highlights_str = ", ".join(p.highlights)
        lines.append(
            f"### {p.name} (ID: {p.id})\n"
            f"Category: {p.get_category_display()}\n"
            f"Price: {p.price_display()}\n"
            f"Description: {p.description}\n"
            f"Specs:\n{specs_str}\n"
            f"Highlights: {highlights_str}\n"
            f"In Stock: {'Yes' if p.in_stock else 'No'}"
        )

    return "\n\n".join(lines)


# ─── Tool 2: search products ──────────────────────────────────────────────────

@mcp.tool()
def search_products(query: str) -> str:
    """
    Search for products by name, category, or description keyword.
    
    Args:
        query: Search term (e.g. "laptop", "wireless", "under 500")
    
    Returns a list of matching products with full details.
    """
    from django.db.models import Q

    results = Product.objects.filter(
        Q(name__icontains=query) |
        Q(category__icontains=query) |
        Q(description__icontains=query),
        in_stock=True
    )

    if not results.exists():
        return f"No products found matching '{query}'."

    lines = []
    for p in results:
        specs_str = "\n".join(f"  {k}: {v}" for k, v in p.specs.items())
        lines.append(
            f"### {p.name}\n"
            f"Category: {p.get_category_display()} | Price: {p.price_display()}\n"
            f"Description: {p.description}\n"
            f"Specs:\n{specs_str}"
        )

    return f"Found {results.count()} product(s) for '{query}':\n\n" + "\n\n".join(lines)


# ─── Tool 3: get product by ID ────────────────────────────────────────────────

@mcp.tool()
def get_product_by_id(product_id: int) -> str:
    """
    Get full details of a specific product by its database ID.

    Args:
        product_id: The integer ID of the product.
    """
    try:
        p = Product.objects.get(pk=product_id, in_stock=True)
    except Product.DoesNotExist:
        return f"Product with ID {product_id} not found."

    specs_str = "\n".join(f"  {k}: {v}" for k, v in p.specs.items())
    highlights_str = "\n".join(f"  • {h}" for h in p.highlights)

    return (
        f"### {p.name}\n"
        f"Category: {p.get_category_display()}\n"
        f"Price: {p.price_display()}\n"
        f"Description: {p.description}\n\n"
        f"Full Specs:\n{specs_str}\n\n"
        f"Key Highlights:\n{highlights_str}"
    )


# ─── Tool 4: filter by budget ────────────────────────────────────────────────

@mcp.tool()
def get_products_by_budget(max_price: float, min_price: float = 0) -> str:
    """
    Find products within a given price range.

    Args:
        max_price: Maximum budget in USD (e.g. 500.0)
        min_price: Minimum price in USD (default 0)
    """
    results = Product.objects.filter(
        price__gte=min_price,
        price__lte=max_price,
        in_stock=True
    ).order_by('price')

    if not results.exists():
        return f"No products found between ${min_price:.0f} and ${max_price:.0f}."

    lines = [f"Products between ${min_price:.0f} – ${max_price:.0f}:\n"]
    for p in results:
        lines.append(f"  • {p.name} ({p.get_category_display()}) — {p.price_display()}")
        lines.append(f"    {p.description}\n")

    return "\n".join(lines)


# ─── Tool 5: get categories ──────────────────────────────────────────────────

@mcp.tool()
def get_categories() -> str:
    """
    List all product categories available in the store with product counts.
    """
    from django.db.models import Count
    cats = (
        Product.objects
        .filter(in_stock=True)
        .values('category')
        .annotate(count=Count('id'))
        .order_by('category')
    )

    if not cats:
        return "No categories found."

    lines = ["Available categories in MCP AI Chatbot:\n"]
    for c in cats:
        label = dict(Product.CATEGORY_CHOICES).get(c['category'], c['category'])
        lines.append(f"  • {label}: {c['count']} product(s)")

    return "\n".join(lines)


if __name__ == "__main__":
    print("🚀 MCP AI Chatbot MCP Server starting...")
    mcp.run(transport="stdio")