from fastapi import FastAPI

app = FastAPI(
    title="ResolveAI",
    description="Multi-Agent Customer Support Resolution Platform",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "resolveai",
        "version": "0.1.0",
    }