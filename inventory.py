
class Inventory(object):
    
    def __init__(self):
        super(Inventory, self).__init__()

    def add(self, name, address, phone, email):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'AP','_CREATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))


        # Get User Count
        row_len = self.Model.read('ap01')
        row_len = len(row_len) + 1 if row_len else '1'

        self.Model.insert(
            'ap01', 
            {
                'AP_ID':f'SP-{row_len}',
                'AP_NAME':name if bool(name) else f'SP-{row_len}',
                'AP_ADDRESS':address,
                'AP_PHONE':phone if phone else 0,
                'AP_EMAIL':email,
                'CRTD_DT':datetime.date(datetime.now()),
                'CRTD_BY':session_id
            }
        )

        return redirect(url_for('supplier'))

    def read(self, id=None):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'AP','_READ')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        data = []

        if id is None:
            # All Users
            data = self.Model.read('ap01',['AP_ID','AP_NAME','AP_ADDRESS'])
            return_path = 'supplier/index.html'
        else:
            data.append(id)

            # Check if Exists
            db_ret = self.Model.read('ap01','*',{'AP_ID':id})

            if db_ret == []:
                flash('ID Not Found')
                return redirect(url_for('supplier'))

            # Append Summary
            (*summary,) = db_ret[0]
            data.append(summary)

            # Append Details
            data.append(self.Model.read('po11','*',{'PO_CUSTOMERID':id}))
            return_path = 'supplier/detail.html'

        return render_template(return_path, message=data)

    def update(self, id, name, address, phone, email):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'AP','_UPDATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        # Check if ID Exists
        db_ret = self.Model.read('ap01', ['AP_ID'],{'AP_ID':id})
        if db_ret == []:
            flash('ID Not Found')
            return redirect(url_for('supplier'))

        # Update New Value
        self.Model.update('ap01',
            {
                'AP_NAME':name if bool(name) else id,
                'AP_ADDRESS':address,
                'AP_PHONE':phone if bool(phone) else 0,
                'AP_EMAIL':email,
                'UPDT_DT':datetime.date(datetime.now()),
                'UPDT_BY':session_id
            },
            {'AP_ID':id}
        )

        return redirect(url_for('supplier'))

# End Class/Method