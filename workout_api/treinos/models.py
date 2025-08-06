from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from workout_api.contrib.models import BaseModel
from workout_api.atleta.models import AtletaModel


class TreinoModel(BaseModel):
    __tablename__ = 'treinos'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=True)
    data_treino: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duracao_minutos: Mapped[int] = mapped_column(Integer, nullable=False)
    realizado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    observacoes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    atleta: Mapped['AtletaModel'] = relationship(back_populates="treinos", lazy='selectin')
    atleta_id: Mapped[int] = mapped_column(ForeignKey("atletas.pk_id")) 