from datetime import datetime
from math import ceil
from sqlite3 import IntegrityError

from fastapi import Path, HTTPException, Query, Form, UploadFile, BackgroundTasks
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from slugify import slugify

from .router import router
from .settings import templates
from .database import cur, conn
from .schemas import Post




@router.get('/', response_class=HTMLResponse, name='index')
async def index(request: Request, page: int = Query(default=1, ge=1)):
    cur.execute('SELECT count(*) from POST')
    objs_count = cur.fetchone()[0]
    page_count = ceil(objs_count / 5)
    cur.execute('SELECT * FROM post ORDER BY date_created DESC LIMIT ? OFFSET ?;',(5,page*5-5 ))
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

@router.get('/contact', response_class=HTMLResponse, name='contact')
async def contact(request: Request):
    return templates.TemplateResponse('contact.html', {'request': request})

def save_file(file: UploadFile):
    with open(file.filename, 'wb') as out:
        out.write(file.file.read())



@router.post('/contact', response_class=HTMLResponse)
async def contact(
        request: Request,
        background_task: BackgroundTasks,
        file: UploadFile,
        title: str = Form(max_length=128),
        author: str = Form(max_length=32),
        message: str = Form(),


):
    background_task.add_task(save_file, file)
    slug = slugify(title)
    date_created = datetime.now()
    cur.execute('''
    INSERT INTO post(
        title,
        author,
        slug,
        date_created,
        body
    ) VALUES (?, ?, ?, ?, ?);
    ''', (title, author, slug, date_created, message))
    try:
        conn.commit()
    except IntegrityError:
        is_submit = False
        error = 'Пост с таким названием существует!'
    else:
        is_submit = True
        error = ''
    return templates.TemplateResponse('contact.html', {'request': request, 'is_submit': is_submit, 'error': error})


@router.get('/{post_slug}', response_class=HTMLResponse, name='post_detail')
async def post_detail(request: Request, post_slug: str = Path(max_length=128)):
    cur.execute('SELECT * FROM post WHERE slug = ?;', (post_slug,))
    obj = Post.from_sql(cur.fetchall())
    if obj:
        return templates.TemplateResponse('post.html', {'request': request, 'post': obj[0]})
    raise HTTPException(status_code=404, detail='page not found')


async def exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse('error.html', {'request': request, 'exc': exc})


exception_data = {
    404: exception_handler,
    500: exception_handler}