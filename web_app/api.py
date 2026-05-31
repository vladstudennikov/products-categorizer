import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Add the project root to sys.path so we can import from other folders
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategy_descriptor_agent.agent import StrategyAnalyzerAgent

app = FastAPI(title="Strategy Analyzer Dashboard")

# Serve static files
app.mount("/static", StaticFiles(directory="web_app/static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("web_app/static/index.html")

@app.get("/api/analyze")
async def analyze():
    """
    Triggers the strategy analysis process.
    """
    try:
        analyzer = StrategyAnalyzerAgent()
        report = analyzer.analyze_strategy()
        return {"report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
