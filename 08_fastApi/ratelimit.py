from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse


app=FastAPI()

limiter=Limiter(key_func=get_remote_address)
app.state.limiter=limiter

@app.exception_handler(RateLimitExceeded)
def rate_limiter_handler(request:Request,exc:RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "detail":"too many Requests"
        }
    )

@app.get("/data")
@limiter.limit("5/minutes")
def get_data(request:Request):
    return{
        "message":"Success"
    }
