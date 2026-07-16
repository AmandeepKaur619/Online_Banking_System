import streamlit as st
import pandas as pd
from fpdf import FPDF
from psycopg2.extras import RealDictCursor
from connection import get_db_connection
from fpdf.enums import XPos, YPos

st.set_page_config(page_title="Online Banking System", layout="centered")


st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #0f3460 100%);
        background-attachment: fixed;
    }
    [data-testid="stSidebar"] { background-color: rgba(26, 26, 46, 0.9) !important; }
    
    /* Card Style */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }
    
    h1, h2, h3, p, div, label, .stMarkdown { color: #ffffff !important; }
    div.stButton > button { background-color: #007bff; color: black; border-radius: 20px; border: none; padding: 10px 24px; }
    div.stButton > button:hover { background-color: #0056b3; transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

@st.dialog("Transaction Successful")
def show_success_popup(action, amount):
    st.success(f"{action} of ₹{amount} completed!")
    if st.button("Close"): st.rerun()


st.title("Online Banking System")


if 'logged_in' not in st.session_state:
    st.session_state.update({'logged_in': False, 'customer_id': None, 'show_balance': False, 
                             'history_authorized': False, 'mini_authorized': False, 'confirm_trans': False})




if not st.session_state.logged_in:
    choice = st.sidebar.radio("Navigation", ["Login", "Register"])
    conn = get_db_connection(); cursor = conn.cursor(cursor_factory=RealDictCursor)
    if choice == "Login":
        user_id, pwd = st.text_input("Customer ID"), st.text_input("Password", type="password")
        if st.button("Login"):
            cursor.execute("SELECT * FROM Customers WHERE CustomerID = %s AND Password = %s", (user_id, pwd))
            user = cursor.fetchone()
            if user: st.session_state.logged_in = True; st.session_state.customer_id = user['customerid']; st.rerun()
            else: st.error("Invalid Login")
    elif choice == "Register":
        name, email, pwd = st.text_input("Name"), st.text_input("Email"), st.text_input("Password", type="password")
        if st.button("Register"):
            try:
                cursor.execute("""INSERT INTO Customers (FullName, Email, Password) VALUES (%s, %s, %s) RETURNING CustomerID""",(name, email, pwd))
                cust_id = cursor.fetchone()["customerid"]
                cursor.execute("INSERT INTO Accounts (CustomerID, Balance) VALUES (%s, %s)",(cust_id, 0.00))
                conn.commit() 
                st.success(f"Registered Successfully!\nYour Customer ID is: {cust_id}")
            except Exception as e:
                conn.rollback()
                st.error(f"Registration failed: {e}")
        conn.close()

else:
    conn = get_db_connection(); cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM Customers WHERE CustomerID = %s", (st.session_state.customer_id,))
    user = cursor.fetchone()
    
    st.sidebar.title(f"Welcome, {user['fullname']}")
    page = st.sidebar.radio("Menu", ["Dashboard", "Quick Actions", "Check Balance", "Mini Statement", "Transaction History", "Logout"])


    if page == "Dashboard":
        st.title("Account Summary")
        st.markdown(f"""
            <div class="glass-card">
                <h3>Account Information</h3>
                <p><b>Customer ID:</b> {user['customerid']}</p>
                <p><b>Customer Name:</b> {user['fullname']}</p>
                <p><b>Account Type:</b> Savings Premium</p>
                <p><b>Email:</b> {user['email']}</p>
            </div>
        """, unsafe_allow_html=True)


    elif page == "Quick Actions":
        st.title("Transaction Type:")
        action = st.radio("Select Action", ["Deposit", "Withdrawal"])
        amount = st.number_input("Amount", min_value=1.0)
        if st.button("Submit"): st.session_state.confirm_trans = True
        
        if st.session_state.confirm_trans:
            txn_pwd = st.text_input("Verify Password", type="password")
            if st.button("Confirm & Execute"):
                if txn_pwd == user['password']:
                    cursor.execute("SELECT AccountID, Balance FROM Accounts WHERE CustomerID = %s", (st.session_state.customer_id,))
                    acc = cursor.fetchone()
                    if action == "Withdrawal" and amount > acc['balance']: st.error("Insufficient Funds!")
                    else:
                        cursor.execute("CALL ProcessTransaction(%s,%s,%s)",(acc["accountid"], amount, action))
                        conn.commit(); st.session_state.confirm_trans = False; show_success_popup(action, amount)
                else: st.error("Wrong Password!")


    elif page == "Check Balance":
        st.title("Account Balance")
        if not st.session_state.show_balance:
            if st.button("View Balance"): st.session_state.ask_pwd = True
            if st.session_state.get('ask_pwd'):
                if st.text_input("Confirm Password", type="password") == user['password'] and st.button("Confirm"):
                    st.session_state.show_balance = True; st.rerun()
        else:
            cursor.execute("SELECT Balance FROM Accounts WHERE CustomerID = %s", (st.session_state.customer_id,))
            st.markdown(f'<div class="glass-card"><h2>Current Balance: ₹{cursor.fetchone()["balance"]}</h2></div>', unsafe_allow_html=True)
            if st.button("Hide"): st.session_state.show_balance = False; st.rerun()

    elif page == "Mini Statement":
        st.title("Mini Statement")
        if not st.session_state.mini_authorized:
            if st.button("Unlock"): st.session_state.ask_mini_pwd = True
            if st.session_state.get('ask_mini_pwd'):
                if st.text_input("Enter Password", type="password") == user['password'] and st.button("Confirm"):
                    st.session_state.mini_authorized = True; st.rerun()
        else:
            cursor.execute("SELECT TransactionDate, TransactionType, Amount FROM Transactions t JOIN Accounts a ON t.AccountID = a.AccountID WHERE a.CustomerID = %s ORDER BY TransactionDate DESC LIMIT 5", (user['customerid'],))
            df = pd.DataFrame(cursor.fetchall())
            st.table(df)
            pdf = FPDF(); pdf.add_page(); pdf.set_font("Helvetica", size=12)
            pdf.cell(200, 10, text="Mini Statement", new_x = XPos.LMARGIN, new_y = YPos.NEXT, align='C'); pdf.ln(10)
            for _, row in df.iterrows(): pdf.cell(200, 10, text=f"{row['transactiondate']} | {row['transactiontype']} | Rs. {row['amount']}",new_x = XPos.LMARGIN, new_y = YPos.NEXT)
            pdf_bytes = bytes(pdf.output(dest="S"))
            st.download_button("Download PDF", data=pdf_bytes, file_name="mini_statement.pdf", mime="application/pdf")
            if st.button("Lock"): st.session_state.mini_authorized = False; st.rerun()

    elif page == "Transaction History":
        st.title("Transaction History")
        if not st.session_state.history_authorized:
            if st.button("Unlock History"): st.session_state.ask_hist_pwd = True
            if st.session_state.get('ask_hist_pwd'):
                if st.text_input("Enter Password", type="password") == user['password'] and st.button("Confirm"):
                    st.session_state.history_authorized = True; st.rerun()
        else:
            cursor.execute("SELECT t.TransactionDate, t.TransactionType, t.Amount FROM Transactions t JOIN Accounts a ON t.AccountID = a.AccountID WHERE a.CustomerID = %s ORDER BY t.TransactionDate DESC", (st.session_state.customer_id,))
            st.table(pd.DataFrame(cursor.fetchall()))
            if st.button("Lock History"): st.session_state.history_authorized = False; st.rerun()


    elif page == "Logout":
        st.session_state.update({'logged_in': False, 'show_balance': False, 'history_authorized': False, 'mini_authorized': False})
        st.rerun()
    conn.close()        