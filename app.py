import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings import title, host, port, origins
import models
from routers.auth import auth_route
from routers.user import user_route


app = FastAPI(title=title, docs_url="/api/docs",
              openapi_url="/api/openapi.json", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_route, prefix="/api/user")
app.include_router(auth_route, prefix="/api/auth")


@app.get("/")
async def root():
    return "API сервер Read Craft Academy"


if __name__ == "__main__":
    models.database_create()

    uvicorn.run("app:app", port=port,
                host=host, reload=True)
