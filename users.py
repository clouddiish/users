import sqlite3


class WrongEmailError(Exception):
    """Exception raised for invalid email input."""

    pass


class WrongNameError(Exception):
    """Exception raised for invalid name input."""

    pass


def create_connection_and_cursor(db_name):
    """
    Creates a SQLite database connection and cursor.

    Args:
        db_name (str): The name of the SQLite database file.

    Returns:
        tuple: A tuple containing the connection and cursor objects.
    """
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    return con, cur


def create_users_table(cur):
    """
    Creates the users table in the database.

    Args:
        cur (sqlite3.Cursor): The SQLite cursor object.
    """
    cur.execute("DROP TABLE IF EXISTS users")

    table = """ CREATE TABLE users (
            name TEXT,
            email TEXT UNIQUE,
            age INTEGER
        ); """
    cur.execute(table)


def insert_initial_values(con, cur):
    """
    Inserts initial user records into the users table.

    Args:
        con (sqlite3.Connection): The SQLite connection object.
        cur (sqlite3.Cursor): The SQLite cursor object.
    """
    data = [
        ("Anne Bee", "anne.bee@email.com", 27),
        ("Cee Dee", "cee.dee@email.com", 19),
        ("Eri Foo", "eri.foo@email.com", 36),
        ("Gee Hii", "gee.hii@email.com", 25),
        ("Izzy Jay", "izzy.jay@email.com", 29),
        ("Kay Lin", "kay.lin@email.com", 22),
        ("Moe Nan", "moe.nan@email.com", 34),
        ("Ollie Poe", "ollie.poe@email.com", 28),
        ("Quinn Rae", "quinn.rae@email.com", 30),
        ("Sam Tee", "sam.tee@email.com", 23),
        ("Uma Vie", "uma.vie@email.com", 35),
        ("Vic Wu", "vic.wu@email.com", 26),
        ("Xen Yoo", "xen.yoo@email.com", 24),
        ("Yara Zee", "yara.zee@email.com", 29),
        ("Zane Ace", "zane.ace@email.com", 21),
        ("Bryce Dee", "bryce.dee@email.com", 32),
        ("Cora Fee", "cora.fee@email.com", 27),
        ("Duke Gee", "duke.gee@email.com", 33),
        ("Elle Hue", "elle.hue@email.com", 25),
        ("Finn Jay", "finn.jay@email.com", 20),
        ("Gwen Key", "gwen.key@email.com", 31),
        ("Hale Lee", "hale.lee@email.com", 28),
        ("Ivy Mee", "ivy.mee@email.com", 22),
        ("Jude Nee", "jude.nee@email.com", 34),
        ("Kale Oye", "kale.oye@email.com", 26),
    ]
    cur.executemany("INSERT INTO users VALUES(?, ?, ?)", data)
    con.commit()


def print_results(results):
    """
    Prints query results in a tabular format.

    Args:
        results (list): A list of tuples containing query results.
    """
    if results:
        print("NAME \t\tEMAIL \t\t\tAGE")
        for row in results:
            print(f"{row[0]} \t{row[1]} \t{row[2]}")
    else:
        print("No results found.")


def get_user_data():
    """
    Collects user data from the console input.

    Returns:
        tuple: A tuple containing the name, email, and age of the user.

    Raises:
        WrongEmailError: If the email input does not contain '@'.
        WrongNameError: If the name input is empty.
    """
    try:
        name = input("Name of the user: ")
        email = input("Email of the user: ")
        age = int(input("Age of the user: "))

        if "@" not in email:
            raise WrongEmailError

        if not name:
            raise WrongNameError

        return name, email, age

    except ValueError:
        print("Age must be an integer. Try again.")

    except WrongEmailError:
        print("Email must contain a @. Try again.")

    except WrongNameError:
        print("Name cannot be empty. Try again.")


def check_if_user_exists(cur):
    """
    Checks if a user with a given name exists in the database.

    Args:
        cur (sqlite3.Cursor): The SQLite cursor object.

    Returns:
        str or None: The user's name if found, otherwise None.
    """
    name = input("Name of the user to update: ")

    cur.execute("SELECT name FROM users WHERE name=?", (name,))
    results = cur.fetchone()

    if not results:
        print("User with this name does not exist. Try again.")
        return

    return name


def select_all(cur):
    """
    Retrieves and displays all users from the database.

    Args:
        cur (sqlite3.Cursor): The SQLite cursor object.
    """
    cur.execute("SELECT * FROM users")
    results = cur.fetchall()
    print_results(results)


def select_search(cur):
    """
    Searches for users by name or email.

    Args:
        cur (sqlite3.Cursor): The SQLite cursor object.
    """
    search_by = input("Enter name or email to find users: ")

    cur.execute(
        "SELECT * FROM users WHERE name LIKE '%' || ? || '%' OR email LIKE '%' || ? || '%'",
        (search_by, search_by),
    )
    results = cur.fetchall()
    print_results(results)


def select_filter(cur):
    """
    Filters users based on name's first letter and age range.

    Args:
        cur (sqlite3.Cursor): The SQLite cursor object.
    """
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
    """
    Creates a new user in the database.

    Args:
        con (sqlite3.Connection): The SQLite connection object.
        cur (sqlite3.Cursor): The SQLite cursor object.
    """
    data = get_user_data()

    try:
        if data:
            cur.execute("INSERT INTO users VALUES(?, ?, ?)", data)
            con.commit()
            print("User created")

    except sqlite3.IntegrityError:
        print("User with this email already exists. Try again.")


def update_user(con, cur):
    """
    Updates an existing user's data in the database.

    Args:
        con (sqlite3.Connection): The SQLite connection object.
        cur (sqlite3.Cursor): The SQLite cursor object.
    """
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
    """
    Deletes a user from the database.

    Args:
        con (sqlite3.Connection): The SQLite connection object.
        cur (sqlite3.Cursor): The SQLite cursor object.
    """
    name = check_if_user_exists(cur)

    if not name:
        return

    cur.execute("DELETE FROM users WHERE name=?", (name,))
    con.commit()
    print(f"User {name} deleted.")


def run(con, cur):
    """
    Runs the main application loop for user management.

    Args:
        con (sqlite3.Connection): The SQLite connection object.
        cur (sqlite3.Cursor): The SQLite cursor object.
    """
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
                print("Invalid option. Try again.")
                print()


con, cur = create_connection_and_cursor("users.db")
run(con, cur)
con.close()
