#!/usr/bin/python3
"""Defines the Base Model Class"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """Base Class"""
    def __init__(self, *args, **kwargs):
        """Initialization of the public instance attributes"""
        if kwargs:
            for k, v in kwargs.items():
                if k != '__class__':
                    setattr(self, k, v)
                if k in ('created_at', 'updated_at'):
                    setattr(self, k, datetime.fromisoformat(v))
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """Returns string representation of the Base Model class"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Updates the updated_at attribute with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns dict represention of the instance"""
        dict_cpy = self.__dict__.copy()
        dict_cpy['__class__'] = self.__class__.__name__
        dict_cpy['created_at'] = self.created_at.isoformat()
        dict_cpy['updated_at'] = self.updated_at.isoformat()
        return dict_cpy
