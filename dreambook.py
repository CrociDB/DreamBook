#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore

class Dreambook(QtGui.QMainWindow):
    
    def __init__(self):
        # Init Qt
        QtGui.QMainWindow.__init__(self)
        self.build_actions()
        self.build_bars()
        self.build_gui()

        # Data
        self.config_store()

        # Load the Dreams list
        self.load_dreams()

    def build_actions(self):
        self.toolbar_exit = QtGui.QAction(QtGui.QIcon('resources/exit.png'), "&Exit", self)
        self.toolbar_exit.setShortcut('Ctrl+Q')
        self.connect(self.toolbar_exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

    def build_bars(self):
        self.resize(750, 500)
        self.setWindowTitle('DreamBook')

        # Menu Bar
        self.menubar = self.menuBar()

        # Menu Dreams
        self.menu_dreams = self.menubar.addMenu("&Dreams")

        self.menu_dreams.addAction(self.toolbar_exit)

        # Menu Help
        self.menu_help = self.menubar.addMenu("&Help")

        # ToolBar
        self.toolbar = self.addToolBar("Toolbar");
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.toolbar_exit)

        # Status Bar
        self.statusBar().showMessage("Ready")

    def build_gui(self):
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        left_grid = QtGui.QGridLayout()
        left_grid.setSpacing(10)

        widget = QtGui.QWidget()
        widget.setLayout(grid)
        left = QtGui.QWidget()
        left.setLayout(left_grid)

        # Dreams list
        self.build_list()
        grid.addWidget(self.dreams_list, 0, 0)

        # Dreams details
        left_grid.addWidget(QtGui.QLabel("Title"), 0, 0)
        left_grid.addWidget(QtGui.QLineEdit(), 1, 0)

        left_grid.addWidget(QtGui.QLabel("Dream"), 2, 0)
        left_grid.addWidget(QtGui.QTextEdit(), 3, 0)

        left_grid.addWidget(QtGui.QLabel("Date"), 4, 0)
        left_grid.addWidget(QtGui.QLineEdit(), 5, 0)

        left_grid.addWidget(QtGui.QPushButton("Save"), 6, 0)

        grid.addWidget(left, 0, 1)
        self.setCentralWidget(widget)

    def build_list(self):
        self.dreams_list_model = QtGui.QStandardItemModel(1, 2)

        self.dreams_list = QtGui.QListView()
        self.dreams_list.setMaximumWidth(250)
        self.dreams_list.setMinimumWidth(100)

        self.dreams_list.setModel(self.dreams_list_model)

    def config_store(self):
        self.dreams = []
        
    def load_dreams(self):
        pass
        

app = QtGui.QApplication(sys.argv)
main = Dreambook()
main.show()
sys.exit(app.exec_())