
import os
import secrets
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

import aiecommon.custom_logger as custom_logger
logger = custom_logger.get_logger()

security = HTTPBasic(auto_error=True)

AIENERGY_HTTP_USERNAME=os.environ["AIENERGY_HTTP_USERNAME"]
AIENERGY_HTTP_PASSWORD=os.environ["AIENERGY_HTTP_PASSWORD"]

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    logger.info(f"Checking authentication with username: {credentials.username}")
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = bytes(
        AIENERGY_HTTP_USERNAME, encoding="utf-8"
    )
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = bytes(
        AIENERGY_HTTP_PASSWORD, encoding="utf-8"
    )
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        logger.info(f"Authentication failed with username: {credentials.username}")

        raise HTTPException(
            status_code=401,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        logger.info(f"Authenticated with username: {credentials.username}")

    return credentials.username




default_router = APIRouter()

@default_router.get("/", response_class=HTMLResponse, include_in_schema=False, dependencies=[Depends(get_current_username)])
async def read_root(request: Request) -> HTMLResponse:
    # # Load the landing page HTML
    # landing_page = Path("./html/landing_page.html").read_text()
    # return HTMLResponse(content=landing_page)
    endpoints = []
    for r in request.app.routes:
        # Starlette routes have .path and .methods; filter out the docs + non-API routes
        if getattr(r, "include_in_schema", False):
            methods = sorted(m for m in getattr(r, "methods", []) if m in {"GET","POST","PUT","PATCH","DELETE"})
            if methods:
                endpoints.append({
                    "path": r.path,
                    "methods": methods,
                    "name": getattr(r, "name", r.path),
                })
    endpoints.sort(key=lambda x: x["path"])
    return request.app.state.templates.TemplateResponse(
        "index.html",
        {"request": request, "title": request.app.title, "endpoints": endpoints}
    )


@default_router.get("/openapi.json", response_class=JSONResponse, include_in_schema=False, dependencies=[Depends(get_current_username)])
async def get_openapi_json(request: Request) -> JSONResponse:

    from fastapi.openapi.utils import get_openapi

    # from app import get_app
    openapi_schema = get_openapi(
        title=request.app.title,
        version=request.app.version,
        description=request.app.description,
        routes=request.app.routes,
    )
    return JSONResponse(openapi_schema)


@default_router.get("/docs", response_class=HTMLResponse, include_in_schema=False, dependencies=[Depends(get_current_username)])
async def get_docs(request: Request) -> HTMLResponse:

    return get_swagger_ui_html(openapi_url="/openapi.json", title=f"{request.app.title} Swagger Docs")

@default_router.get("/redoc", response_class=HTMLResponse, include_in_schema=False, dependencies=[Depends(get_current_username)])
async def get_docs(request: Request) -> HTMLResponse:
    # return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

    return get_redoc_html(openapi_url="/openapi.json", title=f"{request.app.title} Redoc")

@default_router.get("/healthcheck", response_class=JSONResponse)
async def healthcheck(request: Request) -> JSONResponse:
    return {
        "success": True, 
        "service": request.app.state.service_name,
        "hostName": request.app.state.hostname,
    }

