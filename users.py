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


def print_results(results):
    if results:
        print("NAME \t\tEMAIL \t\t\tAGE")
        for row in results:
            print(f"{row[0]} \t{row[1]} \t{row[2]}")
    else:
        print("No results found.")


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


def select_search(cur):
    search_by = input("Enter name or e-mail to find users: ")

    cur.execute(
        "SELECT * FROM users WHERE name LIKE '%' || ? || '%' OR email LIKE '%' || ? || '%'",
        (search_by, search_by),
    )
    results = cur.fetchall()
    print_results(results)


def select_filter(cur):
    first_letter = input(
        "First letter of the name (or click ENTER if not applicable): "
    )
    min_age = input("Minimum age (or click ENTER if not applicable): ")
    max_age = input("Maximum age (or click ENTER if not applicable): ")

    if not min_age:
        min_age = -1000

    if not max_age:
        max_age = 1000

    cur.execute(
        "SELECT * FROM users WHERE name LIKE ? || '%' AND age > ? AND age < ?",
        (first_letter, min_age, max_age),
    )
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

    while True:
        action = input(
            """What do you want to do?
            - vau - view all users
            - cu - create user
            - uu - update user
            - du - delete user
            - su - search users by name or email
            - fu - filter users
            - ex - exit
            """
        ).lower()

        match action:
            case "vau":
                select_all(cur)
                print()
            case "cu":
                create_user(con, cur)
                print()
            case "uu":
                update_user(con, cur)
                print()
            case "du":
                delete_user(con, cur)
                print()
            case "su":
                select_search(cur)
            case "fu":
                select_filter(cur)
            case "ex":
                sure = input("Are you sure? (Y/N) ").lower()
                if sure == "y":
                    break
            case _:
                print("Wrong letter provided.")
                print()


con, cur = create_connection_and_cursor("users.db")
run(con, cur)
con.close()
