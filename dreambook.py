#!/usr/bin/python

import sys
import pickle
from PyQt4 import QtGui, QtCore

class Dreams():
    
    DATA_FILE = 'dreams.db'
    
    def __init__(self):
        if not self.load():
            self.create()
            self.save()
            
    def load(self):
        try:
            file = open(self.DATA_FILE, 'rb')
        except IOError:
            return False
        
        self.dreams = pickle.load(file)
        file.close()
        
        if self.dreams == None: return False
        return True
        
    def create(self):
        self.dreams = []        
        
    def save(self):
        file = open(self.DATA_FILE, 'wb')
        pickle.dump(self.dreams, file)
        file.close()
        
    def add(self, title, content, date):
        id = len(self.dreams)
        self.dreams.append({ 'id': id,'title': title, 'content': content, 'date': date})
        self.save()
        return id
        
    def replace(self, id, title, content, date):
        self.dreams[id] = { 'id': id, 'title': title, 'content': content, 'date': date}
        self.save()
        
    def delete(self, id):
        self.dreams.pop(id)
        self.save()
        
    def check_id(self, id):
        return True in map(lambda x: x['id'] == id, self.dreams)

class Dreambook(QtGui.QMainWindow):
    
    def __init__(self):
        # Init Qt
        QtGui.QMainWindow.__init__(self)
        self.build_actions()
        self.build_bars()
        self.build_gui()

        self.add_events()

        # Data
        self.config_store()
        
        self.current_id = -1
        self.current_dream_changed = False

    def add_events(self):
        self.connect(self.toolbar_new, QtCore.SIGNAL('triggered()'), self.new)
        self.connect(self.toolbar_delete, QtCore.SIGNAL('triggered()'), self.delete)
        self.connect(self.toolbar_exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.connect(self.save_button, QtCore.SIGNAL('clicked()'), self.save_dream)
        
        self.connect(self.text_title, QtCore.SIGNAL("textEdited(QString)"), self.text_changed)
        self.connect(self.text_content, QtCore.SIGNAL("textEdited(QString)"), self.text_changed)
        self.connect(self.text_date, QtCore.SIGNAL("textEdited(QString)"), self.text_changed)

    def build_actions(self):
        self.toolbar_new = QtGui.QAction(QtGui.QIcon('resources/add.png'), "&New", self)
        self.toolbar_new.setShortcut('Ctrl+N')
        
        self.toolbar_delete = QtGui.QAction(QtGui.QIcon('resources/delete.png'), "&Remove", self)
        self.toolbar_delete.setShortcut('Ctrl+D')
        
        self.toolbar_exit = QtGui.QAction(QtGui.QIcon('resources/exit.png'), "&Exit", self)
        self.toolbar_exit.setShortcut('Ctrl+Q')

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
        self.toolbar.addAction(self.toolbar_new)
        self.toolbar.addAction(self.toolbar_delete)
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
        self.text_title = QtGui.QLineEdit()
        left_grid.addWidget(self.text_title, 1, 0)

        left_grid.addWidget(QtGui.QLabel("Dream"), 2, 0)
        self.text_content = QtGui.QTextEdit()
        left_grid.addWidget(self.text_content, 3, 0)

        left_grid.addWidget(QtGui.QLabel("Date"), 4, 0)
        self.text_date = QtGui.QLineEdit()
        left_grid.addWidget(self.text_date, 5, 0)

        self.save_button = QtGui.QPushButton("Save")
        left_grid.addWidget(self.save_button, 6, 0)

        grid.addWidget(left, 0, 1)
        self.setCentralWidget(widget)

    def build_list(self):
        self.dreams_list = QtGui.QListView()
        self.dreams_list.setMaximumWidth(250)
        self.dreams_list.setMinimumWidth(100)
        self.dreams_list.clicked.connect(self.list_clicked)

    def config_store(self):
        self.dreams = Dreams()
        self.update_list()
        
    def update_list(self):
        model = QtGui.QStandardItemModel(self.dreams_list)
        
        for dream in self.dreams.dreams:
            item = QtGui.QStandardItem(dream['title'])
            model.appendRow(item)
            
        self.dreams_list.setModel(model)  
        
    def show_dream(self, index):
        if self.current_dream_changed:
            if self.confirm_save():
                self.save_dream()
        
        self.current_id = index
        self.current_dream_changed = False
        
        self.text_title.setText(self.dreams.dreams[index]['title'])
        self.text_content.setText(self.dreams.dreams[index]['content'])
        self.text_date.setText(self.dreams.dreams[index]['date'])
        
    def confirm_save(self):
        reply = QtGui.QMessageBox.question(
            self, 
            'Save?',
            'You changed your dream. Do you want to save?', 
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, 
            QtGui.QMessageBox.Yes
        )
        
        return reply == QtGui.QMessageBox.Yes
        
    # Events
    
    def new(self):
        self.current_id = -1
        
        self.text_title.setText("")
        self.text_content.setText("")
        self.text_date.setText("")
        
        self.update_list()
        
        self.text_title.setFocus(True)
        
    def delete(self):
        reply = QtGui.QMessageBox.question(
            self, 
            'Remove?',
            'Do you really want to remove that?', 
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, 
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.dreams.delete(self.current_id)
            self.new()            
    
    def save_dream(self):
        if self.current_id > -1 and self.dreams.check_id(self.current_id):
            self.dreams.replace(self.current_id, self.text_title.text(), self.text_content.toPlainText(), self.text_date.text())
        else:
            self.current_id = self.dreams.add(self.text_title.text(), self.text_content.toPlainText(), self.text_date.text())
        
        self.update_list()
        
    def list_clicked(self, index):
        self.show_dream(index.row())
    
    def text_changed(self, text):
        self.current_dream_changed = True
        
app = QtGui.QApplication(sys.argv)
main = Dreambook()
main.show()
sys.exit(app.exec_())