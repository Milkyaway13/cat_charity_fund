from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.error_message import ErrorMessage
from app.models import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """ "Проверка на уникальность название проекта"""
    room_id = await charity_project_crud.get_project_id_by_name(project_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=ErrorMessage.EXIST
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """ "Проверка на наличие проекта"""
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=ErrorMessage.NOT_FOUND
        )
    return project


async def check_invested_amount_delete(project: CharityProject) -> None:
    """Проверка на невозможность удаления
    проекта с внесенным пожертвованием"""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=ErrorMessage.INVESTED
        )


async def check_full_amount_update(project: CharityProject, new_amount: int) -> None:
    """Проверка на  возможность обновления полной суммы проекта"""
    if project.invested_amount > new_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=ErrorMessage.BELOW_DEPOSIT
        )


async def check_close_project(project: CharityProject) -> None:
    """Проверка на возможность редактирвоания закрытого проекта"""
    if project.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=ErrorMessage.CLOSED
        )
