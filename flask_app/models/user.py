from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import message
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:

    DB = 'private_wall_schema'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.messages = []

    # VALIDATIONS
    @staticmethod
    def validate_user(user):
        special_sym = ['$', '@', '#', '%']

        is_valid = True

        if len(user['first_name'].strip()) < 3:
            is_valid = False
            flash ("First Name must be at least 3 characters")
        if len(user['last_name'].strip()) < 3:
            is_valid = False
            flash("Last Name must be at least 3 characters")
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user['password'].strip()) < 8:
            is_valid = False
            flash("Password must be at least 8 characters in length")
        if not any(char.isdigit() for char in user['password']):
            flash('Password should have at least one numeral')
            is_valid = False
        if not any(char.isupper() for char in user['password']):
            flash('Password should have at least one uppercase letter')
            is_valid = False
        if not any(char.islower() for char in user['password']):
            flash('Password should have at least one lowercase letter')
            is_valid = False
        if not any(char in special_sym for char in user['password']):
            flash('Password should have at least one of the symbols $@#')
            is_valid = False
        if not user['password'] == user['confirm_password']:
            is_valid = False
            flash('Passwords do not match')
        return is_valid
    
    # CREATE
    @classmethod
    def save_user(cls, data):
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
                """
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    # READ 
    @classmethod
    def get_by_email(cls, data):
        query = """
                SELECT * FROM users WHERE email = %(email)s;
                """
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_one_user(cls, user_id):
        query = """SELECT * FROM users WHERE id = %(id)s"""
        data = {
            'id': user_id
        }
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])