import os
import random
import pytz
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session,jsonify,session

from database import fetch_all_names_contributions,find_details,save_contribution

app = Flask(__name__)
app.secret_key = "os.environ.get('SECRET_KEY')"  # Change this to a random secret key



@app.route("/")
def index():

    pics = []
    for i in range(1,56):
        pics.append(f"{i}.jpg")

    return render_template("index.html",student=fetch_all_names_contributions(),profile_pics=pics)



@app.route("/profile-details/<string:id>", methods=["GET", "POST"])
def details(id):
    # Fetch the profile details based on the given ID
    profile_data = find_details(id)

    pic_number = random.choice(range(1, 56))


    
    if profile_data:
        # Pass the data to the profile.html template
        return render_template('profile.html', profile=profile_data,profile_pic=f"{pic_number}.jpg")
    else:
        return "Profile not found", 404


@app.route("/about-us")
def about_us():
    return render_template("aboutus.html")

@app.route("/admin", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check credentials
        if username == "neha" and password == "987654":
            session['user_type'] = 'NEHA '
            return redirect(url_for('contribute'))
        elif username == "afra" and password == "654321":
            session['user_type'] = 'AFRA'
            return redirect(url_for('contribute'))
        else:
            # Handle invalid credentials
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/contribute", methods=["GET", "POST"])
def contribute():
    user_type = session.get('user_type')
    if user_type is None:
        # Redirect to login if no user_type is found in session
        return redirect(url_for('login'))
    
    if request.method == "POST":
        data = request.json
        name = data.get('name')
        description = data.get('description')
        team = data.get('team')
        
        # Define the IST timezone
        ist = pytz.timezone('Asia/Kolkata')
        now_ist = datetime.now(ist)
        date = now_ist.strftime("%Y-%m-%d")
        
        success = save_contribution(name, description, team, date)
        
        if success:
            return jsonify({"message": "Contribution saved successfully!"}), 200
        else:
            return jsonify({"message": "Error saving contribution."}), 500

    # Pass user_type to the template
    return render_template("contribute.html", user_type=user_type)





if __name__ == "__main__":
    app.run(debug=True)
