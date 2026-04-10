from vector_search import load_data
import streamlit as st
import json

from fast_pipeline import fast_pipeline
from workflow import run_pipeline

load_data()

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="PRANA-G AI",
    page_icon="🌱",
    layout="wide"
)

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.title("⚙️ Settings")

mode = st.sidebar.radio(
    "Select Mode",
    ["fast ⚡", "smart 🧠"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "⚡ Fast Mode → Low latency\n\n"
    "🧠 Smart Mode → Deep reasoning"
)

# -----------------------
# MAIN HEADER
# -----------------------
st.title("🌱 PRANA-G AI")
st.markdown("### AI-Powered Crop Trait Generator")

st.markdown("---")

# -----------------------
# INPUT SECTION
# -----------------------
col1, col2 = st.columns([3, 1])

with col1:
    user_input = st.text_input(
        "Enter your requirement",
        placeholder="e.g. wheat in desert at high temperature"
    )

with col2:
    generate = st.button("🚀 Generate")

# -----------------------
# PROCESSING
# -----------------------
if generate:

    if user_input.strip() == "":
        st.warning("⚠️ Please enter input")
    else:
        with st.spinner("🧠 Processing with AI..."):

            if "fast" in mode:
                result = fast_pipeline(user_input)
            else:
                result = run_pipeline(user_input)

        st.markdown("---")

        # -----------------------
        # OUTPUT SECTION
        # -----------------------
        st.success("✅ Specification Generated")

        col1, col2 = st.columns(2)

        # LEFT: Structured View
        with col1:
            st.subheader("📊 Summary")

            st.write(f"**🌾 Crop:** {result.get('crop')}")
            st.write(f"**📍 Location:** {result.get('location')}")
            st.write(f"**🌡️ Temperature:** {result.get('temperature')}°C")

            st.write("**⚠️ Stress Factors:**")
            st.write(result.get("stress", []))

            st.write("**🌿 Traits:**")
            st.write(result.get("traits", []))

            st.write(f"**📈 Confidence:** {result.get('confidence')}")

        # RIGHT: JSON View
        with col2:
            st.subheader("🧾 JSON Output")
            st.json(result)

        # -----------------------
        # DOWNLOAD
        # -----------------------
        st.markdown("---")

        json_str = json.dumps(result, indent=2)

        st.download_button(
            label="⬇️ Download spec.json",
            data=json_str,
            file_name="spec.json",
            mime="application/json"
        )
        