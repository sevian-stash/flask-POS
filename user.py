import base64
import json
from flask import render_template, flash, redirect, request, url_for, session
from model import Model
from secret import Secret
from datetime import datetime, date
from markupsafe import escape



class User(object):
    
    def __init__(self):
        super(User, self).__init__()
        self.module_id = ['AP','AR','IV','PR','US']
        self.module_type = ['_CREATE','_READ','_UPDATE','_DELETE']
        self.model = Model()
        [self.db, self.db_cursor] = self.model.init()

    def add(self, user, password):
        # For register

        # Check for Duplicate
        db_ret = self.model.read('us01','*',{'US_NAME':user})
        
        if db_ret != []:
            flash('User with same username already exists')
            return redirect(url_for('login'))

        # Get User Count
        row_len = self.model.read('us01')
        row_len = len(row_len) + 1 if row_len else '1'
        hashed_pass = Secret.hash_password(password)
        
        # For User Summary
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

        # For User Permissions 
        for id in self.module_id:
            self.db_cursor.execute(
                "INSERT INTO us02 (US_ID,US_MODULEID,US_CREATE,US_READ,US_UPDATE,US_DELETE,CRTD_DT,UPDT_DT,CRTD_BY,UPDT_BY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (f'US-{row_len}',
                    id,
                    int(False),int(False),int(False),int(False),
                    datetime.date(datetime.now()),
                    datetime.date(datetime.now()),
                    '-',
                    '-'
                )
            )

        try:
            self.db.commit()
        except Exception as e:
            raise e
            flash(e)
        finally:
            return redirect(url_for('login'))

    def read(self, id=None):
        session_id = self.get_session_id()
        # Status Check
        account_status = self.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.is_allowed(session_id,'_READ')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        return_path = ''
        data = []

        if id is None:
            # All Users
            data = self.model.read('us01',['US_ID','US_NAME'])
            return_path = 'user/index.html'

        else:
            data.append(id)

            # Check if Exists
            db_ret = self.model.read('us01','*',{'US_ID':id})

            if db_ret != []:
                # Append Summary
                (*summary,) = db_ret[0]
                data.append(summary)

                # Append Details
                data.append(self.model.read('us02','*',{'US_ID':id}))
                return_path = 'user/detail.html'

            else:
                flash('ID Not Found')
                return redirect(url_for('user'))

        return render_template(return_path, message=data)

    def update(self, id=None, new_username=None, new_permission=None, password=None):
        session_id = self.get_session_id()
        # Status Check
        account_status = self.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.is_allowed(session_id,'_UPDATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('user'))

        # Update User Account
        if password is None:
            # Only Update if Changed
            old_username = self.model.read('us01',['US_NAME'],{'US_ID':id})[0][0]

            if old_username != new_username:
                self.model.update('us01',
                    {'US_NAME':new_username, 'UPDT_BY':session_id, 'UPDT_DT':datetime.date(datetime.now())},
                    {'US_ID':id})

            # Get Current Permission
            db_ret = self.model.read('us02',['US_CREATE','US_READ','US_UPDATE','US_DELETE'],{'US_ID':id})
            current_permission = dict()

            for idx,item in enumerate(self.module_id):
                current_permission.update({item:{
                        '_CREATE':bool(db_ret[idx][0]),
                        '_READ':bool(db_ret[idx][1]),
                        '_UPDATE':bool(db_ret[idx][2]),
                        '_DELETE':bool(db_ret[idx][3])
                    }
                })

            for module_id in new_permission:
                for module_status in new_permission[module_id].items():
                    # Only Update if Changed
                    if current_permission[module_id][module_status[0]] != new_permission[module_id][module_status[0]]:
                        self.model.update('us02',
                            {f'US{module_status[0]}':int(module_status[1]), 'UPDT_BY':session_id, 'UPDT_DT':datetime.date(datetime.now())},
                            {'US_ID':id,'US_MODULEID':module_id})
 
        # Update User Password (Must be Separated)
        else:
            if len(password) < 8:
                flash('Failed to Change Password (Minimum 8 characters)')
                return redirect(url_for('user'))

            hashed_pass = Secret.hash_password(password)
            self.model.update('us01',
                {'US_PASSWORD':hashed_pass, 'UPDT_DT':datetime.date(datetime.now()), 'UPDT_BY':session_id},
                {'US_ID':id})
            
        self.db.commit()
        flash('Successfully saved')

        return redirect(url_for('user'))

    def login(self, user, password):
        # Check if registered
        db_ret = self.model.read('us01', ['US_ID','US_PASSWORD','US_ACTIVE'], {'US_NAME':user})[0]
        if db_ret == []:
            flash('Not Registered Yet')
            return redirect(url_for('login'))

        # Check if User Active
        if db_ret[2] == 0:
            flash('Account is Deactivated. Please Contact Administrator')
            return redirect(url_for('login'))

        # Check if password valid
        id = db_ret[0]
        hashed_pass = db_ret[1]
        valid = Secret.check_password(password, hashed_pass)

        if not valid:
            flash('Wrong Password')
            return redirect(url_for('login'))

        # Session registration
        encoded_id = base64.b64encode(id.encode('utf-8'))
        session['uid'] = encoded_id.decode('utf-8')

        return redirect(url_for('index'))

    def deactivate(self, id):
        session_id = self.get_session_id()
        # Status Check
        account_status = self.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.is_allowed(session_id,'_DELETE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('user'))

        self.model.update('us01', {'US_ACTIVE':int(False)},{'US_ID':id})

        # If Deactivate Own Account, Logout
        if session_id == id:
            return redirect(url_for('logout'))
        
        flash('Account Deactivated')

        self.db.commit()
        return redirect(url_for('user'))

    def activate(self, id):
        session_id = self.get_session_id()
        # Status Check
        account_status = self.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.is_allowed(session_id,'_CREATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('user'))

        self.model.update('us01', {'US_ACTIVE':int(True)},{'US_ID':id})

        # If Deactivate Own Account, Logout
        if session_id == id:
            return redirect(url_for('logout'))
        
        flash('Account Activated')

        self.db.commit()
        return redirect(url_for('user'))

    def logout(self, path=None):
        if 'uid' in session:
            session.pop('uid', None)

        return True if path is None else path

    def is_logged_in(self):
        validity = True
        if 'uid' not in session:
            flash('Please login before using the app')
            validity = False

        return validity

    def get_session_id(self):
        if 'uid' not in session:
            return None
        id = session['uid'].encode('utf-8')
        id = base64.b64decode(id)

        return id.decode('utf-8')

    def is_allowed(self, id, permission):
        (*permission_status,) = self.model.read('us02', [f'US{permission.capitalize()}'],{'US_ID':id})[0]
        permission_status = permission_status[0]

        return bool(permission_status)

    def is_active(self, id):
        (*active_status,) = self.model.read('us01', ['US_ACTIVE'],{'US_ID':id})[0]
        active_status = active_status[0]

        return bool(active_status)
