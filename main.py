import sys
from PyQt5 import QtWidgets, uic
from models import session, User
import re

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('form.ui', self)
        self.setFixedSize(self.size())
        self.onload()
        self.pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.users.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.users.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.users.verticalHeader().setVisible(False)
        self.users.setAlternatingRowColors(True)
        self.users.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.show()
        self.create.clicked.connect(self.createUser)
        self.delete.clicked.connect(self.deleteUser)
        self.users.doubleClicked.connect(self.getUser)
        self.update.clicked.connect(self.updateUser)
        
    def isEmail(self, email) -> bool:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(regex, email):
            return True 
        else:
            return False
        
    def closeEvent(self, event):
        answer = self.sendQuestion('Do you want to close app? ', 'Info')
        if answer == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        
    def sendError(self, error):
        return QtWidgets.QMessageBox.warning(self, 'Error', error)
    
    def sendMessage(self, message):
        return QtWidgets.QMessageBox.information(self, 'Info', message)
    
    def sendQuestion(self, question, title):
        return QtWidgets.QMessageBox.question(self, title, question, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        
    def onload(self):
        self.getUsers()
        
    def getUser(self):
        user = session.query(User).filter_by(name=self.users.item(self.users.currentRow(), 0).text()).first()
        self.userid.setText(str(user.id))
        self.username.setText(user.name)
        self.email.setText(user.email)
        
    def createUser(self):
        user = User(name=self.username.text(), email=self.email.text())
        user.set_password(self.pwd.text())
        existing_user = session.query(User).filter_by(name=self.username.text()).first()
        if existing_user:
            self.sendError('User already exists')
        elif self.isEmail(self.email.text()) == False:
            self.sendError('Please enter a valid email address')
            self.email.clear()
        elif len(self.pwd.text()) < 6:
            self.sendError('Password must be at least 6 characters')
            self.pwd.clear()
        else:
            session.add(user)
            session.commit()
            self.username.clear()
            self.email.clear()
            self.pwd.clear()
            self.getUsers()
            self.sendMessage(f'User {user.name} created')
            
    def deleteUser(self):
        if self.users.currentRow() == -1:
            self.sendError('Please select a user to delete')
        else:
            name = self.users.item(self.users.currentRow(), 0).text()
            if name:
                question = self.sendQuestion(f'Do you want to delete {name} user?', 'Deleting')
                if question == QtWidgets.QMessageBox.Yes:
                    user = session.query(User).filter_by(name=name).first()
                    session.delete(user)
                    session.commit()
                    self.getUsers()
                    self.sendMessage('Kullanıcı silindi')
                    
    def updateUser(self):
        if self.users.currentRow() == -1:
            self.sendError('Please select a user to update')
        elif self.userid.text() == '':
            self.sendError('Please select a user to update')
        else:
            user = session.query(User).filter_by(id=int(self.userid.text())).first()
            if user:
                if self.isEmail(self.email.text()) == False:
                    self.sendError('Please enter a valid email address')
                    self.email.clear()
                elif len(self.pwd.text()) > 1 and  len(self.pwd.text()) < 6:
                    self.sendError('Password must be at least 6 characters')
                    self.pwd.clear()
                else:
                    if self.pwd.text():
                        user.set_password(self.pwd.text())
                    user.name = self.username.text()
                    user.email = self.email.text()
                    session.commit()
                    self.userid.clear()
                    self.username.clear()
                    self.email.clear()
                    self.pwd.clear()
                    self.getUsers()
                    self.sendMessage('User information updated')
            else:
                self.sendError('User not found')
            
    def getUsers(self):
        users = session.query(User).all()
        self.users.setRowCount(len(users))
        self.users.setColumnCount(5)
        self.users.setHorizontalHeaderLabels(['Username', 'Email', 'Password', 'Created', 'Updated'])
        for user in users:
            self.users.setItem(users.index(user), 0, QtWidgets.QTableWidgetItem(user.name))
            self.users.setItem(users.index(user), 1, QtWidgets.QTableWidgetItem(user.email))
            self.users.setItem(users.index(user), 2, QtWidgets.QTableWidgetItem(user.password))
            self.users.setItem(users.index(user), 3, QtWidgets.QTableWidgetItem(user.created_at.strftime('%d.%m.%Y %H:%M:%S')))
            self.users.setItem(users.index(user), 4, QtWidgets.QTableWidgetItem(user.updated_at.strftime('%d.%m.%Y %H:%M:%S')))
        
app = QtWidgets.QApplication(sys.argv)

window = Window()
window.setWindowTitle('PyQT Crud Application')

sys.exit(app.exec_())