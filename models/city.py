#!/usr/bin/python3
"""Defines a City Class"""
from models.base_model import BaseModel


class City(BaseModel):
    """Defines a City class that inherits from BaseModel"""
    state_id = ""
    name = ""
