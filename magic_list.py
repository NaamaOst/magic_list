# Magic list by Naama Ostshega (13 May 2021)
# Implemeting a MagicList:
# A Python class that implements a simplified list by skipping boundary checks when possible.
# The MagicList support initializing assigned types when cls_type is provided to its constructor:
from dataclasses import dataclass


@dataclass
class Person:
    age: int = 1


class MagicList(list):
    def __init__(self, *args):
        # args can be empty\an input list\cls_type(=assigned data type)
        if args:
            in_string = str(args[0])
            if in_string.startswith('cls_type'):  # Got cls_type that enables the user to use a special data class
                # remove the 'cls_type=' substring in order to get only the specifies class type
                cls_type_st = in_string.replace('cls_type=', '')

                # call the parent constructor
                super(MagicList, self).__init__()
                self.cls_type_st = cls_type_st
            else:  # Got input list that will be used to create the original list data type
                super(MagicList, self).__init__(args[0])
                self.cls_type_st = 'None'
        else:  # when no args - An empty list with no specific type
            super(MagicList, self).__init__()
            self.cls_type_st = 'None'

    # Enables to override the [] assignment
    def __setitem__(self, item, value):
        req_index = item  # The index of the specific list element
        curr_len = self.__len__()  # The length of the current list

        # If req_index >= curr_len: The requested index doesn't exist and need to add it manually
        # (Else - Do nothing, works like in the original list)
        if req_index == curr_len:
            # For debug-print(f'(__setitem__: new_index:{req_index}; len:{len(self)}; cls_type_st:{self.cls_type_st})')

            # If not data class, append new item to list
            if self.cls_type_st == 'None':  # set is not called when it is list of data classes
                self.append(value)  # set value directly
        else:
            # call the original list setitem
            super().__setitem__(item, value)

    # Enables to override the assignment to data class's attribute that doesn't exist yet
    def __getitem__(self, item):
        if self.cls_type_st != 'None':  # Relevant for a list of data class objects
            req_index = item  # The index of the specific list element
            curr_len = self.__len__()  # The length of the current list
            if req_index == curr_len:
                new_data_class = eval(self.cls_type_st)
                self.append(new_data_class)

        return super().__getitem__(item)


# Validation and examples of using the MagicList:
empty_ml = MagicList()
print(f'\nCreated empty magic list: {empty_ml}')
empty_ml[0] = 3
print(f'After empty_ml[0]=3, list is: {empty_ml} ')
empty_ml[1] = 4
print(f'After empty_ml[1]=4, list is: {empty_ml} ')
# empty_ml[5] = 4   # Returns an error

# Init list with values
ml = MagicList((1,2,3))
print(f'\nCreated magic list with values:{ml}')
ml[0] = 10
print(f'After ml[0]=10, list is: {ml} ')
ml[3] = 2
print(f'After ml[3]=10, list is: {ml} ')

ml.append(100)
print(f'After ml.append(100) ml is: {ml}')

person_lst = MagicList("cls_type=Person")
print(f'\nCreated empty magic person list: {person_lst}')
person_lst[0].age = 5
print(f'After "person_lst[0].age = 5" person_lst[0].age is {person_lst[0].age}')
person_lst[1].age = 10
print(f'After "person_lst[1].age = 10" person_lst[1].age is {person_lst[1].age}')
# person_lst[3].age = 10   # Returns an error
