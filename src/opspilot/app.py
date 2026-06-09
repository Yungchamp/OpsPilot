from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from .api import routes_incidents, routes_deployments, routes_logs, routes_analytics, routes_workflows, routes_escalations
from .storage.migrations import run_migrations
from .config import settings

app = FastAPI(title='OpsPilot')

app.include_router(routes_incidents.router, prefix='')
app.include_router(routes_deployments.router, prefix='')
app.include_router(routes_logs.router, prefix='')
app.include_router(routes_analytics.router, prefix='')
app.include_router(routes_workflows.router, prefix='')
app.include_router(routes_escalations.router, prefix='')

# Static + templates
app.mount('/static', StaticFiles(directory='src/opspilot/web/static'), name='static')
templates = Jinja2Templates(directory='src/opspilot/web/templates')


@app.get('/health')
def health():
    return JSONResponse({'status': 'ok'})


@app.on_event('startup')
async def startup_event():
    run_migrations(settings.DB_PATH)

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
