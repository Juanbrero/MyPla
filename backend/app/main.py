from fastapi import FastAPI
import uvicorn
import importlib
import sys
import secure
import os
from app.config.database import engine, Base, init_db
from fastapi.middleware.cors import CORSMiddleware
#Scheme Table DB
from app.models.Event import Event
from app.models.User import User 
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()

csp = secure.ContentSecurityPolicy().default_src("'self'").frame_ancestors("'none'")
hsts = secure.StrictTransportSecurity().max_age(31536000).include_subdomains()
referrer = secure.ReferrerPolicy().no_referrer()
cache_value = secure.CacheControl().no_cache().no_store().max_age(0).must_revalidate()
x_frame_options = secure.XFrameOptions().deny()

secure_headers = secure.Secure(
    csp=csp,
    hsts=hsts,
    referrer=referrer,
    cache=cache_value,
    xfo=x_frame_options,
)


@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    if not any(request.url.path.startswith(path) for path in ["/docs", "/redocs", "/openapi.json"]):
        secure_headers.framework.fastapi(response)
    return response

app.add_middleware(SessionMiddleware, secret_key="!secret")
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
    