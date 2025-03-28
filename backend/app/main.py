from fastapi import FastAPI
import uvicorn
import importlib
import sys
import os
from app.config.database import engine, Base, init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
Base.metadata.create_all(bind=engine)
init_db()

# habilito CORS (ver de restringir origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringirlo a ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def addRoute(app, routes_path):
    for filename in os.listdir(routes_path):
        if filename.endswith(".py") and filename != "__init__.py":
            # Create the module name by removing the ".py" extension
            module_name = f"app.routes.{filename[:-3]}"
            
            # Import the module dynamically
            try:
                module = importlib.import_module(module_name)
            except ModuleNotFoundError as e:
                print(f"Failed to import module {module_name}: {e}")
                continue
            
            # Include the router from the module
            if hasattr(module, "router"):
                app.include_router(module.router)
            else:
                print(f"No router found in module {module_name}")

addRoute(app, "/app/app/routes")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=True)
    