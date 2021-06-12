from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.cmds as mc



def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)



class OutputResolution(QtWidgets.QDialog):
    
    RESOLUTION_ITEMS = [
        ['2000 x 850', 2000.0, 850.0],
        ['1920 x 1080',1920.0, 1080.0],
        ['1280 x 720', 1280.0, 720.0],
        ['960 x 540', 960.0, 540.0]
    ]

    def __init__(self, parent=maya_main_window()):
        super(OutputResolution, self).__init__(parent)

        self.setWindowTitle("Output Resolution")
        self.setMinimumSize(400,180)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.resolution_list_wdg = QtWidgets.QListWidget()
        #self.resolution_list_wdg.addItems(["1920 x 1080", "1280 x 720", "960 x 540"])
        
        for item in self.RESOLUTION_ITEMS:
            list_widget_item = QtWidgets.QListWidgetItem(item[0])
            list_widget_item.setData(QtCore.Qt.UserRole, [item[1], item[2]])
            self.resolution_list_wdg.addItem(list_widget_item)
        
        self.close_btn = QtWidgets.QPushButton('Close')
        
        
        
    def create_layout(self):
    
        
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.close_btn)
        
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.resolution_list_wdg)
        main_layout.addStretch()
        main_layout.addLayout(btn_layout)
        
    def create_connections(self):
        
        self.resolution_list_wdg.itemClicked.connect(self.setoutput_resolution)
     
        
        
        # close
        self.close_btn.clicked.connect(self.close)
        
    def setoutput_resolution(self, item):
        resolution = item.data(QtCore.Qt.UserRole)
        print(resolution)
        
        mc.setAttr('defaultResolution.width', resolution[0])
        mc.setAttr('defaultResolution.height', resolution[1])
        mc.setAttr('defaultResolution.deviceAspectRatio', resolution[0]/resolution[1])
        

            
if __name__ == "__main__":
    
    try:
        dialog.close()
        dialog.deleteLater()
    except:
        pass

    dialog = OutputResolution()
    dialog.show()
