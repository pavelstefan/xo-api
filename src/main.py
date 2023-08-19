from fastapi import FastAPI

from .routes import user, auth, game

app = FastAPI()


@app.get('/status', tags=['utils'])
async def status():
    return 'OK'


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(game.router)
