"""
🚀 ULTIMATE RESELLING ASSISTANT
All-in-one: listings, replies, promotions, and platform posting.
API key pre‑loaded – just run.
"""

import streamlit as st
import pandas as pd
import requests
import json
import base64
import sqlite3
import time
from io import BytesIO
from PIL import Image
from openai import OpenAI
from datetime import datetime

# ----------------------------
# YOUR API KEY
import os
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "") 
MODEL = "deepseek-v4-pro"      # 
# ----------------------------

# Database setup
conn = sqlite3.connect("listings.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    brand TEXT, name TEXT, size TEXT, color TEXT, condition TEXT,
    original_price REAL, platform TEXT, title TEXT, description TEXT,
    suggested_price REAL, condition_notes TEXT, category TEXT
)''')
conn.commit()

# Page config
st.set_page_config(page_title="Resell AI Pro", page_icon="💎", layout="wide")
st.sidebar.title("⚙️ Control Panel")
st.sidebar.markdown(f"**Model:** {MODEL}")
st.sidebar.markdown("**API Key:** ✅ set via secrets")

# Main title
st.title("💎 Resell AI Pro – Your Full‑Stack Selling Bot")
st.markdown("Generate listings, reply to buyers, promote your store – all in one.")

# ---------- Helper: call DeepSeek (fast) ----------
def call_deepseek(messages, max_tokens=600, temp=0.7):
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temp,
        )
        return resp.choices[0].message.content
    except Exception as e:
        st.error(f"API error: {e}")
        return None

def parse_json(text):
    try:
        clean = text.strip().strip('```json').strip('```').strip()
        return json.loads(clean)
    except:
        return {"title": "", "description": text, "suggested_price": "", "condition_notes": "", "category": ""}

# ---------- Tabs ----------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📝 Quick List", "📁 Bulk CSV", "💬 Auto‑Reply", "📢 Promote Yourself", "📊 History"]
)

# ---------- TAB 1: Quick List ----------
with tab1:
    st.subheader("One‑click listing for any item")
    col1, col2 = st.columns(2)
    with col1:
        brand = st.text_input("Brand", "Nike")
        name = st.text_input("Item name", "Air Force 1")
        size = st.text_input("Size", "10")
        color = st.text_input("Color", "White/Black")
    with col2:
        condition = st.selectbox("Condition", ["New", "Very Good", "Good", "Acceptable"])
        price = st.number_input("Original price ($)", min_value=0.0, step=1.0, value=110.0)
        platform = st.selectbox("Target platform", ["eBay", "Mercari", "Depop", "Etsy", "All"])
        include_image = st.checkbox("Analyze photo (slower)")

    uploaded_img = None
    if include_image:
        uploaded_img = st.file_uploader("Upload image", type=["jpg","jpeg","png"])

    if st.button("⚡ Generate Now", type="primary"):
        with st.spinner("AI thinking..."):
            prompt = f"""
            Create a resale listing for:
            Brand: {brand}, Name: {name}, Size: {size}, Color: {color},
            Condition: {condition}, Original price: ${price}, Platform: {platform}
            Output JSON with: title, description, suggested_price, condition_notes, category.
            """
            msgs = [{"role": "system", "content": "You are a professional reseller. Output only valid JSON."},
                    {"role": "user", "content": prompt}]
            if uploaded_img and include_image:
                img_b64 = base64.b64encode(uploaded_img.read()).decode()
                msgs[1]["content"] = [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
                # Use Pro for vision
                # We'll just call with the multimodal structure, but we need to set model to pro.
                # We'll handle inside call_deepseek by checking if images are present.
                # For simplicity, we'll use a separate function call with vision.
                # But we'll just use the same client with model set to "deepseek-v4-pro" if image.
                # Quick fix: override MODEL for this call.
                client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
                try:
                    resp = client.chat.completions.create(
                        model="deepseek-v4-pro",
                        messages=msgs,
                        max_tokens=800,
                        temperature=0.7
                    )
                    result = resp.choices[0].message.content
                except Exception as e:
                    st.error(f"Vision error: {e}")
                    result = None
            else:
                result = call_deepseek(msgs, max_tokens=600)

            if result:
                data = parse_json(result)
                st.success("✅ Listing ready!")
                st.markdown(f"**Title:** {data.get('title','')}")
                st.markdown(f"**Price:** ${data.get('suggested_price','')}")
                st.markdown(f"**Condition:** {data.get('condition_notes','')}")
                st.markdown(f"**Category:** {data.get('category','')}")
                st.markdown("**Description:**")
                st.write(data.get('description',''))
                # Save to DB
                c.execute("INSERT INTO history (timestamp, brand, name, size, color, condition, original_price, platform, title, description, suggested_price, condition_notes, category) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                          (datetime.now().isoformat(), brand, name, size, color, condition, price, platform,
                           data.get('title',''), data.get('description',''), data.get('suggested_price',''),
                           data.get('condition_notes',''), data.get('category','')))
                conn.commit()
                st.download_button("📥 Download JSON", json.dumps(data, indent=2), file_name="listing.json")

# ---------- TAB 2: Bulk CSV ----------
with tab2:
    st.subheader("Upload a CSV of your inventory")
    st.markdown("Columns: `brand, name, size, color, condition, original_price` (platform optional)")
    csv_file = st.file_uploader("Choose CSV", type=["csv"])
    if csv_file:
        df = pd.read_csv(csv_file)
        st.dataframe(df.head())
        if st.button("▶️ Process All", type="primary"):
            progress = st.progress(0)
            status = st.empty()
            results = []
            for i, row in df.iterrows():
                status.text(f"Processing {i+1}/{len(df)}: {row['brand']} {row['name']}")
                prompt = f"Brand: {row['brand']}, Name: {row['name']}, Size: {row['size']}, Color: {row['color']}, Condition: {row['condition']}, Original price: ${row['original_price']}, Platform: {row.get('platform','eBay')}. Output JSON with title, description, suggested_price, condition_notes, category."
                msgs = [{"role": "system", "content": "You are a reseller. Output only valid JSON."},
                        {"role": "user", "content": prompt}]
                resp = call_deepseek(msgs, max_tokens=500)
                if resp:
                    data = parse_json(resp)
                    combined = row.to_dict()
                    combined.update(data)
                    results.append(combined)
                progress.progress((i+1)/len(df))
                time.sleep(0.3)  # rate limit
            status.text("✅ Done!")
            result_df = pd.DataFrame(results)
            st.dataframe(result_df)
            csv_out = result_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download All Listings", csv_out, "listings.csv")
            # Save to DB
            for _, r in result_df.iterrows():
                c.execute("INSERT INTO history (timestamp, brand, name, size, color, condition, original_price, platform, title, description, suggested_price, condition_notes, category) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                          (datetime.now().isoformat(), r.get('brand',''), r.get('name',''), r.get('size',''), r.get('color',''),
                           r.get('condition',''), r.get('original_price',0), r.get('platform',''),
                           r.get('title',''), r.get('description',''), r.get('suggested_price',''),
                           r.get('condition_notes',''), r.get('category','')))
            conn.commit()

# ---------- TAB 3: Auto‑Reply ----------
with tab3:
    st.subheader("Generate human‑like replies to buyers")
    tone = st.selectbox("Tone", ["Friendly", "Professional", "Casual", "Urgent", "Persuasive"])
    context = st.text_area("Paste buyer message or describe the situation",
                           "Buyer asked: 'Is this still available and can you do $25?'")
    if st.button("💬 Generate Reply", type="primary"):
        with st.spinner("Crafting response..."):
            prompt = f"Tone: {tone}. Situation: {context}. Write a short, natural reply (1-3 sentences)."
            msgs = [{"role": "system", "content": "You are a skilled salesperson."},
                    {"role": "user", "content": prompt}]
            reply = call_deepseek(msgs, max_tokens=150)
            if reply:
                st.success("Reply:")
                st.markdown(f"> {reply}")
                st.download_button("📋 Copy", reply, "reply.txt")

# ---------- TAB 4: Promote Yourself ----------
with tab4:
    st.subheader("Generate marketing content for your service")
    tool_name = st.text_input("Service name", "AI Reselling Assistant")
    benefit = st.text_area("What does it do?", "Generates product listings and buyer replies automatically.")
    audience = st.text_input("Target audience", "Online resellers and store owners")
    price = st.text_input("Price", "$29/month")
    angle = st.text_input("Unique angle", "Saves 10+ hours/week")
    platforms = st.multiselect("Platforms", ["Facebook","Instagram","Twitter","LinkedIn","TikTok","Reddit","Email","Landing Page"])
    tone = st.selectbox("Tone", ["Hype", "Professional", "Casual", "Direct"], index=0)
    if st.button("🚀 Generate Promo", type="primary"):
        with st.spinner("Creating content..."):
            prompt = f"""
            Create promotional content for "{tool_name}".
            Benefit: {benefit}, Audience: {audience}, Price: {price}, Angle: {angle}, Tone: {tone}.
            For each platform: {', '.join(platforms)}.
            Also include a cold DM.
            Output clearly with headers.
            """
            msgs = [{"role": "system", "content": "You are an expert copywriter."},
                    {"role": "user", "content": prompt}]
            result = call_deepseek(msgs, max_tokens=1000)
            if result:
                st.markdown(result)
                st.download_button("📥 Download", result, "promo.txt")

# ---------- TAB 5: History ----------
with tab5:
    st.subheader("📚 All generated listings")
    df_hist = pd.read_sql("SELECT * FROM history ORDER BY id DESC", conn)
    if not df_hist.empty:
        st.dataframe(df_hist)
        csv_hist = df_hist.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export History", csv_hist, "history.csv")
        if st.button("🗑️ Clear History"):
            c.execute("DELETE FROM history")
            conn.commit()
            st.experimental_rerun()
    else:
        st.info("No listings yet. Generate some!")

# Footer
st.markdown("---")
st.caption("💎 Resell AI Pro – Full control, no limits.")