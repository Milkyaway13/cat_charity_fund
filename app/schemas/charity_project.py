from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, NonNegativeInt, PositiveInt, validator

from app.core.constants import NAME_MAX_LENGHT, NAME_MIN_LENHGT
from app.error_message import ErrorMessage


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None, max_length=NAME_MAX_LENGHT, min_length=NAME_MIN_LENHGT
    )
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectBase):
    pass

    @validator("name")
    def name_cant_be_empty(cls, value: str):
        if value is None or value == "":
            raise ValueError(ErrorMessage.NO_NAME)
        return value

    @validator("description")
    def description_cant_be_empty(cls, value: str):
        if value is None or value == "":
            raise ValueError(ErrorMessage.NO_DESCRIPTION)
        return value


class CharityProjectCreate(CharityProjectUpdate):
    name: str = Field(..., max_length=NAME_MAX_LENGHT, min_length=NAME_MIN_LENHGT)
    description: str
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
