import streamlit as st
from datetime import datetime
import requests
# Sample Data for Conversation History
conversations = [
    {
        "summary": "Discussed loan options and interest rates.",
        "avg_sentiment": "Positive",
        "ai_suggestions": "Explore lower interest rates",
        "created_at": datetime(2023, 11, 1, 10, 30)
    },
    {
        "summary": "Inquired about account opening procedures.",
        "avg_sentiment": "Neutral",
        "ai_suggestions": "Send welcome guide",
        "created_at": datetime(2023, 10, 28, 15, 45)
    },
]

# Setting Page Configuration
st.set_page_config(page_title="Raiffeisen Bank Conversations", page_icon="🏦")

# Apply CSS to style the sidebar background, text color, borders, and padding
st.markdown(
    """
    <style>
        /* Set the sidebar background color to yellow and text color to black */
        [data-testid="stSidebar"] {
            background-color: #FFCC00;
            color: black;
        }
        /* Make sidebar text color black */
        [data-testid="stSidebar"] * {
            color: black;
        }
        /* Set black borders and add padding below the "Conversation History" header */
        [data-testid="stSidebar"] h2 {
            border: 1px solid black;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px; /* Adds space between the header and conversation list */
        }
        /* Style for entire expander with black border and padding */
        [data-testid="stSidebar"] .st-expander {
            border: 1px solid black;
            border-radius: 5px;
            padding: 5px;
            margin-bottom: 10px; /* Adds space between expanders */
        }
        /* Larger text for expander titles */
        [data-testid="stSidebar"] .st-expander label {
            font-size: 1.2em;
            font-weight: bold;
            color: black;
            display: inline-block;
        }
        /* Styling each conversation block with black borders and padding */
        .conversation-container {
            background-color: #FFCC00;
            color: black;
            border: 1px solid black;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)
# Sidebar - Black Background with Yellow Text for Conversation History Title
st.sidebar.markdown(
    "<h2 style='background-color: black; color: #FFCC00; padding: 10px; border-radius: 5px;'>🟡 Conversation History</h2>", 
    unsafe_allow_html=True
)

conversations = requests.get('http://localhost:8000/convos').json()

# Displaying each Conversation in Sidebar with Yellow Background, Black Text, and Larger Titles with Borders
for idx, conversation in enumerate(conversations):
    with st.sidebar.expander(f"🟡 {conversation['title']}", expanded=False):
        st.markdown(
            f"""
            <div class='conversation-container'>
                <p><strong>Summary:</strong> {conversation['summary']}</p>
                <p><strong>Avg Sentiment:</strong> {conversation['avg_sentiment']}</p>
                <p><strong>AI Suggestions:</strong> {conversation['ai_suggestions']}</p>
                <p><strong>Date:</strong> {conversation['created_at']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Main Area - Header with Yellow Accent
st.markdown("<h1 style='color: #FFCC00;'>Raiffeisen Bank Conversation Analysis</h1>", unsafe_allow_html=True)
st.write("Select a conversation from the left to view details.")
