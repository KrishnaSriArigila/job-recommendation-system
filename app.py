import streamlit as st
import pandas as pd
from job_recommender import recommend_jobs

# ✅ Set browser tab title and icon
st.set_page_config(
    page_title="Job Recommendation System",
    page_icon="💼",
    layout="centered"
)

# ✅ App Title
st.title("💼 Job Recommendation System")

# ✅ Description
st.write("""
Welcome to the **Job Recommendation System**!  
Just enter your skills below and we’ll suggest jobs that best match your profile.  
Try skills like: `Python`, `Machine Learning`, `SQL`, `Java`, etc.
""")

# ✅ Text input
user_input = st.text_input("🛠️ Enter your skills (comma-separated):", "")

# ✅ Button click
if st.button("🔍 Recommend Jobs"):
    if user_input.strip() == "":
        st.warning("Please enter some skills to get recommendations.")
    else:
        try:
            recommendations = recommend_jobs(user_input)

            if recommendations.empty:
                st.info("No matching jobs found. Try different or more skills.")
            else:
                st.success("Top job matches for you:")
                st.dataframe(recommendations.reset_index(drop=True))

        except Exception as e:
            st.error(f"Something went wrong: {e}")



