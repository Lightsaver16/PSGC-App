from main import app


@app.get("/")
def home():
    return {"message": "THE PSGC APP"}