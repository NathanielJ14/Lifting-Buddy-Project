from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

# model the class after the friend table from our database
from flask_app.models import model_exercise


DB = "lifting_buddy_schema"

class Workout:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        

    @classmethod
    def save(cls , data):
        query = "INSERT INTO workouts (name, description, created_at , updated_at ) VALUES (%(name)s, %(description)s, NOW(),NOW());"
        workout_id = connectToMySQL(DB).query_db(query, data)
        return workout_id
    
    

    @staticmethod
    def validate_workout(workout):
        is_valid = True # we assume this is true

        if not workout["name"]:
            is_valid = False
            flash("Name is requried")
        
        if not workout["description"]:
            is_valid = False
            flash("Description is requried")
            
        return is_valid


    @classmethod
    def get_one(cls, workout_id):
        query = "SELECT * FROM workouts WHERE id = %(id)s"
        data = {'id': workout_id}
        results = connectToMySQL(DB).query_db(query, data) 
        return cls(results[0])
    
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM workouts;"
        results = connectToMySQL(DB).query_db(query)

        all_workouts = []
        for dict in results:
            all_workouts.append( cls(dict) )
        return all_workouts
    

    @classmethod
    def update(cls, data):
        query = "UPDATE workouts SET name = %(name)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query,data)
    
    @classmethod
    def delete(cls, workout_id):
        query = "DELETE FROM workouts WHERE id = %(id)s;"
        data = {"id": workout_id}
        return connectToMySQL(DB).query_db(query, data)