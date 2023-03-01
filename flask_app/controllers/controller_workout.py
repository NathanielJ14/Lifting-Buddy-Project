from flask_app import app
from flask import render_template, session, request, redirect
from flask_app.models.model_workout import Workout
#Must import model but make sure you change the name


#Display Routes
@app.route("/")
def home():
	return render_template("home.html")


@app.route("/dashboard")
def dashboard():
	all_workouts = Workout.get_all()
	return render_template("dashboard.html", all_workouts = all_workouts)

@app.route("/myplan")
def my_plan():
	return render_template("myplan.html")

@app.route("/new/plan")
def new_plan():
	return render_template("newplan.html")

@app.route("/update")
def update():
	return render_template("update.html")

@app.route("/exercise")
def exercise():
	return render_template("exercise.html")




#Action Routes
@app.route("/save/workout", methods = ['POST'])
def save_workout():
	if not Workout.validate_workout(request.form):
		return redirect('/new/plan')
	Workout.save(request.form)
	return redirect("/dashboard")