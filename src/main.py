from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import user, auth, game

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/status', tags=['utils'])
async def status():
    return 'OK'


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(game.router)
