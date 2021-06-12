# ONLY WORKS ON WINDOWS


# OS
import os
import shutil
import time


# maya
import maya.cmds as mc
import maya.OpenMaya as om


def path_name():
    # current file path
    filepath = mc.file(q=True,sn=True)
    
    # current file name
    filename = os.path.basename(filepath)
    
    raw,ext = os.path.splitext(filename)
    
    # directory name
    directory = filepath.replace(filename," ")
    dir = directory.split('/')
    del dir[-1:]
    current_directory = "\\".join(dir)


    output = {"filepath":filepath,"filename":filename,"raw":raw,"ext":ext,"current_directory":current_directory}
    return(output)


# Open current working directory for the file
def openPWD():
    path_details = path_name()
    toOpen = "explorer.exe {0}".format(path_details['current_directory'])
    os.system(toOpen)
    


# Create backup file
def create_backup():
    path_details = path_name()
    ls = os.listdir(path_details['current_directory'])
    
    #check and create backup folder
    if not "ma_backup" in ls:
        # Create directory
        ma_backup = os.path.join(path_details['current_directory'],"ma_backup")
        os.mkdir(ma_backup)
        time.sleep(3)


    # check if: backup directory exists
    # if "ma_backup" in ls:
    #curret file path
    current_file_path = os.path.join(path_details['current_directory'],path_details['filename'])
    #new file path
    new_file_name = path_details['raw'] + "_backup" + path_details['ext']
    new_file_path = os.path.join(path_details['current_directory'],"ma_backup",new_file_name)
    # copy the backup file
    om.MGlobal.displayInfo("Backup {0} created sucessuffly".format(new_file_name))
    shutil.copyfile(current_file_path,new_file_path)



# Create up-version file
def up_version():
    path_details = path_name()
    # save the current file
    mc.file(save=True)


    # # Split the file name
    name_split = path_details['raw'].split('_')
    version_string = name_split[-1]
    version_str_to_list = list(version_string)
    version_int = "".join(version_str_to_list[1:])
    up_version = int(version_int) + 1
    version_to_string = str(up_version)
    if len(version_to_string) == 1:
        version = "v00" + version_to_string
    elif len(version_to_string) == 2:
        version = "v0" + version_to_string
    elif len(version_to_string) == 3:
        version = "v" + version_to_string
    else:
        pass


    # replace the version number in the list
    name_split[len(name_split) -1] = version


    new_file_name = "_".join(name_split) + path_details['ext']


    # # Copy new up version
    old_file_path = os.path.join(path_details['current_directory'],path_details['filename'])
    new_file_path = os.path.join(path_details['current_directory'],new_file_name)


    if os.path.isfile(new_file_path):
        mc.error("The file {0} already exists.".format(new_file_name))


    else:
        shutil.copyfile(old_file_path,new_file_path)
        om.MGlobal.displayInfo("Up version {0} created sucessuffly".format(new_file_name))


    # open the up version file
    mc.file(new_file_path,o=True)
    