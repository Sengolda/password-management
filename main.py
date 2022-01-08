import sqlite3
import secrets
from hashlib import sha256
from rich import print
from rich.table import Table


def connect():
    return sqlite3.connect("passwords.db")


def store_passwords(user, master_password):
    try:
        conn = connect()
        c = conn.cursor()
        sql = """ INSERT INTO users VALUES (?,?,?)"""
        to_insert = (user, master_password, "")
        c.execute(sql, to_insert)
        conn.commit()
        return True
    except (Exception,):
        return "You already made an account."


def get_password(user):
    conn = connect()
    c = conn.cursor()
    sql = """SELECT master_password FROM users WHERE user_name = ?"""
    to_select = (user,)
    c.execute(sql, to_select)
    rows = c.fetchone()
    try:
        main_row = rows[0]
    except Exception as e:
        print(e)
        return "You do not have an account."
    else:
        return main_row


def main():
    print("Hi welcome")
    print(r"Do you have an account? (y\n)")
    user_in = input("> ")
    if user_in == "n":
        user = input("> what would you like your user name to be.")
        password = input("> what would you like your master password to be.")
        result = store_passwords(user, password)
        if result is True:
            print("[green]Nice you made your account.[/green]")

        if result == "You already made an account.":
            print(f"[red]{result}[/red]")

    if user_in == "y":
        user_in2 = input("What is your username?")
        user = get_password(user_in2)
        if user == "You do not have an account.":
            print(user)
        else:
            password = input("what is your password?")
            if password != user:
                print("Invalid password.")
            else:
                print("Your in.")
                user_in3 = input(
                    "Would you like to see your passwords or make a new one?\n`m` for make\n`p` to see your passwords\nuse `g` to generate a new one\u200b \u2002"
                )
                if user_in3 == "p":
                    conn = connect()
                    c = conn.cursor()
                    to_insert = (user_in2,)
                    e = c.execute("SELECT passwords FROM users WHERE user_name = ?", to_insert)
                    rows = e.fetchall()
                    row_dict = {"passwords": v[0].split(",") for v in rows}
                    passwords = row_dict.get("passwords")
                    for val in passwords:
                        if not val:
                            passwords.remove(val)

                    table = Table(title="Passwords")
                    table.add_column("Passwords", style="cyan")
                    print("\n\n")
                    for password in passwords:
                        table.add_row(password)
                    print(table)

                if user_in3 == "m":
                    conn = connect()
                    c = conn.cursor()

                    password = input("What would you like your password to be?")
                    current_passwords = c.execute(
                        "SELECT passwords FROM users WHERE user_name = ?", (user_in2,)
                    ).fetchall()
                    current_passwords = current_passwords[0]
                    current_passwords = ",".join(current_passwords)
                    new_passwords = f"{password},{current_passwords}"
                    c.execute("UPDATE users SET passwords = ? WHERE user_name = ?", (new_passwords, user_in2))
                    conn.commit()

                if user_in3 == "g":
                    conn = connect()
                    c = conn.cursor()

                    to_hash = secrets.token_urlsafe(64)
                    hashed_password = sha256(to_hash.encode())
                    current_passwords = c.execute(
                        "SELECT passwords FROM users WHERE user_name = ?", (user_in2,)
                    ).fetchall()
                    current_passwords = current_passwords[0]
                    current_passwords = ",".join(current_passwords)
                    new_passwords = f"{hashed_password.hexdigest()},{current_passwords}"
                    c.execute("UPDATE users SET passwords = ? WHERE user_name = ?", (new_passwords, user_in2))
                    conn.commit()
                    print(f"Your new generated password is: {hashed_password.hexdigest()}")


main()
