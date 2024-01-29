#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        # return FileStorage.__objects
        if cls is not None:
            if isinstance(cls, str):
                cls = eval(cls)
            cls_dict = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    cls_dict[key] = value
            return cls_dict
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Saves storage dictionary to file"""
        temp = ({obj: self.__objects[obj].to_dict()
                for obj in self.__objects.keys()})
        with open(self.__file_path, "w", encoding="utf-8") as fle:
            json.dump(temp, fle)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as fle:
                for obj in json.load(fle).values():
                    name = obj["__class__"]
                    del obj["__class__"]
                    self.new(eval(name)(**obj))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from storage"""
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def close(self):
        """Calls reload() method for deserializing the JSON file to objects"""
        self.reload()
