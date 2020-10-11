from datetime import datetime
from time import time
from flask import current_app
from flask_login import UserMixin
from app import login


class User(UserMixin):

    def __init__(self,username):
        self.username=username

    def verify_ldap(self, password):
        if password == "yup":
            return True

    def get_id(self):
        return(self.username)

@login.user_loader
def load_user(username):
    return User(username)
