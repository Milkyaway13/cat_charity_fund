from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.investing import investing
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, DonationDB, DonationDBSuperUser

router = APIRouter()


@router.get(
    "/",
    response_model=list[DonationDBSuperUser],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(session: AsyncSession = Depends(get_async_session)):
    return await donation_crud.get_multi(session)


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, user)
    return await investing(new_donation, CharityProject, session)


@router.get(
    "/my",
    response_model=list[DonationDB],
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await donation_crud.get_donations_by_user(user, session)
