from Scripts.SavingData import *
from Scripts.Saver import Saver
from Scripts.ConsoleDataManager import ConsoleDataManager as ConsoleData
saver = Saver("data.json")
console_data = ConsoleData(saver)
mode = input("select mode(a - command, b - project, c - other): ")
Commands = saver.Commands
Projects = saver.Projects

while True:
    if(mode == "a"):
        command = int(input("0 - show, 1 - add, 2 - rem, 3 - open, 4 - read, 9 - change mode: "))
        if(command == 0):
             for comm in Commands.get_items():
                  print(comm)
        elif(command == 1):
            name = input("set name: ")
            alias = input("set alias: ")
            Commands.add_item(Command(name, alias))
        elif(command == 2):
             i = int(input("select command to remove: "))
             Commands.remove_item(Commands.get_items()[i].uuid)
        elif(command == 3):
            i = int(input("select command to open: "))
            Commands.get_items()[i].open_command()
        elif(command == 4):
            i = int(input("select command to open: "))
            print(Commands.get_items()[i].get_command_text())
        elif(command == 9):
            mode = input("select mode: a - command, b - project")



    elif(mode == "b"):
        command = int(input("0 - show, 1 - add, 2 - rem, 3 - select, 9 - change mode: "))
        if(command == 0):
            for p in Projects.get_items():
                print(p)
        elif(command == 1):
            name = input("set name: ")
            sln_path = input("set path: ")
            prj_name = input("set project name: ")
            Projects.add_item(Project(name, sln_path, prj_name))
        elif(command == 2):
            i = int(input("select project to remove: "))
            Projects.remove_item(Projects.get_items()[i].uuid)
        elif(command == 3):
            i = int(input("select project to select: "))
            console_data.select_project(Projects.get_items()[i])
        elif(command == 9):
            mode = input("select mode: a - command, b - project")

    elif(mode == "c"):
        command = int(input("0 - get backups path, 1 - set backups path, 2 - reset save, 3 - save to profile, 9 - change mode: "))
        if(command == 0):
            print(saver.get_property("backups_path"))
        elif(command == 1):
            saver.set_property("backups_path", input("Enter backups path:"))
        elif(command == 2):
            saver.reset_save()
        elif(command == 3):
            saver.save_to_profile()
        elif(command == 4):
            console_data.install_environment_variables()
        elif(command == 9):
            mode = input("select mode(a - command, b - project, c - other): ")


