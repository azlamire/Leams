from fastapi import FastAPI, Request

router = FastAPI()


@router.middleware("http")
async def token_check(request: Request):
    pass
    # return JSONResponse(status.HTTP_401_UNAUTHORIZED, content
