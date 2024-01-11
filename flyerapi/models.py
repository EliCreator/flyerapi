from typing import Optional

from pydantic import BaseModel, Field


class CheckResponse(BaseModel):

    info: Optional[str] = Field(default=None)
    warning: Optional[str] = Field(default=None)
    error: Optional[str] = Field(default=None)
    skip: bool = Field(default=False)
