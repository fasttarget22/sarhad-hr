from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date
import json
import os
import hashlib

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'sarhad-express-2024')

# Google Sheets Setup
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def get_sheet():
    creds_json = os.environ.get('GOOGLE_CREDS_JSON')
    if creds_json:
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    else:
        creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet_id = os.environ.get('SHEET_ID', '')
    return client.open_by_key(sheet_id)

def get_ws(name):
    try:
        return get_sheet().worksheet(name)
    except:
        return None

# ── Auth ──────────────────────────────────────────────
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    emp_id = data.get('emp_id','').strip()
    password = data.get('password','').strip()
    ws = get_ws('Employees')
    if not ws:
        return jsonify({'success': False, 'msg': 'Sheet error'})
    rows = ws.get_all_records()
    for r in rows:
        if str(r.get('EmpID','')) == emp_id:
            stored = str(r.get('Password',''))
            if stored == password or stored == hashlib.md5(password.encode()).hexdigest():
                session['user'] = {
                    'id': emp_id,
                    'name': r.get('Name',''),
                    'role': r.get('Role','Employee'),
                    'dept': r.get('Department','')
                }
                return jsonify({'success': True, 'role': r.get('Role','Employee')})
    return jsonify({'success': False, 'msg': 'Invalid credentials'})

@app.route('/api/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

# ── Pages ─────────────────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=session['user'])

@app.route('/employees')
@login_required
def employees_page():
    return render_template('employees.html', user=session['user'])

@app.route('/attendance')
@login_required
def attendance_page():
    return render_template('attendance.html', user=session['user'])

@app.route('/leaves')
@login_required
def leaves_page():
    return render_template('leaves.html', user=session['user'])

@app.route('/documents')
@login_required
def documents_page():
    return render_template('documents.html', user=session['user'])

@app.route('/vehicles')
@login_required
def vehicles_page():
    return render_template('vehicles.html', user=session['user'])

@app.route('/tasks')
@login_required
def tasks_page():
    return render_template('tasks.html', user=session['user'])

@app.route('/payroll')
@login_required
def payroll_page():
    return render_template('payroll.html', user=session['user'])

# ── API: Employees ────────────────────────────────────
@app.route('/api/employees', methods=['GET'])
@login_required
def get_employees():
    ws = get_ws('Employees')
    if not ws:
        return jsonify([])
    rows = ws.get_all_records()
    safe = [{k: v for k, v in r.items() if k != 'Password'} for r in rows]
    return jsonify(safe)

@app.route('/api/employees', methods=['POST'])
@login_required
def add_employee():
    if session['user']['role'] != 'Admin':
        return jsonify({'success': False, 'msg': 'Unauthorized'})
    data = request.json
    ws = get_ws('Employees')
    rows = ws.get_all_records()
    new_id = f"SE{str(len(rows)+1).zfill(3)}"
    ws.append_row([
        new_id, data.get('name',''), data.get('role','Employee'),
        data.get('department',''), data.get('designation',''),
        data.get('phone',''), data.get('email',''),
        data.get('nationality',''), data.get('join_date',''),
        data.get('salary','0'), data.get('staff_type','Office'),
        data.get('password','1234'), datetime.now().strftime('%Y-%m-%d')
    ])
    return jsonify({'success': True, 'id': new_id})

# ── API: Attendance ───────────────────────────────────
@app.route('/api/attendance/clockin', methods=['POST'])
@login_required
def clock_in():
    ws = get_ws('Attendance')
    today = date.today().isoformat()
    now = datetime.now().strftime('%H:%M:%S')
    emp_id = session['user']['id']
    rows = ws.get_all_records()
    for r in rows:
        if str(r.get('EmpID')) == emp_id and r.get('Date') == today and r.get('ClockIn'):
            return jsonify({'success': False, 'msg': 'Already clocked in today'})
    ws.append_row([emp_id, session['user']['name'], today, now, '', '', 'Present'])
    return jsonify({'success': True, 'time': now})

@app.route('/api/attendance/clockout', methods=['POST'])
@login_required
def clock_out():
    ws = get_ws('Attendance')
    today = date.today().isoformat()
    now = datetime.now().strftime('%H:%M:%S')
    emp_id = session['user']['id']
    rows = ws.get_all_records()
    for i, r in enumerate(rows):
        if str(r.get('EmpID')) == emp_id and r.get('Date') == today and r.get('ClockIn') and not r.get('ClockOut'):
            # calculate hours
            try:
                ci = datetime.strptime(r['ClockIn'], '%H:%M:%S')
                co = datetime.strptime(now, '%H:%M:%S')
                hrs = round((co - ci).seconds / 3600, 2)
            except:
                hrs = 0
            row_num = i + 2
            ws.update_cell(row_num, 5, now)
            ws.update_cell(row_num, 6, str(hrs))
            return jsonify({'success': True, 'time': now, 'hours': hrs})
    return jsonify({'success': False, 'msg': 'No active clock-in found'})

@app.route('/api/attendance', methods=['GET'])
@login_required
def get_attendance():
    ws = get_ws('Attendance')
    rows = ws.get_all_records()
    emp_id = session['user']['id']
    role = session['user']['role']
    if role == 'Admin':
        return jsonify(rows)
    return jsonify([r for r in rows if str(r.get('EmpID')) == emp_id])

# ── API: Leaves ───────────────────────────────────────
@app.route('/api/leaves', methods=['GET'])
@login_required
def get_leaves():
    ws = get_ws('Leaves')
    rows = ws.get_all_records()
    emp_id = session['user']['id']
    role = session['user']['role']
    if role == 'Admin':
        return jsonify(rows)
    return jsonify([r for r in rows if str(r.get('EmpID')) == emp_id])

@app.route('/api/leaves', methods=['POST'])
@login_required
def apply_leave():
    data = request.json
    ws = get_ws('Leaves')
    rows = ws.get_all_records()
    lid = f"L{str(len(rows)+1).zfill(4)}"
    ws.append_row([
        lid, session['user']['id'], session['user']['name'],
        data.get('type','Annual'), data.get('from_date',''),
        data.get('to_date',''), data.get('days',1),
        data.get('reason',''), 'Pending', '',
        datetime.now().strftime('%Y-%m-%d %H:%M')
    ])
    return jsonify({'success': True, 'id': lid})

@app.route('/api/leaves/<lid>/approve', methods=['POST'])
@login_required
def approve_leave(lid):
    if session['user']['role'] != 'Admin':
        return jsonify({'success': False})
    ws = get_ws('Leaves')
    rows = ws.get_all_records()
    data = request.json
    for i, r in enumerate(rows):
        if r.get('LeaveID') == lid:
            ws.update_cell(i+2, 9, data.get('status', 'Approved'))
            ws.update_cell(i+2, 10, session['user']['name'])
            return jsonify({'success': True})
    return jsonify({'success': False})

# ── API: Documents ────────────────────────────────────
@app.route('/api/documents', methods=['GET'])
@login_required
def get_documents():
    ws = get_ws('Documents')
    rows = ws.get_all_records()
    today = date.today()
    result = []
    for r in rows:
        expiry_str = r.get('ExpiryDate', '')
        status = 'Valid'
        days_left = None
        if expiry_str:
            try:
                exp = date.fromisoformat(expiry_str)
                days_left = (exp - today).days
                if days_left < 0:
                    status = 'Expired'
                elif days_left <= 30:
                    status = 'Critical'
                elif days_left <= 60:
                    status = 'Expiring'
            except:
                pass
        r['Status'] = status
        r['DaysLeft'] = days_left
        result.append(r)
    emp_id = session['user']['id']
    role = session['user']['role']
    if role == 'Admin':
        return jsonify(result)
    return jsonify([r for r in result if str(r.get('EmpID')) == emp_id])

@app.route('/api/documents', methods=['POST'])
@login_required
def add_document():
    data = request.json
    ws = get_ws('Documents')
    rows = ws.get_all_records()
    did = f"D{str(len(rows)+1).zfill(4)}"
    emp_id = data.get('emp_id', session['user']['id'])
    ws.append_row([
        did, emp_id, data.get('emp_name',''),
        data.get('doc_type',''), data.get('doc_number',''),
        data.get('issue_date',''), data.get('expiry_date',''),
        data.get('notes',''), datetime.now().strftime('%Y-%m-%d')
    ])
    return jsonify({'success': True, 'id': did})

# ── API: Vehicles ─────────────────────────────────────
@app.route('/api/vehicles', methods=['GET'])
@login_required
def get_vehicles():
    ws = get_ws('Vehicles')
    if not ws:
        return jsonify([])
    rows = ws.get_all_records()
    today = date.today()
    for r in rows:
        for field in ['InsuranceExpiry', 'RegistrationExpiry', 'FitnessExpiry']:
            exp_str = r.get(field, '')
            if exp_str:
                try:
                    exp = date.fromisoformat(exp_str)
                    days = (exp - today).days
                    r[field + '_Days'] = days
                    r[field + '_Status'] = 'Expired' if days < 0 else 'Critical' if days <= 30 else 'Expiring' if days <= 60 else 'Valid'
                except:
                    pass
    return jsonify(rows)

@app.route('/api/vehicles', methods=['POST'])
@login_required
def add_vehicle():
    if session['user']['role'] != 'Admin':
        return jsonify({'success': False})
    data = request.json
    ws = get_ws('Vehicles')
    rows = ws.get_all_records()
    vid = f"V{str(len(rows)+1).zfill(3)}"
    ws.append_row([
        vid, data.get('plate',''), data.get('make',''),
        data.get('model',''), data.get('year',''),
        data.get('type',''), data.get('color',''),
        data.get('chassis',''), data.get('engine',''),
        data.get('insurance_expiry',''), data.get('reg_expiry',''),
        data.get('fitness_expiry',''), data.get('assigned_driver',''),
        data.get('status','Active'), datetime.now().strftime('%Y-%m-%d')
    ])
    return jsonify({'success': True, 'id': vid})

# ── API: Tasks ────────────────────────────────────────
@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    ws = get_ws('Tasks')
    rows = ws.get_all_records()
    emp_id = session['user']['id']
    role = session['user']['role']
    if role == 'Admin':
        return jsonify(rows)
    return jsonify([r for r in rows if str(r.get('AssignedTo')) == emp_id])

@app.route('/api/tasks', methods=['POST'])
@login_required
def add_task():
    if session['user']['role'] != 'Admin':
        return jsonify({'success': False})
    data = request.json
    ws = get_ws('Tasks')
    rows = ws.get_all_records()
    tid = f"T{str(len(rows)+1).zfill(4)}"
    ws.append_row([
        tid, data.get('title',''), data.get('description',''),
        data.get('assigned_to',''), data.get('assigned_name',''),
        data.get('task_type','Office'), data.get('priority','Medium'),
        data.get('deadline',''), 'Pending', '',
        session['user']['name'], datetime.now().strftime('%Y-%m-%d %H:%M')
    ])
    return jsonify({'success': True, 'id': tid})

@app.route('/api/tasks/<tid>/update', methods=['POST'])
@login_required
def update_task(tid):
    ws = get_ws('Tasks')
    rows = ws.get_all_records()
    data = request.json
    for i, r in enumerate(rows):
        if r.get('TaskID') == tid:
            ws.update_cell(i+2, 9, data.get('status','In Progress'))
            ws.update_cell(i+2, 10, data.get('note',''))
            return jsonify({'success': True})
    return jsonify({'success': False})

# ── API: Payroll ──────────────────────────────────────
@app.route('/api/payroll', methods=['GET'])
@login_required
def get_payroll():
    ws = get_ws('Payroll')
    rows = ws.get_all_records()
    emp_id = session['user']['id']
    role = session['user']['role']
    if role == 'Admin':
        return jsonify(rows)
    return jsonify([r for r in rows if str(r.get('EmpID')) == emp_id])

@app.route('/api/payroll', methods=['POST'])
@login_required
def add_payroll():
    if session['user']['role'] != 'Admin':
        return jsonify({'success': False})
    data = request.json
    ws = get_ws('Payroll')
    rows = ws.get_all_records()
    pid = f"P{str(len(rows)+1).zfill(4)}"
    basic = float(data.get('basic', 0))
    allowance = float(data.get('allowance', 0))
    deduction = float(data.get('deduction', 0))
    overtime = float(data.get('overtime', 0))
    net = basic + allowance + overtime - deduction
    ws.append_row([
        pid, data.get('emp_id',''), data.get('emp_name',''),
        data.get('month',''), basic, allowance,
        overtime, deduction, net,
        data.get('payment_method','Bank'), data.get('status','Pending'),
        datetime.now().strftime('%Y-%m-%d')
    ])
    return jsonify({'success': True, 'id': pid, 'net': net})

# ── API: Dashboard Stats ──────────────────────────────
@app.route('/api/stats')
@login_required
def get_stats():
    try:
        emp_ws = get_ws('Employees')
        att_ws = get_ws('Attendance')
        doc_ws = get_ws('Documents')
        leave_ws = get_ws('Leaves')
        task_ws = get_ws('Tasks')
        today = date.today().isoformat()

        emps = emp_ws.get_all_records() if emp_ws else []
        atts = att_ws.get_all_records() if att_ws else []
        docs = doc_ws.get_all_records() if doc_ws else []
        leaves = leave_ws.get_all_records() if leave_ws else []
        tasks = task_ws.get_all_records() if task_ws else []

        today_att = [a for a in atts if a.get('Date') == today]
        pending_leaves = [l for l in leaves if l.get('Status') == 'Pending']
        pending_tasks = [t for t in tasks if t.get('Status') == 'Pending']

        expiring_docs = 0
        for d in docs:
            try:
                exp = date.fromisoformat(d.get('ExpiryDate',''))
                days = (exp - date.today()).days
                if 0 <= days <= 60:
                    expiring_docs += 1
            except:
                pass

        return jsonify({
            'total_employees': len(emps),
            'today_present': len(today_att),
            'pending_leaves': len(pending_leaves),
            'expiring_docs': expiring_docs,
            'pending_tasks': len(pending_tasks)
        })
    except Exception as e:
        return jsonify({'error': str(e), 'total_employees': 0, 'today_present': 0,
                        'pending_leaves': 0, 'expiring_docs': 0, 'pending_tasks': 0})

@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
