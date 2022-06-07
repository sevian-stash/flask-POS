from flask import render_template, flash, redirect, url_for
from model import Model
from user import User

class Transaction(object):
    User = User()
    Model = Model()

    def __init__(self):
        super(Transaction, self).__init__()
        self.detail_row_len = 200
        self.category = ['Umpan','Peralatan','Lainnya']
        self.uom = ['M','Pcs','Ml']

    def read(self, id=None):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'SO','_READ')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        data = []

        data.append(self.category)
        data.append(self.uom)
        data.append(self.Model.read('iv01',['IV_ID', 'IV_NAME','IV_CATEGORY','IV_UOM','IV_QTY','IV_SELLPRICE']))
        data.append(f"SO-{len(self.Model.read('iv11')) + 1 if self.Model.read('iv11') else 1}")

        return_path = 'transaction/index.html'

        return render_template(return_path, message=data)

