from fastapi import FastAPI

from views.settings import static
from views.views import router
from views.database import insert_posts


app = FastAPI()
app.mount('/static', static, 'static')
app.include_router(router=router)
# insert_posts()
