### Setup Guide: Self-Hosted MySQL on Azure VM

---

#### Azure Resource Overview

- **Service:** Azure Virtual Machine (Ubuntu 22.04)  
- **Region:** `East US 2` (or your preferred region)  
- **VM Size:** B1ms or D2s (based on workload)  
- **Ports:** Ensure port `3306` is open for MySQL access

---

#### Deployment Steps

1. **Create Ubuntu VM**  
   - Go to Azure Portal → Create Resource → Virtual Machine  
   - Choose Ubuntu 22.04, region, and VM size  
   - Set admin credentials and allow SSH access

2. **Install MySQL Server**
   ```bash
   sudo apt update
   sudo apt install mysql-server mysql-client
   sudo mysql
   ```

3. **Configure MySQL for External Access**
   ```bash
   sudo apt install nano
   sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
   ```
   In the bind address, change to:
   ```
   bind-address = 0.0.0.0
   ```
   - Save and exit:
     ```
     Ctrl O (to save)
     Ctrl X (to exit)
     ```
     
   - Restart MySQL:
     ```bash
     sudo systemctl restart mysql
     ```


4. **Create Database and User**
   ```sql
   CREATE DATABASE class_db_netid;
   CREATE USER 'class_user'@'%' IDENTIFIED BY 'change_me';
   GRANT ALL PRIVILEGES ON class_db_netid.* TO 'class_user'@'%';
   ```

5. **Open Port 3306 in Network Security Group**  
   - Go to VM → Networking → Add inbound rule for TCP port 3306

---

#### Python Integration

##### 1. Install Dependencies
```bash
pip install pymysql sqlalchemy python-dotenv
```

##### 2. Create `.env` File
```env
VM_DB_HOST=your-vm-public-ip
VM_DB_PORT=3306
VM_DB_USER=class_user
VM_DB_PASS=change_me
VM_DB_NAME=class_db_netid
```

##### 3. Connect Using SQLAlchemy
```python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

db_url = (
    f"mysql+pymysql://{os.getenv('VM_DB_USER')}:{os.getenv('VM_DB_PASS')}"
    f"@{os.getenv('VM_DB_HOST')}:{os.getenv('VM_DB_PORT')}/{os.getenv('VM_DB_NAME')}"
)

engine = create_engine(db_url, pool_pre_ping=True)

with engine.connect() as conn:
    result = conn.execute("SELECT COUNT(*) FROM your_table")
    print(result.scalar())
```

---

#### Security Notes

- Never commit `.env` files to Git  
- Use strong passwords and limit access by IP  

---

#### Verification

- Confirm MySQL is running: `systemctl status mysql`  
- Connect via Python and verify query output  
- Check firewall and port accessibility

---
```
