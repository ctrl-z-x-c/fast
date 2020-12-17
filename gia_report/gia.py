from pydantic import BaseModel
from typing import Optional, List
from .solution import loop
from test_aioredis import set_redis, get_redis

from fastapi import APIRouter

Gia_Router = APIRouter()


# input template
class DifStage(BaseModel):
    stageData: List[dict] = [
        {
            "stage": 20,
            "stageResult": {"right": 233, "error": 172},
        },
        {
            "stage": 21,
            "stageResult": {"right": 102, "error": 10},
        },
        {
            "stage": 22,
            "stageResult": {"right": 87, "error": 10},
        },
        {
            "stage": 23,
            "stageResult": {"right": 40, "error": 5},
        },
        {
            "stage": 24,
            "stageResult": {"right": 149, "error": 2},
        }
    ]


# input template
class GiaPost(BaseModel):
    userInfo: dict = {
        "provinceName": "北京",
        "cityName": "北京市",
        "regionName": "东城区",
        "reportNo": "20007615495",
        "nickname": "倪一",
        "gradeName": "高三",
        "mobile": "",
        "sex": 1,
    }


# return template
class GiaResults(BaseModel):
    result_dict: dict = {
        "20": {
        },
        "21": {
        },
        "22": {
        },
        "23": {
        },
        "24": {
        },
    }

    userinfo: dict


@Gia_Router.post('/gia', response_model=GiaResults)
async def gia(
        userinfo: GiaPost, stagedata: DifStage
):
    # the finally result dict,include 5 kinds and gti
    result_dict = await loop(stagedata)

    return {
        "result_dict": result_dict,
        "userinfo": userinfo
    }
