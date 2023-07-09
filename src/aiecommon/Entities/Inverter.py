from pydantic import BaseModel


class Inverter(BaseModel):
    lifetime: int
