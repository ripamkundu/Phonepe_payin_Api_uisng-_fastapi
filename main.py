from fastapi import FastAPI
from routers.payapi import router as payapi_router
from routers.callback import router as callback_router
import uvicorn

app = FastAPI(
   title="PhonePe",
   description="PhonePe",
   version="1.0.0",
   openapi_url="/openapi.json",
   docs_url="/docs",
   redoc_url="/redoc",
)

app.include_router(payapi_router)
app.include_router(callback_router)


if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
