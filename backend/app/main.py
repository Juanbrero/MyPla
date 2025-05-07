from fastapi import FastAPI
import uvicorn
import importlib
import sys
import secure
import os
from app.config.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
#Alembic
from alembic.config import Config
from alembic import command


from starlette.middleware.sessions import SessionMiddleware

#Esta linea importa e install ic, para poder hacer debug
from icecream import install

#ic.disable()


install()
ic.configureOutput(contextAbsPath=False, includeContext=True)

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
    # If que permite evitar las cabeceras seguras para los paths descriptos,
    # Debe eliminarse el if cuando se pase a produccion
    if not any(request.url.path.startswith(path) for path in ["/docs", "/redoc", "/openapi.json"]):
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


def run_migrations():
    """
    Function read files of alembic and upgrade or create models
    """
    base_dir = os.path.dirname(__file__)
    alembic_cfg = Config(os.path.join(base_dir, '..', 'alembic.ini'))
    command.upgrade(alembic_cfg, "head")



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

#Como en local las variables de entorno no se instancias, salvo en VSCode,
# y para no agregar la libreria dotenv, prueba tomar el variable $PORT
# si no tiene el valor llama a dotenv
if os.getenv('PORT') is None:
    import dotenv
    dotenv.load_dotenv('.env') 

addRoute(app, "app/routes")

if __name__ == "__main__":
    run_migrations()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=True)
    