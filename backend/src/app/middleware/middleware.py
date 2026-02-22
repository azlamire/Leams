from fastapi import FastAPI, Request, status

router = FastAPI()


@router.middleware("http")
async def token_check(request: Request):
    has_token = request.headers.get("Authorization")
    # return JSONResponse(status.HTTP_401_UNAUTHORIZED, content
