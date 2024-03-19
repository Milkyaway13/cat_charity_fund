from typing import Union, Type
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investing(
        obj: Union[Donation, CharityProject],
        model: Type[Union[Donation, CharityProject]],
        session: AsyncSession
):
    available_items = await get_available_items(model, session)
    if available_items is None:
        return obj
    for item in available_items:
        obj_remains = obj.get_remains()
        item_remains = item.get_remains()
        if item_remains >= obj_remains:
            crediting_funds(obj, item, obj_remains)
            if item.full_amount == item.invested_amount:
                close_object(item)
            session.add(item)
            break
        else:
            crediting_funds(obj, item, item_remains)
            close_object(item)
            session.add(item)
    if obj.full_amount == obj.invested_amount:
        close_object(obj)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


async def get_available_items(
        model: Type[Union[Donation, CharityProject]],
        session: AsyncSession
) -> list[Union[Donation, CharityProject]]:
    available_items = await session.execute(
        select(model).where(
            model.fully_invested.is_(False)
        ).order_by(
            model.create_date
        )
    )
    return available_items.scalars().all()


def crediting_funds(
        obj: Union[Donation, CharityProject],
        item: Union[CharityProject, Donation],
        donation: int
) -> None:
    item.invested_amount += donation
    obj.invested_amount += donation


def close_object(obj: Union[Donation, CharityProject]) -> None:
    obj.fully_invested = True
    obj.close_date = datetime.now()