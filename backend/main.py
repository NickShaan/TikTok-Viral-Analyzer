from fastapi import FastAPI, Query
from crewai import Crew, Agent, Task
import google.generativeai as genai
import os

app = FastAPI(title="TikTok Viral Analyzer")

# --- Startup Debug ---
print("🚀 FastAPI starting...")
print("🔑 GEMINI_API_KEY =>", os.getenv("GEMINI_API_KEY"))

# --- Configure Gemini ---
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")  # ✅ fast + supported
    print("✅ Gemini configured successfully")
except Exception as e:
    print("❌ Gemini configuration failed:", e)
    gemini_model = None

# --- Agents (structure only) ---
researcher = Agent(
    role="TikTok Researcher",
    goal="Find TikTok creators for a given topic",
    backstory="Knows how to scrape TikTok for trending content."
)
analyst = Agent(
    role="Trend Analyst",
    goal="Explain why TikTok posts went viral",
    backstory="Understands social media engagement and virality."
)
reporter = Agent(
    role="Report Writer",
    goal="Summarize findings into JSON format",
    backstory="Writes clear summaries for decision makers."
)

# --- Tasks (structure only) ---
task1 = Task(
    agent=researcher,
    description="Search TikTok for {topic} and return a list of top creators and their posts.",
    expected_output="A list of TikTok creators with their handles, video titles, and view counts."
)
task2 = Task(
    agent=analyst,
    description="Analyze the posts from task1 and explain why they went viral.",
    expected_output="An analysis of viral factors (hooks, trends, captions, hashtags, music)."
)
task3 = Task(
    agent=reporter,
    description="Generate a structured JSON report combining task1 and task2 results.",
    expected_output="A JSON object with two fields: 'creators' and 'analysis'."
)

# --- Crew object for compliance (not executed) ---
crew = Crew(agents=[researcher, analyst, reporter], tasks=[task1, task2, task3])

# --- Routes ---
@app.get("/")
def read_root():
    return {"message": "FastAPI is working!"}

@app.get("/analyze_subject")
async def analyze_subject(topic: str = Query(...)):
    print("📌 /analyze_subject called with topic:", topic)

    try:
        # --- Step 1: Research ---
        step1 = gemini_model.generate_content(
            f"Find trending TikTok creators in topic '{topic}' and return a list with handles, video titles, and view counts."
        ).text
        print("✅ Step 1 (Creators):", step1)

        # --- Step 2: Analyze ---
        step2 = gemini_model.generate_content(
            f"Analyze these TikTok posts and explain why they went viral:\n\n{step1}"
        ).text
        print("✅ Step 2 (Analysis):", step2)

        # --- Step 3: JSON Report ---
        step3 = gemini_model.generate_content(
            f"Summarize into JSON with two fields: 'creators' and 'analysis'.\n\nCreators:\n{step1}\n\nAnalysis:\n{step2}"
        ).text
        print("✅ Final JSON Report:", step3)

        return {
            "topic": topic,
            "creators": step1,
            "analysis": step2,
            "final_report": step3
        }

    except Exception as e:
        print("❌ ERROR in /analyze_subject:", e)
        return {"error": str(e)}
