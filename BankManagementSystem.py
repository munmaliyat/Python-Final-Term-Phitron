import random

class User:
    def __init__(self, name, email, address, account_type, password):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.account_number = self.generate_account_number()
        self.transaction_history = []
        self.loan_taken = 0
        self.password = password

    def generate_account_number(self):
        return random.randint(10000, 99999)

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f"Deposited ${amount}")

    def withdraw(self, amount):
        if self.balance < amount:
            print("Error: Withdrawal amount exceeded.")
        else:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew ${amount}")

    def check_balance(self):
        return self.balance

    def check_transaction_history(self):
        return self.transaction_history

    def take_loan(self, amount):
        if self.loan_taken < 2:
            self.loan_taken += 1
            self.balance += amount
            self.transaction_history.append(f"Loan taken: ${amount}")
        else:
            print("Error: You have already taken the maximum number of loans.")

    def transfer(self, recipient, amount):
        if recipient is None:
            print("Error: Account does not exist.")
        elif self.balance >= amount:
            self.balance -= amount
            recipient.balance += amount
            self.transaction_history.append(f"Transferred ${amount} to {recipient.name}")

    def check_bankrupt(self):
        if self.balance < 0:
            return True
        return False

class Admin:
    def __init__(self, password):
        self.users = []
        self.loan_enabled = True
        self.password = password

    def create_user_account(self, name, email, address, account_type):
        password = input(f"Create a password for {name}: ")
        user = User(name, email, address, account_type, password)
        self.users.append(user)
        return user

    def delete_user_account(self, user):
        if user in self.users:
            self.users.remove(user)
        else:
            print("Error: User not found.")

    def see_all_user_accounts(self):
        print("All User Accounts:")
        for user in self.users:
            print(f"Name: {user.name}, Account Number: {user.account_number}")

    def check_total_available_balance(self):
        total_balance = sum(user.check_balance() for user in self.users)
        return total_balance

    def check_total_loan_amount(self):
        total_loan_amount = sum(user.loan_taken for user in self.users)
        return total_loan_amount

    def toggle_loan_feature(self, enable=True):
        self.loan_enabled = enable
        if enable:
            print("Loan feature is now enabled.")
        else:
            print("Loan feature is now disabled.")

def create_user_account():
    while True:
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        address = input("Enter your address: ")
        account_type = input("Enter account type (Savings or Current): ").capitalize()
        password = input("Create a password: ")

        if account_type in ["Savings", "Current"]:
            return User(name, email, address, account_type, password)
        else:
            print("Error: Invalid account type. Please enter 'Savings' or 'Current.")

def main():
    admin_password = "admin"
    admin = Admin(admin_password)
    user = None

    print("WELCOME TO BANK MANAGEMENT SYSTEM")
    print("---------------------------------")

    while True:
        print("\nMenu:")
        print("1. User")
        print("2. Admin")
        print("3. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            print("1. Log In")
            print("2. Register")

            choice2 = input("\nEnter your choice: ")

            if choice2 == "2":
                user = create_user_account()
                print("------------------------")
                print("Registration Successful!")
                print("------------------------")

            elif choice2 == "1":
                if user is not None:
                    user_password = input("Enter your password: ")

                    if user_password == user.password:
                        while True:
                            print("\nUser Dashboard:")
                            print("1. Deposit")
                            print("2. Withdraw")
                            print("3. Check Balance")
                            print("4. Transaction History")
                            print("5. Take Loan")
                            print("6. Transfer")
                            print("7. Exit")

                            user_choice = input("Enter your choice: ")

                            if user_choice == "1":
                                amount = float(input("Enter the deposit amount: "))
                                user.deposit(amount)

                            elif user_choice == "2":
                                amount = float(input("Enter the withdrawal amount: "))
                                user.withdraw(amount)
                            elif user_choice == "3":
                                print(f"Your balance: ${user.check_balance()}")
                            elif user_choice == "4":
                                print("Transaction History:")
                                for transaction in user.check_transaction_history():
                                    print(transaction)
                            elif user_choice == "5":
                                amount = float(input("Enter the loan amount: "))
                                user.take_loan(amount)
                            elif user_choice == "6":
                                recipient_name = input("Enter the recipient's name: ")
                                recipient = next((u for u in admin.users if u.name == recipient_name), None)
                                if recipient:
                                    amount = float(input(f"Enter the amount to transfer to {recipient_name}: "))
                                    user.transfer(recipient, amount)
                                else:
                                    print("Error: Recipient not found.")
                            elif user_choice == "7":
                                break
                            else:
                                print("Error: Invalid choice. Please select a valid option.")
                    else:
                        print("Error: Incorrect password")
                        continue
                else:
                    print("Error: You need to register first by selecting '2. Register'")

        elif choice == "2":
            admin_password_attempt = input("Enter Admin password: ")
            if admin_password_attempt != admin.password:
                print("Error: Incorrect Admin password.")
                continue

            while True:
                print("\nAdmin Dashboard:")
                print("1. Create User Account")
                print("2. Delete User Account")
                print("3. View All User Accounts")
                print("4. Check Total Available Balance")
                print("5. Check Total Loan Amount")
                print("6. Toggle Loan Feature")
                print("7. Exit")

                admin_choice = input("Enter your choice: ")

                if admin_choice == "1":
                    name = input("Enter user's name: ")
                    email = input("Enter user's email: ")
                    address = input("Enter user's address: ")
                    account_type = input("Enter user's account type (Savings or Current): ").capitalize()
                    admin.create_user_account(name, email, address, account_type)
                    print("User account created.")
                elif admin_choice == "2":
                    admin.see_all_user_accounts()
                    account_number = int(input("Enter the account number of the user to delete: "))
                    user_to_delete = next((u for u in admin.users if u.account_number == account_number), None)
                    if user_to_delete:
                        admin.delete_user_account(user_to_delete)
                        print("User account deleted.")
                    else:
                        print("Error: User not found.")
                elif admin_choice == "3":
                    admin.see_all_user_accounts()
                elif admin_choice == "4":
                    total_balance = admin.check_total_available_balance()
                    print(f"Total Available Balance in the Bank: ${total_balance}")
                elif admin_choice == "5":
                    total_loan_amount = admin.check_total_loan_amount()
                    print(f"Total Loan Amount in the Bank: ${total_loan_amount}")
                elif admin_choice == "6":
                    enable_loan = input("Do you want to enable (E) or disable (D) the loan feature? ").strip().lower()
                    if enable_loan == "e":
                        admin.toggle_loan_feature(True)
                    elif enable_loan == "d":
                        admin.toggle_loan_feature(False)
                    else:
                        print("Error: Invalid input. Please enter 'E' to enable or 'D' to disable.")
                elif admin_choice == "7":
                    break
                else:
                    print("Error: Invalid choice. Please select a valid option.")
        elif choice == "3":
            break
        else:
            print("Error: Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
