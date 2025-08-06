from typing import Annotated, Optional
from datetime import datetime
from pydantic import Field, PositiveInt

from workout_api.contrib.schemas import BaseSchema, OutMixin

class Treino(BaseSchema): 
    nome: Annotated[str, Field(description="Nome do treino", examples=['Treino A - Pernas'], max_length=100)]
    descricao: Annotated[Optional[str], Field(None, description="Descrição do treino", examples=['Foco em força'])]
    data_treino: Annotated[datetime, Field(description="Data do treino", examples=['2024-01-15T14:00:00'])]
    duracao_minutos: Annotated[PositiveInt, Field(description="Duração do treino em minutos", examples=[60])]
    observacoes: Annotated[Optional[str], Field(None, description="Observações adicionais", examples=['Observações adicionais'])]


class TreinoIn(Treino):
    atleta_id: Annotated[int, Field(description="id do atleta")]

class TreinoOut(Treino, OutMixin):
    realizado: Annotated[bool, Field(description="se o treino foi realizado")]
    atleta_id: Annotated[int, Field(description="id do atleta")]

class TreinoUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do treino', max_length=100)]
    descricao: Annotated[Optional[str], Field(None, description='Descrição do treino')]
    data_treino: Annotated[Optional[datetime], Field(None, description='Data e hora do treino')]
    duracao_minutos: Annotated[Optional[PositiveInt], Field(None, description='Duração do treino em minutos')]
    realizado: Annotated[Optional[bool], Field(None, description='Se o treino foi realizado')]
    observacoes: Annotated[Optional[str], Field(None, description='Observações adicionais')] 