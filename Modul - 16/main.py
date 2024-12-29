# Импорт библиотек
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List
from pydantic import BaseModel

# Создаем экземпляр приложения FastAPI
app = FastAPI()
users = []  # Храним пользователей в виде списка
templates = Jinja2Templates(directory='templates')  # Подключение шаблонизатора



class User(BaseModel):
    id: int
    username: str
    age: int


# Получение всех пользоватилей
@app.get('/')
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/users/{user_id}')
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        # Возвращаем список всех пользователей
        return templates.TemplateResponse('users.html', {'request': request, 'user': users[user_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail='Message not found!')


@app.post('/user/{username}/{age}')
async def registered_user(username: str, age: int) -> User:
    # Регистрируем нового пользователя с уникальным ID
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int) -> User:
    # Обновляем данные существующего пользователя
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
        
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def deleted_user(user_id: int) -> User:
    # Удаляем пользователя по его ID
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
        
    raise HTTPException(status_code=404, detail='User was not found')
