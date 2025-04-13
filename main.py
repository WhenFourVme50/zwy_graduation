from fastapi import FastAPI
from apis.user_apis import router as user_routers

app = FastAPI()

app.include_router(user_routers, prefix="/user")

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    # 启动 Uvicorn 服务器
    uvicorn.run(app, host="0.0.0.0", port=8001)
