from fastapi import FastAPI

app = FastAPI()


@app.get("/")
@app.get("/status")
async def check_status():
    """ Check the status of the server.
    Returns:
        str: A message indicating if the server is running.
    """
    return "Server is running"