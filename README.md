# Sarhad Express HR System
## Company: Sarhad Express Land Transport LLC, Dubai UAE
## Code: 574758

---

## 🚀 DEPLOYMENT GUIDE

### Step 1 — Google Sheets Setup

Create a new Google Sheet with these 8 tabs (exact names):

| Tab Name | Columns |
|----------|---------|
| **Employees** | EmpID, Name, Role, Department, Designation, Phone, Email, Nationality, JoinDate, Salary, StaffType, Password, CreatedAt |
| **Attendance** | EmpID, Name, Date, ClockIn, ClockOut, Hours, Status |
| **Leaves** | LeaveID, EmpID, Name, LeaveType, FromDate, ToDate, Days, Reason, Status, ApprovedBy, CreatedAt |
| **Documents** | DocID, EmpID, EmpName, DocType, DocNumber, IssueDate, ExpiryDate, Notes, CreatedAt |
| **Vehicles** | VehicleID, Plate, Make, Model, Year, Type, Color, Chassis, Engine, InsuranceExpiry, RegistrationExpiry, FitnessExpiry, AssignedDriver, Status, CreatedAt |
| **Tasks** | TaskID, Title, Description, AssignedTo, AssignedName, TaskType, Priority, Deadline, Status, CompletionNote, AssignedBy, CreatedAt |
| **Payroll** | PayrollID, EmpID, EmpName, Month, Basic, Allowance, Overtime, Deduction, NetSalary, PaymentMethod, Status, CreatedAt |
| **Config** | Key, Value |

### Add First Admin Row in Employees tab:
```
SE001 | Admin User | Admin | HR | HR Manager | +971501234567 | admin@sarhad.ae | Pakistani | 2024-01-01 | 5000 | Office | admin123 | 2024-01-01
```

---

### Step 2 — Google Service Account

1. Go to https://console.cloud.google.com
2. Create new project: **sarhad-hr**
3. Enable APIs:
   - Google Sheets API
   - Google Drive API
4. Create Service Account → Download JSON key
5. Share your Google Sheet with the service account email (Editor access)

---

### Step 3 — GitHub

```bash
cd sarhad-hr
git init
git add .
git commit -m "Sarhad Express HR System v1.0"
git remote add origin https://github.com/YOUR_USERNAME/sarhad-hr.git
git push -u origin main
```

---

### Step 4 — Render Deployment

1. Go to https://render.com → New Web Service
2. Connect GitHub repo
3. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
4. Environment Variables:
   ```
   SECRET_KEY = sarhad-express-574758-secret
   SHEET_ID = (your Google Sheet ID from URL)
   GOOGLE_CREDS_JSON = (paste entire contents of credentials JSON file)
   ```
5. Deploy!

---

### Step 5 — Custom Domain (Optional)

In Render → Settings → Custom Domains:
- Add your domain e.g. `hr.sarhadexpress.ae`
- Add CNAME record in your DNS pointing to Render URL

---

## 📋 MODULES INCLUDED

| Module | Features |
|--------|----------|
| ✅ Login | Employee ID + Password, 3 languages |
| ✅ Dashboard | Stats, quick clock in/out |
| ✅ Employees | Add/view employees, search |
| ✅ Attendance | Clock In/Out with timestamp |
| ✅ Leave | Apply, approve/reject |
| ✅ Documents | Visa/Passport/EID tracker with expiry alerts |
| ✅ Vehicles | Fleet management, doc expiry |
| ✅ Tasks | Assign & track work |
| ✅ Payroll | Salary calculation, WPS ready |

## 🌍 LANGUAGES
- English (LTR)
- Arabic عربي (RTL)
- Urdu اردو (RTL)

## 👥 ROLES
- **Admin** — Full access, approve leaves, add employees, assign tasks
- **Employee** — Own attendance, own leave, own tasks, own payslip

## 🔔 DOCUMENT ALERTS
- 🟢 Valid — 90+ days
- 🟡 Expiring — 60 days
- 🔴 Critical — 30 days
- ⚫ Expired

---

## Health Check
```
curl https://YOUR-APP.onrender.com/health
```
