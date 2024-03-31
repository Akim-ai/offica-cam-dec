from typing import Optional

from pydantic import BaseModel, IPvAnyAddress, NonNegativeInt


class IPostCamera(BaseModel):
    id: int = None
    name: str
    ip_endpoint: str
    is_active: bool = True
    
    


class IPutCamera(IPostCamera):
    id: NonNegativeInt
