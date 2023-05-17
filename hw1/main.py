from fastapi import FastAPI, HTTPException
import aiohttp
import os
from urllib.parse import urlencode

app = FastAPI()

host = os.environ["API_HOST"]
api_key = os.environ["API_KEY"]


@app.get("/v1/forecast")
async def forecast(city: str, dt: int):
    try:
        async with aiohttp.ClientSession() as session:
            params = urlencode({"key": api_key, "q": city, "dt": dt})
            async with session.get(host + "/v1/forecast.json?" + params) as response:
                response = await response.json()
                return {
                    "city": response["location"]["name"],
                    "unit": "celsius",
                    "temperature": response["forecast"]["forecastday"][0]["day"][
                        "avgtemp_c"
                    ],
                }
    except aiohttp.ClientConnectorError as e:
        raise HTTPException(status_code=502)


@app.get("/v1/current")
async def forecast(city: str):
    try:
        async with aiohttp.ClientSession() as session:
            params = urlencode({"key": api_key, "q": city})
            async with session.get(host + "/v1/current.json?" + params) as response:
                response = await response.json()
                return {
                    "city": response["location"]["name"],
                    "unit": "celsius",
                    "temperature": response["current"]["temp_c"],
                }
    except aiohttp.ClientConnectorError as e:
        raise HTTPException(status_code=502)
