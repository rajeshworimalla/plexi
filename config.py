import mysql.connector
from datetime import datetime
from flask import jsonify
from fuzzywuzzy import process


def get_connection():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="plexidb"
    )


def get_user_info(email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE email = %s AND password = %s;", (email, password))
    results = cur.fetchone()
    conn.close()
    if results:
        return results
    else:
        return False

# print(get_user_info('requester@gmail.com', 'password'))


def insert_new_user(username, password, email, role, main_job, bio, age,location,number):
    conn = get_connection()
    cur = conn.cursor()
    date = datetime.now()
    formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("INSERT INTO users(username, password, email, role, main_job, bio,age,location,phone_number, task_completed, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (username, password, email, role, main_job, bio, age,location,number,0,formatted_date))
    conn.commit()
    conn.close()


def user_exists(username, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username = %s OR email = %s;", (username, email))
    results = cur.fetchall()
    conn.close()
    if results:
        return True
    else:
        return False


def get_all_jobs():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM jobs")
    results = cur.fetchall()
    conn.close()
    return results


def get_jobs_by(requester):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM jobs WHERE employer = %s", (requester,))
    results = cur.fetchall()
    conn.close()
    return results


def get_applications_by(tasker_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""SELECT application_id, date_applied, employer, title, phone, email, app_status
                    FROM applications
                    INNER JOIN jobs ON applications.job_id = jobs.job_id WHERE user_id = %s;""", (tasker_id,))
    results = cur.fetchall()
    formatted_results = []
    for row in results:
        application_id, date_applied, employer, title, phone, email, app_status = row
        formatted_date = datetime.strptime(
            str(date_applied), '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y, %I:%M %p')
        formatted_results.append({
            'application_id': application_id,
            'date_applied': formatted_date,
            'employer': employer,
            'title': title,
            'phone': phone,
            'email': email,
            'app_status': app_status
        })

    conn.close()
    return formatted_results


def get_job_by_user_id(user_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM jobs WHERE requester_id = %s", (user_id,))
    results = cur.fetchall()
    conn.close()
    return results


def get_job_by_job_id(job_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM jobs WHERE job_id = %s", (job_id,))
    results = cur.fetchall()
    conn.close()

    for job in results:
        if 'date_added' in job:
            original_date = job['date_added']
            formatted_date = original_date.strftime('%d %b %Y')
            job['date_added'] = formatted_date
        else:
            job['date_added'] = 'Unknown'

    return results[0]


def save_application(job_id, date_applied, user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO applications(job_id, date_applied, app_status, user_id) VALUES(%s, %s, %s, %s)",
                (job_id, date_applied, 'Pending', user_id))
    conn.commit()
    conn.close()
    return True


def post_job_details(job_title, job_description, payment, task_date, task_location, employer, requester_id, phone, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO jobs(title, employer, salary, location, description,requester_id, phone, email, date_added, status) VALUES( %s, %s, %s, %s,%s, %s, %s, %s, %s, 'Recruiting')",
                (job_title, employer, payment, task_location, job_description, requester_id, phone, email, task_date))
    conn.commit()
    conn.close()


def get_chat_list(user_id):
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            chats.id,
            CASE 
                WHEN chats.user1_id = %s THEN u2.username
                ELSE u1.username
            END AS username,
            messages.message AS last_message,
            messages.timestamp AS last_message_time
        FROM chats
        JOIN users u1 ON u1.id = chats.user1_id
        JOIN users u2 ON u2.id = chats.user2_id
        LEFT JOIN (
            SELECT chat_id, message, timestamp
            FROM messages
            WHERE id IN (
                SELECT MAX(id) FROM messages GROUP BY chat_id
            )
        ) messages ON messages.chat_id = chats.id
        WHERE chats.user1_id = %s OR chats.user2_id = %s;
    """, (user_id, user_id, user_id))
    chat_list = cursor.fetchall()

    # Format the last_message_time for each chat
    for chat in chat_list:
        if chat['last_message_time']:  # Ensure there's a timestamp to format
            original_time = chat['last_message_time']
            # If `last_message_time` is a datetime object
            if isinstance(original_time, datetime):
                chat['last_message_time'] = original_time.strftime('%a, %H:%M')
            else:
                # Parse if it's a string
                parsed_time = datetime.strptime(original_time, '%Y-%m-%d %H:%M:%S')
                chat['last_message_time'] = parsed_time.strftime('%a, %H:%M')
    conn.close()
    return chat_list

def get_chat_window(chat_id, user_id):
    # Get chat details
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
       SELECT 
    users.username AS chat_partner, 
    chats.id AS chat_id
FROM chats
JOIN users ON 
    (users.id = chats.user1_id AND chats.user2_id = %s) OR 
    (users.id = chats.user2_id AND chats.user1_id = %s)
WHERE chats.id = %s;

    """, (user_id, user_id, chat_id))
    chat = cursor.fetchone()

    conn.close()
    return chat


def check_chat_exists(sender_id, recipient_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if a chat already exists between the two users
    query = """
    SELECT id
    FROM chats
    WHERE (user1_id = %s AND user2_id = %s) OR (user1_id = %s AND user2_id = %s)
    """
    cursor.execute(query, (sender_id, recipient_id, recipient_id, sender_id))
    chat_id = cursor.fetchone()
    if chat_id:
        return jsonify({'chat_id': chat_id,  'message': 'Chat exists exists'})
    else:
        return jsonify({'chat_id': chat_id,  'message': 'Chat doesnt exists'})

def insert_message(chat_id, user_id, message):
    # Save the message in the database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (chat_id, sender_id, message) VALUES (%s, %s, %s)",
        (chat_id, user_id, message)
    )
    conn.commit()
    conn.close()
    return jsonify({'status': 'Message sent'}), 200


def get_messages(chat_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT messages.message, messages.timestamp, users.username AS sender
        FROM messages 
        JOIN users ON users.id = messages.sender_id 
        WHERE messages.chat_id = %s
        ORDER BY messages.timestamp
    """, (chat_id,))
    chat_messages = cursor.fetchall()
    conn.close()
    return chat_messages


def get_search_results(query):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # Enable dictionary-like rows

    # # Search query using SQL `LIKE`
    # cursor.execute(
    #     "SELECT id, title, employer, date_added, location FROM jobs WHERE title LIKE %s LIMIT 10",
    #     (f"%{query}%",)
    # )
    # jobs = cursor.fetchall()
    cursor.execute(
        "SELECT * FROM users WHERE username LIKE %s LIMIT 10",
        (f"%{query}%",)
    )
    users = cursor.fetchall()
    conn.close()
    # # Combine results
    # results = {
    #     'jobs': jobs,
    #     'users': users,
    # }
    return users


def create_chat(sender_id, recipient_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO chats (user1_id, user2_id)
            VALUES (%s, %s)
        """, (sender_id, recipient_id))
        
        conn.commit()
        return cursor.lastrowid  # Return the newly created chat ID
    
    except Exception as e:
        print(f"Error creating chat: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()



def total_applications(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        select count(application_id) FROM applications WHERE user_id = %s""", (user_id,))
    total_applications = cursor.fetchone()
    if total_applications[0] == 0:
        return 1
    conn.close()
    return total_applications[0]


def accepted_applications(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        select count(application_id) FROM applications WHERE user_id = %s and app_status = 'Accepted';""", (user_id,))
    accepted_applications = cursor.fetchone()
    conn.close()
    return accepted_applications[0]


def pending_applications(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        select count(application_id) FROM applications WHERE user_id = %s and app_status = 'Pending';""", (user_id,))
    pending_applications = cursor.fetchone()
    conn.close()
    return pending_applications[0]


def rejected_applications(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        select count(application_id) FROM applications WHERE user_id = %s and app_status = 'Rejected';""", (user_id,))
    rejected_applications = cursor.fetchone()
    conn.close()
    return rejected_applications[0]


def reviewed_applications(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        select count(application_id) FROM applications WHERE user_id = %s and app_status = 'Reviewed';""", (user_id,))
    rejected_applications = cursor.fetchone()
    conn.close()
    return rejected_applications[0]


def get_chart_data(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch applications data grouped by month
    cursor.execute(
        "SELECT MONTH(date_applied) AS month, COUNT(*) FROM applications WHERE user_id = %s GROUP BY month", (user_id,))
    application_data = [0] * 12
    for row in cursor.fetchall():
        application_data[row[0] - 1] = row[1]  # Map to the correct month index

    # Fetch shortlisted data grouped by month
    cursor.execute(
        "SELECT MONTH(date_applied) AS month, COUNT(*) FROM applications WHERE user_id = %s AND app_status = 'shortlisted' GROUP BY month", (user_id,))
    shortlisted_data = [0] * 12
    for row in cursor.fetchall():
        shortlisted_data[row[0] - 1] = row[1]

    conn.close()
    return {"applications": application_data, "shortlisted": shortlisted_data}


def update_password(user_id, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET password = %s
        WHERE id = %s;
        """, (new_password, user_id))
    conn.commit()
    cursor.close()
    conn.close()


def update_email(user_id, new_email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET email = %s
        WHERE id = %s;
        """, (new_email, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_user_by_email(email):
    # Database connection and delete query
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE email = %s", (email,))
    conn.commit()
    cursor.close()
    conn.close()

def search_jobs(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM jobs WHERE title LIKE %s LIMIT 10",
        (f"%{query}%",)
    )
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def filter_search_jobs(location,budget): 
    conn = get_connection()
    cursor = conn.cursor()

    
    query = "SELECT * FROM jobs WHERE 1=1"
    params = []

    if budget and location == "":
        query += " AND salary < %s"
        params.append(budget)


    elif location and budget =="":
        query += " AND location LIKE %s"
        location_pattern = f"%{location}%"
        params.append(location_pattern)

    elif location and  budget:
        location_pattern = f"%{location}%"
        query += " AND salary < %s AND location LIKE %s"
        params.append(budget)
        params.append(location_pattern)

    else:
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    print([location, budget,query])
    return results


def switch_role(user_id , user_role):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        UPDATE users
        SET role = %s
        WHERE id = %s;
        """
    if user_role == 'requester':  
        cursor.execute(query, ('tasker', user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return 'tasker'
    elif user_role == 'tasker':
        cursor.execute(query,('requester',user_id) )
        conn.commit()
        cursor.close()
        conn.close()
        return 'requester'
    else:
        cursor.close()
        conn.close()
        return "Can't change role with superadmin account."
        
def get_all_applications():
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT application_id, date_applied, employer, title, phone, email, app_status
        FROM applications
        INNER JOIN jobs ON applications.job_id = jobs.job_id """
    cursor.execute(query)
    results = cursor.fetchall()
    formatted_results = []
    for row in results:
        application_id, date_applied, employer, title, phone, email, app_status = row
        formatted_date = datetime.strptime(
            str(date_applied), '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y, %I:%M %p')
        formatted_results.append({
            'application_id': application_id,
            'date_applied': formatted_date,
            'employer': employer,
            'title': title,
            'phone': phone,
            'email': email,
            'app_status': app_status
        })
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return formatted_results

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        select * from users
        """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    conn.close()
    return user

def get_user_by_userid(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        select * from users where id = %s
        """, (user_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results[0]

def delete_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        DELETE from users where id = %s
        """, (user_id,))    
    conn.commit()
    cursor.close()
    conn.close()
    return 'deleted'

def get_applications_by_jobid(job_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT applications.application_id, applications.date_applied, users.id AS user_id,
           users.username, jobs.title, jobs.phone, jobs.email, applications.app_status
    FROM applications
    INNER JOIN jobs ON applications.job_id = jobs.job_id
    INNER JOIN users ON applications.user_id = users.id
    WHERE jobs.job_id = %s;
""", (job_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
def get_job_id_by_app_id(app_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
   SELECT job_id FROM applications WHERE application_id=%s
""", (app_id,))
    job_id = cursor.fetchall()
    conn.close()
    cursor.close()
    return job_id[0]

def accept_app(application_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    job_id_dict = get_job_id_by_app_id(application_id)
    job_id = job_id_dict['job_id']
    cursor.execute("""
    UPDATE applications
    SET app_status = 'Accepted'
    WHERE application_id = %s;
""", (application_id,))
    cursor.execute("""
    UPDATE applications
    SET app_status = 'Rejected'
    WHERE application_id != %s AND job_id= %s;
""", (application_id,job_id))
    conn.commit()
    conn.close()
    cursor.close()
    
def reject_app(application_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    job_id_dict = get_job_id_by_app_id(application_id)
    cursor.execute("""
    UPDATE applications
    SET app_status = 'Rejected'
    WHERE application_id = %s;
""", (application_id,))
    conn.commit()
    conn.close()
    cursor.close()
    
def get_applications_by_app_id(app_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""SELECT * FROM applications WHERE application_id = %s;""", (app_id,))
    results = cur.fetchall()
    conn.close()
    return results[0]

def update_job(job_id,description):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""UPDATE jobs SET description = %s WHERE job_id = %s""", (description,job_id))
    conn.commit()
    cur.close()
    conn.close()
    
def update_user_details(user_id, username, bio, main_job):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""UPDATE users SET bio = %s,main_job=%s,username=%s  WHERE id = %s""", (bio,main_job,username,user_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_job(job_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""DELETE FROM jobs WHERE job_id=%s""", (job_id,))
    conn.commit()
    cur.close()
    conn.close()
    
def delete_app_by_id(app_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""DELETE FROM applications WHERE application_id=%s""", (app_id,))
    conn.commit()
    cur.close()
    conn.close()
    
def mark_job(job_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""UPDATE jobs SET status = 'Completed' WHERE job_id = %s""", (job_id,))
    conn.commit()
    cur.close()
    conn.close()
    
def  get_username_by_userid(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""SELECT username FROM users WHERE id=%s""", (user_id,))
    id = cur.fetchall()
    cur.close()
    conn.close()
    if id:
        return id[0][0]
    else:
        return 'Not Found'
print(get_username_by_userid(98))
    
    
