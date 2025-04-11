import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Streamlit page config
st.set_page_config(
    page_title="Whop Market Trends Analyzer",
    page_icon="📈",
    layout="centered"
)

# Custom CSS Styling (Same as Crypto App)
st.markdown("""
<style>
    :root {
        --primary-color: #4A6FFF;
        --secondary-color: #344054;
        --background-color: #F9FAFB;
        --text-color: #1D2939;
        --light-gray: #EAECF0;
    }

    .stApp { background-color: var(--background-color); }
    .main-title {
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 32px;
        margin-bottom: 8px;
        padding-top: 20px;
    }
    .subtitle {
        color: var(--secondary-color);
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 16px;
        margin-bottom: 25px;
        opacity: 0.8;
    }
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 500;
        font-size: 16px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #3A5CD0;
    }
    .stTextInput>div>div>input {
        border-radius: 6px;
        border: 1px solid var(--light-gray);
        padding: 12px 16px;
        font-size: 16px;
    }
    .stTextInput>div>div>input:focus {
        border-color: var(--primary-color);
    }
    .info-box {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(16, 24, 40, 0.1);
        text-align: center;
        font-size: 18px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Headers
st.markdown("<div class='main-title'>E-commerce Product Insights</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Powered by Groq + DuckDuckGo</div>", unsafe_allow_html=True)

# Input
query = st.text_input("", placeholder="Enter The Product Here ...").strip()

# Agent setup
whop_agent = Agent(
    name="Whop Trend Analyst",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=[
        "You are a business trend analyst.",
        "Use DuckDuckGo to search for trends, reviews, Reddit discussions, and blog chatter about Whop App and competitors.",
        "Summarize using sentiment analysis, key market drivers, pros/cons, and potential market opportunities.",
        "Format the output in markdown with bullets, emojis, and headings."
    ],
    markdown=True
)

# Button to run query
if st.button("Generate Response"):
    if query:
        with st.spinner("Analyzing..."):
            try:
                response = whop_agent.run(query).content
                st.markdown(f"<div class='info-box'>{response}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error("Failed to fetch insights.")
                st.exception(e)
    else:
        st.warning("Please enter a valid query.")
