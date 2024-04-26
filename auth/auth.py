import os
import sqlite3
from flask import redirect, url_for, session

def google_login(oauth):
    google = oauth.register(
        name='google',
        client_id= os.environ.get('GOOGLE_CLIENT_ID'),
        client_secret= os.environ.get('GOOGLE_CLIENT_SECRET'),
        access_token_url='https://oauth2.googleapis.com/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={'scope': 'openid email profile'},
        server_metadata_url= 'https://accounts.google.com/.well-known/openid-configuration'
    )
    return google

def login(oauth):
    google = google_login(oauth)
    google = oauth.create_client('google')
    redirect_uri = url_for('login_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

def authorize(oauth):
    google = google_login(oauth)
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo', token=token)
    user_info = resp.json()
    save_user_info(user_info)
    session['user_info'] = user_info
    
    setup_redirect = 'https://websenseai.netlify.app/setup'
    login_redirect = 'https://websenseai.netlify.app/login'
    if os.environ.get('FLASK_ENV') == 'development':
        setup_redirect = 'http://localhost:5173/setup'
        login_redirect = 'http://localhost:5173/login'
        

    if user_info is not None:
        return redirect(setup_redirect)
    else:
        return redirect(login_redirect)

def save_user_info(user_info):
    try:
        conn = sqlite3.connect('./db_config/config_database.db')

        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users_info
            (email text, family_name text, given_name text, id text, locale text, name text, picture text, verified_email boolean, bot_id text)
        ''')

        # check if the user is already in the database
        c.execute("SELECT * FROM users_info WHERE id = ?", (user_info.get('id'),))
        row = c.fetchone()

        if row is None:
            c.execute("INSERT INTO users_info VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                        user_info.get('email'), 
                        user_info.get('family_name'),
                        user_info.get('given_name'), 
                        user_info.get('id'), 
                        user_info.get('locale'), 
                        user_info.get('name'), 
                        user_info.get('picture'), 
                        user_info.get('verified_email'), 
                        ""
                        )
            )
        else:
            print("ID is already in the database")

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")