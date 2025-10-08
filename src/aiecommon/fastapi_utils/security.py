import os
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

import aiecommon.custom_logger as custom_logger
logger = custom_logger.get_logger()


AIENERGY_HTTP_USERNAME = os.environ["AIENERGY_HTTP_USERNAME"]
AIENERGY_HTTP_PASSWORD = os.environ["AIENERGY_HTTP_PASSWORD"]

security = HTTPBasic(auto_error=True)

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

