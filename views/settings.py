from pathlib import Path
from os.path import join
from fastapi.templating import  Jinja2Templates
from fastapi.staticfiles import  StaticFiles

def query(v, **query_paprams):

    from urllib.parse import urlencode
    return f'{v}?{urlencode(query_paprams)}'

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=join(BASE_DIR,'templates'))
templates.env.filters['query'] = query
static =StaticFiles(directory=join(BASE_DIR,'static'))

