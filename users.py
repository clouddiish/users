import sqlite3


def create_connection_and_cursor(db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    return (con, cur)


def create_users_table(cur):
    cur.execute("DROP TABLE IF EXISTS users")

    table = """ CREATE TABLE users (
            name TEXT,
            email TEXT,
            age INTEGER
        ); """

    cur.execute(table)

    print("Table is ready")


def insert_initial_values(con, cur):
    data = [
        ("Anne Bee", "anne.bee@email.com", 27),
        ("Cee Dee", "cee.dee@email.com", 19),
        ("Eri Foo", "eri.foo@email.com", 36),
        ("Gee Hii", "gee.hii@email.com", 25),
        ("Izzy Jay", "izzy.jay@email.com", 29),
    ]

    cur.executemany("INSERT INTO users VALUES(?, ?, ?)", data)
    con.commit()

    print("Values inserted")


def print_results(results):
    print("NAME \t\tEMAIL \t\t\tAGE")
    for row in results:
        print(f"{row[0]} \t{row[1]} \t{row[2]}")


def get_user_data():
    try:
        name = input("Name of the user: ")
        email = input("Email of the user: ")
        age = int(input("Age of the user: "))
        return (name, email, age)

    except ValueError:
        print("Age must be an integer. Try again.")


def check_if_user_exists(cur):
    name = input("Name of the user to update: ")

    cur.execute("SELECT name FROM users WHERE name=?", (name,))
    results = cur.fetchone()

    if not results:
        print("User with this name does not exits. Try again.")
        return

    return name


def select_all(cur):
    cur.execute("SELECT * FROM users")
    results = cur.fetchall()
    print_results(results)


def create_user(con, cur):
    data = get_user_data()

    if data:
        cur.execute("INSERT INTO users VALUES(?, ?, ?)", data)
        con.commit()

        print("User created")


def update_user(con, cur):
    name = check_if_user_exists(cur)

    if not name:
        return

    data = get_user_data()

    if data:
        cur.execute(
            "UPDATE users SET name=?, email=?, age=? WHERE name=?", (*data, name)
        )
        con.commit()
        print(f"User {name} updated.")


def delete_user(con, cur):
    name = check_if_user_exists(cur)

    if not name:
        return

    cur.execute("DELETE FROM users WHERE name=?", (name,))
    con.commit()
    print(f"User {name} deleted.")


def run(con, cur):
    create_users_table(cur)
    insert_initial_values(con, cur)

    select_all(cur)
    # create_user(con, cur)
    # update_user(con, cur)
    delete_user(con, cur)


con, cur = create_connection_and_cursor("users.db")
run(con, cur)
con.close()
