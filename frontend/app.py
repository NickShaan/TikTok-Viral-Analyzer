import streamlit as st
import requests
import json

# FastAPI backend URL
BACKEND_URL = "http://127.0.0.1:8000/analyze_subject"

st.set_page_config(page_title="TikTok Viral Analyzer", page_icon="🎬", layout="wide")

st.title("🎬 TikTok Viral Analyzer")
st.write("Enter a topic (e.g., trading, fitness, comedy) and analyze why related TikToks go viral.")

# --- Input box ---
topic = st.text_input("Enter Topic", "")

if st.button("Analyze"):
    if not topic.strip():
        st.warning("⚠️ Please enter a topic first.")
    else:
        with st.spinner("Analyzing TikTok content..."):
            try:
                # Call FastAPI backend
                response = requests.get(BACKEND_URL, params={"topic": topic})
                if response.status_code == 200:
                    data = response.json()

                    if "error" in data:
                        st.error(f"Backend Error: {data['error']}")
                    else:
                        st.subheader(f"📌 Topic: {data['topic']}")

                        # Try to parse final report JSON
                        try:
                            report = json.loads(data["final_report"])
                        except Exception:
                            report = None

                        # Tabs for better UI
                        tab1, tab2, tab3 = st.tabs(["👤 Creators", "📊 Analysis", "📝 JSON Report"])

                        with tab1:
                            if report and "creators" in report:
                                st.markdown("**Summary:**")
                                st.write(report["creators"].get("summary", ""))
                                st.markdown("**Methods:**")
                                for m in report["creators"].get("methods", []):
                                    st.write(f"- {m}")
                            else:
                                st.write(data["creators"])

                        with tab2:
                            if report and "analysis" in report:
                                st.markdown("**Summary:**")
                                st.write(report["analysis"].get("summary", ""))
                                st.markdown("**Factors:**")
                                for f in report["analysis"].get("factors", []):
                                    st.write(f"- {f}")
                            else:
                                st.write(data["analysis"])

                        with tab3:
                            st.json(report if report else data["final_report"])

                else:
                    st.error(f"Backend returned error: {response.status_code}")
            except Exception as e:
                st.error(f"Request failed: {e}")
