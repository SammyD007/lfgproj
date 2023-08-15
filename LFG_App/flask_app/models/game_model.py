from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request, session

db = 'LFG_app_schema'

class Game:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def submit_game(cls, data, user_id):
        query = '''INSERT INTO games (name, user_id)
        VALUES (%(name)s, %(user_id)s);'''
    
        data['user_id'] = user_id
        db_response = connectToMySQL(db).query_db(query, data)
        return db_response
    
    @classmethod
    def get_all_games(cls):
        query = '''SELECT * FROM games;'''
        db_response = connectToMySQL(db).query_db(query)
        return db_response
    
    @classmethod
    def get_game_id_by_name(cls, game_name):
        query = 'SELECT id FROM games WHERE name = %(game_name)s;'
        game_data = {'game_name': game_name}
        db_response = connectToMySQL(db).query_db(query, game_data)
        if db_response:
            return db_response[0]['id']
        return None

    
    @classmethod
    def get_results(cls, game_id):
        query = '''SELECT users.first_name AS user_name, games.name AS game_name
        FROM users
        JOIN user_has_games ON users.id = user_has_games.user_id
        JOIN games ON user_has_games.game_id = games.id
        WHERE games.id = %(game_id)s;'''
        db_response = connectToMySQL(db).query_db(query, {'game_id': game_id})
        return db_response
    
    @classmethod
    def add_game(cls, user_id, game_name):
        game_query = '''SELECT id FROM games WHERE name = %(game_name)s;'''
        game_data = {'game_name': game_name}
        game_result = connectToMySQL(db).query_db(game_query, game_data)

        if not game_result:
            print(f"Game '{game_name}' not found.")
            return

        game_id = game_result[0]['id']

        query = '''INSERT INTO user_has_games (user_id, game_id) VALUES (%(user_id)s, %(game_id)s);'''
        user_game_data = {'user_id': user_id, 'game_id': game_id}
        db_response = connectToMySQL(db).query_db(query, user_game_data)

        return db_response