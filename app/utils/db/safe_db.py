from fastapi import HTTPException
from functools import wraps
from sqlalchemy.exc import IntegrityError
import logging
import re

logger = logging.getLogger(__name__)

error_regex = r"[()]"


def db_safe():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *arg, **kwargs):
            try:
                result = await func(self, *arg, **kwargs)
                await self.db.commit()
                return result
            except IntegrityError as e:
                await self.db.rollback()
                logger.warning(f"IntegrityError in {func.__name__}: {str(e)}")
                detail = str(e.orig)
                print("DEBUG", detail)
                message = "unique constrained voilated"
                if "Cannot insert duplicate key row" in detail:
                    match = re.search(r"The duplicate key value is \((.*?)\)", detail)
                    if match:
                        duplicate_value = match.group(1)
                        message = f"Duplicate entry for: {duplicate_value}"

                raise HTTPException(status_code=400, detail=message)

            except Exception as e:
                await self.db.rollback()
                logger.exception(f"Database operation failed in {func.__name__}")
                raise HTTPException(status_code=500, detail="Internal Server error")

        return wrapper

    return decorator
