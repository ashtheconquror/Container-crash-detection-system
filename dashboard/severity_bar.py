import streamlit as st

def severity_bar(level, color):
    st.markdown(
        f"""
        <div style="
            background-color:{color};
            padding:20px;
            border-radius:10px;
            text-align:center;
            color:white;
            font-size:22px;
            font-weight:bold;">
            Severity Level: {level}
        </div>
        """,
        unsafe_allow_html=True
    )
