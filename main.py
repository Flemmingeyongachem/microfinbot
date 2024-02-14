from fastapi import FastAPI, Request, Response, status
from user.views import user_router
from tortoise.contrib.fastapi import register_tortoise
from dotenv import find_dotenv,dotenv_values
from tortoise import Tortoise
from typing import Final
from telegram.ext import MessageHandler, CommandHandler, ContextTypes, Application, filters
from bot import (start_command, start,web_app_data, help_command,cashin_command,handle_message,errors)
from contextlib import asynccontextmanager
from telegram import Update
from fastapi.responses import HTMLResponse,FileResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


origins = [
    'http://127.0.0.1:3000',
    'localhost:3000',
    # 'https://f9d1-102-244-223-238.ngrok-free.app',
    
]


templates = Jinja2Templates(directory="frontend/dist/")

settings = dotenv_values(find_dotenv('.env'))
secret_key = settings.get('secret_key')
db_user = settings.get('db_user')
db_port = settings.get('db_port')
db_name = settings.get('db_name')
db_host = settings.get('db_host')
db_password = settings.get('db_password')

#bot settings
TOKEN : Final = settings.get('BOT_TOKEN')
BOT_USERNAME : Final = settings.get("BOT_USERNAME")

webhook: Final = "https://f9d1-102-244-223-238.ngrok-free.app/api/v1/webhook/"

finbot = (
    Application.builder()
    .updater(None)
    .token(TOKEN) # replace <your-bot-token>
    .read_timeout(7)
    .get_updates_read_timeout(42)
    .build()
)

@asynccontextmanager
async def lifespan(_: FastAPI):
    await finbot.bot.setWebhook(webhook)
    async with finbot:
        await finbot.start()
        yield
        await finbot.stop()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="frontend/dist/static"), name="static")

app.include_router(user_router)

@app.post("/api/v1/webhook/")
async def process_update(request: Request):
    req = await request.json()
    update = Update.de_json(req, finbot.bot)
    await finbot.process_update(update)
    return Response(status_code=status.HTTP_200_OK)



# @app.get("/", response_class=HTMLResponse)
# @app.get("/{path:path}")
# async def serve_spa(request: Request, path:str):
#     return templates.TemplateResponse("index.html", {"request": request})



# @app.get("/{catchall:path}")
# async def serve_react_app(catchall: str):
#     return FileResponse("frontend/dist/index.html")

# @app.get("/{path:path}")
# async def serve_react_app(path: str):
#     return RedirectResponse(url=f"/{path}")




#Commands
finbot.add_handler(CommandHandler("start", start))
# finbot.add_handler(CommandHandler("start", start_command))
finbot.add_handler(CommandHandler('help', help_command))
finbot.add_handler(CommandHandler('cashin', cashin_command))

#Messages
# finbot.add_handler(MessageHandler(filters.TEXT,handle_message))
finbot.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))


#errors
finbot.add_error_handler(errors)




# register_tortoise(
#     app,
#     db_url=f"asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
#     modules= {"models":["models"]},
#     generate_schemas=True,
#     add_exception_handlers=True
# )

TORTOISE_ORM = {
        "connections": {
            "default": f"asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
            },
        "apps": {
            "models": {
                "models": ["models", "aerich.models"],
                "default_connection": "default",
            },
        }
    }

async def init_db(app):
    await Tortoise.init(config=TORTOISE_ORM)
    register_tortoise(app, 
                      config=TORTOISE_ORM,
                      generate_schemas=True,
                      add_exception_handlers=True
                      )
    # await Tortoise.generate_schemas()
    
    
@app.on_event("startup")
async def startup_event():
    await init_db(app)
    
@app.on_event('shutdown')
async def close_db_connection():
    await Tortoise.close_connections()
    



# aerich init -t path.to.tortoise_config.TORTOISE_ORM
# aerich init-db
# aerich migrate # Generate and apply new migrations based on model changes
# aerich upgrade # Apply pending migrations
# aerich downgrade # Rollback the most recent migration
# aerich history # View the migration history