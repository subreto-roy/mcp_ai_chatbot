import json
from groq import Groq
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


def index(request):
    return render(request, 'index.html')


@api_view(['GET'])
def product_list(request):
    products = Product.objects.filter(in_stock=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@csrf_exempt
@require_http_methods(['POST'])
def chat(request):
    try:
        body = json.loads(request.body)
        messages = body.get('messages', [])
        if not messages:
            return JsonResponse({'error': 'No messages provided'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    product_context = get_product_context_via_mcp()

    system_prompt = f"""You are ShopAssist AI, a helpful product assistant.
Use the product data below to answer customer questions accurately.

{product_context}

Guidelines:
- Be concise but informative. Use bullet points when listing specs.
- Recommend products based on customer needs and budget.
- Always mention the exact price and key specs when describing a product.
- Be friendly, professional, and enthusiastic about tech."""

    client = Groq(api_key=settings.GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt}
        ] + messages,
        max_tokens=1000,
        temperature=0.5,
    )

    reply = response.choices[0].message.content
    return JsonResponse({'reply': reply})