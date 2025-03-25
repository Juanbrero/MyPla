from fastapi import FastAPI
import uvicorn
import importlib
import sys
import os
from app.config.database import engine, Base, init_db

app = FastAPI()
Base.metadata.create_all(bind=engine)
init_db()

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
    uvicorn.run(app, host="127.0.0.1", port=9001, reload=True)
    