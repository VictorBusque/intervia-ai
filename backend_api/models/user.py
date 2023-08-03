from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    id: str
    email: Optional[str] = None
