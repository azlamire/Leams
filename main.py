import os
from fastapi import FastAPI
from ../scripts/scrapper/main.py import main
import asyncio, json

app = FastAPI()

async def jowly_categories():
    categories = main()
    with open(os.path.abspath(f'scrapper/idk.json'),'w') as file:
        file.write(json.dumps(categories))

@app.get("/")
def xz()
    asyncio.create_task
