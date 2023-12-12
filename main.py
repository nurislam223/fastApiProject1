from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

ratings = [
    {"comic_id": 1, "user_id": 1, "value": 1 },
    {"comic_id": 1, "user_id": 2, "value": 2 },
    {"comic_id": 1, "user_id": 3, "value": 3 },
    {"comic_id": 2, "user_id": 1, "value": 1},
    {"comic_id": 2, "user_id": 2, "value": 2},
    {"comic_id": 2, "user_id": 3, "value": 3},
    {"comic_id": 3, "user_id": 1, "value": 1 },
    {"comic_id": 3, "user_id": 2, "value": 2 },
    {"comic_id": 3, "user_id": 3, "value": 3 }
]


@app.get("/")
def home():
    return "hello world"


class Comic(BaseModel):
    id: int
    title: str
    author: str
    rating: float = Field(default=0)


class Rating(BaseModel):
    comic_id: int
    user_id: int
    value: int = Field(None, ge=1, le=5)


@app.post("/api/ratings/")
async def change_rating(data: Rating):
    user_rating = [r["value"] for r in ratings if r["user_id"] == data.user_id and r["comic_id"] == data.comic_id]
    if len(user_rating) >= 1:
        for i in ratings:
            if i["user_id"] == data.user_id:
                i["value"] = data.value
    else:
        ratings.append(data.__dict__)
    rating_list = [rating["value"] for rating in ratings if rating["comic_id"] == data.comic_id]
    ratings_avg = sum(rating_list)/len(rating_list)
    return {"status": 200, "data": ratings_avg}


@app.get("/api/comics/{comic_id}/rating/")
async def get_rating(comic_id: int):
    avg = 0
    summ = 0
    for rating in ratings:
        if rating.get("comic_id") == comic_id:
            avg += rating.get("value")
            summ += 1
    if summ == 0:
        return {"status": 200, "data": "Еще никто не оценил"}
    else:
        return {"status": 200, "data": avg/summ}







