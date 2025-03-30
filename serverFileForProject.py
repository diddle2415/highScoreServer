#Andrew Alfano, 3/20/2025
#File for the server that will host the highscore database
#Simple, sqlite3 is used to make the database itself and flask is used for server stuff
#Takes a score from the game, sorts it into the database, and can return a json of the top 10 of the list to be printed

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__) #create a flask server instance
CORS(app)

def initialize(): #initialize database
    with sqlite3.connect("highscores.db") as conn: #creates the databse file
        cursor = conn.cursor() #used for interacting with entries in the db
        cursor.execute('''CREATE TABLE IF NOT EXISTS scores (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            score INTEGER,
                            name TEXT
                          )''')
        #line above explained: Create structure if it hasnt been made already, 
        #give things an id, which is an integer that automatically increments,
        #create an entry for a score, which is just an integer
        conn.commit() #commit changes
        
        
@app.route('/submitScore', methods=['POST']) #called to submit a new score to the database
def submitScore():
    print("Submitting a score")
    data = request.json
    score = data.get('score')
    name = data.get('name', 'AAA') #default name is AAA in case no name is recieved. Shouldnt happen because AAA is also default in godot

    if score is None: #if request contains no score
        return jsonify({"error": "Invalid data"}), 400 #invalid data code returned in the json

    with sqlite3.connect("highscores.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO scores (score, name) VALUES (?, ?)", (score, name)) #inserts the new entry into the structure
        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM scores") 
        totalScores = cursor.fetchone()[0] #grab the amount of saved scores from the database

        if totalScores > 12:
            cursor.execute("DELETE FROM scores WHERE score = (SELECT MIN(score) FROM scores)") #delete the lowest score
            conn.commit #doing it this way to ensure scores dont get stopped from being added to the list
            print("score purged") #testing to see if this shows up in server logs

    return jsonify({"message": "score submitted successfully"}), 200 #ok returned in the json

#called to get top scores
@app.route('/highScores', methods=['GET']) #called to take scores to print as the highscore list in game
def getHighscores():
    print("Getting high scores")
    with sqlite3.connect("highscores.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT score, name FROM scores ORDER BY score DESC LIMIT 10") #pull top 10 scores from list
        scores = cursor.fetchall()

    scoreList = [{"score": s[0], "name": s[1]} for s in scores] #format the scores as a dictionary, which is what godot code expects
    return jsonify(scoreList) #return a json file of all the scores

if __name__ == '__main__': #only run if being run on "main", or in other words if run directly
    initialize()
    app.run(host='0.0.0.0', port=5000) #run it on this machine on port 5000
