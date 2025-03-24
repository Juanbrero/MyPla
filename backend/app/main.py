from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "¡Hola, FastAPI está funcionando!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9001, reload=True)
    