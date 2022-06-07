from flask import render_template, flash, redirect, url_for
from model import Model
from user import User
from account_payable import Account_Payable
from datetime import datetime, date, timedelta

class Purchase_Order(object):
    User = User()
    Model = Model()
    Account_Payable = Account_Payable()

    def __init__(self):
        super(Purchase_Order, self).__init__()
        self.detail_row_len = 200

    def add(self, data):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'PO','_CREATE')
        if not access_permission:
            flash("Not Allowed")
            return redirect(url_for('purchase_order'))

        # Supplier Check
        supplier = self.Model.read('ap01', ['AP_ID'], {'AP_ID':data['po11']['PO_CUSTOMERID']})
        if supplier == []:
            flash("Supplier not Found")
            return redirect(url_for('purchase_order'))

        # Get User Count
        row_len = self.Model.read('po11')
        row_len = len(row_len) + 1 if row_len else '1'

        # Insert Summary
        model_status = self.Model.insert(
            'po11', 
            {
                'PO_ID':f'PO-{row_len}',
                'PO_CUSTOMERID': data['po11']['PO_CUSTOMERID'],
                'PO_QTY': data['po11']['PO_QTY'] if bool(data['po11']['PO_QTY']) else 0,
                'PO_AMOUNT': data['po11']['PO_AMOUNT'] if bool(data['po11']['PO_AMOUNT']) else 0,
                'PO_STATUS': data['po11']['PO_STATUS'] if str(data['po11']['PO_STATUS']) != 'None' else '1',
                'CRTD_DT':datetime.date(datetime.now()),
                'CRTD_BY':session_id
            }
        )

        if model_status != 0:
            flash(f'Failed to Add Purchase Order')
            return redirect(url_for('purchase_order'))

        # Insert Detail
        for key in data['po12']:
            # Item Check
            item = self.Model.read('iv01', ['IV_ID'], {'IV_ID':data['po12'][key]['PO_ITEMID']})
            
            if item != []:
                model_status = self.Model.insert(
                    'po12', 
                    {
                        'PO_ID':f'PO-{row_len}',
                        'PO_ITEMID': data['po12'][key]['PO_ITEMID'],
                        'PO_ITEMNAME': data['po12'][key]['PO_ITEMNAME'],
                        'PO_ITEMPRICE': data['po12'][key]['PO_ITEMPRICE'] if bool(data['po12'][key]['PO_ITEMPRICE']) else 0,
                        'PO_ITEMQTY': data['po12'][key]['PO_ITEMQTY'] if bool(data['po12'][key]['PO_ITEMQTY']) else 0,
                        'UPDT_DT':datetime.date(datetime.now()),
                        'UPDT_BY':session_id
                    }
                )

                if model_status != 0:
                    flash(f'Failed to Add Purchase Order')
                    return redirect(url_for('purchase_order'))

        flash(f'PO-{row_len} has been Created')

        return self.account_payable_add(f'PO-{row_len}', data)

    def read(self, id=None):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'PO','_READ')
        if not access_permission:
            flash("Not Allowed")
            return redirect(url_for('index'))

        data = []

        if id is None:
            # All Users
            data = self.Model.read(
                'po11 po LEFT JOIN ap01 ap ON po.PO_CUSTOMERID = ap.AP_ID',
                ['po.PO_ID','ap.AP_NAME','po.PO_AMOUNT', 'po.CRTD_DT'])

            return_path = 'purchase_order/index.html'

        else:
            data.append(id)

            # Check if Exists
            db_ret = self.Model.read('po11','*',{'PO_ID':id})

            if db_ret == []:
                flash('ID Not Found')
                return redirect(url_for('purchase_order'))

            # Append Summary
            (*summary,) = db_ret[0]
            data.append(summary)

            # Append Details
            data.append(self.Model.read('po12','*',{'PO_ID':id}))
            data.append(self.detail_row_len)

            return_path = 'purchase_order/detail.html'

        return render_template(return_path, message=data)

    def update(self, data):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'PO','_UPDATE')
        if not access_permission:
            flash("Not Allowed")
            return redirect(url_for('purchase_order'))

        # Check if ID Exists
        db_ret = self.Model.read('po11', ['PO_ID'],{'PO_ID':data['po11']['PO_ID']})
        if db_ret == []:
            flash('ID Not Found')
            return redirect(url_for('purchase_order'))

        # Update New Value
        model_status = self.Model.update('po11',
            {
                'PO_CUSTOMERID':data['po11']['PO_CUSTOMERID'],
                'PO_QTY': data['po11']['PO_QTY'] if bool(data['po11']['PO_QTY']) else 0,
                'PO_AMOUNT': data['po11']['PO_AMOUNT'] if bool(data['po11']['PO_AMOUNT']) else 0,
                'PO_STATUS': data['po11']['PO_STATUS'] if str(data['po11']['PO_STATUS']) != 'None' else '1',
                'UPDT_DT':datetime.date(datetime.now()),
                'UPDT_BY':session_id
            },
            {'PO_ID':data['po11']['PO_ID']}
        )

        if model_status != 0:
            flash('Failed to Save')
            return redirect(url_for('purchase_order'))

        model_status = self.Model.delete('po12',{'PO_ID':data['po11']['PO_ID']})

        if model_status != 0:
            flash('Failed to Save')
            return redirect(url_for('purchase_order'))

        for item in data['po12']:
            model_status = self.Model.insert('po12',
                {
                    'PO_ID':data['po12'][item]['PO_ID'],
                    'PO_ITEMID':data['po12'][item]['PO_ITEMID'],
                    'PO_ITEMNAME':data['po12'][item]['PO_ITEMNAME'],
                    'PO_ITEMPRICE': data['po12'][item]['PO_ITEMPRICE'] if bool(data['po12'][item]['PO_ITEMPRICE']) else 0,
                    'PO_ITEMQTY': data['po12'][item]['PO_ITEMQTY'] if bool(data['po12'][item]['PO_ITEMQTY']) else 0,
                    'UPDT_DT':datetime.date(datetime.now()),
                    'UPDT_BY':session_id
                }
            )

            if model_status != 0:
                flash('Failed to Save')

        if model_status == 0:
            flash(f'{data["po11"]["PO_ID"]} has been Updated')

        return redirect(url_for('purchase_order'))

    def activate(self, id):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'PO','_CREATE')
        if not access_permission:
            flash("Not Allowed")
            return redirect(url_for('purchase_order'))

        # Check if ID Exists
        db_ret = self.Model.read('po11', ['PO_ID'],{'PO_ID':id})
        if db_ret == []:
            flash('ID Not Found')
            return redirect(url_for('purchase_order'))

        # Update New Value
        model_status = self.Model.update('po11',
            {
                'PO_STATUS': '2',
                'UPDT_DT':datetime.date(datetime.now()),
                'UPDT_BY':session_id
            },
            {'PO_ID':id}
        )

        if model_status != 0:
            flash('Failed to Save')
            return redirect(url_for('purchase_order'))

        flash(f'{id} Activated')

        return redirect(url_for('purchase_order'))

    # Sync with AP
    def account_payable_add(self, id, data):
        # Get User Count
        row_len = self.Model.read('ar11')
        row_len = len(row_len) + 1 if row_len else '1'

        ap_data = dict()

        print(id)
        # Insert Summary
        ap_duedt = datetime.date(datetime.now() + timedelta(days=7))
        ap_duedt = datetime.strptime(str(ap_duedt),'%Y-%m-%d').strftime('%d/%m/%Y')
        ap_data.update({'ap11':
            {
                'AP_CUSTOMERID': data['po11']['PO_CUSTOMERID'],
                'AP_PURCHASEORDERID': id,
                'AP_AMOUNT': data['po11']['PO_AMOUNT'] if bool(data['po11']['PO_AMOUNT']) else 0,
                'AP_QTY': data['po11']['PO_QTY'] if bool(data['po11']['PO_QTY']) else 0,
                'AP_STATUS': '2',
                'AP_DUEDT': ap_duedt
            }
        })

        # Insert Detail
        ap_data.update({'ap12': {}})
        for idx,key in enumerate(data['po12']):
            ap_data['ap12'].update({f'row_{idx}': {
                'AP_ITEMID':data['po12'][key]['PO_ITEMID'],
                'AP_ITEMNAME':data['po12'][key]['PO_ITEMNAME'],
                'AP_ITEMQTY':data['po12'][key]['PO_ITEMPRICE'] if bool(data['po12'][key]['PO_ITEMPRICE']) else 0,
                'AP_ITEMPRICE':data['po12'][key]['PO_ITEMQTY'] if bool(data['po12'][key]['PO_ITEMQTY']) else 0
                }
            })

        self.Account_Payable.add(ap_data)

        return redirect(url_for('purchase_order'))
