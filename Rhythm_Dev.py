from Scripts.Utilities.SavingData import *
from config import Config
from Scripts.Utilities.Repositories import ObjectRepository, FileRepository
from Scripts.Utilities.Savers import project_saver, command_saver, launcher_saver
from Scripts.Blocks.ConsoleDataManager import *

#prj = Project("RoDv", r"Get/Out/From/Here", "no.need.you.to.know")
#project_saver.reps[Project].add_item(prj)

#cmd = Command("Open-Selected-App", "go-app")
#command_saver.reps[Command].add_item(cmd)
#command_saver.reps[Command].open_file(cmd)

#lch = Launcher("vs-c")
#launcher_saver.reps[Launcher].add_item(lch)
#for i in launcher_saver.reps[Launcher].get_items():
#    print(i)
#set_environment_variable("rodv_variables_path", str(get_variables_dir()))
save_to_profile()
select_project(project_saver.reps[Project].get_items()[0])