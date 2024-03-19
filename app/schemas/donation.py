from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, NonNegativeInt, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    comment: Optional[str]


class DonationDB(DonationBase):
    id: int
    create_date: datetime
    comment: Optional[str]

    class Config:
        orm_mode = True


class DonationDBSuperUser(DonationDB):
    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: bool

    class Config:
        orm_mode = True
