from fastapi import APIRouter
# from fastapi.responses import JSONResponse
# from app.services.s3 import S3Client

# TODO: Make something with this func and Depends
# import json

router = APIRouter()


@router.get("/main/categories{id}")
async def get_categories(id: int):
    pass
    # with open("category.json", "r") as testing:
    #     test = json.load(testing)
    #     try:
    #         return list(test.items())[id][1]
    #     except:
    #         return JSONResponse(status_code=404, content={"content": ""})


@router.get("/main/subs{id}")
async def get_subs(id: int):
    pass
    # content = await S3Client(bucket_name="testing").get_file(name_file="DemoSubs.json")
    # return content


@router.get("/main/streams{id}")
async def get_streams(id: int):
    # // TODO: hardcoded link though, solve it
    pass
    # with open("streams.json", "r") as testing:
    #     test = json.load(testing)
    #     try:
    #         print(list(test.items())[id])
    #         return list(test.items())[id]
    #     except:
    #         return JSONResponse(status_code=404, content={"content": ""})
