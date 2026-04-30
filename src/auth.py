from database import connect, hash_password, log_audits

current_user = ""
current_role = ""

def login(username, password):
    global current_user, current_role
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT username, role FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    row = cursor.fetchone()
    conn.close()
    if row:
        current_user = row[0]
        current_role = row[1]
        log_audits(current_user, "logged in")
        return True
    return False

def logout():
    global current_user, current_role
    log_audits(current_user, "logged out")
    current_user = ""
    current_role = ""

def register_user(username, password, role):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)",
                  (username, hash_password(password), role))
        conn.commit()
        conn.close()
        log_audits(current_user, "registered: " + username)
        return True
    except:
        return False
