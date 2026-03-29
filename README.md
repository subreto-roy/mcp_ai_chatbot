ShopAssist AI — MCP-Powered Product Assistant
ShopAssist AI is a full-stack AI-powered tech store where users can interact with an intelligent chatbot to explore products. The highlight of this project is the integration of MCP (Model Context Protocol) — a cutting-edge standard by Anthropic that allows AI models to access external tools and live data sources.
Instead of hardcoding product data into the AI prompt, the MCP server exposes the MySQL database as a set of callable tools — get_all_products, search_products, get_products_by_budget, and more. This means the AI always reads live, real-time data directly from the database before answering user queries.
Key Features:

🤖 AI chatbot powered by LLaMA 3.3 via Groq API
🔌 Custom MCP server with 5 database tools
🗄️ Django REST API with MySQL backend
💬 Multi-turn conversation with full chat history
⚡ Real-time product data — no hardcoding

Tech Stack: Python, Django, Django REST Framework, MySQL, MCP, Groq API, LLaMA 3.3, HTML/CSS/JS
