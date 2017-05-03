from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
from User import *
import math
import sys
import ctypes

class MainUI(QMainWindow):
    def __init__(self , parent = None):
        QMainWindow.__init__(self, None)
        #setting main window
        self.setMinimumSize(1280, 720)
        self.setWindowTitle("MBM v.0")
        self.parent = parent
        self.UIinit()

    # init UI form (attribute)
    def UIinit(self):
        #init mainWidget

        #user32 = ctypes.windll.user32
        #screensize = user32.GetSystemMetrics(1)
        #form_name = "mainForm(" + str(screensize) + ")" + ".ui"
        form_name = "mainForm(1080).ui"
        form = None

        try:
            loader = QUiLoader()
            form = loader.load(form_name, None)
            self.setCentralWidget(form)
        except:
            loader = QUiLoader()
            form = loader.load("mainForm(1080).ui", None)
            self.setCentralWidget(form)

        self.setCentralWidget(form)
        self.profile = form.findChild(QLabel, "profile")
        self.menu = form.findChild(QComboBox, "comboBox")
        self.menu.activated[str].connect(self.changePage)
        
        #CalendarImplementation
        self.monthLabel = form.findChild(QLabel, "monthLabel")
        dateeT = QDate.currentDate()
        

        #initDate
        self.L00 = form.findChild(QLabel, "L00")
        self.L01 = form.findChild(QLabel, "L01")
        self.L02 = form.findChild(QLabel, "L02")
        self.L03 = form.findChild(QLabel, "L03")
        self.L04 = form.findChild(QLabel, "L04")
        self.L05 = form.findChild(QLabel, "L05")
        self.L06 = form.findChild(QLabel, "L06")
        self.L10 = form.findChild(QLabel, "L10")
        self.L11 = form.findChild(QLabel, "L11")
        self.L12 = form.findChild(QLabel, "L12")
        self.L13 = form.findChild(QLabel, "L13")
        self.L14 = form.findChild(QLabel, "L14")
        self.L15 = form.findChild(QLabel, "L15")
        self.L16 = form.findChild(QLabel, "L16")
        self.L20 = form.findChild(QLabel, "L20")
        self.L21 = form.findChild(QLabel, "L21")
        self.L22 = form.findChild(QLabel, "L22")
        self.L23 = form.findChild(QLabel, "L23")
        self.L24 = form.findChild(QLabel, "L24")
        self.L25 = form.findChild(QLabel, "L25")
        self.L26 = form.findChild(QLabel, "L26")
        self.L30 = form.findChild(QLabel, "L30")
        self.L31 = form.findChild(QLabel, "L31")
        self.L32 = form.findChild(QLabel, "L32")
        self.L33 = form.findChild(QLabel, "L33")
        self.L34 = form.findChild(QLabel, "L34")
        self.L35 = form.findChild(QLabel, "L35")
        self.L36 = form.findChild(QLabel, "L36")
        self.L40 = form.findChild(QLabel, "L40")
        self.L41 = form.findChild(QLabel, "L41")
        self.L42 = form.findChild(QLabel, "L42")
        self.L43 = form.findChild(QLabel, "L43")
        self.L44 = form.findChild(QLabel, "L44")
        self.L45 = form.findChild(QLabel, "L45")
        self.L46 = form.findChild(QLabel, "L46")
        self.L50 = form.findChild(QLabel, "L50")
        self.L51 = form.findChild(QLabel, "L51")
        self.L52 = form.findChild(QLabel, "L52")
        self.L53 = form.findChild(QLabel, "L53")
        self.L54 = form.findChild(QLabel, "L54")
        self.L55 = form.findChild(QLabel, "L55")
        self.L56 = form.findChild(QLabel, "L56")
               

        #setTime
        self.changeDate(dateeT.getDate())
        #Button
        self.BacButton = form.findChild(QPushButton, "BackButton")
        self.BacButton.clicked.connect(self.BackButton)
        self.NexButton = form.findChild(QPushButton, "NextButton")
        self.NexButton.clicked.connect(self.NextButton)
        

        #init Subwidget
        '''
        self.subWidget = form.findChild(QStackedWidget, "stackedWidget")
        self.subWidget.setCurrentIndex(0)

        #Edit Profile section components
        self.save_warn_label = form.findChild(QLabel, "save_warn_label")

        self.name_line = form.findChild(QLineEdit, "name_lineEdit")
        self.middlename_line = form.findChild(QLineEdit, "middlename_lineEdit")
        self.surname_line = form.findChild(QLineEdit, "surname_lineEdit")
        self.nickname_line = form.findChild(QLineEdit, "nickname_lineEdit")
        self.phone_line = form.findChild(QLineEdit, "phone_lineEdit")
        self.email_line = form.findChild(QLineEdit, "email_lineEdit")
        self.address_text = form.findChild(QTextEdit, "address_textEdit")
        self.bio_text = form.findChild(QTextEdit, "bio_textEdit")

        self.birth_edit = form.findChild(QDateEdit, "dateEdit")
        self.nation_box = form.findChild(QComboBox, "nation_box")
        self.position_box = form.findChild(QComboBox, "position_box")
        self.department_box = form.findChild(QComboBox, "department_box")
        self.save_button = form.findChild(QPushButton, "save_button")
        self.cancel_button = form.findChild(QPushButton, "cancel_button")
        self.change_password_button = form.findChild(QPushButton, "change_password_button")

        self.save_button.clicked.connect(self.saveProfile)
        self.cancel_button.clicked.connect(self.backToMainPage)
        self.change_password_button.clicked.connect(self.changePassWordWidget)

        #Change password section component
        self.cur_password = form.findChild(QLineEdit, "cur_password")
        self.new_password = form.findChild(QLineEdit, "new_password")
        self.re_password = form.findChild(QLineEdit, "re_password")
        self.warn_change_label = form.findChild(QLabel, "warn_change_label")

        self.confirm_password_button = form.findChild(QPushButton, "confirm_password_button")
        self.cancel_password_button =  form.findChild(QPushButton, "cancel_password_button")

        self.confirm_password_button.clicked.connect(self.confirm_password)
        self.cancel_password_button.clicked.connect(self.backToProfilePage)
        '''
    def BackButton(self):
        m = int(self.CurDate[1])
        m -= 1
        y = int(self.CurDate[0])
        if(m < 1):
            m = 12
            y -= 1
        self.changeDate((y,m,self.CurDate[2]))

    def NextButton(self):
        m = int(self.CurDate[1])
        m += 1
        y = int(self.CurDate[0])
        if(m > 12):
            m = 1
            y += 1
        self.changeDate((y,m,self.CurDate[2]))
        
    def changeDate(self,date):
        month = ['January','February','March','April','May','June','July','August','September','October','November','December']
        week = ["Sat","Sun","Mon","Tue","Wed","Thu","Fri"]
        limit = 0
        self.CurDate = date
        
        self.monthLabel.setText(str(month[self.CurDate[1]-1])+" "+str(self.CurDate[0]))
        count = 1
        wek = self.calcalendar(1,int(self.CurDate[1]),int(self.CurDate[0]))
        startDate = wek -1
        if(startDate < 0):
            startDate = 6
        elif(startDate > 6):
            startDate = 0
        mon = self.CurDate[1]
        if(mon == 2):
            if(self.calFebruary(int(self.CurDate[0]))):
                limit = 29
            else:
                limit = 28
        elif(mon == 4 or mon == 6 or mon == 9 or mon == 11 ):
            limit = 30
        else:
            limit = 31
        for i in range(6):
            for j in range(7):
                lab = 'L'+str(i)+str(j)
                n = getattr(self,lab)
                if(j >= startDate or i > 0):
                    if(count <= limit):
                        n.setText(str(count))
                        count += 1
                    else:
                        n.setText(str(""))
                else:
                    n.setText(str(""))
                
    def calFebruary(self,Y): 
        if(Y > 0 and type(Y) == int):
            if(0 == (Y % 400)):
                checkLeap = True
            else:
                if ((0 == (Y % 4)) and (not (0 == (Y % 100)))):
                     checkLeap = True
                else:
                    checkLeap = False
            return checkLeap           
        else:
            print("Wrong Type")
    def calcalendar(self,day,month,year):
        FebVar = 28
        if(month == 1):
            month = 13
            year -= 1
        if(month == 2):
            if(self.calFebruary(year)):
                FebVar = 29
            month = 14
            year -= 1
        if(day > FebVar and month == 14):
            print("no this day")
        else:
            q = day
            m = month
            k = year % 100
            j = math.floor(year / 100)
            h = q + math.floor(13*(m+1)/5) + k + math.floor(k/4) + math.floor(j/4) + 5*j
            h = h % 7
            return h

    def mainPageSlot(self):
        print("test")

    def settingSlot(self):
        print("test")

    def saveProfile(self):
        self.parent.user.name = (self.name_line.text())
        self.parent.user.middle_name = (self.middlename_line.text())
        self.parent.user.last_name = (self.surname_line.text())
        self.parent.user.nickname = (self.nickname_line.text())
        self.parent.user.phone_number = self.phone_line.text()
        self.parent.user.email = self.email_line.text()
        #have more
        #send user(modified) back to server
        self.parent.send("updateProfile", self.parent.user)
        self.loadProfile()
        self.save_warn_label.setText("Profile already updated (saved)")

    def loadProfile(self):
        self.name_line.setText(self.parent.user.name)
        self.middlename_line.setText(self.parent.user.middle_name)
        self.surname_line.setText(self.parent.user.last_name)
        self.nickname_line.setText(self.parent.user.nickname)
        self.phone_line.setText(self.parent.user.phone_number)
        self.email_line.setText(self.parent.user.email)
        self.save_warn_label.setText("")

    def confirm_password(self):
        if self.cur_password.text() != self.parent.user.password:
            self.warn_change_label.setText("Wrong current password")
        elif self.re_password.text() == "" or self.new_password.text() == "":
            self.warn_change_label.setText("Please enter password")
        elif self.re_password.text() != self.new_password.text():
            self.warn_change_label.setText("Re-enter password wrong")
        elif not self.passwordValidation(self.new_password.text()):
            self.warn_change_label.setText("Password must contain digit and Capital letter")
        else:
            self.parent.user.password = self.new_password.text()
            self.parent.send("updateProfile", self.parent.user)
            self.warn_change_label.setText("Password Changed (Completed)")

    def changePassWordWidget(self):
        self.warn_change_label.setText("")
        self.new_password.setText("")
        self.cur_password.setText("")
        self.re_password.setText("")
        self.subWidget.setCurrentIndex(3)

    def backToMainPage(self):
        if self.menu.currentText() == "Edit Profile":
            self.subWidget.setCurrentIndex(0)

    def backToProfilePage(self):
        self.subWidget.setCurrentIndex(1)

    def changePage(self):
        if(self.menu.currentText() == "Main Page"):
            self.subWidget.setCurrentIndex(0)
        elif(self.menu.currentText() == "Edit Profile"):
            print(self.parent.user)
            self.subWidget.setCurrentIndex(1)
            self.loadProfile()
        elif (self.menu.currentText() == "Settings"):
            self.subWidget.setCurrentIndex(2)

    def passwordValidation(self, password):
        isDigit = False
        isCapitalized = False
        for alp in password:
            if alp.isdigit():
                isDigit = True
            if alp.isupper():
                isCapitalized = True
        if not (isDigit and isCapitalized):
            return False
        return True

def main():
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    app.exec_()

if __name__ == "__main__":
    main()

