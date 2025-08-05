
import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# get OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_DEMO_MODE = not OPENAI_API_KEY  # it Enables demo mode if key is missing

if not USE_DEMO_MODE:
    client = OpenAI(api_key=OPENAI_API_KEY)

# the page configuration
st.set_page_config(page_title="Banking Feedback Analyzer", layout="wide")

st.title("Banking Feedback Analyzer :D")
st.markdown("Upload customer feedback in CSV format and get automated sentiment and insights using GPT.")

# uploading the CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        if "feedback" not in df.columns:
            st.error("CSV must have a column named 'feedback'!!")
        else:
            st.success(f"Loaded {len(df)} feedback entries.")
            st.dataframe(df.head(), use_container_width=True)

            # Analyzing feedback with GPT
            with st.spinner("Analyzing feedback..."):

                def analyze_feedback(text):
                    if USE_DEMO_MODE:
                        return "Demo mode is enabled. No analysis performed."
                    try:
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {
                                    "role": "system",
                                    "content": "You are an AI assistant that provides short summaries and sentiment ratings (positive, neutral, negative) of customer feedback in banking."
                                },
                                {
                                    "role": "user",
                                    "content": f"Analyze this customer feedback: {text}"
                                }
                            ]
                        )
                        return response.choices[0].message.content.strip()
                    except Exception as e:
                        return f"Error: {str(e)}"

                df["Analysis"] = df["feedback"].apply(analyze_feedback)

            st.subheader("📊 Analyzed Feedback")
            st.dataframe(df, use_container_width=True)

            # leting user download the results (optional)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Results as CSV", data=csv, file_name="analyzed_feedback.csv", mime="text/csv")

    except Exception as e:
        st.error(f"!! Error reading file: {e}")
else:
    st.info("Please upload a CSV file containing a 'feedback' column.")