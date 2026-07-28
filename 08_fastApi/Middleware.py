from fastapi import FastAPI,Request
import time

app = FastAPI()

# @app.middleware('http')
# async def my_middleware(request: Request,call_next):
#     response = await call_next(request)
#     print('response sent')
#     return response


@app.middleware('http')
async def log_middle(request:Request,call_next):
    start_time=time.time()

    response = await call_next(request)
    process_time=time.time()-start_time
    print(f'path:{request.url.path} | Time:{process_time}')
    return response