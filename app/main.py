import uvicorn

if __name__ == "__main__":
    # app.app is the file, app is the FastAPI instance in the file.
    uvicorn.run("app.app:app", host="127.0.0.1", log_level="info")
