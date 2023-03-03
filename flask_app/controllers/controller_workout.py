from flask_app import app
from flask import render_template, session, request, redirect, flash
from flask_app.models.model_workout import Workout
from flask_app.models.model_exercise import Exercise
#Must import model but make sure you change the name


#Display Routes
@app.route("/")
def home():
	return render_template("home.html")


@app.route("/dashboard")
def dashboard():
	all_workouts = Workout.get_all()
	return render_template("dashboard.html", all_workouts = all_workouts)

@app.route("/myplan/<int:workout_id>")
def my_plan(workout_id):
	workout = Workout.get_one(workout_id)
	return render_template("myplan.html", workout = workout)

@app.route("/new/plan")
def new_plan():
	return render_template("newplan.html")

@app.route("/update/<int:workout_id>")
def update(workout_id):
	workout = Workout.get_one(workout_id)
	return render_template("update.html", workout = workout)

@app.route("/exercise/<int:workout_id>")
def exercise(workout_id):
	workout = Workout.get_one(workout_id)
	return render_template("exercise.html", workout = workout)




#Action Routes
@app.route("/save/workout", methods = ['POST'])
def save_workout():
	if not Workout.validate_workout(request.form):
		return redirect('/new/plan')
	Workout.save(request.form)
	return redirect("/dashboard")


@app.route("/update/workout/<int:workout_id>", methods = ['POST'])
def update_workout(workout_id):
	data = {
		'id' : workout_id,
		'name': request.form['name'],
		'description': request.form['description']
	}
	if not Workout.validate_workout(request.form):
		return redirect(f'/update/{workout_id}')
	
	Workout.update(data)
	return redirect("/dashboard")


@app.route('/workout/delete/<int:workout_id>')
def delete(workout_id):
    Workout.delete(workout_id)
    return redirect('/dashboard')


#action routes for exercises

@app.route("/save/exercise/<int:workout_id>", methods = ['POST'])
def save_exercise(workout_id):
	if not Exercise.validate_exercise(request.form):
		return redirect(f'/exercise/{workout_id}')
	workout = Workout.get_one(workout_id)
	session['name'] = request.form['name']
	session['muscle'] = request.form['muscle']
	session['sets'] = request.form['sets']
	session['workout_id'] = workout

	Exercise.save(session)
	return redirect(f"/myplan/{workout_id}")




@app.route('/workout/delete/<int:workout_id>')
def delete_exercise(workout_id):
    Workout.delete(workout_id)
    return redirect('/dashboard')



