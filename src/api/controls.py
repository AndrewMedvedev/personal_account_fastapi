from jose.exceptions import JWTError

from jose import jwt
import json
import aiohttp
from src.config import Settings


async def send_data_recomendate(data):
    async with aiohttp.ClientSession() as session:
        data = {
            "top_n": data.top_n,
            "user": {
                "gender": data.gender,
                "age": data.age,
                "sport": data.sport,
                "foreign": data.foreign,
                "gpa": data.gpa,
                "total_points": data.points,
                "bonus_points": data.bonus_points,
                "exams": data.exams,
                "education": data.education,
                "study_form": data.study_form,
            },
        }

        async with session.post(
            Settings.RECOMENDATE,
            json=data,
        ) as resp:
            rec = await resp.text()
            return json.loads(rec)


async def send_data_classifier_applicants(data, directions):
    async with aiohttp.ClientSession() as session:

        correct_data = {"applicants": []}
        array = [
            correct_data["applicants"].append(
                {
                    "gender": data.gender,
                    "gpa": data.gpa,
                    "priority": data.priority,
                    "points": data.points,
                    "direction": i[23::],
                }
            )
            for i in directions
        ]

        async with session.post(
            Settings.CLASSIFIER,
            json=correct_data,
        ) as resp:
            rec = await resp.text()
            return json.loads(rec)


async def send_data_classifier_applicant(data):
    async with aiohttp.ClientSession() as session:
        data = {
            "gender": data.gender,
            "gpa": data.gpa,
            "priority": data.priority,
            "points": data.points,
            "direction": data.direction,
        }

        async with session.post(
            Settings.CLASSIFIER_FREE,
            json=data,
        ) as resp:
            rec = await resp.text()
            return json.loads(rec)


async def token(token):
    if not token:
        return None
    else:
        try:
            access = jwt.decode(token, Settings.SECRET_KEY, Settings.ALGORITHM)
            if "user_name" not in access and "mode" not in access:
                return None
            if access.get("mode") != "access_token":
                return None
            return access.get("user_name")
        except JWTError:
            return None
