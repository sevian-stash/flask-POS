from flask import render_template, flash, redirect, url_for
from model import Model
from user import User
from datetime import datetime, date

class Inventory(object):
    User = User()
    Model = Model()
    
    def __init__(self):
        super(Inventory, self).__init__()

    def add(self, name, category, qty, sell_price, buy_price, uom):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'IV','_CREATE')
        if not access_permission:
            flash("Not Allowed")
            return redirect(url_for('inventory'))


        # Get User Count
        row_len = self.Model.read('iv01')
        row_len = len(row_len) + 1 if row_len else '1'

        model_status = self.Model.insert(
            'iv01', 
            {
                'IV_ID':f'IV-{row_len}',
                'IV_NAME':name if bool(name) else f'IV-{row_len}',
                'IV_CATEGORY':category if str(category) != 'None' else 3,
                'IV_QTY':qty if bool(qty) else 0,
                'IV_SELLPRICE':sell_price if bool(sell_price) else 0,
                'IV_BUYPRICE':buy_price if bool(buy_price) else 0,
                'IV_UOM':uom if str(uom) != 'None' else 2,
                'IV_ACTIVE':bool(True),
                'CRTD_DT':datetime.date(datetime.now()),
                'CRTD_BY':session_id
            }
        )

        if model_status != 0:
            flash(f'Failed to Add Inventory')
            return redirect(url_for('inventory'))

        flash(f'IV-{row_len} has been Created')

        return redirect(url_for('inventory'))

    def read(self, id=None):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'IV','_READ')
        if not access_permission:
            flash("Not Allowed")
            return redirect(url_for('index'))

        data = []

        if id is None:
            # All Users
            data = self.Model.read('iv01',['IV_ID','IV_NAME','IV_QTY','IV_SELLPRICE'])
            return_path = 'inventory/index.html'
        else:
            data.append(id)

            # Check if Exists
            db_ret = self.Model.read('iv01','*',{'IV_ID':id})

            if db_ret == []:
                flash('ID Not Found')
                return redirect(url_for('inventory'))

            # Append Summary
            (*summary,) = db_ret[0]
            data.append(summary)

            # Append Details
            data.append(self.Model.read(
                'po11 p1 LEFT JOIN po12 p2 ON p2.PO_ID = p1.PO_ID LEFT JOIN ap01 ap ON ap.AP_ID = p1.PO_CUSTOMERID',
                ['p1.PO_ID','ap.AP_NAME','p2.PO_ITEMQTY','p2.PO_ITEMPRICE','p1.CRTD_DT','p1.CRTD_BY'],
                {'p2.PO_ITEMID':id}
            ))
            data.append(self.Model.read(
                'iv11 i1 LEFT JOIN iv12 i2 ON i2.IV_ID = i1.IV_ID LEFT JOIN ar01 ar ON i1.IV_CUSTOMERID = ar.AR_ID',
                ['i1.IV_ID','ar.AR_NAME','i2.IV_ITEMQTY','i2.IV_ITEMPRICE','i1.CRTD_DT','i1.CRTD_BY'],
                {'i2.IV_ITEMID':id}
            ))
            return_path = 'inventory/detail.html'

        return render_template(return_path, message=data)

    def update(self, id, name, category, qty, buy_price, sell_price, uom):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'IV','_UPDATE')
        if not access_permission:
            flash("Not Allowed")
            return redirect(url_for('inventory'))

        # Check if ID Exists
        db_ret = self.Model.read('iv01', ['IV_ID'],{'IV_ID':id})
        if db_ret == []:
            flash('ID Not Found')
            return redirect(url_for('inventory'))

        # Check if Item Active
        item_status = self.is_item_active(id)
        if not item_status:
            flash("Item is Inactive")
            return redirect(url_for('inventory'))

        # Update New Value
        self.Model.update('iv01',
            {
                'IV_NAME':name if bool(name) else f'IV-{row_len}',
                'IV_CATEGORY':category,
                'IV_QTY':qty if bool(qty) else 0,
                'IV_BUYPRICE':buy_price if bool(buy_price) else 0,
                'IV_SELLPRICE':sell_price if bool(sell_price) else 0,
                'IV_UOM':uom,
                'UPDT_DT':datetime.date(datetime.now()),
                'UPDT_BY':session_id
            },
            {'IV_ID':id}
        )

        flash(f'{id} has been Updated')

        return redirect(url_for('inventory'))

    def deactivate(self, id):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'IV','_DELETE')
        if not access_permission:
            flash("Not Allowed")
            return redirect(url_for('inventory'))

        self.Model.update('iv01', {'IV_ACTIVE':int(False)},{'IV_ID':id})

        flash(f'{id} Inventory Deactivated')

        return redirect(url_for('inventory'))

    def activate(self, id):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'IV','_CREATE')
        if not access_permission:
            flash("Not Allowed")
            return redirect(url_for('inventory'))

        self.Model.update('iv01', {'IV_ACTIVE':int(True)},{'IV_ID':id})

        # If Deactivate Own Account, Logout
        if session_id == id:
            return redirect(url_for('logout'))
        
        flash(f'{id} Inventory Activated')

        return redirect(url_for('inventory'))

    def is_item_active(self, id):
        (*active_status,) = self.Model.read('iv01', ['IV_ACTIVE'],{'IV_ID':id})[0]
        active_status = active_status[0]

        return bool(active_status)

# End Class/Method