from sqlalchemy import Column, String, Text

from app.core.db import Base
from .base_model import InvestModelBase
from app.core.constants import NAME_MAX_LENGHT


class CharityProject(Base, InvestModelBase):
    name = Column(String(NAME_MAX_LENGHT), unique=True, nullable=False)
    description = Column(Text, nullable=False)