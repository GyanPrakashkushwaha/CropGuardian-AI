import httpx

async def get_static_weather():
    lat = 52.52    # static for now  
    lon = 13.41
# https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation,precipitation_probability,soil_moisture_0_to_1cm,shortwave_radiation
    url = f"""https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation,precipitation_probability,soil_moisture_0_to_1cm,shortwave_radiation"""
    
    print(url)

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=20.0)
        resp.raise_for_status()
        return resp.json()
