
import streamlit as st
from hello import Bank, BankError

# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 Bank Management System")
st.caption("A simple and secure bank management application")

# ----------------------------------
# INITIALIZE BANK
# ----------------------------------

bank = Bank()

if "account" not in st.session_state:
    st.session_state.account = None


# ----------------------------------
# HELPER FUNCTIONS
# ----------------------------------

def handle_error(error):
    st.error(str(error))


def update_session_account(account):
    """Store only public account information in the session."""
    st.session_state.account = {
        "name": account["name"],
        "age": account["age"],
        "email": account["email"],
        "account_number": account["account_number"],
        "balance": account["balance"]
    }


def logout():
    st.session_state.account = None
    st.rerun()


# ----------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------

if st.session_state.account is None:

    menu = st.sidebar.selectbox(
        "Navigation",
        ["Home", "Create Account", "Login"]
    )

else:

    menu = st.sidebar.selectbox(
        "Navigation",
        [
            "Dashboard",
            "Deposit",
            "Withdraw",
            "Transactions",
            "Update Details",
            "Close Account"
        ]
    )

# ----------------------------------
# HOME PAGE
# ----------------------------------

if menu == "Home":

    st.subheader("Welcome to Our Bank!")

    st.write(
        "Manage your banking activities using this application."
    )

    st.info(
        "Create a new account or log in to access your account."
    )


# ----------------------------------
# CREATE ACCOUNT
# ----------------------------------

elif menu == "Create Account":

    st.subheader("📝 Create New Account")

    with st.form("create_account_form"):

        name = st.text_input("Full Name")

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=18,
            step=1
        )

        email = st.text_input("Email Address")

        pin = st.text_input(
            "Create 4-digit PIN",
            type="password",
            max_chars=4
        )

        submitted = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

        if submitted:

            try:

                account = bank.create_account(
                    name=name,
                    age=age,
                    email=email,
                    pin=pin
                )

                st.success("Account created successfully!")

                st.write("Your account details:")

                st.write("**Name:**", account["name"])

                st.write(
                    "**Account Number:**",
                    account["account_number"]
                )

                st.info(
                    "Please save your account number."
                )

            except BankError as error:
                handle_error(error)


# ----------------------------------
# LOGIN
# ----------------------------------

elif menu == "Login":

    st.subheader("🔐 Account Login")

    with st.form("login_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "Enter your PIN",
            type="password",
            max_chars=4
        )

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True
        )

        if submitted:

            try:

                account = bank.login(
                    account_number.strip(),
                    pin
                )

                update_session_account(account)

                st.success("Login successful!")

                st.rerun()

            except BankError as error:
                handle_error(error)


# ----------------------------------
# DASHBOARD
# ----------------------------------

elif menu == "Dashboard":

    account = st.session_state.account

    st.subheader("📊 Account Dashboard")

    st.write(f"Welcome, **{account['name']}!**")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Account Balance",
            f"SAR {account['balance'] / 100:.2f}"
        )

    with col2:

        st.metric(
            "Account Number",
            account["account_number"]
        )

    st.divider()

    st.write("**Personal Information**")

    st.write("Name:", account["name"])

    st.write("Age:", account["age"])

    st.write("Email:", account["email"])

    if st.button("Logout", use_container_width=True):
        logout()


# ----------------------------------
# DEPOSIT MONEY
# ----------------------------------

elif menu == "Deposit":

    st.subheader("💰 Deposit Money")

    with st.form("deposit_form"):

        amount = st.number_input(
            "Enter Deposit Amount (SAR)",
            min_value=0.01,
            max_value=10000.00,
            value=10.00,
            step=10.00
        )

        submitted = st.form_submit_button(
            "Deposit Money",
            use_container_width=True
        )

        if submitted:

            try:

                account = bank.deposit(
                    st.session_state.account["account_number"],
                    amount
                )

                update_session_account(account)

                st.success("Money deposited successfully!")

                st.metric(
                    "Updated Balance",
                    f"SAR {account['balance'] / 100:.2f}"
                )

            except BankError as error:
                handle_error(error)


# ----------------------------------
# WITHDRAW MONEY
# ----------------------------------

elif menu == "Withdraw":

    st.subheader("💸 Withdraw Money")

    with st.form("withdraw_form"):

        amount = st.number_input(
            "Enter Withdrawal Amount (SAR)",
            min_value=0.01,
            value=10.00,
            step=10.00
        )

        submitted = st.form_submit_button(
            "Withdraw Money",
            use_container_width=True
        )

        if submitted:

            try:

                account = bank.withdraw(
                    st.session_state.account["account_number"],
                    amount
                )

                update_session_account(account)

                st.success("Withdrawal successful!")

                st.metric(
                    "Remaining Balance",
                    f"SAR {account['balance'] / 100:.2f}"
                )

            except BankError as error:
                handle_error(error)


# ----------------------------------
# TRANSACTION HISTORY
# ----------------------------------

elif menu == "Transactions":

    st.subheader("📜 Transaction History")

    try:

        transactions = bank.get_transactions(
            st.session_state.account["account_number"]
        )

        if transactions:

            st.dataframe(
                transactions,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No transactions available.")

    except BankError as error:
        handle_error(error)


# ----------------------------------
# UPDATE ACCOUNT DETAILS
# ----------------------------------

elif menu == "Update Details":

    st.subheader("✏️ Update Account Details")

    account = st.session_state.account

    with st.form("update_form"):

        name = st.text_input(
            "Full Name",
            value=account["name"]
        )

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=int(account["age"])
        )

        email = st.text_input(
            "Email Address",
            value=account["email"]
        )

        submitted = st.form_submit_button(
            "Update Details",
            use_container_width=True
        )

        if submitted:

            try:

                updated_account = bank.update_details(
                    account["account_number"],
                    name=name,
                    age=age,
                    email=email
                )

                update_session_account(updated_account)

                st.success("Account details updated successfully!")

            except BankError as error:
                handle_error(error)


# ----------------------------------
# CLOSE ACCOUNT
# ----------------------------------

elif menu == "Close Account":

    st.subheader("❌ Close Bank Account")

    st.warning(
        "Closing your account is permanent. "
        "Your account balance must be zero."
    )

    confirm = st.checkbox(
        "I confirm that I want to close my account."
    )

    if st.button(
        "Close Account",
        disabled=not confirm,
        use_container_width=True
    ):

        try:

            bank.close_account(
                st.session_state.account["account_number"]
            )

            st.session_state.account = None

            st.success("Account closed successfully!")

            st.rerun()

        except BankError as error:
            handle_error(error)

