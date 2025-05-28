from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from apis.user_apis import router as user_routers
from apis.shelter_apis import router as shelter_routers
from apis.animal_apis import router as animal_routers

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境建议指定具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_routers, prefix="/user")
app.include_router(shelter_routers, prefix="/shelter")
app.include_router(animal_routers, prefix="/animal")

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    # 启动 Uvicorn 服务器
    uvicorn.run(app, host="0.0.0.0", port=8001)
