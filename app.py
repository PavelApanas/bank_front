from fastapi import FastAPI

from views.settings import static
from views.views import router, exception_data



app = FastAPI(exception_handlers=exception_data)
app.mount('/static', static, 'static')
app.include_router(router=router)
# insert_posts()
