# Project Setup: Azure MySQL + VM Deployment

## Cloud Provider and Regions

- **Cloud Chosen:** Microsoft Azure
- **Resources Used:**
  - **Azure Database for MySQL** — Region: `East US`
  - **Azure Virtual Machine (Ubuntu 22.04)** — Region: `East US 2`



### Python + MySQL on Azure
This guide outlines two options for connecting Python scripts to MySQL on Azure.

### Option 1: Azure-Managed MySQL (Flexible Server)
#### Steps to Reproduce
- Create a MySQL Flexible Server in Azure (`East US`)
  - Set admin credentials
  - Allow your IP in firewall settings
- Install Python dependencies locally:
  ```bash
  pip install mysql-connector-python python-dotenv
  ```
- Create a `.env` file with database credentials:
  ```env
  VM_DB_HOST=your-mysql-hostname
  VM_DB_PORT=3306
  VM_DB_USER=your-username
  VM_DB_PASS=your-password
  VM_DB_NAME=your-database-name
  ```
- Load environment variables in Python:
  ```python
  from dotenv import load_dotenv
  load_dotenv()
  ```
- Connect using SQLAlchemy
- Log output and confirm successful queries

---

### Option 2: Self-Hosted MySQL on Azure VM
#### Steps to Reproduce
- Deploy Ubuntu VM in Azure (`East US 2`)
- Install MySQL Server:
  ```bash
  sudo apt update
  sudo apt install mysql-server mysql-client
  ```
- Create database and user
- Enable external access:
  ```ini
  bind-address = 0.0.0.0
  ```
- Open port `3306` in VM’s network security group
- Install Python and dependencies (same as Option 1)
- Use `.env` for credentials and connect locally
- Run scripts and verify output

---


### Connection String Patterns

```python
# SQLAlchemy pattern
SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 
    )
```

#### Secrets Management

- Secrets are stored in a `.env` file (not committed to Git)
- Loaded using `dotenv.load_dotenv()` in Python
- Example `.env` structure:
```
##### VM (self-managed MySQL)
VM_DB_HOST=10.0.1.10
VM_DB_PORT=3306
VM_DB_USER=class_user
VM_DB_PASS=change_me
VM_DB_NAME=class_db_netid

##### Managed MySQL
MAN_DB_HOST=your-managed-endpoint
MAN_DB_PORT=3306
MAN_DB_USER=class_user
MAN_DB_PASS=change_me
MAN_DB_NAME=class_db_netid
```

---

### Screenshots Summary

#### VM Path (Self-Hosted MySQL)

| Step | Screenshot | Description |
|------|------------|-------------|
| 1 | ![VM Creation](link-to-vm-creation-screenshot) | Azure VM deployment summary showing region, OS, and public IP |
| 2 | ![Firewall Rules](link-to-firewall-screenshot) | Network security group with port 3306 open for MySQL access |
| 3 | ![MySQL Status](link-to-mysql-status-screenshot) | Output of `systemctl status mysql` confirming MySQL is running |
| 4 | ![MySQL Version](link-to-mysql-version-screenshot) | Output of `mysql --version` showing installed version |
| 5 | ![MySQL Prompt](link-to-mysql-prompt-screenshot) | `mysql` CLI showing `SHOW DATABASES;` with your DB/table listed |

---

#### Managed Path (Azure-Managed MySQL)

| Step | Screenshot | Description |
|------|------------|-------------|
| 1 | ![Managed MySQL Setup](link-to-managed-mysql-screenshot) | Azure MySQL Flexible Server setup summary with endpoint and admin info |
| 2 | ![Authorized IPs](link-to-authorized-ips-screenshot) | Firewall rules showing allowed IP ranges for managed MySQL |
| 3 | ![Query Window](link-to-query-window-screenshot) | Azure portal query editor or metrics page showing successful query |

---

#### Python Runs

| Step | Screenshot | Description |
|------|------------|-------------|
| 1 | ![Environment Layout](link-to-env-screenshot) | `.env` file structure (no secrets) and Python script loading variables |
| 2 | ![Script Output](link-to-script-output-screenshot) | Terminal output showing row count and successful connection |


---