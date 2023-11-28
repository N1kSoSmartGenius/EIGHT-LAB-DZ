import psycopg2
import sys
from PyQt5.QtWidgets import(QApplication, QWidget,QTabWidget, QAbstractScrollArea,QVBoxLayout, QHBoxLayout,QTableWidget, QGroupBox,QTableWidgetItem, QPushButton, QMessageBox)
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._connect_to_db()
        self.setWindowTitle("Sсhedule")
        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        self._create_shedule_tab()
        self._create_teachers_tab()
        self._create_subjects_tab()



    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="tg_bot", user="postgres", password="5591", host="localhost", port="5432")
        self.cursor = self.conn.cursor()



    def _create_subjects_tab(self):
        self.subjects_tab = QWidget()
        self.tabs.addTab(self.subjects_tab,"Subjects")
        self.subjects_tab_gbox = QGroupBox("Subjects")
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.subjects_tab_gbox)
        self._create_all_subjects_table()
        self.update_subjects_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_subjects_button)
        self.update_subjects_button.clicked.connect(self._update_subject)
        self.subjects_tab.setLayout(self.svbox)


    def _create_all_subjects_table(self):
        self.all_subjects_table = QTableWidget()
        self.all_subjects_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.all_subjects_table.setColumnCount(3)
        self.all_subjects_table.setHorizontalHeaderLabels(["Subject", "Join", "Delete"])
        self._update_subjects_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.all_subjects_table)
        self.subjects_tab_gbox.setLayout(self.mvbox)

    def _update_subjects_table(self):
        self.cursor.execute("SELECT * FROM subject")
        records = list(self.cursor.fetchall())
        self.all_subjects_table.setRowCount(len(records)+1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.all_subjects_table.setItem(i, 0,
            QTableWidgetItem(str(r[0])))
            self.all_subjects_table.setCellWidget(i, 1, joinButton)
            self.all_subjects_table.setCellWidget(i, 2, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i, data=r:self._change_subject(num,data))
            deleteButton.clicked.connect(lambda ch, data=r:self._delete_subject(data))
        addButton = QPushButton("Add")
        self.all_subjects_table.setCellWidget(i+1, 1, addButton)
        addButton.clicked.connect(lambda ch,num=i+1:self._insert_subject(num))      
        self.all_subjects_table.resizeRowsToContents()

    
    def _change_subject(self,rowNum,data):
        row = list()
        for i in range(self.all_subjects_table.columnCount()):
            try:
                row.append(self.all_subjects_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE subject SET name=%s WHERE name=%s",(row[0],data[0]))
            self.conn.commit()
            self._update_subjects_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")

    def _delete_subject(self,data):
        try:
            self.cursor.execute(f"DELETE FROM subject WHERE name='{data[0]}';")
            self.conn.commit()
            self._update_subjects_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")
    def _insert_subject(self,rowNum):
        row = list()
        for i in range(self.all_subjects_table.columnCount()):
            try:
                row.append(self.all_subjects_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:   
            self.cursor.execute(f"INSERT INTO subject(name) VALUES ('{row[0]}')")
            self.conn.commit()
            self._update_subjects_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")



   
    def _update_subject(self):
        self._update_subjects_table()



    def _create_teachers_tab(self):
        self.teachers_tab = QWidget()
        self.tabs.addTab(self.teachers_tab,"Teachers")
        self.teachers_gbox = QGroupBox("Teachers")
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.teachers_gbox)
        self._create_teachers_table()
        self.update_teachers_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_teachers_button)
        self.update_teachers_button.clicked.connect(self._update_teachers)
        self.teachers_tab.setLayout(self.svbox)


    def _create_teachers_table(self):
        self.teachers_table = QTableWidget()
        self.teachers_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.teachers_table.setColumnCount(4)
        self.teachers_table.setHorizontalHeaderLabels(["Teacher","Subject","Join","Delete"])
        self._update_teachers_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.teachers_table)
        self.teachers_gbox.setLayout(self.mvbox)



    def _update_teachers_table(self):
        self.cursor.execute("SELECT * FROM teacher")
        records = list(self.cursor.fetchall())
        self.teachers_table.setRowCount(len(records)+1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.teachers_table.setItem(i, 0, QTableWidgetItem(str(r[1])))
            self.teachers_table.setItem(i, 1, QTableWidgetItem(str(r[2])))
            self.teachers_table.setCellWidget(i, 2, joinButton)
            self.teachers_table.setCellWidget(i, 3, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i, data=r:self._change_teachers(num,data))
            deleteButton.clicked.connect(lambda ch,data=r:self._delete_teachers(data))
        addButton = QPushButton("Add")
        self.teachers_table.setCellWidget(i+1, 2, addButton)
        addButton.clicked.connect(lambda ch, num=i+1:self._insert_teacher(num))
        self.teachers_table.resizeRowsToContents()
    def _change_teachers(self,rowNum,data):
        row = list()
        for i in range(self.teachers_table.columnCount()):
            try:
                row.append(self.teachers_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE teacher SET full_name=%s, subject=%s WHERE full_name=%s and subject=%s",(row[0],row[1],data[1],data[2]))
            self.conn.commit()
            self._update_teachers_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")
    def _delete_teachers(self,data):
        try:
            self.cursor.execute(f"DELETE FROM teacher WHERE full_name='{data[1]}' and subject='{data[2]}'")
            self.conn.commit()
            self._update_teachers_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")
    def _insert_teacher(self,rowNum):
        row = list()
        for i in range(self.teachers_table.columnCount()):
            try:
                row.append(self.teachers_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f"INSERT INTO teacher(full_name,subject) VALUES ('{row[0]}','{row[1]}')")
            self.conn.commit()
            self._update_teachers_table()
        except:
             QMessageBox.about(self,"Error","Enter all fields")



    def _update_teachers(self):
        self._update_teachers_table()






    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Shedule")
        self.monday_gbox = QGroupBox("Monday")
        self.tuesday_gbox = QGroupBox("Tuesday")
        self.wednesday_gbox = QGroupBox("Wednesday")
        self.thursday_gbox = QGroupBox("Thursday")
        self.friday_gbox = QGroupBox("Friday")
        self.saturday_gbox = QGroupBox("Saturday")


        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.tabs_day = QTabWidget(self)
        self.shbox1.addWidget(self.tabs_day)

        self.monday_tab = QWidget(self)
        self.tabs_day.addTab(self.monday_tab,"Monday")
        self.tuesday_tab = QWidget(self)
        self.tabs_day.addTab(self.tuesday_tab,"Tuesday")
        self.wednesday_tab = QWidget(self)
        self.tabs_day.addTab(self.wednesday_tab,"Wednesday")
        self.thursday_tab = QWidget(self)
        self.tabs_day.addTab(self.thursday_tab,"Thursday")
        self.friday_tab = QWidget(self)
        self.tabs_day.addTab(self.friday_tab,"Friday")
        self.saturday_tab = QWidget(self)
        self.tabs_day.addTab(self.saturday_tab,"Saturday")
    
        self._create_monday_table()
        self._create_tuesday_table()
        self._create_wednesday_table()
        self._create_thursday_table()
        self._create_friday_table()
        self._create_saturday_table()


        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)
        self.shedule_tab.setLayout(self.svbox)



    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.monday_table.setColumnCount(6)
        self.monday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room_numb", "Teacher","Join","Delete"])
        self._update_monday_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_tab.setLayout(self.mvbox)


    def _update_monday_table(self):
        self.cursor.execute("SELECT * FROM timetable2 WHERE day='Monday'")
        records = list(self.cursor.fetchall())
        self.monday_table.setRowCount(len(records)+1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.monday_table.setItem(i, 0,
            QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 1,
            QTableWidgetItem(str(r[4])))
            self.monday_table.setItem(i, 2,
            QTableWidgetItem(str(r[3])))
            self.monday_table.setItem(i, 3,
            QTableWidgetItem(str(r[5])))
            self.monday_table.setCellWidget(i, 4, joinButton)
            self.monday_table.setCellWidget(i, 5, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i, data=r:self._change_monday_table(num,data))
            deleteButton.clicked.connect(lambda ch, data=r:self._delete_from_monday_table(data))
        addButton = QPushButton("Add")
        self.monday_table.setCellWidget(i+1,4,addButton)
        addButton.clicked.connect(lambda ch,num=i+1,data=r:self._insert_in_monday_table(num,data))
        self.monday_table.resizeRowsToContents()



    def _change_monday_table(self, rowNum,data):
        row = list()
        for i in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f"UPDATE timetable2 SET subject='{row[0]}', start_time='{row[2]}', room_numb='{row[1]}', teacher='{row[3]}' WHERE subject='{data[2]}'")
            self.conn.commit()
            self._update_monday_table()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")





    def _delete_from_monday_table(self,data):
        try:
            self.cursor.execute(f"DELETE FROM timetable2 WHERE subject='{data[2]}' and start_time='{data[3]}' and room_numb='{data[4]}' and teacher='{data[5]}'")
            self.conn.commit()
            self._update_monday_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")




    def _insert_in_monday_table(self,rowNum,data):
        row = list()
        for i in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f"INSERT INTO timetable2(day,subject,start_time,room_numb,teacher) VALUES ('{data[1]}','{row[0]}','{row[2]}','{row[1]}','{row[3]}')")
            self.conn.commit()
            self._update_monday_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")




    def _create_tuesday_table(self):
        self.tuesday_table = QTableWidget()
        self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tuesday_table.setColumnCount(6)
        self.tuesday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room_numb", "Teacher","Join","Delete"])
        self._update_tuesday_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.tuesday_table)
        self.tuesday_tab.setLayout(self.mvbox)


    def _update_tuesday_table(self):
        self.cursor.execute("SELECT * FROM timetable2 WHERE day='Tuesday'")
        records = list(self.cursor.fetchall())
        self.tuesday_table.setRowCount(len(records)+1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.tuesday_table.setItem(i, 0,
            QTableWidgetItem(str(r[2])))
            self.tuesday_table.setItem(i, 1,
            QTableWidgetItem(str(r[4])))
            self.tuesday_table.setItem(i, 2,
            QTableWidgetItem(str(r[3])))
            self.tuesday_table.setItem(i, 3,
            QTableWidgetItem(str(r[5])))
            self.tuesday_table.setCellWidget(i, 4, joinButton)
            self.tuesday_table.setCellWidget(i, 5, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i, data=r:self._change_tuesday_table(num,data))
            deleteButton.clicked.connect(lambda ch, data=r:self._delete_from_tuesday_table(data))
        addButton = QPushButton("Add")
        self.tuesday_table.setCellWidget(i+1,4,addButton)
        addButton.clicked.connect(lambda ch,num=i+1,data=r:self._insert_in_tuesday_table(num,data))
        self.tuesday_table.resizeRowsToContents()



    def _change_tuesday_table(self, rowNum,data):
        row = list()
        for i in range(self.tuesday_table.columnCount()):
            try:
                row.append(self.tuesday_table.item(rowNum, i).text())
            except:
                row.append(None)

        try:
            self.cursor.execute(f"UPDATE timetable2 SET subject='{row[0]}', start_time='{row[2]}', room_numb='{row[1]}', teacher='{row[3]}' WHERE subject='{data[2]}'")
            self.conn.commit()
            self._update_tuesday_table()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")





    def _delete_from_tuesday_table(self,data):
        try:
            self.cursor.execute(f"DELETE FROM timetable2 WHERE subject='{data[2]}' and start_time='{data[3]}' and room_numb='{data[4]}' and teacher='{data[5]}'")
            self.conn.commit()
            self._update_tuesday_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")


            

    def _insert_in_tuesday_table(self,rowNum,data):
        row = list()
        for i in range(self.tuesday_table.columnCount()):
            try:
                row.append(self.tuesday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f"INSERT INTO timetable2(day,subject,start_time,room_numb,teacher) VALUES ('{data[1]}','{row[0]}','{row[2]}','{row[1]}','{row[3]}')")
            self.conn.commit()
            self._update_tuesday_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")




    def _create_wednesday_table(self):
        self.wednesday_table = QTableWidget()
        self.wednesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.wednesday_table.setColumnCount(6)
        self.wednesday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room_numb", "Teacher","Join","Delete"])
        self._update_wednesday_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.wednesday_table)
        self.wednesday_tab.setLayout(self.mvbox)


    def _update_wednesday_table(self):
        self.cursor.execute("SELECT * FROM timetable2 WHERE day='Wednesday'")
        records = list(self.cursor.fetchall())
        self.wednesday_table.setRowCount(len(records)+1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.wednesday_table.setItem(i, 0,
            QTableWidgetItem(str(r[2])))
            self.wednesday_table.setItem(i, 1,
            QTableWidgetItem(str(r[4])))
            self.wednesday_table.setItem(i, 2,
            QTableWidgetItem(str(r[3])))
            self.wednesday_table.setItem(i, 3,
            QTableWidgetItem(str(r[5])))
            self.wednesday_table.setCellWidget(i, 4, joinButton)
            self.wednesday_table.setCellWidget(i, 5, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i, data=r:self._change_wednesday_table(num,data))
            deleteButton.clicked.connect(lambda ch, data=r:self._delete_from_wednesday_table(data))
        addButton = QPushButton("Add")
        self.wednesday_table.setCellWidget(i+1,4,addButton)
        addButton.clicked.connect(lambda ch,num=i+1,data=r:self._insert_in_wednesday_table(num,data))
        self.wednesday_table.resizeRowsToContents()



    def _change_wednesday_table(self, rowNum,data):
        row = list()
        for i in range(self.wednesday_table.columnCount()):
            try:
                row.append(self.wednesday_table.item(rowNum, i).text())
            except:
                row.append(None)

        try:
            self.cursor.execute(f"UPDATE timetable2 SET subject='{row[0]}', start_time='{row[2]}', room_numb='{row[1]}', teacher='{row[3]}' WHERE subject='{data[2]}'")
            self.conn.commit()
            self._update_wednesday_table()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")





    def _delete_from_wednesday_table(self,data):
        try:
            self.cursor.execute(f"DELETE FROM timetable2 WHERE subject='{data[2]}' and start_time='{data[3]}' and room_numb='{data[4]}' and teacher='{data[5]}'")
            self.conn.commit()
            self._update_wednesday_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")


            

    def _insert_in_wednesday_table(self,rowNum,data):
        row = list()
        for i in range(self.wednesday_table.columnCount()):
            try:
                row.append(self.wednesday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f"INSERT INTO timetable2(day,subject,start_time,room_numb,teacher) VALUES ('{data[1]}','{row[0]}','{row[2]}','{row[1]}','{row[3]}')")
            self.conn.commit()
            self._update_wednesday_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")
    







    def _create_thursday_table(self):
        self.thursday_table = QTableWidget()
        self.thursday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.thursday_table.setColumnCount(6)
        self.thursday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room_numb", "Teacher","Join","Delete"])
        self._update_thursday_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.thursday_table)
        self.thursday_tab.setLayout(self.mvbox)


    def _update_thursday_table(self):
        self.cursor.execute("SELECT * FROM timetable2 WHERE day='Thursday'")
        records = list(self.cursor.fetchall())
        self.thursday_table.setRowCount(len(records)+1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.thursday_table.setItem(i, 0,
            QTableWidgetItem(str(r[2])))
            self.thursday_table.setItem(i, 1,
            QTableWidgetItem(str(r[4])))
            self.thursday_table.setItem(i, 2,
            QTableWidgetItem(str(r[3])))
            self.thursday_table.setItem(i, 3,
            QTableWidgetItem(str(r[5])))
            self.thursday_table.setCellWidget(i, 4, joinButton)
            self.thursday_table.setCellWidget(i, 5, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i, data=r:self._change_thursday_table(num,data))
            deleteButton.clicked.connect(lambda ch, data=r:self._delete_from_thursday_table(data))
        addButton = QPushButton("Add")
        self.thursday_table.setCellWidget(i+1,4,addButton)
        addButton.clicked.connect(lambda ch,num=i+1,data=r:self._insert_in_thursday_table(num,data))
        self.thursday_table.resizeRowsToContents()



    def _change_thursday_table(self, rowNum,data):
        row = list()
        for i in range(self.thursday_table.columnCount()):
            try:
                row.append(self.thursday_table.item(rowNum, i).text())
            except:
                row.append(None)

        try:
            self.cursor.execute(f"UPDATE timetable2 SET subject='{row[0]}', start_time='{row[2]}', room_numb='{row[1]}', teacher='{row[3]}' WHERE subject='{data[2]}'")
            self.conn.commit()
            self._update_thursday_table()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")





    def _delete_from_thursday_table(self,data):
        try:
            self.cursor.execute(f"DELETE FROM timetable2 WHERE subject='{data[2]}' and start_time='{data[3]}' and room_numb='{data[4]}' and teacher='{data[5]}'")
            self.conn.commit()
            self._update_thursday_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")


            

    def _insert_in_thursday_table(self,rowNum,data):
        row = list()
        for i in range(self.thursday_table.columnCount()):
            try:
                row.append(self.thursday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f"INSERT INTO timetable2(day,subject,start_time,room_numb,teacher) VALUES ('{data[1]}','{row[0]}','{row[2]}','{row[1]}','{row[3]}')")
            self.conn.commit()
            self._update_thursday_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")


    def _create_friday_table(self):
        self.friday_table = QTableWidget()
        self.friday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.friday_table.setColumnCount(6)
        self.friday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room_numb", "Teacher","Join","Delete"])
        self._update_friday_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.friday_table)
        self.friday_tab.setLayout(self.mvbox)


    def _update_friday_table(self):
        self.cursor.execute("SELECT * FROM timetable2 WHERE day='Friday'")
        records = list(self.cursor.fetchall())
        self.friday_table.setRowCount(len(records)+1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.friday_table.setItem(i, 0,
            QTableWidgetItem(str(r[2])))
            self.friday_table.setItem(i, 1,
            QTableWidgetItem(str(r[4])))
            self.friday_table.setItem(i, 2,
            QTableWidgetItem(str(r[3])))
            self.friday_table.setItem(i, 3,
            QTableWidgetItem(str(r[5])))
            self.friday_table.setCellWidget(i, 4, joinButton)
            self.friday_table.setCellWidget(i, 5, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i, data=r:self._change_friday_table(num,data))
            deleteButton.clicked.connect(lambda ch, data=r:self._delete_from_friday_table(data))
        addButton = QPushButton("Add")
        self.friday_table.setCellWidget(i+1,4,addButton)
        addButton.clicked.connect(lambda ch,num=i+1,data=r:self._insert_in_friday_table(num,data))
        self.friday_table.resizeRowsToContents()



    def _change_friday_table(self, rowNum,data):
        row = list()
        for i in range(self.friday_table.columnCount()):
            try:
                row.append(self.friday_table.item(rowNum, i).text())
            except:
                row.append(None)

        try:
            self.cursor.execute(f"UPDATE timetable2 SET subject='{row[0]}', start_time='{row[2]}', room_numb='{row[1]}', teacher='{row[3]}' WHERE subject='{data[2]}'")
            self.conn.commit()
            self._update_friday_table()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")





    def _delete_from_friday_table(self,data):
        try:
            self.cursor.execute(f"DELETE FROM timetable2 WHERE subject='{data[2]}' and start_time='{data[3]}' and room_numb='{data[4]}' and teacher='{data[5]}'")
            self.conn.commit()
            self._update_friday_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")


            

    def _insert_in_friday_table(self,rowNum,data):
        row = list()
        for i in range(self.friday_table.columnCount()):
            try:
                row.append(self.friday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f"INSERT INTO timetable2(day,subject,start_time,room_numb,teacher) VALUES ('{data[1]}','{row[0]}','{row[2]}','{row[1]}','{row[3]}')")
            self.conn.commit()
            self._update_friday_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")



    def _create_saturday_table(self):
        self.saturday_table = QTableWidget()
        self.saturday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.saturday_table.setColumnCount(6)
        self.saturday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room_numb", "Teacher","Join","Delete"])
        self._update_saturday_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.saturday_table)
        self.saturday_tab.setLayout(self.mvbox)


    def _update_saturday_table(self):
        self.cursor.execute("SELECT * FROM timetable2 WHERE day='Saturday'")
        records = list(self.cursor.fetchall())
        self.saturday_table.setRowCount(len(records)+1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.saturday_table.setItem(i, 0,
            QTableWidgetItem(str(r[2])))
            self.saturday_table.setItem(i, 1,
            QTableWidgetItem(str(r[4])))
            self.saturday_table.setItem(i, 2,
            QTableWidgetItem(str(r[3])))
            self.saturday_table.setItem(i, 3,
            QTableWidgetItem(str(r[5])))
            self.saturday_table.setCellWidget(i, 4, joinButton)
            self.saturday_table.setCellWidget(i, 5, deleteButton)
            joinButton.clicked.connect(lambda ch, num=i, data=r:self._change_saturday_table(num,data))
            deleteButton.clicked.connect(lambda ch, data=r:self._delete_from_saturday_table(data))
        addButton = QPushButton("Add")
        self.saturday_table.setCellWidget(i+1,4,addButton)
        addButton.clicked.connect(lambda ch,num=i+1,data=r:self._insert_in_saturday_table(num,data))
        self.saturday_table.resizeRowsToContents()



    def _change_saturday_table(self, rowNum,data):
        row = list()
        for i in range(self.saturday_table.columnCount()):
            try:
                row.append(self.saturday_table.item(rowNum, i).text())
            except:
                row.append(None)

        try:
            self.cursor.execute(f"UPDATE timetable2 SET subject='{row[0]}', start_time='{row[2]}', room_numb='{row[1]}', teacher='{row[3]}' WHERE subject='{data[2]}'")
            self.conn.commit()
            self._update_saturday_table()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")





    def _delete_from_saturday_table(self,data):
        try:
            self.cursor.execute(f"DELETE FROM timetable2 WHERE subject='{data[2]}' and start_time='{data[3]}' and room_numb='{data[4]}' and teacher='{data[5]}'")
            self.conn.commit()
            self._update_saturday_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")


            

    def _insert_in_saturday_table(self,rowNum,data):
        row = list()
        for i in range(self.saturday_table.columnCount()):
            try:
                row.append(self.saturday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f"INSERT INTO timetable2(day,subject,start_time,room_numb,teacher) VALUES ('{data[1]}','{row[0]}','{row[2]}','{row[1]}','{row[3]}')")
            self.conn.commit()
            self._update_saturday_table()
        except:
            QMessageBox.about(self,"Error","Enter all fields")


    def _update_shedule(self):
        self._update_monday_table()
        self._update_tuesday_table()
        self._update_wednesday_table()
        self._update_thursday_table()
        self._update_saturday_table()
    






app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())



