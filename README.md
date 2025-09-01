TikTok Viral Analyzer
=====================

Important Note
--------------
This project does not fetch real-time TikTok trending data because TikTok does not provide a public API for such access.  
Instead, the system demonstrates the required pipeline (CrewAI + LLM orchestration + FastAPI backend + Streamlit frontend)  
and generates structured analysis and reports using Google Gemini LLM.  
If TikTok APIs or datasets were available, they could easily be integrated into this system.

Project Overview
----------------
This project was developed as part of the CrewAI Internship Task.  
It analyzes TikTok topics and explains why related videos might go viral, using a combination of:
- CrewAI agents and tasks (Researcher, Analyst, Reporter)
- A FastAPI backend
- A Streamlit frontend
- Google Gemini LLM for reasoning and structured output

The focus is on simulating the workflow and producing structured JSON insights, not on scraping TikTok directly.

Project Structure
-----------------
```
tiktok-viral-analyzer/
│
├── backend/
│   └── main.py          # FastAPI backend with CrewAI + Gemini integration
│
├── frontend/
│   └── app.py           # Streamlit frontend UI
│
├── requirements.txt     # Python dependencies
├── README.md            # Documentation
```
Workflow
--------
1. Backend (FastAPI)
   - Defines three agents: Researcher, Analyst, Reporter.
   - Each agent has a task:
     - Researcher: finds TikTok creators (simulated).
     - Analyst: explains why posts go viral.
     - Reporter: outputs structured JSON report.
   - Uses Gemini to generate outputs.

2. Frontend (Streamlit)
   - Provides a user interface where a topic is entered (e.g., love, fitness, trading).
   - Sends requests to the backend API.
   - Displays:
     - Creators
     - Analysis
     - JSON Report

3. LLM (Gemini)
   - Generates structured explanations.
   - Produces JSON output that the frontend can parse and display.

How to Run
----------
1. Backend (FastAPI)
   ```
   cd backend
   python -m uvicorn main:app --reload --port 8000
   ```
   Backend available at: http://127.0.0.1:8000  
   Example endpoint: http://127.0.0.1:8000/analyze_subject?topic=love

2. Frontend (Streamlit)
   In another terminal:
   ```
   cd frontend
   streamlit run app.py
   ```
   Frontend available at: http://localhost:8501

Example Output
--------------
Input:
```
http://127.0.0.1:8000/analyze_subject?topic=love
```

Response:
```json
{
  "creators": {
    "summary": "Real-time trending TikTok creators are not available via API.",
    "methods": [
      "Check TikTok's For You page",
      "Use relevant hashtags (#love, #couplegoals)",
      "Explore Discover page",
      "Use third-party analytics websites"
    ]
  },
  "analysis": {
    "summary": "Virality depends on relatability, emotional resonance, production quality, and use of trends.",
    "factors": [
      "Relatability",
      "Emotional resonance",
      "High-quality production",
      "Trending sounds and hashtags",
      "Community engagement",
      "Algorithm luck"
    ]
  }
}
```

Notes
-----
- Real-time TikTok scraping is not included (no public API available).  
- This project demonstrates workflow orchestration and structured output using LLMs.  
- The architecture is modular: real TikTok data could be integrated in the future.
