#!/usr/bin/python3
"""Defines the AirBnB_clone console."""
import cmd
from shlex import split
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Defines the AirBnB_clone command interpreter."""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review"
    }

    def emptyline(self):
        """Ignores empty spaces."""
        pass

    def do_quit(self, line):
        """Exits the interpreter."""
        return True

    def do_EOF(self, line):
        """Exits the interpreter."""
        print("")
        return True

    def do_create(self, line):
        """Creates a new class instance with given keys/values
        and print its id.
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")

            kwargs = {}
            for i in range(1, len(my_list)):
                key, value = tuple(my_list[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                obj = eval(my_list[0])()
            else:
                obj = eval(my_list[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Prints a string representation of an instance
        Exceptions:
            SyntaxError: no args given
            NameError: no object that has the name
            IndexError: no id given
            KeyError: no valid id given
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")
            if my_list[0] not in self.__classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key in objects:
                print(objects[key])
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, line):
        """Deletes instances based on class name and id
        Exceptions:
            SyntaxError: no args given
            NameError: no object with the name given
            IndexError: no id given
            KeyError: no valid id given
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")
            if my_list[0] not in self.__classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key in objects:
                del objects[key]
                storage.save()
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_all(self, line):
        """Displays string representations of all instances of a
        given class. If no class, it displays all instantiated objects.
        """
        if not line:
            objs = storage.all()
            print([objs[key].__str__() for key in objs])
            return
        try:
            args = line.split(" ")
            if args[0] not in self.__classes:
                raise NameError()

            objs = storage.all(eval(args[0]))
            print([objs[key].__str__() for key in objs])

        except NameError:
            print("** class doesn't exist **")

    def do_update(self, line):
        """Updates instances by adding or updating attributes
        Exceptions:
            SyntaxError: no args given
            NameError: no object with the name given
            IndexError: no id given
            KeyError: no valid id given
            AttributeError: no attribute given
            ValueError: no value given
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = split(line, " ")
            if my_list[0] not in self.__classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key not in objects:
                raise KeyError()
            if len(my_list) < 3:
                raise AttributeError()
            if len(my_list) < 4:
                raise ValueError()
            value = objects[key]
            try:
                value.__dict__[my_list[2]] = eval(my_list[3])
            except Exception:
                value.__dict__[my_list[2]] = my_list[3]
                value.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except AttributeError:
            print("** attribute name missing **")
        except ValueError:
            print("** value missing **")

    def count(self, line):
        """count the no. of instances
        """
        count = 0
        try:
            my_list = split(line, " ")
            if my_list[0] not in self.__classes:
                raise NameError()
            objs = storage.all()
            for key in objs:
                name = key.split('.')
                if name[0] == my_list[0]:
                    count += 1
            print(counter)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        """strips args and returns a string command back
        Args:
            args: list of args
        Return:
            returns string of args
        """
        args_list = []
        args_list.append(args[0])
        try:
            my_dict = eval(
                args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            args_str = args[1][args[1].find('(')+1:args[1].find(')')]
            args_list.append(((args_str.split(", "))[0]).strip('"'))
            args_list.append(my_dict)
            return args_list
        args_str = args[1][args[1].find('(')+1:args[1].find(')')]
        args_list.append(" ".join(args_str.split(", ")))
        return " ".join(argsL for argsL in args_list)

    def default(self, line):
        """retrieves instances of a class and
        no. of instances
        """
        my_list = line.split('.')
        if len(my_list) >= 2:
            if my_list[1] == "all()":
                self.do_all(my_list[0])
            elif my_list[1] == "count()":
                self.count(my_list[0])
            elif my_list[1][:4] == "show":
                self.do_show(self.strip_clean(my_list))
            elif my_list[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(my_list))
            elif my_list[1][:6] == "update":
                args = self.strip_clean(my_list)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, value in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, value))
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
