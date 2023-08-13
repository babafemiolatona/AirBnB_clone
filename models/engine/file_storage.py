#!/usr/bin/python3
"""Define class FileStorage"""
import json
import models


class FileStorage:
    '''
        Serializes instances to JSON file and deserializes to JSON file.
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """
            Set in __objects the obj with key <obj class name>.id
        """
        k = str(obj.__class__.__name__) + "." + str(obj.id)
        dict_val = obj
        FileStorage.__objects[k] = dict_val

    def save(self):
        """Serializes __objects attribute to JSON file"""
        obj_dict = {}
        for k, v in FileStorage.__objects.items():
            obj_dict[k] = v.to_dict()

        with open(FileStorage.__file_path, mode='w', encoding="UTF8") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(FileStorage.__file_path, encoding="UTF8") as f:
                FileStorage.__objects = json.load(f)
            for k, v in FileStorage.__objects.items():
                class_name = v["__class__"]
                class_name = models.cls_list[class_name]
                FileStorage.__objects[k] = class_name(**v)
        except FileNotFoundError:
            pass
