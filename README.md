#  Online Banking System

A simple **Online Banking System** developed using **Python, Streamlit, and PostgreSQL**. This project provides a user-friendly interface for performing basic banking operations while securely storing customer and transaction data in a PostgreSQL database.

##  Features

- Customer Registration
- Secure Login
- Deposit Money
- Withdraw Money
- Check Account Balance
- View Transaction History
- PostgreSQL Database Integration
- Interactive Streamlit Web Interface

##  Technologies Used

- Python
- Streamlit
- PostgreSQL
- psycopg2

##  Project Structure

```
.
├── app.py              # Main Streamlit application
├── connection.py       # PostgreSQL database connection (not included)
├── .gitignore
└── README.md
```

> **Note:** `connection.py` is intentionally excluded from this repository because it contains local database credentials.

##  Setup

1. Clone the repository

```bash
git clone https://github.com/your-username/your-repository.git
```

2. Install the required packages

```bash
pip install -r requirements.txt
```

3. Configure your PostgreSQL database.

4. Create a `connection.py` file with your PostgreSQL connection details.

5. Run the application

```bash
streamlit run app.py
```
6. Optional - If cloning the repository, connection file structure
# connection.py

import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="your_database_name",
    user="your_username",
    password="your_password",
    port="5432"
)

##  Screenshots

Login / Registration window :
<img width="1536" height="765" alt="image" src="https://github.com/user-attachments/assets/7605e8dd-4ac1-41d6-9ccf-8c88e6ba36b5" />

Dashboard :
<img width="1535" height="774" alt="image" src="https://github.com/user-attachments/assets/f493ded1-a9c0-4a3e-892d-ce2742af9d77" />

Deposit / Withdrawal window :
<img width="1536" height="768" alt="image" src="https://github.com/user-attachments/assets/d2674ab2-ef8f-448e-b210-d081ea9cd93b" />

Check Balance window :
<img width="1536" height="756" alt="image" src="https://github.com/user-attachments/assets/a92c060f-daf1-4425-9e37-d50bd2f17e9a" />

Mini Statement :
<img width="1536" height="769" alt="image" src="https://github.com/user-attachments/assets/bb3df07c-86fa-4d7a-a0ce-628ee90e91cc" />
can DOWNLOAD as PDF file :
<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/d4dab9b1-944c-4412-ae41-c40e6c3a853c" />

Transaction History :
<img width="1536" height="739" alt="image" src="https://github.com/user-attachments/assets/4ad1b705-b03a-41f6-a4a4-68c7d9afb449" />


##  Future Enhancements

- User authentication improvements
- Fund transfer between accounts
- Account statements
- Dashboard analytics
- Email/SMS notifications

##  Author

**Amandeep Kaur**

M.Sc. Data Science | Lovely Professional University
