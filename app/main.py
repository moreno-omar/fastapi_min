import uvicorn

if __name__ == "__main__":
    # app.app is the file, app is the FastAPI instance in the file.
    uvicorn.run("app.app:app", host="0.0.0.0", log_level="info")