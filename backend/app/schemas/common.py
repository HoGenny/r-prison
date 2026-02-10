from pydantic import BaseModel


class HealthResponse(BaseModel):
    ok: bool


class MessageResponse(BaseModel):
    message: str
