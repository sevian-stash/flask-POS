import base64
from flask import render_template, flash, redirect, request, url_for, session
from model import Model
from secret import Secret
from datetime import datetime, date
from markupsafe import escape



class User(object):
    
    def __init__(self):
        super(User, self).__init__()
        self.model = Model()
        [self.db, self.db_cursor] = self.model.init()

    def add(self, user, password):
        # For register
        return_message = ''
        self.db_cursor.execute("SELECT US_PASSWORD FROM us01 WHERE US_NAME = %s", (user,))
        db_ret = self.db_cursor.fetchone()
        
        if db_ret is not None:
            flash('User with same username already exists')
            return redirect(url_for('login'))

        self.db_cursor.execute('SELECT * FROM us01')
        row_len = self.db_cursor.fetchall()
        row_len = len(row_len) + 1 if row_len else '1'
        hashed_pass = Secret.hash_password(password)
        
        self.db_cursor.execute(
            "INSERT INTO us01 (US_ID,US_NAME,US_PASSWORD,CRTD_DT,UPDT_DT,CRTD_BY,UPDT_BY) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            # Execute only capable of 4 args, use tuple for more
            (f'US-{row_len}',
                user,
                hashed_pass,
                datetime.date(datetime.now()),
                datetime.date(datetime.now()),
                '-',
                '-'
            )
        )
        self.db.commit()
        self.db_cursor.close()
        return redirect(url_for('login'))

    def read(self, id):
        if id is None:
            # Return all
            return 
        else:
            # return by id
            return
        return

    def update(self):
        return 

    def delete(self):
        return

    def login(self, user, password, path=None):
        return_message = ''
        self.db_cursor.execute("SELECT US_PASSWORD FROM us01 WHERE US_NAME = %s", (user,))
        db_ret = self.db_cursor.fetchone()

        # Check if registered
        if db_ret is None:
            flash('Not Registered Yet')
            return redirect(url_for('login'))

        # Check if password valid
        hashed_pass = db_ret[0]
        valid = Secret.check_password(password, hashed_pass)

        if not valid:
            flash('Wrong Password')
            return redirect(url_for('login'))

        # Session registration
        encoded_user = base64.b64encode(user.encode('utf-8'))
        session['uid'] = encoded_user.decode('utf-8')

        self.db_cursor.close()
        return path if path is not None else redirect(url_for('index'))

    def logout(self, path=None):
        if 'uid' in session:
            session.pop('uid', None)

        return True if path is None else path

    def is_logged_in(self, path=None):
        if 'uid' not in session:
            flash('Please login before using the app')
            return redirect(url_for('login'))

        return True if path is None else path
