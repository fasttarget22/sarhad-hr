import os
os.environ['SHEET_ID'] = 'demo_mode'
os.environ['SECRET_KEY'] = 'sarhad-express-574758'

from unittest.mock import MagicMock, patch

DB = {
    'Employees': [
        {'EmpID':'SE000','Name':'Admin User','Role':'Admin','Department':'HR','Designation':'HR Manager','Phone':'+971501234567','Email':'admin@sarhad.ae','Nationality':'Pakistani','JoinDate':'2024-01-01','Salary':5000,'StaffType':'Office','Password':'admin123','CreatedAt':'2024-01-01'},
        {'EmpID':'SE001','Name':'AMNA ALI SAEED SALEM ALKAABI','Role':'Employee','Department':'Admin','Designation':'Relations Officer','Phone':'+971502000001','Email':'amna@sarhad.ae','Nationality':'Emirati','JoinDate':'2024-01-01','Salary':0,'StaffType':'WFH','Password':'1234','CreatedAt':'2024-01-01'},
        {'EmpID':'SE002','Name':'ALANOOD MALALLA ALI GHAREEB ALHOSANI','Role':'Employee','Department':'Admin','Designation':'Follow-up Officer','Phone':'+971502000002','Email':'alanood@sarhad.ae','Nationality':'Emirati','JoinDate':'2024-01-01','Salary':0,'StaffType':'WFH','Password':'1234','CreatedAt':'2024-01-01'},
        {'EmpID':'SE003','Name':'FATIMA RASHED SAIF NASSER ALNUAIMI','Role':'Employee','Department':'Admin','Designation':'Sales Officer','Phone':'+971502000003','Email':'fatima@sarhad.ae','Nationality':'Emirati','JoinDate':'2024-01-01','Salary':0,'StaffType':'WFH','Password':'1234','CreatedAt':'2024-01-01'},
        {'EmpID':'SE004','Name':'KHALID MOHAMMAD SADEQ AMAN AL ALI','Role':'Employee','Department':'IT','Designation':'IT Operations Technician','Phone':'+971502000004','Email':'khalid@sarhad.ae','Nationality':'Emirati','JoinDate':'2024-01-01','Salary':0,'StaffType':'WFH','Password':'1234','CreatedAt':'2024-01-01'},
        {'EmpID':'SE005','Name':'Muhammad Asif Khan','Role':'Employee','Department':'Transport','Designation':'Senior Driver','Phone':'+971503000001','Email':'asif@sarhad.ae','Nationality':'Pakistani','JoinDate':'2023-06-01','Salary':2500,'StaffType':'Driver','Password':'1234','CreatedAt':'2023-06-01'},
    ],
    'Attendance': [],
    'Leaves': [
        {'LeaveID':'L0001','EmpID':'SE005','Name':'Muhammad Asif Khan','LeaveType':'Annual Leave','FromDate':'2026-07-10','ToDate':'2026-07-20','Days':10,'Reason':'Family visit','Status':'Approved','ApprovedBy':'Admin','CreatedAt':'2026-06-25'},
        {'LeaveID':'L0002','EmpID':'SE003','Name':'FATIMA RASHED SAIF NASSER ALNUAIMI','LeaveType':'Sick Leave','FromDate':'2026-07-05','ToDate':'2026-07-06','Days':2,'Reason':'Medical','Status':'Pending','ApprovedBy':'','CreatedAt':'2026-06-28'},
    ],
    'Documents': [
        {'DocID':'D0001','EmpID':'SE001','EmpName':'AMNA ALI SAEED SALEM ALKAABI','DocType':'Labour Card','DocNumber':'127755855','IssueDate':'2024-06-22','ExpiryDate':'2027-06-22','Notes':'Dubai Work Permit','CreatedAt':'2024-06-22'},
        {'DocID':'D0002','EmpID':'SE002','EmpName':'ALANOOD MALALLA ALI GHAREEB ALHOSANI','DocType':'Labour Card','DocNumber':'115192940','IssueDate':'2023-06-10','ExpiryDate':'2026-06-10','Notes':'EXPIRED','CreatedAt':'2023-06-10'},
        {'DocID':'D0003','EmpID':'SE003','EmpName':'FATIMA RASHED SAIF NASSER ALNUAIMI','DocType':'Labour Card','DocNumber':'127756779','IssueDate':'2024-06-22','ExpiryDate':'2027-06-22','Notes':'Dubai Work Permit','CreatedAt':'2024-06-22'},
        {'DocID':'D0004','EmpID':'SE004','EmpName':'KHALID MOHAMMAD SADEQ AMAN AL ALI','DocType':'Labour Card','DocNumber':'123444255','IssueDate':'2024-01-02','ExpiryDate':'2027-01-02','Notes':'Dubai Work Permit','CreatedAt':'2024-01-02'},
        {'DocID':'D0005','EmpID':'SE005','EmpName':'Muhammad Asif Khan','DocType':'Passport','DocNumber':'AK1234567','IssueDate':'2020-08-15','ExpiryDate':'2026-08-15','Notes':'','CreatedAt':'2023-06-01'},
    ],
    'Vehicles': [
        {'VehicleID':'V001','Plate':'Dubai A 12345','Make':'Toyota','Model':'Hiace','Year':'2021','Type':'Van','Color':'White','Chassis':'JTFRS22P1M0123456','Engine':'2TR-FE-789','InsuranceExpiry':'2026-09-15','RegistrationExpiry':'2026-11-01','FitnessExpiry':'2026-08-20','AssignedDriver':'Muhammad Asif Khan','Status':'Active','CreatedAt':'2021-01-01'},
        {'VehicleID':'V002','Plate':'Dubai B 67890','Make':'Isuzu','Model':'NQR','Year':'2020','Type':'Truck','Color':'White','Chassis':'JAANQR75L07123456','Engine':'4HK1-789','InsuranceExpiry':'2025-12-01','RegistrationExpiry':'2026-03-15','FitnessExpiry':'2025-11-30','AssignedDriver':'Unassigned','Status':'Active','CreatedAt':'2020-01-01'},
    ],
    'Tasks': [
        {'TaskID':'T0001','Title':'Follow up with clients','Description':'Call 5 pending clients today','AssignedTo':'SE002','AssignedName':'ALANOOD MALALLA ALI GHAREEB ALHOSANI','TaskType':'Remote','Priority':'Urgent','Deadline':'2026-07-02','Status':'Pending','CompletionNote':'','AssignedBy':'Admin User','CreatedAt':'2026-06-30'},
        {'TaskID':'T0002','Title':'Dubai-Sharjah Delivery','Description':'Deliver cargo to warehouse','AssignedTo':'SE005','AssignedName':'Muhammad Asif Khan','TaskType':'Trip/Delivery','Priority':'High','Deadline':'2026-07-01','Status':'Completed','CompletionNote':'Delivered at 14:30','AssignedBy':'Admin User','CreatedAt':'2026-06-30'},
    ],
    'Payroll': [
        {'PayrollID':'P0001','EmpID':'SE005','EmpName':'Muhammad Asif Khan','Month':'2026-05','Basic':2500,'Allowance':500,'Overtime':300,'Deduction':0,'NetSalary':3300,'PaymentMethod':'WPS','Status':'Paid','CreatedAt':'2026-06-01'},
    ],
    'Config': []
}

class DemoWorksheet:
    def __init__(self, name):
        self.name = name
    def get_all_records(self):
        return list(DB.get(self.name, []))
    def append_row(self, row):
        cols_map = {
            'Employees': ['EmpID','Name','Role','Department','Designation','Phone','Email','Nationality','JoinDate','Salary','StaffType','Password','CreatedAt'],
            'Attendance': ['EmpID','Name','Date','ClockIn','ClockOut','Hours','Status'],
            'Leaves': ['LeaveID','EmpID','Name','LeaveType','FromDate','ToDate','Days','Reason','Status','ApprovedBy','CreatedAt'],
            'Documents': ['DocID','EmpID','EmpName','DocType','DocNumber','IssueDate','ExpiryDate','Notes','CreatedAt'],
            'Vehicles': ['VehicleID','Plate','Make','Model','Year','Type','Color','Chassis','Engine','InsuranceExpiry','RegistrationExpiry','FitnessExpiry','AssignedDriver','Status','CreatedAt'],
            'Tasks': ['TaskID','Title','Description','AssignedTo','AssignedName','TaskType','Priority','Deadline','Status','CompletionNote','AssignedBy','CreatedAt'],
            'Payroll': ['PayrollID','EmpID','EmpName','Month','Basic','Allowance','Overtime','Deduction','NetSalary','PaymentMethod','Status','CreatedAt'],
        }
        cols = cols_map.get(self.name, [])
        record = {c: (row[i] if i < len(row) else '') for i, c in enumerate(cols)}
        DB.setdefault(self.name, []).append(record)
    def update_cell(self, row, col, value):
        cols_map = {
            'Attendance': ['EmpID','Name','Date','ClockIn','ClockOut','Hours','Status'],
            'Leaves': ['LeaveID','EmpID','Name','LeaveType','FromDate','ToDate','Days','Reason','Status','ApprovedBy','CreatedAt'],
            'Tasks': ['TaskID','Title','Description','AssignedTo','AssignedName','TaskType','Priority','Deadline','Status','CompletionNote','AssignedBy','CreatedAt'],
        }
        cols = cols_map.get(self.name, [])
        idx = row - 2
        if 0 <= idx < len(DB[self.name]) and 0 < col <= len(cols):
            DB[self.name][idx][cols[col-1]] = value

class DemoSheet:
    def worksheet(self, name):
        return DemoWorksheet(name)

class DemoClient:
    def open_by_key(self, key):
        return DemoSheet()

with patch('gspread.authorize', return_value=DemoClient()), \
     patch('google.oauth2.service_account.Credentials.from_service_account_file', return_value=MagicMock()), \
     patch('google.oauth2.service_account.Credentials.from_service_account_info', return_value=MagicMock()):
    from app import app
    print('')
    print('=' * 50)
    print('  SARHAD EXPRESS HR - DEMO MODE')
    print('=' * 50)
    print('  Open browser: http://localhost:5000')
    print('  Admin login:  SE000 / admin123')
    print('  Staff login:  SE001 / 1234')
    print('=' * 50)
    print('')
    app.run(debug=False, port=5000, host='0.0.0.0')
