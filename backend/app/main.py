from fastapi import FastAPI

app = FastAPI(title="Primer API")


@app.get("/health")
async def health():
    return {"status": "ok"}
