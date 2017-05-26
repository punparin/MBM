from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
from User import *
import math
import sys
import datetime
import calendar
import time
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
        self.formm = form
        self.setCentralWidget(form)
        self.profile = form.findChild(QLabel, "profile")
        self.menu = form.findChild(QComboBox, "comboBox")
        self.menu.activated[str].connect(self.changePage)
        
        #monthLabelInit
        self.monthLabel = form.findChild(QLabel, "monthLabel")

        #setCurrentTime
        self.mo = datetime.datetime.now().month
        self.ye = datetime.datetime.now().year
        calendar.setfirstweekday(calendar.SUNDAY)
        

        #initDate
        self.L00 = form.findChild(QLabel, "L00")
        self.L01 = form.findChild(QLabel, "L01")
        self.L02 = form.findChild(QLabel, "L02")
        self.L03 = form.findChild(QLabel, "L03")
        self.L04 = form.findChild(QLabel, "L04")
        self.L05 = form.findChild(QLabel, "L05")
        self.L06 = form.findChild(QLabel, "L06")
        self.L07 = form.findChild(QLabel, "L07")
        self.L08 = form.findChild(QLabel, "L08")
        self.L09 = form.findChild(QLabel, "L09")
        self.L10 = form.findChild(QLabel, "L10")
        self.L11 = form.findChild(QLabel, "L11")
        self.L12 = form.findChild(QLabel, "L12")
        self.L13 = form.findChild(QLabel, "L13")
        self.L14 = form.findChild(QLabel, "L14")
        self.L15 = form.findChild(QLabel, "L15")
        self.L16 = form.findChild(QLabel, "L16")
        self.L17 = form.findChild(QLabel, "L17")
        self.L18 = form.findChild(QLabel, "L18")
        self.L19 = form.findChild(QLabel, "L19")
        self.L20 = form.findChild(QLabel, "L20")
        self.L21 = form.findChild(QLabel, "L21")
        self.L22 = form.findChild(QLabel, "L22")
        self.L23 = form.findChild(QLabel, "L23")
        self.L24 = form.findChild(QLabel, "L24")
        self.L25 = form.findChild(QLabel, "L25")
        self.L26 = form.findChild(QLabel, "L26")
        self.L27 = form.findChild(QLabel, "L27")
        self.L28 = form.findChild(QLabel, "L28")
        self.L29 = form.findChild(QLabel, "L29")
        self.L30 = form.findChild(QLabel, "L30")
        self.L31 = form.findChild(QLabel, "L31")
        self.L32 = form.findChild(QLabel, "L32")
        self.L33 = form.findChild(QLabel, "L33")
        self.L34 = form.findChild(QLabel, "L34")
        self.L35 = form.findChild(QLabel, "L35")
        self.L36 = form.findChild(QLabel, "L36")
        self.L37 = form.findChild(QLabel, "L37")
        self.L38 = form.findChild(QLabel, "L38")
        self.L39 = form.findChild(QLabel, "L39")
        self.L40 = form.findChild(QLabel, "L40")
        self.L41 = form.findChild(QLabel, "L41")

        #InitQWidget
        self.w00 = form.findChild(QWidget, "w00")
        self.w01 = form.findChild(QWidget, "w01")
        self.w02 = form.findChild(QWidget, "w02")
        self.w03 = form.findChild(QWidget, "w03")
        self.w04 = form.findChild(QWidget, "w04")
        self.w05 = form.findChild(QWidget, "w05")
        self.w06 = form.findChild(QWidget, "w06")
        self.w07 = form.findChild(QWidget, "w07")
        self.w08 = form.findChild(QWidget, "w08")
        self.w09 = form.findChild(QWidget, "w09")
        self.w10 = form.findChild(QWidget, "w10")
        self.w11 = form.findChild(QWidget, "w11")
        self.w12 = form.findChild(QWidget, "w12")
        self.w13 = form.findChild(QWidget, "w13")
        self.w14 = form.findChild(QWidget, "w14")
        self.w15 = form.findChild(QWidget, "w15")
        self.w16 = form.findChild(QWidget, "w16")
        self.w17 = form.findChild(QWidget, "w17")
        self.w18 = form.findChild(QWidget, "w18")
        self.w19 = form.findChild(QWidget, "w19")
        self.w20 = form.findChild(QWidget, "w20")
        self.w21 = form.findChild(QWidget, "w21")
        self.w22 = form.findChild(QWidget, "w22")
        self.w23 = form.findChild(QWidget, "w23")
        self.w24 = form.findChild(QWidget, "w24")
        self.w25 = form.findChild(QWidget, "w25")
        self.w26 = form.findChild(QWidget, "w26")
        self.w27 = form.findChild(QWidget, "w27")
        self.w28 = form.findChild(QWidget, "w28")
        self.w29 = form.findChild(QWidget, "w29")
        self.w30 = form.findChild(QWidget, "w30")
        self.w31 = form.findChild(QWidget, "w31")
        self.w32 = form.findChild(QWidget, "w32")
        self.w33 = form.findChild(QWidget, "w33")
        self.w34 = form.findChild(QWidget, "w34")
        self.w35 = form.findChild(QWidget, "w35")
        self.w36 = form.findChild(QWidget, "w36")
        self.w37 = form.findChild(QWidget, "w37")
        self.w38 = form.findChild(QWidget, "w38")
        self.w39 = form.findChild(QWidget, "w39")
        self.w40 = form.findChild(QWidget, "w40")
        self.w41 = form.findChild(QWidget, "w41")

        #settabWidget
        self.tabW = form.findChild(QTabWidget, "tabWidget")
        self.gTabWidX = self.tabW.x()
        self.gTabWidY = self.tabW.y()
               

        #setTime
        self.changeDate()
        
        #Button
        self.BacButton = form.findChild(QPushButton, "BackButton")
        self.BacButton.clicked.connect(self.BackButton)
        self.NexButton = form.findChild(QPushButton, "NextButton")
        self.NexButton.clicked.connect(self.NextButton)
        

        #init Subwidget
        self.subWidget = form.findChild(QStackedWidget, "stackedWidget")
        self.subWidget.setCurrentIndex(0)

        #Edit Profile section components
        '''
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
    def WeekInit(self,wList):
        #LabelInit
        self.Lw00 = self.formm.findChild(QLabel, "LP00")
        self.Lw01 = self.formm.findChild(QLabel, "LP01")
        self.Lw02 = self.formm.findChild(QLabel, "LP02")
        self.Lw03 = self.formm.findChild(QLabel, "LP03")
        self.Lw04 = self.formm.findChild(QLabel, "LP04")
        self.Lw05 = self.formm.findChild(QLabel, "LP05")
        self.Lw06 = self.formm.findChild(QLabel, "LP06")

        #ButtonInit
        self.backMainButton = self.formm.findChild(QPushButton, "backMainButton")
        self.backMainButton.clicked.connect(self.backToMainPage)

        #setDateInWeek
        for i in range(7):
            Lweek = 'Lw0'+str(i)
            w = getattr(self,Lweek)
            if(wList[i] != 0):
                w.setText(str(wList[i]))
            else:
                w.setText("")
            
        
    def mousePressEvent(self,e):
        plusX = self.gTabWidX
        plusY = self.gTabWidY
        ex = e.x()-(plusX-4)
        ey = e.y()-(plusY+20)
        for i in range(5):
            for j in range(10):
                Labell = 'L'+str(i)+str(j)
                lab = 'w'+str(i)+str(j)
                if(lab =='w42' or Labell =='L42'):
                    break
                nl = getattr(self,Labell)
                if(nl.text() != ""):
                    n = getattr(self,lab)
                    if(n.geometry().contains(ex,ey)):
                        st = int(nl.text()) 
                        for k in range(len(self.dList)):
                           if(st in self.dList[k]):
                               self.goToWeekPage(self.dList[k]) ##inputweekList
               
    def BackButton(self):
        self.mo -= 1
        if(self.mo < 1):
            self.mo = 12
            self.ye -= 1
        self.changeDate()

    def NextButton(self):
        self.mo += 1
        if(self.mo > 12):
            self.mo = 1
            self.ye += 1
        self.changeDate()
    
    
    def changeDate(self):
        month = ['January','February','March','April','May','June','July','August','September','October','November','December']
        week = ["Sat","Sun","Mon","Tue","Wed","Thu","Fri"]
        limit = 0
        count = 1
        dLst,startDate,limit = self.calcalendar()
        self.dList = dLst
        startDate += 1
        #setMonth
        self.monthLabel.setText(str(month[self.mo-1])+" "+str(self.ye))
        
        for i in range(5):
            for j in range(10):
                lab = 'L'+str(i)+str(j)
                if(lab =='L42'):
                    break
                n = getattr(self,lab)
                if(j >= startDate or i > 0):
                    if(count <= limit):
                        n.setText(str(count))
                        count += 1
                    else:
                        n.setText(str(""))
                else:
                    n.setText(str(""))

    def calcalendar(self):
        dayNum =  calendar.monthrange(self.ye,self.mo)
        stdate = dayNum[0]
        limit = dayNum[1]
        d = calendar.monthcalendar(self.ye,self.mo)
        #return d -> tuple(Firstweekday,monthrange)
        return d,stdate,limit

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
        if (self.menu.currentText() == "Edit Profile") or(self.menu.currentText() == "week"):
            self.menu.setCurrentIndex(0)
            self.subWidget.setCurrentIndex(0)

    def backToProfilePage(self):
        self.subWidget.setCurrentIndex(1)

    def goToWeekPage(self,weekList):
        if (self.menu.currentText() == "Main Page"):
            self.menu.setCurrentIndex(4)
            self.subWidget.setCurrentIndex(5)
            self.WeekInit(weekList)

    def changePage(self):
        #Index 0 (main_page)
        #Index 1 (edit_profile)
        #Index 2 (setting)
        #Index 3 (change_password)
        #Index 4 (project_page)
        #Index 5 (week)
        if(self.menu.currentText() == "Main Page"):
            self.subWidget.setCurrentIndex(0)
        elif(self.menu.currentText() == "Edit Profile"):
            print(self.parent.user)
            self.subWidget.setCurrentIndex(1)
            self.loadProfile()
        elif (self.menu.currentText() == "Settings"):
            self.subWidget.setCurrentIndex(2)
        elif(self.menu.currentText() == "week"):
            self.subWidget.setCurrentIndex(5)
        

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

