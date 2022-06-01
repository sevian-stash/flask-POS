import base64
import json
from flask import render_template, flash, redirect, url_for, session
from model import Model
from user import User
from secret import Secret
from datetime import datetime, date

class Customer(object):
    User = User()
    Model = Model()
    
    def __init__(self):
        super(Customer, self).__init__()

    def add(self, name, address, phone, status):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'_READ')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))


        # Get User Count
        row_len = self.Model.read('ar01')
        row_len = len(row_len) + 1 if row_len else '1'

        self.Model.insert(
            'ar01', 
            {
                'AR_ID':f'AR-{row_len}',
                'AR_NAME':name,
                'AR_ADDRESS':address if address else '-',
                'AR_PHONE':phone if phone else 0,
                'AR_STATUS':f'{status}',
                'CRTD_DT':datetime.date(datetime.now()),
                'CRTD_BY':session_id
            }
        )

        return redirect(url_for('customer'))

    def read(self, id=None):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'_READ')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        data = []

        if id is None:
            # All Users
            data = self.Model.read('ar01',['AR_ID','AR_NAME','AR_ADDRESS'])
            return_path = 'customer/index.html'
        else:
            data.append(id)

            # Check if Exists
            db_ret = self.Model.read('ar01',['AR_STATUS'],{'AR_ID':id})

            print(db_ret)

            if db_ret != []:
                (*status,) = db_ret[0]
                data.append(','.join(status[0]))

                db_ret = self.Model.read('ar01','*',{'AR_ID':id})
                # Append Summary
                (*summary,) = db_ret[0]
                data.append(summary)

                # Append Details
                data.append(self.Model.read('iv11','*',{'IV_CUSTOMERID':id}))
                return_path = 'customer/detail.html'

            else:
                flash('ID Not Found')
                return redirect(url_for('customer'))
        print(data)
        return render_template(return_path, message=data)

    def update(self):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'_READ')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))


        return 

    def delete(self):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'_READ')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))


        return

# End Class/Method