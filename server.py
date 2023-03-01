from flask_app import app
#import * ALL * controller files!!
from flask_app.controllers import controller_workout

    #must be at the bottom
    
if __name__=="__main__":
    app.run(debug=True)