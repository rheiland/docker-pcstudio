import os
import zipfile
import shutil
from pathlib import Path
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QFrame,QApplication,QWidget,QTabWidget,QFormLayout,QLineEdit, QGroupBox, QHBoxLayout,QVBoxLayout,QRadioButton,QLabel,QCheckBox,QComboBox,QScrollArea,  QMainWindow,QGridLayout, QPushButton, QFileDialog, QMessageBox, QStackedWidget, QSplitter, QScrollArea

from studio_classes import DoubleValidatorWidgetBounded
# from PyQt5.QtWidgets import QCompleter, QSizePolicy
# from PyQt5.QtCore import QSortFilterProxyModel
# from PyQt5.QtSvg import QSvgWidget
# from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QIntValidator
# from PyQt5.QtCore import QRectF, Qt

try:
    from galaxy_ie_helpers import put, find_matching_history_ids, get
except:
    print("----- cannot import from galaxy_ie_helpers ")
    pass

class ScrollLabel(QScrollArea):
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)

        lay = QVBoxLayout(content)
        self.label = QLabel(content)
        self.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        lay.addWidget(self.label)

    def setText(self, text):
        self.label.setText(text)


class GalaxyHistoryWindow(QWidget):
    # def __init__(self, output_dir):
    def __init__(self):   # we use vis_tab for some of the methods called
        super().__init__()

        stylesheet = """ 
            QPushButton{ border: 1px solid; border-color: rgb(145, 200, 145); border-radius: 1px;  background-color: lightgreen; color: black; width: 64px; padding-right: 8px; padding-left: 8px; padding-top: 3px; padding-bottom: 3px; } 

            """

        # self.output_dir = output_dir
        self.file_id = 0

        self.setStyleSheet(stylesheet)
        
        #-------------------------------------------
        self.scroll = QScrollArea()  # might contain centralWidget

        self.vbox = QVBoxLayout()
        glayout = QGridLayout()

        # hbox = QHBoxLayout()
        self.vbox.addLayout(glayout)

        #-------------------------------------------
        idx_row = 0
        self.get_file_button = QPushButton("get file with ID=")
        self.get_file_button.setEnabled(True)
        self.get_file_button.setStyleSheet("background-color: lightgreen;")
        self.get_file_button.clicked.connect(self.get_file_cb)
        glayout.addWidget(self.get_file_button, idx_row,0,1,2) # w, row, column, rowspan, colspan

        self.file_id_w = QLineEdit("0")  # str(self.vis_tab.axes_x_center))
        self.file_id_w.setEnabled(True)
        self.file_id_w.setFixedWidth(70)
        self.file_id_w.setValidator(QIntValidator())
        self.file_id_w.textChanged.connect(self.file_id_changed)
        glayout.addWidget(self.file_id_w , idx_row,2, 1,1) # w, row, column, rowspan, colspan
        #--------------------------------

        idx_row += 1
        glayout.addWidget(QLabel(f"pwd: {Path.cwd()}"), idx_row,0,1,2) # w, row, column, rowspan, colspan

        idx_row += 1
        self.show_files_button = QPushButton("dir")
        self.show_files_button.setStyleSheet("background-color: lightgreen;")
        self.show_files_button.clicked.connect(self.show_files_cb)
        glayout.addWidget(self.show_files_button, idx_row,0,1,1) # w, row, column, rowspan, colspan

        self.relative_path = QLineEdit(".")
        self.relative_path.setFixedWidth(80)
        # self.relative_path.setValidator(QIntValidator())
        # self.relative_path.textChanged.connect(self.file_id_changed)
        glayout.addWidget(self.relative_path, idx_row,1,1,1) # w, row, column, rowspan, colspan

        self.dir_files = ScrollLabel(self)
        # setting text to the label
        # dir_files = os.listdir(self.relative_path.text())
        # self.dir_files.setText(str(dir_files))
        # setting geometry
        self.dir_files.setGeometry(100, 100, 200, 80)
        
        self.vbox.addWidget(self.dir_files)

        #----------

        #----------
        self.close_button = QPushButton("Close")
        self.close_button.setStyleSheet("background-color: lightgreen;")
        # self.close_button.setFixedWidth(150)
        self.close_button.clicked.connect(self.close_galaxy_history_cb)

        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)

        self.vbox.addWidget(self.close_button)
        # self.layout.setStretch(0,1000)

        self.setLayout(self.vbox)
        self.resize(200, 200)   # try to fix the size
        # self.resize(250, 220)   # try to fix the size


    #--------
    # def show_info_message(self, message):
    #     msgBox = QMessageBox()
    #     msgBox.setIcon(QMessageBox.Information)
    #     msgBox.setText(message)
    #     msgBox.setStandardButtons(QMessageBox.Ok)
    #     msgBox.exec_()

    def get_file_cb(self,sval):
        self.file_id = int(self.file_id_w.text())
        try:
            msgBox = QMessageBox()
            msgBox.setText(f'Copying the requested data from the Galaxy History')
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            # fid = find_matching_history_ids(self.file_id)
            # get(fid)
            get(self.file_id)
            # print("dummy get")
        except:
            print("Unable to get the file from History")
            msgBox = QMessageBox()
            msgBox.setText(f'get_file_cb: Unable to get file with History ID {self.file_id}. Perhaps you got it previously.')
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()

    def file_id_changed(self,sval):
        try:
            self.file_id = int(sval)
        except:
            pass

    def save_png_cb(self):
        self.vis_tab.png_frame = 0
        self.vis_tab.save_png = self.save_png_checkbox.isChecked()
        
    def show_files_cb(self):
        dir_files = os.listdir(self.relative_path.text())
        self.dir_files.setText(str(dir_files))
        return

    #----------
    def close_galaxy_history_cb(self):
        self.close()

#----------------------------------------------------------------
class LoadProjectWindow(QWidget):
    # def __init__(self, output_dir):
    def __init__(self):   # we use vis_tab for some of the methods called
        super().__init__()

        stylesheet = """ 
            QPushButton{ border: 1px solid; border-color: rgb(145, 200, 145); border-radius: 1px;  background-color: lightgreen; color: black; width: 64px; padding-right: 8px; padding-left: 8px; padding-top: 3px; padding-bottom: 3px; } 

            """

        # self.output_dir = output_dir
        self.file_id = 0

        self.setStyleSheet(stylesheet)
        
        #-------------------------------------------
        self.scroll = QScrollArea()  # might contain centralWidget

        self.vbox = QVBoxLayout()
        glayout = QGridLayout()

        # hbox = QHBoxLayout()
        self.vbox.addLayout(glayout)

        #-------------------------------------------
        idx_row = 0
        self.get_file_button = QPushButton("Get my_model.zip on History with ID=")
        self.get_file_button.setFixedWidth(250)
        self.get_file_button.setEnabled(True)
        self.get_file_button.setStyleSheet("background-color: lightgreen;")
        self.get_file_button.clicked.connect(self.get_project_cb)
        glayout.addWidget(self.get_file_button, idx_row,0,1,2) # w, row, column, rowspan, colspan

        self.file_id_w = QLineEdit("0")  # str(self.vis_tab.axes_x_center))
        self.file_id_w.setEnabled(True)
        self.file_id_w.setFixedWidth(70)
        self.file_id_w.setValidator(QIntValidator())
        self.file_id_w.textChanged.connect(self.file_id_changed)
        glayout.addWidget(self.file_id_w , idx_row,2, 1,1) # w, row, column, rowspan, colspan
        #--------------------------------

        idx_row += 1
        msg = "Select the ID value of a 'my_model.zip' on the\nGalaxy History then press the Get button above.\nThis will unzip those files into your /config directory."
        # glayout.addWidget(QLabel(f"pwd: {Path.cwd()}"), idx_row,0,1,2) # w, row, column, rowspan, colspan
        glayout.addWidget(QLabel(msg), idx_row,0,1,3) # w, row, column, rowspan, colspan

        #----------
        self.close_button = QPushButton("Close")
        self.close_button.setStyleSheet("background-color: lightgreen;")
        # self.close_button.setFixedWidth(150)
        self.close_button.clicked.connect(self.close_load_project)

        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)

        self.vbox.addWidget(self.close_button)
        # self.layout.setStretch(0,1000)

        self.setLayout(self.vbox)
        self.resize(190, 200)   # try to fix the size
        # self.resize(250, 220)   # try to fix the size


    #--------
    def show_info_message(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def get_project_cb(self,sval):
        self.file_id = int(self.file_id_w.text())
        zip_file = "my_model.zip"
        msgBox = QMessageBox()
        from_filename = "/import/"   # default dir used by "get()"; our Docker container created this dir
        try:
            msgBox = QMessageBox()
            msgBox.setText(f'Copying the requested data from the Galaxy History')
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            # fid = find_matching_history_ids(self.file_id)
            # get(fid)
            get(self.file_id)
            from_filename += self.file_id
            try:
                print(f"get_project_cb(): attempting to copy {from_filename} to {zip_file}")
                shutil.copy(from_filename, zip_file)
            except:
                msg = f"Error: unable to copy {from_filename} to {zip_file}"
                print(msg)
                msgBox.setText(msg)
                msgBox.setStandardButtons(QMessageBox.Ok)
                returnValue = msgBox.exec()
            # print("dummy get")
            # os.chdir("config")
            # os.chdir("..")
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(path="config")
                # print("Successful zip extractall")
                msgBox.setText(f'Successful extractall into /config')
                msgBox.setStandardButtons(QMessageBox.Ok)
                returnValue = msgBox.exec()
        except FileNotFoundError:
            msg = f"Error: The file {zip_file} was not found."
            print(msg)
            msgBox.setText(msg)
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
        except zipfile.BadZipFile:
            msg = f"Error: The file {zip_file} is not a valid or supported zip file."
            print(msg)
            msgBox.setText(msg)
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
        except Exception as e:
            msg = f'get_project_cb(): There was a problem getting or unzipping {from_filename} with History ID {self.file_id}. Perhaps you got it previously.'
            print(msg)
            msgBox.setText(msg)
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()

    def file_id_changed(self,sval):
        try:
            self.file_id = int(sval)
        except:
            pass

    # def save_png_cb(self):
    #     self.vis_tab.png_frame = 0
    #     self.vis_tab.save_png = self.save_png_checkbox.isChecked()
        
    # def show_files_cb(self):
    #     dir_files = os.listdir(self.relative_path.text())
    #     self.dir_files.setText(str(dir_files))
    #     return

    #----------
    def close_load_project(self):
        self.close()

