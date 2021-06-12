
from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance


import maya.OpenMayaUI as omui
import maya.OpenMaya as om

import maya.cmds as mc
import maya.mel as mm




def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    

class Commands():
    
    @staticmethod
    def Exec(type, cmd):
        if cmd == "help":
            cmd = "h"
        if type == "python":
            print(f"python '{cmd}'")
        else:
            try:
                mm.eval(cmd)
                om.MGlobal.displayInfo('Executed')

            except (RuntimeError, TypeError, NameError) as err:
                
                om.MGlobal.displayError(f'"{cmd}" is not a valid command.')
                

class CMD_exec(QtWidgets.QLineEdit):
    
    Data = ['help']
    Index = -1
    Type = 'mel'

    def __init__(self, parent=None):
        super(CMD_exec, self).__init__(parent)
        
        # set styling
        self.setStyleSheet(
                            "color:#DBDBDB;"
                            "background-color:#404040;"
                            "height:35;"
                            "font:19px;"
                            "border-radius:1px;"
                            "border: 1px solid #6B6550;"
                                                    )
        
        print(f"Command Line Type: {CMD_exec.Type}")

    def keyPressEvent(self, key_event):
        key = key_event.key()
        if key == QtCore.Qt.Key_Enter or key == QtCore.Qt.Key_Return:
            # get data from line edit
            text = self.text()
            self.clear()
            if text == "python":
                CMD_exec.Type = "python"
                
            elif text == 'mel':
                CMD_exec.Type = "mel"
                
            else:
                
                # execute the command
                Commands.Exec(CMD_exec.Type, text)
                

                # append the data to Data list
                if not text == CMD_exec.Data[-1]:
                    if len(text) > 0:
                        CMD_exec.Data.append(text)
                    # set the Index to 0
                CMD_exec.Index = -1

                print(text)

            

        
        ctrl = key_event.modifiers() == QtCore .Qt.ControlModifier
        if ctrl:
            if key == QtCore.Qt.Key_J:
                if abs(CMD_exec.Index) <= len(CMD_exec.Data): 

                    data = CMD_exec.Data[CMD_exec.Index]
                    self.setText(data)
                  
                    CMD_exec.Index = CMD_exec.Index - 1
                
                if abs(CMD_exec.Index) > len(CMD_exec.Data): 
                    CMD_exec.Index = -1
                
                
            if key == QtCore.Qt.Key_K:
                print('Moving Up')
        
        super(CMD_exec, self).keyPressEvent(key_event)
    


   

class GreyExec(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(GreyExec, self).__init__(parent)

        self.setWindowTitle("Grey Exec")

        self.setMinimumWidth(500)
        self.setMinimumHeight(50)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
        self.setStyleSheet("background-color:#292929;")

    def create_widgets(self):
        data = ['hey', 'nothing']
        # completer = QtWidgets.QCompleter[data]
        self.lineedit = CMD_exec(self)


    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        # main_layout.setContentsMargins(4,4,4,4)
        
        # CMD exec layout
        cmd_exe_layout = QtWidgets.QHBoxLayout()
        cmd_exe_layout.addWidget(self.lineedit)
        
        # add the main layout
        main_layout.addLayout(cmd_exe_layout)


    def create_connections(self):
        #self.lineedit.enter_pressed.connect(self.on_enter_pressed)
        pass

        

    def on_enter_pressed(self, text):
        print(text)


if __name__ == "__main__":

    try:
        dialog.close() # pylint: disable=E0601
        dialog.deleteLater()
    except:
        pass

    dialog = GreyExec()
    # dialog.removeEventFilter(dialog.lineedit)
    dialog.show()

