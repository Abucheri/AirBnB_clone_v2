#!/usr/bin/python3

"""This module defines a database storage engine using SQLAlchemy"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """
    This class manages storage of hbnb models in a database using SQLAlchemy
    """
    __engine = None
    __session = None

    def __init__(self):
        """Creates a new instance of DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        if cls is None:
            obj_data = self.__session.query(State).all()
            obj_data.extend(self.__session.query(City).all())
            obj_data.extend(self.__session.query(User).all())
            obj_data.extend(self.__session.query(Place).all())
            obj_data.extend(self.__session.query(Review).all())
            obj_data.extend(self.__session.query(Amenity).all())
        else:
            if isinstance(str, cls):
                cls = eval(cls)
            obj_data = self.__session.query(cls)
        return ({"{}.{}".format(type(obj).__name__, obj.id): obj for obj
                in obj_data})

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        SessionM = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(SessionM)
        self.__session = Session()

    def close(self):
        """Call close() method on the private session
        attribute (self.__session)
        """
        self.__session.close()
