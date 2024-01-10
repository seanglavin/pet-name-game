from fastapi import FastAPI
import httpx
from dotenv import load_dotenv
import os
from app.get_cats_data import get_cats


load_dotenv()


app = FastAPI()


PETFINDER_API_KEY = os.getenv("PETFINDER_API_KEY")
PETFINDER_API_SECRET = os.getenv("PETFINDER_API_SECRET")

access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJJRWxZUzRETFFLQ1N1UURyTm90TmZHWFpVNkg3RmI5MENIMzNRNGR5NlVsTkJld0hhYSIsImp0aSI6IjFhYjdhOTM4YmE1ZThiOTM2ZDBkMDJhM2ZjNjg0YmExM2NiZTAwZTY1OWIwZjQ1YjE3ZWRkYjA0YmQ5ODcxMDM1Yjg1ZDI2ZjU3YjYzZThlIiwiaWF0IjoxNzA0ODQ3NjQ4LCJuYmYiOjE3MDQ4NDc2NDgsImV4cCI6MTcwNDg1MTI0OCwic3ViIjoiIiwic2NvcGVzIjpbXX0.HEC-iB2jT6v-WODxj2KfCMMitFUwZubLfeVfgdGOoZeG17p0MLscOyhK4dX4QQyqoPG0hwGJZIR_Vfl8T_LNV4DPEx4w6DkzLKgm40Q8grAw5WWONeQMl2ne6evQgUTKQvsYAIqfCIPGXmol1Ipf6cbJHYrQe6KnccmAv3ihwSEid11qBFWW58AVBrofXUK03avN35cb5-skrOQYYc9V5vO0RlXW53hQwm9NpLfy8235QHF75gyEPANpBUk4-B0xbvvQjH2XjhffEOHw4vjHHnF_PjL7b9vmqZtVjeM7ikmSzbWFuUhG-2qx2m2MlB5yGONFFd27yFIldDj2oX3cRA"


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/get_cats")
async def get_cats_endpont():
    cats_data = get_cats()
    return cats_data