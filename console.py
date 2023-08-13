#!/usr/bin/env python3
"""Console module for the HBNB project"""
import cmd
import shlex
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the HBNB project"""

    prompt = "(hbnb) "
    clslist = {'BaseModel': BaseModel, 'State': State, 'City': City,
               'Amenity': Amenity, 'Place': Place, 'Review': Review,
               'User': User}

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program using EOF (Ctrl+D)"""
        print()
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id
        """
        if arg == '':
            print("** class name missing **")
        elif arg not in HBNBCommand.clslist:
            print("** class doesn't exist **")
        else:
            obj_dict = eval(arg)()
            obj_dict.save()
            print(obj_dict.id)

    def do_show(self, args):
        """
            Print the string representation of an instance
            based on the class name and id
        """
        args_list = args.split()
        if len(args_list) == 0:
            print("** class name missing **")
            return
        if len(args_list) == 1:
            print("** instance id missing **")
            return

        storage = FileStorage()
        storage.reload()
        instance_dict = storage.all()

        cls_name = args_list[0]
        obj_id = args_list[1]

        try:
            cls = globals()[cls_name]
        except KeyError:
            print("** class doesn't exist **")
            return

        k = "{}.{}".format(cls_name, obj_id)

        if k in instance_dict:
            instance = instance_dict[k]
            print(instance)
        else:
            print("** no instance found **")

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id"""
        args_list = args.split()
        if len(args_list) == 0:
            print("** class name missing **")
            return
        elif len(args_list) == 1:
            print("** instance id missing **")
            return
        cls_name = args_list[0]
        cls_id = args_list[1]
        storage = FileStorage()
        storage.reload()
        instance_dict = storage.all()
        try:
            eval(cls_name)
        except NameError:
            print("** class doesn't exist **")
            return

        k = "{}.{}".format(cls_name, cls_id)
        try:
            del instance_dict[k]
            storage.save()
        except KeyError:
            print("** no instance found **")

    def do_all(self, args):
        """
            Prints all string representation of all instances based
            or not on the class name
        """
        obj_list = []
        storage = FileStorage()
        storage.reload()
        obj = storage.all()
        args_list = args.split()

        if len(args_list) > 0:
            try:
                cls_to_filter = eval(args_list[0])
            except NameError:
                print("** class doesn't exist **")
        else:
            cls_to_filter = None

        for key, val in obj.items():
            if cls_to_filter is None or isinstance(val, cls_to_filter):
                obj_list.append(str(val))

        print(obj_list)

    def do_update(self, args):
        """
            Update an instance based on the class name and id
            sent as args
        """
        storage = FileStorage()
        storage.reload()
        args_list = shlex.split(args)
        if len(args_list) == 0:
            print("** class name missing **")
            return
        elif len(args_list) == 1:
            print("** instance id missing **")
            return
        elif len(args_list) == 2:
            print("** attribute name missing **")
            return
        elif len(args_list) == 3:
            print("** value missing **")
            return
        try:
            eval(args_list[0])
        except NameError:
            print("** class doesn't exist **")
            return
        key = args_list[0] + "." + args_list[1]
        instance_dict = storage.all()
        try:
            obj_val = instance_dict[key]
        except KeyError:
            print("** no instance found **")
            return
        try:
            attr_type = type(getattr(obj_val, args[2]))
            args[3] = attr_type(args[3])
        except AttributeError:
            pass
        setattr(obj_val, args_list[2], args_list[3])
        obj_val.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
