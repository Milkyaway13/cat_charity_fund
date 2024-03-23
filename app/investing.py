from datetime import datetime
from typing import Type, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investing(
    obj: Union[Donation, CharityProject],
    model: Type[Union[Donation, CharityProject]],
    session: AsyncSession,
) -> Union[Donation, CharityProject]:
    available_items = await get_available_items(model, session)
    if available_items is None:
        return obj

    for item in available_items:
        obj_remains = obj.get_remains()
        item_remains = item.get_remains()

        if item_remains >= obj_remains:
            donation_amount = min(obj_remains, item_remains)
            item.invested_amount += donation_amount
            obj.invested_amount += donation_amount

            if item.full_amount == item.invested_amount:
                close_object(item)

            session.add(item)
            break

        donation_amount = item_remains
        item.invested_amount += donation_amount
        obj.invested_amount += donation_amount
        close_object(item)
        session.add(item)

    if obj.full_amount == obj.invested_amount:
        close_object(obj)

    session.add(obj)
    await session.commit()
    await session.refresh(obj)

    return obj


async def get_available_items(
    model: Type[Union[Donation, CharityProject]], session: AsyncSession
) -> list[Union[Donation, CharityProject]]:
    available_items = await session.execute(
        select(model).where(model.fully_invested.is_(False)).order_by(model.create_date)
    )
    return available_items.scalars().all()


def close_object(obj: Union[Donation, CharityProject]) -> None:
    obj.fully_invested = True
    obj.close_date = datetime.now()
