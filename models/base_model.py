#!/usr/bin/python3
"""Defines the Base Model Class"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """Base Class"""
    def _init_(self, *args, **kwargs):
        """Initialization of the public instance attributes"""
        if kwargs:
            for k, v in kwargs.items():
                if k != '_class_':
                    setattr(self, k, v)
                if k in ('created_at', 'updated_at'):
                    setattr(self, k, datetime.fromisoformat(v))
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def _str_(self):
        """Returns string representation of the Base Model class"""
        return "[{}] ({}) {}".format(self._class.name_,
                                     self.id, self._dict_)

    def save(self):
        """Updates the updated_at attribute with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns dict represention of the instance"""
        dict_cpy = self._dict_.copy()
        dict_cpy['_class'] = self.class.name_
        dict_cpy['created_at'] = self.created_at.isoformat()
        dict_cpy['updated_at'] = self.updated_at.isoformat()
        return dict_cpy
