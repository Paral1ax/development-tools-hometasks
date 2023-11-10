import datetime
from enum import Enum
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return str()


@app.post('/post')
def post() -> Timestamp:
    now = datetime.datetime.now()
    new_timestamp = Timestamp(id=len(post_db), timestamp=int(now.timestamp()))
    post_db.append(new_timestamp)
    return new_timestamp


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=422)


@app.get('/dog')
def get_dogs(kind: str):
    print(kind)
    if kind not in DogType._value2member_map_:
        raise HTTPException(status_code=422, detail="Item not found")
    kind_filter = filter(lambda dogs: dogs.kind == kind, dogs_db.values())
    return list(kind_filter)


@app.post('/dog')
def create_dog(dog: Dog) -> Dog:
    if dog.kind not in DogType or not isinstance(dog.pk, int):
        raise HTTPException(status_code=422, detail="Item cant be created")
    pk = len(dogs_db)
    new_dog = Dog(name=dog.name, pk=pk, kind=dog.kind)
    dogs_db[pk] = new_dog
    return new_dog


@app.get('/dog/{pk}')
def get_dog_by_pk(pk: int) -> Dog:
    if dogs_db.get(pk) is None:
        raise HTTPException(status_code=422, detail="Item not found")
    return dogs_db.get(pk)


@app.patch('/dog/{pk}')
def update_dog_by_pk(pk: int, dog: Dog) -> Dog:
    if dogs_db.get(pk) is None:
        raise HTTPException(status_code=422, detail="Item not found")
    dogs_db[pk].kind = dog.kind
    dogs_db[pk].name = dog.name
    return dogs_db[pk]
