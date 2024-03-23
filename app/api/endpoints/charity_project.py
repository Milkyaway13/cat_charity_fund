from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_close_project,
    check_full_amount_update,
    check_invested_amount_delete,
    check_name_duplicate,
    check_project_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.investing import investing
from app.models import Donation
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)

router = APIRouter()


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    return await investing(new_project, Donation, session)


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    await check_invested_amount_delete(project)
    await check_close_project(project)
    return await charity_project_crud.remove(project, session)


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    await check_close_project(project)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_full_amount_update(project, obj_in.full_amount)
    return await charity_project_crud.update(project, obj_in, session)
