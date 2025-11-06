### Setup Guide: Azure Managed MySQL (Flexible Server)

---

#### Azure Resource Overview

- **Service:** Azure Database for MySQL — Flexible Server  
- **Region:** `West US 3` (or your preferred region)  
- **Tier:** Basic or General Purpose (based on workload)

---

#### Deployment Steps

1. **Create MySQL Flexible Server**  
   - Go to Azure Portal → Create Resource → MySQL Flexible Server  
   - Choose region, resource group, and server name  
   - Set admin username and password  
   - Select public access and allow your IP  
   - Disable SSL enforcement *(I forgot to disable the SSL at first and keeps giving me error in connection)*

2. **Configure Firewall Rules**  
   - Add `0.0.0.0` IP address

3. **Create Database**  
   - Use Azure Portal or connect via MySQL CLI:  
     ```bash
     mysql -h <server-name>.mysql.database.azure.com -u <admin>@<server-name> -p
     CREATE DATABASE class_db_netid;
     ```

---

### Python Integration

##### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

##### 2. Create `.env` File
```env
MAN_DB_HOST=your-managed-endpoint
MAN_DB_PORT=3306
MAN_DB_USER=class_user
MAN_DB_PASS=change_me
MAN_DB_NAME=class_db_netid
```

##### 3. Connect Using SQLAlchemy
```python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

db_url = (
    f"mysql+pymysql://{os.getenv('MAN_DB_USER')}:{os.getenv('MAN_DB_PASS')}"
    f"@{os.getenv('MAN_DB_HOST')}:{os.getenv('MAN_DB_PORT')}/{os.getenv('MAN_DB_NAME')}"
)

engine = create_engine(db_url, pool_pre_ping=True)

with engine.connect() as conn:
    result = conn.execute("SELECT COUNT(*) FROM your_table")
    print(result.scalar())
```

---

#### Security Notes

- Never commit `.env` files to Git  

---

#### Verification

- Confirm connection via Python script  
- Check query logs in Azure Portal  
- Monitor metrics and alerts for uptime

---
