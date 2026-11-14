# Bank-Management-System
A Python-based Bank Management System built with Streamlit, featuring account creation, secure PIN authentication, deposits, withdrawals, transaction history, and account management.
# 🏦 Bank Management System

A simple Bank Management System developed using **Python and Streamlit**. This application allows users to create and manage bank accounts through an interactive web interface.

## 🚀 Features

- **Create Account:** Register a new bank account with personal details and a 4-digit PIN.
- **Secure Login:** Authenticate users using their account number and PIN.
- **Dashboard:** View account information, account number, and current balance.
- **Deposit Money:** Deposit money into an account.
- **Withdraw Money:** Withdraw money with balance validation.
- **Transaction History:** View previous deposits and withdrawals.
- **Update Details:** Update personal account information.
- **Close Account:** Close an account when its balance is zero.
- **PIN Security:** PINs are hashed using PBKDF2-HMAC-SHA256 with individual salts.
- **Data Storage:** Store account and transaction information using JSON.

## 🛠️ Technologies Used

- Python
- Streamlit
- JSON
- hashlib
- secrets
- pathlib

## 📁 Project Structure

```text
bank-management-system/
│
├── app.py              # Streamlit web application
├── hello.py            # Bank management logic
├── main.py             # Original command-line version
├── requirements.txt    # Project dependencies
├── .gitignore          # Git ignored files
├── README.md           # Project documentation
│
└── data.json           # Local database (not committed)
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/bank-management-system.git
```

### 2. Navigate to the Project Directory

```bash
cd bank-management-system
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 💻 Application Modules

| Module | Description |
|---|---|
| Account Creation | Creates new bank accounts |
| Authentication | Verifies account number and PIN |
| Deposit | Adds money to an account |
| Withdrawal | Deducts money from an account |
| Transactions | Displays transaction history |
| Update Details | Updates customer information |
| Close Account | Deletes an account with zero balance |

## 🔐 Security Notes

- PINs are stored as salted PBKDF2-HMAC-SHA256 hashes.
- Account information is stored in a JSON file.
- Users must authenticate to access their accounts.

**Important:** This project is intended for educational and demonstration purposes. It is not a production-ready banking system. It does not implement production-grade authorization, database security, encryption at rest, or multi-user concurrency controls.

## 📌 Future Improvements

- Database integration using SQLite or MySQL.
- Improved authentication and authorization.
- Admin dashboard.
- Account-to-account transfers.
- Improved user interface.
- Deployment using Streamlit Community Cloud.

## 👨‍💻 Author

Developed as a Python programming project.

## 📄 License

This project is available under the MIT License.

