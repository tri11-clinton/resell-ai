"""
🔌 MCP Server for Resell AI Pro
Exposes listing generation, price check, and auto‑reply via JSON‑RPC.
"""

from jsonrpcserver import method, serve
import json
from openai import OpenAI
import os

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY not set")

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

@method
def generate_listing(brand: str, name: str, size: str, color: str, condition: str, price: float) -> dict:
    """Generate a resale listing for an item."""
    prompt = f"Brand: {brand}, Name: {name}, Size: {size}, Color: {color}, Condition: {condition}, Original: ${price}. Output JSON with title, description, suggested_price, condition_notes."
    msgs = [{"role": "system", "content": "You are a reseller. Output only valid JSON."},
            {"role": "user", "content": prompt}]
    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=msgs,
            max_tokens=500,
            temperature=0.7
        )
        content = resp.choices[0].message.content
        return json.loads(content.strip().strip('```json').strip('```').strip())
    except Exception as e:
        return {"error": str(e)}

@method
def price_war_analysis(competitor_prices: list, my_price: float) -> dict:
    """Analyze competitor prices and recommend a counter‑price."""
    prompt = f"Competitor prices: {competitor_prices}. My price: {my_price}. Suggest optimal price and strategy."
    msgs = [{"role": "system", "content": "You are a pricing strategist."},
            {"role": "user", "content": prompt}]
    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=msgs,
            max_tokens=200,
            temperature=0.5
        )
        return {"recommendation": resp.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

@method
def auto_reply(buyer_message: str, tone: str = "friendly") -> str:
    """Generate a human‑like reply to a buyer."""
    prompt = f"Tone: {tone}. Buyer message: {buyer_message}. Write a short, natural reply."
    msgs = [{"role": "system", "content": "You are a helpful salesperson."},
            {"role": "user", "content": prompt}]
    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=msgs,
            max_tokens=150,
            temperature=0.8
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("🔌 MCP Server running on port 5000")
    serve(port=5000)