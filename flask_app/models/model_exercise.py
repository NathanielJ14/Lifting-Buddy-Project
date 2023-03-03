from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

# model the class after the friend table from our database
from flask_app.models import model_workout


DB = "lifting_buddy_schema"

class Exercise:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.muscle = data['muscle']
        self.sets = data['sets']
        self.workout_id = data['workout_id']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        

    @classmethod
    def save(cls , data):
        query = "INSERT INTO exercises (name, muscle, sets, workout_id, created_at , updated_at ) VALUES (%(name)s, %(muscle)s, %(sets)s, %(workout_id)s, NOW(),NOW());"
        exercise_id = connectToMySQL(DB).query_db(query, data)
        return exercise_id
    
    

    @staticmethod
    def validate_exercise(exercise):
        is_valid = True # we assume this is true

        if not exercise["name"]:
            is_valid = False
            flash("Exercise name is requried")
        
        if not exercise["muscle"]:
            is_valid = False
            flash("Muscle group is requried")

        if not exercise["sets"]:
            is_valid = False
            flash("Sets/Reps is requried")
            
        return is_valid


    @classmethod
    def get_one(cls, exercise_id):
        query = "SELECT * FROM exercise WHERE id = %(id)s"
        data = {'id': exercise_id}
        results = connectToMySQL(DB).query_db(query, data) 
        return cls(results[0])
    
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM exercises LEFT JOIN workouts ON exercises.workout_id = workouts.id;"
        results = connectToMySQL(DB).query_db( query)

        all_exercises = []
        for dict in results:
    
            workout_data = {
                "id" : dict["workouts.id"],
                "name" : dict["workouts.name"],
                "description" : dict["description"],
                "created_at" : dict["workouts.created_at"],
                "updated_at" : dict["workouts.updated_at"],
            }
            
            workout_instance = model_workout.Workout(workout_data)
            exercise = cls(dict)
            exercise.workout = workout_instance
            all_exercises.append(exercise)

        return all_exercises
    

    @classmethod
    def delete(cls, exercise_id):
        query = "DELETE FROM exercises WHERE id = %(id)s;"
        data = {"id": exercise_id}
        return connectToMySQL(DB).query_db(query, data)