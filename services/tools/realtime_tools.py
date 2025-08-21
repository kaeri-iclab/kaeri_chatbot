import requests
from datetime import datetime
from langchain_core.tools import tool
import os


@tool
def get_current_datetime() -> str:
    """
    Returns the current date and time in a human-readable format.
    Use this tool to answer any questions about the current date, time, or day of the week.
    오늘의 날짜, 현재 시간, 요일과 관련된 질문에 답하기 위해 이 도구를 사용하세요.
    """
    now = datetime.now()
    return now.strftime("%Y년 %m월 %d일 %A %H시 %M분")

@tool
def get_current_weather(city: str) -> str:
    """
    Provides the current weather for a specified city.
    Use this tool for any questions about the weather.
    특정 도시의 현재 날씨에 대한 질문에 이 도구를 사용하세요.
    """
    # 사용자의 편의를 위해 대전의 위도, 경도를 미리 설정해 둡니다.
    city_coords = {
        "대전": {"latitude": 36.3504, "longitude": 127.3845},
        # 필요하다면 다른 도시를 추가할 수 있습니다.
        "서울": {"latitude": 37.5665, "longitude": 126.9780}
    }

    if city not in city_coords:
        return f"죄송합니다, '{city}'의 날씨 정보는 제공하지 않습니다. '대전'의 날씨를 물어봐 주세요."

    coords = city_coords[city]
    lat = coords["latitude"]
    lon = coords["longitude"]

    # Open-Meteo API URL
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킴
        data = response.json()

        current = data["current_weather"]
        temp = current["temperature"]
        windspeed = current["windspeed"]
        weather_code = current["weathercode"]

        # 날씨 코드를 이해하기 쉬운 한글로 변환
        weather_desc = "맑음"
        if weather_code > 0 and weather_code <= 3:
            weather_desc = "구름 조금"
        elif weather_code > 3:
            weather_desc = "흐림 또는 비/눈"

        return f"현재 {city}의 날씨는 '{weather_desc}'이며, 기온은 섭씨 {temp}도, 풍속은 시속 {windspeed}km 입니다."

    except requests.exceptions.RequestException as e:
        return f"날씨 정보를 가져오는 중 오류가 발생했습니다: {e}"
