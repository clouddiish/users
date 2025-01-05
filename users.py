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


def create_user(con, cur):
    try:
        name = input("Name of the user: ")
        email = input("Email of the user: ")
        age = int(input("Age of the user: "))

    except ValueError:
        print("Age must be an integer. Try again.")
        return

    data = (name, email, age)

    cur.execute("INSERT INTO users VALUES(?, ?, ?)", data)
    con.commit()

    print("User created")


def run(con, cur):
    create_users_table(cur)
    insert_initial_values(con, cur)

    create_user(con, cur)


con, cur = create_connection_and_cursor("users.db")
run(con, cur)
con.close()
