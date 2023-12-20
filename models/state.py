#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship('City', cascade='all, delete', backref='state')
    else:
        from models import storage

        @property
        def cities(self):
            """
            Getter attribute that returns the list of City instances with
            state_id equal to the current State.id
            """
            Clist = []
            for city in list(storage.all(City).values()):
                if city.state_id == self.id:
                    Clist.append(city)
            return Clist
