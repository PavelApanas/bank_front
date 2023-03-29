from math import ceil
from fastapi import Path, HTTPException, Query
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from .router import router
from .settings import templates
from .database import cur
from .schemas import Post


@router.get('/', response_class=HTMLResponse, name='index')
async def index(request: Request, page: int = Query(default=1, ge=1)):
    cur.execute('SELECT count(*) from POST')
    objs_count = cur.fetchone()[0]
    page_count = ceil(objs_count / 5)
    cur.execute('SELECT * FROM post LIMIT ? OFFSET ?;',(5,page*5-5 ))
    objs = Post.from_sql(cur.fetchall())
    return templates.TemplateResponse('index.html', {
        'request': request,
        'posts': objs,
        'current_page': page,
        'page_count': page_count
    })


@router.get('/about', response_class=HTMLResponse, name='about')
async def about(request: Request):
    return templates.TemplateResponse('about.html', {'request': request})


@router.get('/{post_slug}', response_class=HTMLResponse, name='post_detail')
async def post_detail(request: Request, post_slug: str = Path(max_length=128)):
    cur.execute('SELECT * FROM post WHERE slug = ?;', (post_slug,))
    obj = Post.from_sql(cur.fetchall())
    if obj:
        return templates.TemplateResponse('post.html', {'request': request, 'post': obj[0]})
    raise HTTPException(status_code=404, detail='page not found')
