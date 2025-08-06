from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.atleta.models import AtletaModel
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.treinos.models import TreinoModel
from workout_api.treinos.schemas import TreinoIn, TreinoOut, TreinoUpdate


router = APIRouter()

@router.post(
    '/',
    summary="criar um novo treino",
    status_code=status.HTTP_201_CREATED,
    response_model=TreinoOut
)
async def post(
    db_session: DatabaseDependency,
    treino_in: TreinoIn = Body(...)
) -> TreinoOut:
    # verifica se o atleta existe
    atleta = (await db_session.execute(
        select(AtletaModel).filter_by(pk_id=treino_in.atleta_id))
    ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta com ID {treino_in.atleta_id} não encontado."
        )
    
    try:
        # cria o objeto TreinoOut com ID único e timestamp de criação
        treino_out = TreinoOut(
            id=uuid4(),
            created_at=datetime.now(timezone.utc),
            realizado=False,
            **treino_in.model_dump()
        )

        # cria o modelo para persistir no banco
        treino_model = TreinoModel(**treino_out.model_dump())

        # adiciona o treino ao banco de dados
        db_session.add(treino_model)
        # confirma
        await db_session.commit()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao inserir os dados no banco: {str(e)}"
        )
    
    return treino_out

@router.get(
    "/",
    summary="Consultar todos os treinos",
    status_code=status.HTTP_200_OK,
    response_model=list[TreinoOut],
)
async def query(db_session: DatabaseDependency) -> list[TreinoOut]:
    # busca todos os treinos no banco de dados
    treinos = (await db_session.execute(select(TreinoModel))).scalars().all()

    # converte os modelos para schemas de saída
    return [TreinoOut.model_validate(treino) for treino in treinos]

@router.get(
    '/atleta/{atleta_id}',
    summary='Consultar treinos de um alteta específico',
    status_code=status.HTTP_200_OK,
    response_model=list[TreinoOut],
)
async def query_by_atleta(atleta_id: int, db_session: DatabaseDependency) -> list[TreinoOut]:
    # verifica se o atleta existe
    atleta = (await db_session.execute(
        select(AtletaModel).filter_by(pk_id=atleta_id)
    )).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta com id {atleta_id} não encontrado.'
        )
    
    treinos = (await db_session.execute(
        select(TreinoModel).filter_by(atleta_id=atleta_id)
    )).scalars().all()

    return [TreinoOut.model_validate(treino) for treino in treinos]


@router.get(
    '/{id}', 
    summary='Consultar um treino específico pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=TreinoOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> TreinoOut:
    
    treino = (await db_session.execute(
        select(TreinoModel).filter_by(id=id))
    ).scalars().first()

    if not treino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Treino não encontrado no id: {id}'
        )
    
    return TreinoOut.model_validate(treino)

@router.patch(
    '/{id}', 
    summary='Editar um treino pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=TreinoOut,
)
async def patch(id: UUID4, db_session: DatabaseDependency, treino_up: TreinoUpdate = Body(...)) -> TreinoOut:
    treino = (await db_session.execute(
        select(TreinoModel).filter_by(id=id))
    ).scalars().first()

    if not treino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Treino não encontrado no id: {id}'
        )
    
    treino_update = treino_up.model_dump(exclude_unset=True)
    
    for key, value in treino_update.items():
        setattr(treino, key, value)

    await db_session.commit()
    await db_session.refresh(treino)

    return TreinoOut.model_validate(treino)

@router.patch(
    '/{id}/realizar', 
    summary='Marcar treino como realizado',
    status_code=status.HTTP_200_OK,
    response_model=TreinoOut,
)
async def marcar_realizado(id: UUID4, db_session: DatabaseDependency) -> TreinoOut:
    treino = (await db_session.execute(
        select(TreinoModel).filter_by(id=id))
    ).scalars().first()

    if not treino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Treino não encontrado no id: {id}'
        )
    
    treino.realizado = True
    
    await db_session.commit()
    
    await db_session.refresh(treino)

    return TreinoOut.model_validate(treino)

@router.delete(
    '/{id}', 
    summary='Deletar um treino pelo ID',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    treino = (await db_session.execute(
        select(TreinoModel).filter_by(id=id))
    ).scalars().first()

    if not treino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Treino não encontrado no id: {id}'
        )
    
    await db_session.delete(treino)
    await db_session.commit() 