import json
import anthropic
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from .mcp_client import get_product_context_via_mcp


# ─── Frontend View ───────────────────────────────────────────────────────────

def index(request):
    """Serve the main frontend page."""
    return render(request, 'index.html')


# ─── REST API ─────────────────────────────────────────────────────────────────

@api_view(['GET'])
def product_list(request):
    """Return all products as JSON for the frontend."""
    products = Product.objects.filter(in_stock=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, pk):
    """Return a single product."""
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


# ─── AI Chat Endpoint ─────────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(['POST'])
def chat(request):
    """
    Chat endpoint — uses MCP server to fetch live product data,
    then calls Claude to answer the user's question.
    """
    try:
        body = json.loads(request.body)
        messages = body.get('messages', [])
        if not messages:
            return JsonResponse({'error': 'No messages provided'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # Fetch product context via MCP server
    product_context = get_product_context_via_mcp()

    system_prompt = f"""You are MCP AI Chatbot, a helpful product assistant for MCP AI Chatbot.
Use the product data below to answer customer questions accurately.

{product_context}

Guidelines:
- Be concise but informative. Use bullet points when listing specs.
- Recommend products based on customer needs and budget.
- If a product is not in our catalog, politely say so.
- Always mention the exact price and key specs when describing a product.
- Be friendly, professional, and enthusiastic about tech."""

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    response = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=1000,
        system=system_prompt,
        messages=messages,
    )

    reply = response.content[0].text
    return JsonResponse({'reply': reply})