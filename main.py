import datetime
import sys
from PyQt5 import QtWidgets, uic
from models import session, User
import re
import pyperclip

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('form.ui', self)
        self.setFixedSize(self.size())
        self.onload()
        self.pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.uyeler.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.uyeler.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.uyeler.verticalHeader().setVisible(False)
        self.uyeler.setAlternatingRowColors(True)
        self.uyeler.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.show()
        # double click table row
        self.uyeler.itemClicked.connect(self.copyText)
        self.ekle.clicked.connect(self.createUser)
        self.sil.clicked.connect(self.deleteUser)
        self.uyeler.doubleClicked.connect(self.getUser)
        self.guncelle.clicked.connect(self.updateUser)
        
    def isEmail(self, email) -> bool:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(regex, email):
            return True 
        else:
            return False
        
    def copyText(self, item):
        text = item.text()
        pyperclip.copy(text)
        
    def sendError(self, error):
        return QtWidgets.QMessageBox.warning(self, 'Hata', error)
    
    def sendMessage(self, message):
        return QtWidgets.QMessageBox.information(self, 'Bilgi', message)
    
    def sendQuestion(self, question, title):
        return QtWidgets.QMessageBox.question(self, title, question, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        
    def onload(self):
        self.getUsers()
        
    def getUser(self):
        user = session.query(User).filter_by(name=self.uyeler.item(self.uyeler.currentRow(), 0).text()).first()
        self.userid.setText(str(user.id))
        self.username.setText(user.name)
        self.email.setText(user.email)
        
    def createUser(self):
        user = User(name=self.username.text(), email=self.email.text())
        user.set_password(self.pwd.text())
        existing_user = session.query(User).filter_by(name=self.username.text()).first()
        if existing_user:
            self.sendError('Bu kullanıcı zaten kayıtlı')
        elif self.isEmail(self.email.text()) == False:
            self.sendError('Lütfen geçerli bir eposta adresi giriniz')
            self.email.clear()
        elif len(self.pwd.text()) < 6:
            self.sendError('Şifre en az 6 karakter olmalıdır')
            self.pwd.clear()
        else:
            session.add(user)
            session.commit()
            self.username.clear()
            self.email.clear()
            self.pwd.clear()
            self.getUsers()
            self.sendMessage(f'{user.name} adında kullanıcı başarıyla eklendi')
            
    def deleteUser(self):
        if self.uyeler.currentRow() == -1:
            self.sendError('Lütfen silmek istediğiniz kullanıcıyı seçiniz')
        else:
            name = self.uyeler.item(self.uyeler.currentRow(), 0).text()
            if name:
                question = self.sendQuestion(f'{name} adlı kullanıcıyı silmek istediğinize emin misiniz?', 'Silme')
                if question == QtWidgets.QMessageBox.Yes:
                    user = session.query(User).filter_by(name=name).first()
                    session.delete(user)
                    session.commit()
                    self.getUsers()
                    self.sendMessage('Kullanıcı silindi')
                    
    def updateUser(self):
        if self.uyeler.currentRow() == -1:
            self.sendError('Lütfen güncellemek istediğiniz kullanıcıyı seçiniz')
        else:
            user = session.query(User).filter_by(id=int(self.userid.text())).first()
            if user:
                if self.isEmail(self.email.text()) == False:
                    self.sendError('Lütfen geçerli bir eposta adresi giriniz')
                    self.email.clear()
                elif len(self.pwd.text()) > 1 and  len(self.pwd.text()) < 6:
                    self.sendError('Şifre en az 6 karakter olmalıdır')
                    self.pwd.clear()
                else:
                    if self.pwd.text():
                        user.set_password(self.pwd.text())
                    user.name = self.username.text()
                    user.email = self.email.text()
                    user.updated_at = datetime.datetime.now()
                    session.commit()
                    self.userid.clear()
                    self.username.clear()
                    self.email.clear()
                    self.pwd.clear()
                    self.getUsers()
                    self.sendMessage('Kullanıcı bilgileri güncellendi')
            else:
                self.sendError('Kullanıcı bulunamadı')
            
    def getUsers(self):
        users = session.query(User).all()
        self.uyeler.setRowCount(len(users))
        self.uyeler.setColumnCount(5)
        self.uyeler.setHorizontalHeaderLabels(['Adı', 'Eposta', 'Şifre', 'Katılım', 'Güncelleme'])
        for user in users:
            self.uyeler.setItem(users.index(user), 0, QtWidgets.QTableWidgetItem(user.name))
            self.uyeler.setItem(users.index(user), 1, QtWidgets.QTableWidgetItem(user.email))
            self.uyeler.setItem(users.index(user), 2, QtWidgets.QTableWidgetItem(user.password))
            self.uyeler.setItem(users.index(user), 3, QtWidgets.QTableWidgetItem(user.created_at.strftime('%d.%m.%Y %H:%M:%S')))
            self.uyeler.setItem(users.index(user), 4, QtWidgets.QTableWidgetItem(user.updated_at.strftime('%d.%m.%Y %H:%M:%S')))
        
app = QtWidgets.QApplication(sys.argv)

window = Window()
window.setWindowTitle('PyQT Crud Application')

sys.exit(app.exec_())