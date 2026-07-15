"""
AION – AI Omniverse
Universal AI automation for 10+ industries.
Complete implementation – 10 niches, 10 features each.
"""

import streamlit as st
import pandas as pd
import json
import base64
import sqlite3
import time
import os
from datetime import datetime
from openai import OpenAI

# ----------------------------
# PAGE CONFIG
st.set_page_config(page_title="AION", page_icon="♾️", layout="wide")
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%); }
    .css-1d391kg { background: rgba(255,255,255,0.85) !important; backdrop-filter: blur(12px); border-radius: 20px; padding: 1.5rem; box-shadow: 0 8px 32px rgba(0,0,0,0.06); border: 1px solid rgba(255,255,255,0.4); }
    h1, h2, h3 { color: #0f172a; font-weight: 700; letter-spacing: -0.02em; }
    .stButton > button { background: linear-gradient(135deg, #3b82f6, #2563eb); color: white; border-radius: 40px; padding: 0.6rem 1.8rem; font-weight: 600; border: none; box-shadow: 0 4px 12px rgba(59,130,246,0.25); transition: all 0.2s; }
    .stButton > button:hover { transform: translateY(-2px) scale(1.02); box-shadow: 0 8px 20px rgba(59,130,246,0.35); }
    .stTabs [data-baseweb="tab"] { background: rgba(255,255,255,0.6); border-radius: 40px !important; padding: 0.3rem 1.2rem; font-weight: 500; color: #475569; border: 1px solid transparent; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background: #3b82f6 !important; color: white !important; border-color: #3b82f6 !important; }
    .footer { text-align: center; padding: 2rem 0 1rem; color: #94a3b8; font-size: 0.9rem; border-top: 1px solid #e2e8f0; margin-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# API KEY (set in secrets or .env)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
if not DEEPSEEK_API_KEY:
    st.error("🔑 API Key missing. Set DEEPSEEK_API_KEY in Streamlit secrets or .env.")
    st.stop()

def call_deepseek(messages, max_tokens=600, temp=0.7, model="deepseek-chat"):
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temp,
        )
        return resp.choices[0].message.content
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

# ----------------------------
# NICHE CONFIGURATION – 10 Niches, 10 Features Each
# To keep the code manageable, we define a function that builds the full dictionary.
def build_niche_config():
    # Helper to create a feature definition
    def feature(name, prompt_template, inputs):
        return {"name": name, "prompt": prompt_template, "inputs": inputs}

    # All 10 niches
    config = {}

    # 1. Real Estate
    config["Real Estate"] = {
        "system": "You are a senior real estate agent with 20 years of experience.",
        "features": [
            feature("Property Description", 
                    "Write a compelling property description for a {property_type} in {location} with {bedrooms} bedrooms, {bathrooms} bathrooms, priced at ${price}.",
                    [{"label":"Property Type","key":"property_type","default":"Single-family home"},
                     {"label":"Location","key":"location","default":"Austin, TX"},
                     {"label":"Bedrooms","key":"bedrooms","default":"3"},
                     {"label":"Bathrooms","key":"bathrooms","default":"2"},
                     {"label":"Price","key":"price","default":"500000"}]),
            feature("Email Campaign", 
                    "Write a short email campaign (subject + body) to promote a new listing in {location}.",
                    [{"label":"Location","key":"location","default":"Austin, TX"}]),
            feature("Open House Script", 
                    "Write a 2‑minute script for an open house introduction for a {property_type}.",
                    [{"label":"Property Type","key":"property_type","default":"luxury condo"}]),
            feature("Market Trend Analyzer", 
                    "Summarize current real estate market trends in {location} for {property_type}.",
                    [{"label":"Location","key":"location","default":"Austin, TX"},
                     {"label":"Property Type","key":"property_type","default":"single-family"}]),
            feature("Buyer Persona Generator", 
                    "Create a detailed buyer persona for a {property_type} in {location}.",
                    [{"label":"Property Type","key":"property_type","default":"condo"},
                     {"label":"Location","key":"location","default":"Austin"}]),
            feature("Listing Photo Caption", 
                    "Generate 5 creative captions for listing photos of a {property_type}.",
                    [{"label":"Property Type","key":"property_type","default":"modern home"}]),
            feature("FAQ Generator", 
                    "Generate 10 frequently asked questions and answers for a {property_type} listing.",
                    [{"label":"Property Type","key":"property_type","default":"townhouse"}]),
            feature("Price Recommendation", 
                    "Suggest a list price for a {property_type} in {location} based on comparable sales.",
                    [{"label":"Property Type","key":"property_type","default":"condo"},
                     {"label":"Location","key":"location","default":"Miami"}]),
            feature("Follow‑up Email Sequence", 
                    "Write a 3‑email follow‑up sequence for a potential buyer who viewed a {property_type}.",
                    [{"label":"Property Type","key":"property_type","default":"single-family home"}]),
            feature("CMA Report Summary", 
                    "Summarize a comparative market analysis for a {property_type} in {location}.",
                    [{"label":"Property Type","key":"property_type","default":"duplex"},
                     {"label":"Location","key":"location","default":"Seattle"}])
        ]
    }

    # 2. Dropshipping
    config["Dropshipping"] = {
        "system": "You are a dropshipping expert with deep knowledge of e‑commerce.",
        "features": [
            feature("Product Description", 
                    "Write a persuasive product description for {product_name}, highlighting its features and benefits.",
                    [{"label":"Product Name","key":"product_name","default":"Bamboo Phone Stand"}]),
            feature("Ad Copy (Facebook/Google)", 
                    "Write 3 ad headlines and 3 ad descriptions for {product_name}.",
                    [{"label":"Product Name","key":"product_name","default":"Smart Water Bottle"}]),
            feature("Competitor Price Analysis", 
                    "Analyze competitor pricing for {product_name} and suggest a competitive price.",
                    [{"label":"Product Name","key":"product_name","default":"Wireless Earbuds"}]),
            feature("Trending Item Finder", 
                    "Suggest 5 trending products in the {category} niche right now.",
                    [{"label":"Category","key":"category","default":"home office"}]),
            feature("Supplier Outreach Email", 
                    "Write a professional email to a supplier asking about wholesale prices for {product_name}.",
                    [{"label":"Product Name","key":"product_name","default":"Yoga Mat"}]),
            feature("Social Media Post Scheduler", 
                    "Generate 7 days of social media posts for promoting {product_name}.",
                    [{"label":"Product Name","key":"product_name","default":"Portable Blender"}]),
            feature("Meta Title & Description", 
                    "Generate SEO‑friendly meta title and description for {product_name}.",
                    [{"label":"Product Name","key":"product_name","default":"LED Desk Lamp"}]),
            feature("A/B Test Headlines", 
                    "Provide 5 variations of headlines for a product page of {product_name}.",
                    [{"label":"Product Name","key":"product_name","default":"Ergonomic Chair"}]),
            feature("Return Policy Drafter", 
                    "Write a concise return policy for an online store selling {product_name}.",
                    [{"label":"Product Name","key":"product_name","default":"Fitness Tracker"}]),
            feature("Customer Review Reply Template", 
                    "Write 3 templates for replying to positive and negative reviews for {product_name}.",
                    [{"label":"Product Name","key":"product_name","default":"Plant-based Protein Powder"}])
        ]
    }

    # 3. Affiliate Marketing
    config["Affiliate Marketing"] = {
        "system": "You are a successful affiliate marketer with 10 years of experience.",
        "features": [
            feature("Review Article Generator", 
                    "Write a detailed review article for {product_name} including pros, cons, and a final verdict.",
                    [{"label":"Product Name","key":"product_name","default":"Noise-Cancelling Headphones"}]),
            feature("YouTube Script", 
                    "Write a 5‑minute YouTube script reviewing {product_name}.",
                    [{"label":"Product Name","key":"product_name","default":"Budget Gaming Mouse"}]),
            feature("Instagram Caption + Hashtags", 
                    "Create an engaging Instagram caption and 10 hashtags for {product_name}.",
                    [{"label":"Product Name","key":"product_name","default":"Sunscreen Lotion"}]),
            feature("Email Squeeze Page Copy", 
                    "Write copy for a landing page offering a free guide about {topic}.",
                    [{"label":"Topic","key":"topic","default":"weight loss"}]),
            feature("Landing Page Headline", 
                    "Generate 5 headline options for a landing page promoting {product_name}.",
                    [{"label":"Product Name","key":"product_name","default":"Online Course"}]),
            feature("CTA Button Text", 
                    "Suggest 5 call‑to‑action button texts for a page about {product_name}.",
                    [{"label":"Product Name","key":"product_name","default":"E‑book"}]),
            feature("Product Comparison Table", 
                    "Create a comparison table between {product_name} and its top 3 competitors.",
                    [{"label":"Product Name","key":"product_name","default":"Smartwatch"}]),
            feature("Bonus Content Idea", 
                    "Suggest 3 bonus content pieces to increase conversions for {product_name}.",
                    [{"label":"Product Name","key":"product_name","default":"Course on Photography"}]),
            feature("Social Proof Quote", 
                    "Write 3 fake (but realistic) social proof quotes for {product_name}.",
                    [{"label":"Product Name","key":"product_name","default":"Skincare Set"}]),
            feature("Affiliate Disclosure", 
                    "Write a clear and compliant affiliate disclosure for a blog post about {product_name}.",
                    [{"label":"Product Name","key":"product_name","default":"Weighted Blanket"}])
        ]
    }

    # 4. Freelance Writing
    config["Freelance Writing"] = {
        "system": "You are a top‑tier freelance writer and editor.",
        "features": [
            feature("Blog Outline", 
                    "Create a detailed outline for a blog post on {topic}.",
                    [{"label":"Topic","key":"topic","default":"Productivity Tips"}]),
            feature("Introduction Paragraph", 
                    "Write an engaging introduction for an article about {topic}.",
                    [{"label":"Topic","key":"topic","default":"Meditation"}]),
            feature("Conclusion Generator", 
                    "Write a compelling conclusion for a piece on {topic}.",
                    [{"label":"Topic","key":"topic","default":"Time Management"}]),
            feature("Tone Editor", 
                    "Rewrite the following text to be more {tone}: {text}",
                    [{"label":"Text to edit","key":"text","default":"This product is good."},
                     {"label":"Desired tone","key":"tone","default":"enthusiastic"}]),
            feature("Headline Rewriter", 
                    "Generate 5 alternative headlines for a blog post on {topic}.",
                    [{"label":"Topic","key":"topic","default":"Healthy Eating"}]),
            feature("Bullet Point Expander", 
                    "Expand the following bullet points into a full paragraph: {bullets}",
                    [{"label":"Bullet points","key":"bullets","default":"• Easy to use\n• Affordable\n• High quality"}]),
            feature("Summarizer", 
                    "Summarize the following text in 100 words: {text}",
                    [{"label":"Text to summarize","key":"text","default":"Long article..."}]),
            feature("Content Repurposer", 
                    "Repurpose this blog post into a Twitter thread: {text}",
                    [{"label":"Blog post text","key":"text","default":"..."}]),
            feature("SEO Keyword Suggester", 
                    "Suggest 10 SEO keywords for a blog post about {topic}.",
                    [{"label":"Topic","key":"topic","default":"Vegan Recipes"}]),
            feature("Readability Improver", 
                    "Improve the readability of this text: {text}",
                    [{"label":"Text","key":"text","default":"Complex sentences..."}])
        ]
    }

    # 5. Social Media Management
    config["Social Media Management"] = {
        "system": "You are a social media strategist for top brands.",
        "features": [
            feature("Content Calendar", 
                    "Create a 7‑day content calendar for a brand in the {industry} industry.",
                    [{"label":"Industry","key":"industry","default":"fitness"}]),
            feature("Hashtag Research", 
                    "Provide 20 relevant hashtags for a post about {topic}.",
                    [{"label":"Topic","key":"topic","default":"yoga"}]),
            feature("Bio Generator", 
                    "Write a short, engaging bio for a brand that sells {product}.",
                    [{"label":"Product","key":"product","default":"organic tea"}]),
            feature("Engagement Reply", 
                    "Write a thoughtful reply to a comment: '{comment}'",
                    [{"label":"Comment","key":"comment","default":"I love this product!"}]),
            feature("Story Poll Ideas", 
                    "Suggest 5 interactive story poll ideas for a brand that sells {product}.",
                    [{"label":"Product","key":"product","default":"handmade jewelry"}]),
            feature("Reel Script", 
                    "Write a 15‑second Reel script showcasing {product}.",
                    [{"label":"Product","key":"product","default":"skincare set"}]),
            feature("Carousel Design Ideas", 
                    "Propose a 5‑slide carousel concept about {topic}.",
                    [{"label":"Topic","key":"topic","default":"sustainable living"}]),
            feature("Comment Reply Templates", 
                    "Provide 3 reply templates for common comments on posts about {topic}.",
                    [{"label":"Topic","key":"topic","default":"travel"}]),
            feature("DM Auto‑Responder", 
                    "Write a friendly auto‑reply for DMs asking about {product}.",
                    [{"label":"Product","key":"product","default":"custom prints"}]),
            feature("Analytics Insight", 
                    "Based on engagement data, suggest how to improve posts for {platform}.",
                    [{"label":"Platform","key":"platform","default":"Instagram"}])
        ]
    }

    # 6. Course Creators
    config["Course Creators"] = {
        "system": "You are an expert course creator and instructional designer.",
        "features": [
            feature("Lesson Outline", 
                    "Create a detailed outline for a lesson on {topic}.",
                    [{"label":"Topic","key":"topic","default":"Photography Basics"}]),
            feature("Quiz Questions", 
                    "Generate 5 multiple‑choice quiz questions for a lesson on {topic}.",
                    [{"label":"Topic","key":"topic","default":"Digital Marketing"}]),
            feature("Module Description", 
                    "Write a 2‑paragraph description for a module titled '{module_title}'.",
                    [{"label":"Module Title","key":"module_title","default":"Introduction to Python"}]),
            feature("Email Sequence", 
                    "Write a 5‑email sequence to promote a course on {topic}.",
                    [{"label":"Topic","key":"topic","default":"Yoga for Beginners"}]),
            feature("Sales Page Copy", 
                    "Write persuasive sales page copy for a course called '{course_name}'.",
                    [{"label":"Course Name","key":"course_name","default":"Learn to Code"}]),
            feature("Student Testimonial Generator", 
                    "Write 3 realistic student testimonials for a course on {topic}.",
                    [{"label":"Topic","key":"topic","default":"Public Speaking"}]),
            feature("Course Title Ideas", 
                    "Suggest 10 attention‑grabbing titles for a course on {topic}.",
                    [{"label":"Topic","key":"topic","default":"Meditation"}]),
            feature("Learning Objectives", 
                    "List 5 clear learning objectives for a course on {topic}.",
                    [{"label":"Topic","key":"topic","default":"Excel for Business"}]),
            feature("Bonus Content", 
                    "Suggest 3 bonus content pieces to add value to a course on {topic}.",
                    [{"label":"Topic","key":"topic","default":"Freelance Writing"}]),
            feature("Checklist Creator", 
                    "Create a checklist for students to complete before starting a course on {topic}.",
                    [{"label":"Topic","key":"topic","default":"Web Development"}])
        ]
    }

    # 7. Recruiting
    config["Recruiting"] = {
        "system": "You are a senior HR recruiter with 15 years of experience.",
        "features": [
            feature("Job Description", 
                    "Write a job description for a {role} position in the {industry} industry.",
                    [{"label":"Role","key":"role","default":"Software Engineer"},
                     {"label":"Industry","key":"industry","default":"FinTech"}]),
            feature("Candidate Outreach Email", 
                    "Write a polite outreach email to a candidate for a {role} position.",
                    [{"label":"Role","key":"role","default":"Data Scientist"}]),
            feature("Interview Questions", 
                    "Generate 10 interview questions for a {role} position.",
                    [{"label":"Role","key":"role","default":"Product Manager"}]),
            feature("Rejection Email", 
                    "Write a compassionate rejection email for a candidate who interviewed for {role}.",
                    [{"label":"Role","key":"role","default":"Graphic Designer"}]),
            feature("Offer Letter Draft", 
                    "Draft a professional offer letter for a {role} position with salary {salary}.",
                    [{"label":"Role","key":"role","default":"Sales Rep"},
                     {"label":"Salary","key":"salary","default":"$70,000"}]),
            feature("Onboarding Checklist", 
                    "Create a 30‑day onboarding checklist for a new {role}.",
                    [{"label":"Role","key":"role","default":"Marketing Coordinator"}]),
            feature("Job Board Description", 
                    "Write a short description for posting a {role} job on a job board.",
                    [{"label":"Role","key":"role","default":"Accountant"}]),
            feature("LinkedIn Message", 
                    "Write a LinkedIn InMail to a potential candidate for a {role} position.",
                    [{"label":"Role","key":"role","default":"UX Designer"}]),
            feature("Salary Range Suggester", 
                    "Suggest a competitive salary range for a {role} in {location}.",
                    [{"label":"Role","key":"role","default":"DevOps Engineer"},
                     {"label":"Location","key":"location","default":"New York"}]),
            feature("Skill Assessment", 
                    "Design a short skill assessment for a {role} candidate.",
                    [{"label":"Role","key":"role","default":"Content Writer"}])
        ]
    }

    # 8. Local Services
    config["Local Services"] = {
        "system": "You are a small business consultant specializing in local services.",
        "features": [
            feature("Service Description", 
                    "Write a compelling description for a {service} service in {location}.",
                    [{"label":"Service","key":"service","default":"Plumbing"},
                     {"label":"Location","key":"location","default":"Chicago"}]),
            feature("Google My Business Post", 
                    "Create a post for Google My Business promoting {service}.",
                    [{"label":"Service","key":"service","default":"Landscaping"}]),
            feature("Customer Review Reply", 
                    "Write a reply to a customer review: '{review}'",
                    [{"label":"Review","key":"review","default":"Great service!"}]),
            feature("Appointment Reminder", 
                    "Write a polite appointment reminder for a {service} appointment.",
                    [{"label":"Service","key":"service","default":"Dental cleaning"}]),
            feature("Flyer Copy", 
                    "Write copy for a flyer advertising {service} in {location}.",
                    [{"label":"Service","key":"service","default":"Tutoring"},
                     {"label":"Location","key":"location","default":"Boston"}]),
            feature("Radio Ad Script", 
                    "Write a 30‑second radio ad script for {service}.",
                    [{"label":"Service","key":"service","default":"Car detailing"}]),
            feature("Website Headline", 
                    "Generate 5 headline options for a website selling {service}.",
                    [{"label":"Service","key":"service","default":"House cleaning"}]),
            feature("Testimonial Request", 
                    "Write an email asking a happy client for a testimonial about {service}.",
                    [{"label":"Service","key":"service","default":"Personal training"}]),
            feature("Seasonal Promotion", 
                    "Create a seasonal promotion idea for {service} in {season}.",
                    [{"label":"Service","key":"service","default":"Roofing"},
                     {"label":"Season","key":"season","default":"spring"}]),
            feature("Referral Program", 
                    "Design a simple referral program for a {service} business.",
                    [{"label":"Service","key":"service","default":"Pet grooming"}])
        ]
    }

    # 9. Financial Advisors
    config["Financial Advisors"] = {
        "system": "You are a certified financial planner with 20 years of experience.",
        "features": [
            feature("Market Update Summary", 
                    "Write a weekly market update summary for a {segment} investor.",
                    [{"label":"Segment","key":"segment","default":"retail"}]),
            feature("Client Portfolio Review", 
                    "Write a summary of a client's portfolio review, highlighting performance.",
                    [{"label":"Client Name","key":"client_name","default":"John Doe"}]),
            feature("Investment Strategy", 
                    "Suggest an investment strategy for a client with {risk_tolerance} risk tolerance.",
                    [{"label":"Risk Tolerance","key":"risk_tolerance","default":"moderate"}]),
            feature("Newsletter Draft", 
                    "Write a draft for a monthly financial newsletter with topics: {topics}.",
                    [{"label":"Topics","key":"topics","default":"Retirement, Taxes, Real Estate"}]),
            feature("Risk Assessment", 
                    "Evaluate the risk level of a client's current portfolio.",
                    [{"label":"Portfolio Description","key":"portfolio","default":"80% stocks, 20% bonds"}]),
            feature("Retirement Plan Outline", 
                    "Create a high‑level retirement plan for a 45‑year‑old client earning {income}.",
                    [{"label":"Income","key":"income","default":"$100,000"}]),
            feature("Tax Tip Generator", 
                    "Provide 5 tax‑saving tips for a {income} earner.",
                    [{"label":"Income","key":"income","default":"$75,000"}]),
            feature("Estate Planning Checklist", 
                    "List 10 steps for basic estate planning.",
                    []),
            feature("Fee Schedule Explanation", 
                    "Write a clear explanation of advisory fees for a prospective client.",
                    []),
            feature("Client Meeting Agenda", 
                    "Create an agenda for a first‑time client meeting.",
                    [])
        ]
    }

    # 10. Event Planners
    config["Event Planners"] = {
        "system": "You are a professional event planner with 15 years of experience.",
        "features": [
            feature("Event Description", 
                    "Write a captivating description for a {event_type} event.",
                    [{"label":"Event Type","key":"event_type","default":"Corporate Gala"}]),
            feature("Invitation Copy", 
                    "Write a formal invitation for a {event_type}.",
                    [{"label":"Event Type","key":"event_type","default":"Wedding"}]),
            feature("Schedule Outline", 
                    "Create a detailed schedule for a {event_type} from start to finish.",
                    [{"label":"Event Type","key":"event_type","default":"Conference"}]),
            feature("Vendor Email", 
                    "Write an email to a vendor requesting a quote for {service}.",
                    [{"label":"Service","key":"service","default":"catering"}]),
            feature("Thank‑You Message", 
                    "Write a thank‑you note to send to attendees after a {event_type}.",
                    [{"label":"Event Type","key":"event_type","default":"Fundraiser"}]),
            feature("Sponsor Pitch", 
                    "Write a pitch to attract sponsors for a {event_type}.",
                    [{"label":"Event Type","key":"event_type","default":"Tech Summit"}]),
            feature("Program Script", 
                    "Write a script for the emcee of a {event_type}.",
                    [{"label":"Event Type","key":"event_type","default":"Awards Ceremony"}]),
            feature("Checklist", 
                    "Create a comprehensive checklist for planning a {event_type}.",
                    [{"label":"Event Type","key":"event_type","default":"Birthday Party"}]),
            feature("Budget Breakdown", 
                    "Provide a sample budget breakdown for a {event_type} with {budget} budget.",
                    [{"label":"Event Type","key":"event_type","default":"Wedding"},
                     {"label":"Budget","key":"budget","default":"$10,000"}]),
            feature("Post‑Event Feedback", 
                    "Design a short feedback form for attendees of a {event_type}.",
                    [{"label":"Event Type","key":"event_type","default":"Workshop"}])
        ]
    }

    return config

# Build the configuration
NICHE_FEATURES = build_niche_config()

# ----------------------------
# SIDEBAR – Niche Selection
st.sidebar.title("♾️ AION")
st.sidebar.markdown("Your AI Omniverse")
niche_list = list(NICHE_FEATURES.keys())
selected_niche = st.sidebar.selectbox("Select Your Industry", niche_list)

st.sidebar.markdown("---")
st.sidebar.caption("🔑 API Key: " + ("✅ Connected" if DEEPSEEK_API_KEY else "❌ Missing"))

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧠 Quick Actions")
if st.sidebar.button("📝 Generate Example"):
    st.session_state.quick_prompt = "Give me an example output for this niche."

# ----------------------------
# MAIN AREA
st.title(f"♾️ AION – {selected_niche}")
st.caption(f"Automate your {selected_niche} workflows with AI.")

# Get the niche config
niche_config = NICHE_FEATURES[selected_niche]
features = niche_config["features"]
system_prompt = niche_config["system"]

# Create tabs for each feature
feature_names = [f["name"] for f in features]
tabs = st.tabs(feature_names)

for idx, tab in enumerate(tabs):
    with tab:
        feature = features[idx]
        st.subheader(feature["name"])
        # Build input fields dynamically
        inputs = {}
        for input_def in feature["inputs"]:
            label = input_def["label"]
            key = input_def["key"]
            default = input_def.get("default", "")
            if "text" in input_def.get("type", "text"):  # default to text
                inputs[key] = st.text_input(label, value=default, key=f"{selected_niche}_{idx}_{key}")
            # Could add other types, but for simplicity we use text_input

        if st.button(f"🚀 Generate {feature['name']}", key=f"btn_{selected_niche}_{idx}"):
            with st.spinner("AI is working..."):
                # Format the prompt with user inputs
                try:
                    prompt_text = feature["prompt"].format(**inputs)
                except KeyError as e:
                    st.error(f"Missing placeholder: {e}. Please fill all fields.")
                    continue

                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt_text}
                ]
                result = call_deepseek(messages, max_tokens=800, temp=0.7)
                if result:
                    st.success("✅ Generated!")
                    st.markdown(result)

# ----------------------------
# HISTORY (optional – we can store in DB, but for simplicity we skip)

# ----------------------------
# FOOTER
st.markdown("---")
st.markdown('<div class="footer">♾️ AION – Your AI Omniverse. All rights reserved.</div>', unsafe_allow_html=True)