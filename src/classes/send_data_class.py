import json

from aiohttp import ClientSession

from src.config import Settings
from src.database.schemas import PredictFree, PredictModel


class SendData:

    def __init__(self):
        self.settings = Settings
        self.clientsession = ClientSession

    async def send_data_recomendate(
        self,
        data: PredictModel,
    ) -> dict:
        async with self.clientsession() as session:
            data = {
                "gender": data.gender,
                "foreign_citizenship": data.foreign_citizenship,
                "military_service": data.military_service,
                "gpa": data.gpa,
                "points": data.points,
                "bonus_points": data.bonus_points,
                "exams": data.exams,
            }

            async with session.post(
                self.settings.RECOMENDATE,
                json=data,
                ssl=False,
            ) as resp:
                rec = await resp.text()
                directions = json.loads(rec)
                return directions.get("directions")

    async def send_data_classifier_applicants(
        self,
        data: PredictModel,
        directions: list,
    ) -> dict:
        async with self.clientsession() as session:
            correct_data = {"applicants": []}
            array = [
                correct_data["applicants"].append(
                    {
                        "year": data.year,
                        "gender": data.gender,
                        "gpa": data.gpa,
                        "points": data.points,
                        "direction": str(i.get("name")),
                    }
                )
                for i in directions
            ]

            async with session.post(
                url=self.settings.CLASSIFIER,
                json=correct_data,
                ssl=False,
            ) as resp:
                rec = await resp.text()
                data = json.loads(rec)
                return data.get("probabilities")

    async def send_data_classifier_applicant(
        self,
        data: PredictFree,
    ) -> dict:
        async with self.clientsession() as session:
            data = {
                "year": data.year,
                "gender": data.gender,
                "gpa": data.gpa,
                "points": data.points,
                "direction": data.direction,
            }

            async with session.post(
                url=f"{self.settings.CLASSIFIER_FREE}",
                json=data,
                ssl=False,
            ) as resp:
                rec = await resp.text()
                return json.loads(rec)

    async def send_data_directions(
        self,
        direction_id: int,
    ) -> dict:
        async with self.clientsession() as session:
            async with session.get(
                url=f"{self.settings.DIRECTION}{direction_id}",
                ssl=False,
            ) as data:
                direction_data = await data.text()
                direction = json.loads(direction_data)
                return direction.get("description")

    async def send_data_points(
        self,
        direction_id: int,
    ) -> dict:
        async with self.clientsession() as session:
            async with session.get(
                url=f"{self.settings.DIRECTION_POINTS}{direction_id}",
                ssl=False,
            ) as data:
                direction_points_data = await data.text()
                cl = json.loads(direction_points_data)
                return cl.get("history")

    async def send_message_bot(
        self,
        message: str,
    ) -> dict:
        async with self.clientsession() as session:
            data = {
                "question": message,
            }
            async with session.post(
                url=self.settings.RAG_GigaChat_API,
                json=data,
                ssl=False,
            ) as data:
                answer_data = await data.text()
                return json.loads(answer_data)

    async def visitor_add(
        self,
        event_id: int,
        user_id: int,
    ) -> dict:
        async with self.clientsession() as session:
            async with session.post(
                url=f"{self.settings.VISITORS_ADD}{event_id}/{user_id}",
                ssl=False,
            ) as data:
                add_data = await data.text()
                return json.loads(add_data)

    async def visitor_get(
        self,
        user_id: int,
    ) -> dict:
        async with self.clientsession() as session:
            async with session.get(
                url=f"{self.settings.VISITORS_GET}{user_id}",
                ssl=False,
            ) as data:
                get_data = await data.text()
                return json.loads(get_data)

    async def visitor_delete(
        self,
        event_id: int,
        user_id: int,
    ) -> dict:
        async with self.clientsession() as session:
            async with session.delete(
                url=f"{self.settings.VISITORS_DELETE}{event_id}/{user_id}",
                ssl=False,
            ) as data:
                delete_data = await data.text()
                return json.loads(delete_data)

    async def get_token_user_vk(
        self,
        params: dict,
    ) -> dict:
        async with self.clientsession() as session:
            async with session.post(
                Settings.VK_TOKEN_URL,
                json=params,
                ssl=False,
            ) as data:
                user_data = await data.json()
                return user_data

    async def get_data_user_vk(
        self,
        params: dict,
    ) -> dict:
        async with self.clientsession() as session:
            async with session.post(
                Settings.VK_API_URL,
                json=params,
                ssl=False,
            ) as data:
                user_data = await data.json()
                return user_data.get("user")

    async def get_token_user_yandex(
        self,
        params: str,
    ) -> dict:
        async with self.clientsession() as session:
            async with session.post(
                url=Settings.YANDEX_TOKEN_URL,
                data=params,
                ssl=False,
            ) as data:
                user_data = await data.json()
                return user_data

    async def get_data_user_yandex(
        self,
        params: dict,
    ) -> dict:
        async with self.clientsession() as session:
            async with session.get(
                Settings.YANDEX_API_URL,
                params=params,
                ssl=False,
            ) as data:
                user_data = await data.json()
                return user_data

    async def registration_vk(self, params: dict):
        async with self.clientsession() as session:
            async with session.post(
                Settings.REGISTRATION_VK,
                json=params,
                ssl=False,
            ) as data:
                vk = await data.json()
                return vk

    async def registration_yandex(self, params: dict):
        async with self.clientsession() as session:
            async with session.post(
                Settings.REGISTRATION_YANDEX,
                json=params,
                ssl=False,
            ) as data:
                yandex = await data.json()
                return yandex
