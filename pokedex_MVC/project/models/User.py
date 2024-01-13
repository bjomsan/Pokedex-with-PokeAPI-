import sqlite3

# helper-function for findUser() to make the code cleaner.
def run_query(query, username, password):
    conn = sqlite3.connect("project/pokemonDatabase.db")
    cursor = conn.cursor()
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

# checking if user exists in database and return error if not
def findUser(username, password):
    query = f"SELECT username FROM user WHERE username = ? AND password = ?"
    result = run_query(query, username, password)
    try:
        result = str(result[0])
    except:
        pass
    if result == username:
        return result
    else:
        return "Error: Invalid username or password"
    
# helper-function for create_user() to make the code cleaner
def existing_user(username):
    conn = sqlite3.connect("project/pokemonDatabase.db")
    cursor = conn.cursor()
    query = "SELECT username FROM user WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    conn.close()
    return result

# checking if username is already taken, if not - insert new user to database
def create_user(username, password):
    isuser = existing_user(username)
    # if not isuer, means the username does not already exist
    if not isuser:
        conn = sqlite3.connect("project/pokemonDatabase.db")
        cursor = conn.cursor()
        try:
            query = "INSERT INTO user (username, password) VALUES (?, ?)"
            cursor.execute(query, (username, password))
            conn.commit()
            print("User inserted successfully.")
        except sqlite3.Error as e:
            print("Error inserting user:", e)
        conn.close()

        # this part is to doublecheck that the new user is in the databse
        result = findUser(username, password)
        if username in result:
            return True
        else:
            return False
    else:
        return False