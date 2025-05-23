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
                message = "unique constrained voilated"
                if "duplicate key value violates unique constraint" in detail:
                    if "Key" in detail and "=" in detail:
                        key_info = (
                            detail.split("Key ")[1].strip()
                            # .strip("() .")
                        )
                        message = f"Unique constraint violated: {re.sub(error_regex,'',key_info)}"

                raise HTTPException(status_code=400, detail=message)

            except Exception as e:
                await self.db.rollback()
                logger.exception(f"Database operation failed in {func.__name__}")
                raise HTTPException(status_code=500, detail="Internal Server error")

        return wrapper

    return decorator
