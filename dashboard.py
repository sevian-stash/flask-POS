from flask import render_template, flash, redirect, url_for
from user import User
from model import Model

class Dashboard(object):
    User = User()
    Model = Model()
    
    def __init__(self):
        super(Dashboard, self).__init__()

    def read(self):
        return render_template('dashboard/index.html')
