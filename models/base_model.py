#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            # from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            # storage.new(self)
        else:
            #  kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
            # '%Y-%m-%dT%H:%M:%S.%f')
            # kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
            # '%Y-%m-%dT%H:%M:%S.%f')
            if 'id' not in kwargs:
                kwargs['id'] = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                kwargs['created_at'] = datetime.now()
            if 'updated_at' not in kwargs:
                kwargs['updated_at'] = datetime.now()

            if ('updated_at' in kwargs and
                    isinstance(kwargs['updated_at'], str)):
                kwargs['updated_at'] = (datetime.strptime(kwargs['updated_at'],
                                        '%Y-%m-%dT%H:%M:%S.%f'))
            if ('created_at' in kwargs and
                    isinstance(kwargs['created_at'], str)):
                kwargs['created_at'] = (datetime.strptime(kwargs['created_at'],
                                        '%Y-%m-%dT%H:%M:%S.%f'))
            # del kwargs['__class__']
            # Safely remove '__class__'
            kwargs.pop('__class__', None)
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = self.__dict__.copy()
        return "[{}] ({}) {}".format(type(self).__name__, self.id, cls)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = str(type(self).__name__)
        dictionary.pop('_sa_instance_state', None)
        if hasattr(self, 'created_at'):
            dictionary['created_at'] = self.created_at.isoformat()
        if hasattr(self, 'updated_at'):
            dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """Deletes the current instance from storage (models.storage)"""
        from models import storage
        storage.delete(self)
