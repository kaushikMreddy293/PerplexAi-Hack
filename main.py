from fastapi import FastAPI, Query, HTTPException
from perplexity_Client import get_perplexity_response

app = FastAPI()

@app.get("/ask")
def ask(query: str = Query(..., description="Your question for Perplexity")):
    try:
        result = get_perplexity_response(query)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
