from fastapi import FastAPI
from .fastapi_server import router as api_router
from .websocket_server import router as ws_router

# 创建 FastAPI 实例
app = FastAPI(title="NebulaVerseAI API", version="1.0")

# 注册 REST API 和 WebSocket 端点
app.include_router(api_router, prefix="/api")
app.include_router(ws_router, prefix="/ws")

__all__ = ["app"]
