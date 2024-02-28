from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Message:

    DB = 'private_wall_schema'

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.receiver_id = data['receiver_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None

    # CREATE
    @classmethod
    def save_message(cls, data):
        query = """
                INSERT INTO messages (user_id, receiver_id, content)
                VALUES (%(user_id)s, %(receiver_id)s, %(content)s )
                """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_all_messages_with_user(cls):
        query = """
            SELECT * FROM messages LEFT JOIN users on messages.user_id = users.id
            """
        results = connectToMySQL(cls.DB).query_db(query)
        all_messages = []
        for row_from_db in results:
            one_message = cls(row_from_db)
            user_data = {
                'id': row_from_db['users.id'],
                'first_name': row_from_db['first_name'],
                'last_name': row_from_db['last_name'],
                'email': row_from_db['email'],
                'password': row_from_db['password'],
                'created_at': row_from_db['users.created_at'],
                'updated_at': row_from_db['users.updated_at']
                }
            user_instance = user.User(user_data)
            one_message.owner = user_instance
            all_messages.append(one_message)
        return all_messages