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

You can add screenshots of the application here.

##  Future Enhancements

- User authentication improvements
- Fund transfer between accounts
- Account statements
- Dashboard analytics
- Email/SMS notifications

##  Author

**Amandeep Kaur**

M.Sc. Data Science | Lovely Professional University
