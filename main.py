from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from config import update_password,mark_job, get_id_by_name,update_user_details, delete_app_by_id, delete_job, update_job,get_applications_by_app_id, reject_app,get_job_id_by_app_id, accept_app, get_applications_by_jobid, delete_user_by_id, get_user_by_userid,get_all_users,get_all_applications, switch_role, filter_search_jobs, search_jobs, get_job_by_job_id, update_email, get_chart_data, accepted_applications, pending_applications, total_applications, rejected_applications, reviewed_applications, get_user_info, insert_new_user, check_chat_exists, user_exists, get_chat_window, get_all_jobs, get_applications_by, get_search_results, get_messages, get_job_by_user_id, save_application, post_job_details, get_chat_list, insert_message, create_chat
from datetime import datetime
from math import ceil
from config import delete_user_by_email,check_chat_exists,get_user_by_email

app = Flask(__name__)
app.secret_key = "ihatesecretkeys"
alert = ''

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Get email and password from the form
        email = request.form.get('email')  # Use .get() to avoid KeyError
        password = request.form.get('password')

        # Check if email or password is missing
        if not email or not password:
            return render_template('login.html', login_alert="Email and password are required."), 400

        # Fetch user info from the database
        results = get_user_info(email, password)
        if results:
            user_id = results[0]
            email = results[3]
            session['username'] = results[1]
            session['password'] = results[2]
            session['email'] = email
            session['user_id'] = user_id
            session['user_role'] = results[4]
            session['user_bio'] = results[5]
            session['main_job'] = results[6]
            session['task_completed'] = results[7]
            session['user_age'] = results[8]
            session['location'] = results[9]
            session['phone'] = results[10]
            session['date_created'] = results[11]
            print(session)
            return redirect(url_for('dashboard'))
        else:
            # If credentials are incorrect
            return render_template('login.html', login_alert="Invalid username or password."), 401

    # For GET requests, render the login page
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print("Received Form Data:", request.form)  # Debugging
        
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']
        main_job = request.form['main_job']
        bio = request.form['bio']
        age = request.form['age']
        location = request.form['location']
        number = request.form['phone-number']
        confirm_password = request.form['confirm-password']
        username = first_name + last_name
        
        # Check if user already exists
        if not user_exists(username, email):
            if password != confirm_password:
                return render_template('login.html', signup_alert="The passwords do not match.")
            # Insert new user if everything is correct
            insert_new_user(username, password, email, role, main_job, bio, age, location, number)
            return redirect(url_for('login'))  # Corrected this line to reference the 'login' endpoint
        else:
            return render_template('login.html', signup_alert="User already exists.")
    
    return render_template('login.html')  # Ensure 'login.html' is the correct template for signup



@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    session.pop('user_id', None)
    session.pop('user_role', None)
    session.pop('main_job', None)
    session.pop('user_age', None)
    session.pop('phone', None)
    session.pop('date_created', None)
    session.pop('location', None)
    session.pop('task_completed', None)
    session.pop('user_bio', None)
    
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('index.html', css_file='css/index.css')


@app.route('/users')
def users():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    users = get_all_users()
    return render_template('users.html', js_file = 'js/users.js', user = session,app_users= users, css_file='css/users.css')



@app.route('/switch')
def switch():
    if 'username' not in session:
        return redirect(url_for('home'))
    switch_user_role = switch_role(session['user_id'],session['user_role'])
    if switch_user_role:
        if session['user_role'] == 'tasker':
            session['user_role'] = 'requester'
        elif session['user_role'] == 'requester': 
            session['user_role'] = 'tasker'
    return redirect(url_for('settings_others'))

@app.route('/filter_jobs', methods=['GET', 'POST'])
def filter_jobs():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        location = request.form.get('location', '')  # Default to an empty string if no location is provided
        budget = request.form.get('budget', 0)  # Get budget from the form, default to 0
        current_page = request.args.get('page', 1, type=int)
        rows_per_page = 9
        
        # Call the filtering function, passing location and budget
        all_jobs = filter_search_jobs(location, budget)
        total_jobs = len(all_jobs)
        total_pages = (total_jobs + rows_per_page - 1) // rows_per_page

        start_index = (current_page - 1) * rows_per_page
        end_index = start_index + rows_per_page
        paginated_jobs = all_jobs[start_index:end_index]
        
        return render_template(
            "dashboard.html",
            css_file="css/dashboard.css",
            user=session,
            jobs=paginated_jobs,
            current_page=current_page,
            total_pages=total_pages,
            js_file='js/dashboard.js'
        )

    return render_template('index.html', css_file='css/index.css')

@app.route('/search_for_jobs', methods= ['POST', 'GET'])
def search_for_jobs():
    if 'username' not in session:
        return redirect(url_for('home'))
   
    if request.method == 'POST':
        query = request.form['query']
        current_page = request.args.get('page', 1, type=int)
        rows_per_page = 9      
        all_jobs = search_jobs(query)
        total_jobs = len(all_jobs)
        total_pages = (total_jobs + rows_per_page -
                       1) // rows_per_page 

      
        start_index = (current_page - 1) * rows_per_page
        end_index = start_index + rows_per_page
        paginated_jobs = all_jobs[start_index:end_index]

        return render_template(
            "dashboard.html",
            css_file="css/dashboard.css",
            user = session,
            jobs=paginated_jobs,
            current_page=current_page,
            total_pages=total_pages,
            js_file = 'js/dashboard.js'
        )
        


@app.route('/search_result', methods=['POST'])
def search_result():
    if 'username' in session:
        if request.method == 'POST':
            query = request.form['tosearch']
            results = get_search_results(query)
            return render_template("search_results.html",user=session, results=results, css_file='css/search_results.css')


@app.route('/view_profile/<int:user_id>', methods=['GET', 'POST'])
def view_profile(user_id):
    if 'username' not in session:
        return redirect(url_for('home'))
    user_details = get_user_by_userid(user_id)
    return render_template('view-profile.html', user_details = user_details, user= session,  css_file='css/view-profile.css')

@app.route('/view_applications/<int:job_id>', methods=['GET', 'POST'])
def view_application(job_id):
    if 'username' not in session:
        return redirect(url_for('home'))
    user_details = get_applications_by_jobid(job_id)
    return render_template('view-application.html',applications = user_details, user_details = user_details, user= session,  js_file = 'js/application.js', css_file='css/application.css')

@app.route('/accept/<int:app_id>', methods=['GET', 'POST'])
def accept(app_id):
    if 'username' not in session:
        return redirect(url_for('home'))
    job_id_dict = get_job_id_by_app_id(app_id)
    job_id =job_id_dict['job_id']
    app=get_applications_by_app_id(app_id)
    if app['app_status']!= 'Rejected' and app['app_status']!='Accepted': 
        accept_app(app_id)
        return redirect(url_for('view_application',job_id = job_id ))
    else:
        return redirect(url_for('view_application',job_id = job_id ))
    
@app.route('/reject/<int:app_id>', methods=['GET', 'POST'])
def reject(app_id):
    if 'username' not in session:
        return redirect(url_for('home'))
    job_id_dict = get_job_id_by_app_id(app_id)
    job_id =job_id_dict['job_id']
    app=get_applications_by_app_id(app_id)
    if app['app_status']!= 'Accepted' and app['app_status']!='Rejected': 
        reject_app(app_id)
        return redirect(url_for('view_application',job_id = job_id ))
    else:
        return redirect(url_for('view_application',job_id = job_id ))
    
@app.route('/delete_profile/<int:user_id>', methods=['GET', 'POST'])
def delete_profile(user_id):
    if 'username' not in session:
        return redirect(url_for('home'))
    delete_user_by_id(user_id)
    return redirect(url_for('users'))

@app.route('/delete_application/<int:app_id>', methods=['GET', 'POST'])
def delete_application(app_id):
    if 'username' not in session:
        return redirect(url_for('home'))
    delete_app_by_id(app_id)
    return redirect(url_for('applications'))
    


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' in session:
        
        current_page = request.args.get('page', 1, type=int)
        rows_per_page = 9 

       
        all_jobs = get_all_jobs()
        total_jobs = len(all_jobs)
        total_pages = (total_jobs + rows_per_page -
                       1) // rows_per_page

        start_index = (current_page - 1) * rows_per_page
        end_index = start_index + rows_per_page
        paginated_jobs = all_jobs[start_index:end_index]

        return render_template(
            "dashboard.html",
            css_file="css/dashboard.css",
            user = session,
            jobs=paginated_jobs,
            current_page=current_page,
            total_pages=total_pages,
            js_file= 'js/dashboard.js'
        )
    else:
        return redirect(url_for('home'))


@app.route('/applications', methods=['GET'])
def applications():
    if 'username' in session:
        if session['user_role'] == 'admin':
            applications = get_all_applications()
            return render_template("application.html", user = session,js_file = 'js/application.js', css_file="css/application.css", applications=applications)
        applications = get_applications_by(session['user_id'])
        return render_template("application.html", user = session,js_file = 'js/application.js', css_file="css/application.css", applications=applications)
    else:
        return redirect(url_for('home'))


@app.route('/inbox/<int:chat_id>')
def inbox(chat_id):
    if 'user_id' not in session:
        return redirect('/')
    messages = get_messages(chat_id)
    return messages

@app.route('/chats')
def chats():
    if 'user_id' not in session:
        return redirect('/')
    chat_list = get_chat_list(session['user_id'])
    alert =  request.args.get('alert')
    return render_template('chat.html', chat_list=chat_list, alert = alert, user= session, css_file='css/messages.css')


@app.route('/tasks')
def tasks():
    if 'user_id' not in session:
        return redirect('/')
    user_jobs = get_job_by_user_id(session['user_id'])  
    per_page = 3  
    page = request.args.get('page', 1, type=int) 
    
    total_jobs = len(user_jobs)
    total_pages = ceil(total_jobs / per_page)
    
    # Slice the jobs for the current page
    start = (page - 1) * per_page
    end = start + per_page
    jobs_for_page = user_jobs[start:end]
    
    return render_template('tasks.html', user_jobs=jobs_for_page, page=page, total_pages=total_pages, user= session, css_file='css/tasks.css')



@app.route('/start_chat', methods=['POST', 'GET'])
def start_chat():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 403

    recipient_name = request.form['tosearch']
    recipient = recipient_name.strip()
    recipient_id = get_id_by_name(recipient)
    
    if recipient_id == "Not Found":
        return redirect(url_for('chats', alert = 'User Not Found'))
    sender_id = session['user_id']
    existing_chat = check_chat_exists(sender_id, recipient_id)
    existing_chat_data = existing_chat.get_json()
    print(existing_chat_data)
    if existing_chat_data.get("chat_id"):
        get_chat_window(existing_chat_data['chat_id'], session['user_id'])
        chat_list = get_chat_list(session['user_id'])
        return render_template('chat_window.html',
                               chat_id=chat['chat_id'],
                               chat_partner=chat['chat_partner'],
                               user_name=session['username'],
                               chat_description="Chatting with " +
                               chat['chat_partner'],
                               css_file='css/messages.css',
                               chat_list=chat_list,
                               user =session)
    # Create a new chat
    new_chat_id = create_chat(sender_id, recipient_id)
    if new_chat_id:
        chat = get_chat_window(new_chat_id, session['user_id'])
        chat_list = get_chat_list(session['user_id'])
        # Render the chat window with chat details
        return render_template('chat_window.html',
                               chat_id=chat['chat_id'],
                               chat_partner=chat['chat_partner'],
                               user_name=session['username'],
                               chat_description="Chatting with " +
                               chat['chat_partner'],
                               css_file='css/messages.css',
                               chat_list=chat_list,
                               user=session)
        # return jsonify({'chat_id': new_chat_id, 'message': 'Chat created successfully'}), 201
    else:
        return jsonify({'error': 'Failed to create chat'}), 500


@app.route('/chat/<int:chat_id>')
def chat_window(chat_id):
    if 'user_id' not in session:
        return redirect('/')
    chat = get_chat_window(chat_id, session['user_id'])
    chat_list = get_chat_list(session['user_id'])
    return render_template('chat_window.html',
                           chat_id=chat['chat_id'],
                           chat_partner=chat['chat_partner'],
                           user_name=session['username'],
                           chat_description="Chatting with " +
                           chat['chat_partner'],
                           css_file='css/messages.css',
                           chat_list=chat_list,
                           user= session)


@app.route('/messages/<int:chat_id>')
def messages(chat_id):
    if 'user_id' not in session:
        return redirect('/')
    chat_messages = get_messages(chat_id)
    return jsonify(chat_messages)


@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return "Unauthorized", 403

    data = request.get_json()  
    if not data or 'message' not in data or 'chat_id' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    chat_id = data['chat_id']
    message = data['message']

    insert_message(chat_id, session['user_id'], message)

@app.route('/statistics', methods=['GET'])
def statistics():
    if 'username' in session:
        total = total_applications(session['user_id'])
        accepted = accepted_applications(session['user_id'])
        pending = pending_applications(session['user_id'])
        rejected = rejected_applications(session['user_id'])
        reviewed = reviewed_applications(session['user_id'])
        accepted_percent = int((accepted/total)*100)
        pending_percent = int((pending/total)*100)
        rejected_percent = int((rejected/total)*100)
        reviewed_percent = int((reviewed/total)*100)

        applications = {
            'total': total,
            'accepted': accepted,
            'pending': pending,
            'rejected': rejected,
            'reviewed': reviewed,
            'accepted_percent': accepted_percent,
            'pending_percent': pending_percent,
            'rejected_percent': rejected_percent,
            'reviewed_percent': reviewed_percent
        }
        return render_template("statistics.html", css_file="css/statistics.css",user = session, js_file="js/statistics.js", applications=applications)
    else:
        return redirect(url_for('home'))


@app.route('/chart-data', methods=['GET'])
def chart_data():
    try:
        if 'username' not in session:
            return redirect(url_for('home'))
        data = get_chart_data(session['user_id'])
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'username' not in session:
        return redirect(url_for('home'))
    return redirect(url_for('settings_details'))


@app.route('/settings-details', methods=['GET', 'POST'])
def settings_details():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template('settings-details.html', user=session, css_file='css/view-profile.css', css_file2='css/settings.css' )

@app.route('/settings_others', methods=['GET', 'POST'])
def settings_others():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template('settings-others.html', user=session, css_file='css/settings-others.css', css_file2='css/settings.css' )


@app.route('/settings-profile', methods=['GET', 'POST'])
def settings_profile():
    if 'username' not in session:
        return redirect(url_for('home'))
    alert = ''
    success_alert = ''
    if request.method == 'POST': 
        username = request.form['username']
        bio = request.form['bio']
        main_job = request.form['job-title']
        
        # Check if required fields are filled
        if not username or not bio or not main_job:
            alert = "All fields are required."
        else:
            update_user_details(session['user_id'], username, bio, main_job)
            session['username'] = username  # Update session with new username
            success_alert = "Profile updated successfully."
    
    return render_template('settings-profile.html', user=session, success_alert=success_alert, alert=alert, css_file='css/settings.css')



@app.route('/settings_password', methods=['GET', 'POST'])
def settings_password():
    if 'username' not in session:
        return redirect(url_for('home'))
    alert = ''
    success_alert = ''
    if request.method == 'POST':
        old_pass = request.form['current-pass']
        new_pass = request.form['new-pass']
        confirm_pass = request.form['confirm-pass']
        
        # Validate inputs
        if not old_pass or not new_pass or not confirm_pass:
            alert = "All fields are required."
        elif new_pass != confirm_pass:
            alert = "The new passwords do not match."
        elif old_pass != session['password']:
            alert = "The current password is incorrect."
        elif new_pass == old_pass:
            alert = "The new password cannot be the same as the old password."
        else:
            # Update password
            update_password(session['user_id'], new_pass)
            session['password'] = new_pass  # Update session with new password
            success_alert = "Password changed successfully."
            return redirect(url_for('settings_password'))  # Refresh page
    
    return render_template('settings-password.html', success_alert=success_alert, alert=alert, user=session, css_file='css/settings-password.css', css_file2='css/settings.css')



@app.route('/settings-email', methods=['GET', 'POST'])
def settings_email():
    if 'username' not in session:
        return redirect(url_for('home'))
    alert = ''
    if request.method == 'POST':
        old_email = request.form['current-email']
        new_email = request.form['new-email']
        confirm_email  = request.form['confirm-email']
        if new_email == confirm_email: 
            if new_email != old_email:
                update_email(session['user_id'], new_email)
                alert = "Email Updated."
            else:
                alert = "The new email cannot be the same as old email."
        else: 
            alert = "The email doesn't match."
    return render_template('settings-email.html', alert = alert, user = session, css_file='css/settings-email.css', css_file2='css/settings.css')

@app.route('/settings_billings', methods = ['GET' , 'POST'])
def settings_billings():
    if 'username' not in session:
      return redirect(url_for('home'))
    return render_template('settings-billings.html', user= session, css_file='css/settings-billings.css',css_file2='css/settings.css')

@app.route('/payment/<int:job_id>', methods = ['GET' , 'POST'])
def payment(job_id):
    if 'username' not in session:
      return redirect(url_for('home'))
    alert = ""
    job = get_job_by_job_id(job_id)
    if request.method == 'POST':
        alert = "Payment Successful"
    return render_template('payment.html', job =job,alert= alert,user= session,css_file2='css/payment.css')


@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    if 'username' not in session:
        return redirect(url_for('home'))
    timestamp = datetime.now()
    user_id = session['user_id']
    date_applied = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    save_application(job_id, date_applied, user_id)
    if save_application:
        return redirect(url_for('view_job',job_id = job_id, alert = 'Your application has been submitted succesfully.'))
    else:
        return 'error fetching the data '


@app.route('/view_job/<int:job_id>', methods=['GET'])
def view_job(job_id):
    if 'username' not in session:
        return redirect(url_for('/'))
    alert = request.args.get('alert')   
    job = get_job_by_job_id(job_id)
    return render_template("view-job.html", alert = alert, job=job,user = session, css_file = 'css/view_job.css')

@app.route('/mark_complete/<int:job_id>', methods=['GET'])
def mark_complete(job_id):
    if 'username' not in session:
        return redirect(url_for('/'))
    mark_job(job_id)
    return redirect(url_for('view_job',job_id = job_id))

@app.route('/edit_post/<int:job_id>', methods=['GET','POST'])
def edit_post(job_id):
    if 'username' not in session:
        return redirect(url_for('/'))
    alert = request.args.get('alert')   
    job = get_job_by_job_id(job_id)
    if request.method == 'POST':
        description = request.form['job_description']
        update_job(job_id,description)
        return redirect(url_for('view_job', job_id=job_id))
    return render_template("edit-post.html", alert = alert, job=job,user = session, css_file = 'css/view_job.css')

@app.route('/delete_post/<int:job_id>', methods=['GET','POST'])
def delete_post(job_id):
    if 'username' not in session:
        return redirect(url_for('/'))
    alert = request.args.get('alert') 
    job = get_job_by_job_id(job_id) 
    delete_job(job_id)
    return redirect(url_for('tasks'))

from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

@app.route('/create_task', methods=['POST', 'GET'])
def create_task():
    if 'username' in session:
        if request.method == "POST":
            # Retrieving form data
            job_title = request.form.get('job-title')
            job_description = request.form.get('job-description')
            payment = request.form.get('job-salary')
            task_location = request.form.get('job-location')
            
            # Validating form fields to ensure they are not empty
            if not job_title or not job_description or not payment or not task_location:
                error_message = "All fields are required!"
                return render_template("create_task.html", user=session, error_message=error_message, css_file="css/create-tasks.css")
            
            # Get the current datetime
            current_datetime = datetime.now()
            task_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            
            # Calling the function to save task details (assumed to save into the database)
            post_job_details(job_title, job_description, payment, task_date, task_location, session['username'], session['user_id'], session['phone'], session['email'])
            
            # Redirect to the tasks page
            return redirect(url_for('tasks'))
        
        # Render task creation form if GET request
        return render_template("create_task.html", user=session, css_file="css/create-tasks.css")
    
    # If not logged in, redirect to login page
    return redirect(url_for('login'))


@app.route('/delete_user', methods=['POST'])
def delete_user():
    # Ensure the user is logged in (optional)
    if 'user_id' not in session:
        return redirect(url_for('home'))

    # Get email from form data
    email = request.form.get('email')
    if email:
        try:
            # Call the delete function to remove the user from the database
            delete_user_by_email(email)
            return "User deleted successfully", 200
        except Exception as e:
            return f"Error deleting user: {str(e)}", 500
    else:
        return "Email is required", 400


    


if __name__ == "__main__":
    app.run(debug=True)
