from typing import Literal
from pydantic import BaseModel, Field, field_validator

class InvestigacionRequest(BaseModel):
    pregunta: str = Field(min_length=8, max_length=2000)
    modo: Literal["rapido", "comparativo", "profundo"] = "rapido"
    usar_web: bool = True

    @field_validator("pregunta", mode="before")
    @classmethod
    def limpiar(cls, value):
        return value.strip() if isinstance(value, str) else value

class Fuente(BaseModel):
    titulo: str
    url: str

class Cita(Fuente):
    inicio: int
    fin: int

class Bloque(BaseModel):
    texto: str
    citas: list[Cita] = Field(default_factory=list)

class InvestigacionResponse(BaseModel):
    pregunta: str
    modo: str
    modelo: str
    fecha: str
    web_solicitada: bool
    web_utilizada: bool
    bloques: list[Bloque]
    fuentes: list[Fuente]
    avisos: list[str]

