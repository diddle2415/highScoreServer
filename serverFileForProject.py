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
        
def initializeInstructorDB():
    with sqlite3.connect("instructions.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS instructorSets (
                             id INTEGER PRIMARY KEY AUTOINCREMENT,           
                             name TEXT,
                             growthRate INTEGER
                             maxSize INTEGER
                             maxSeedCastDistance INTEGER
                             maxSeedNumber INTEGER
                             seedViability INTEGER
                             energyInputGrazer INTEGER
                             energyOutputGrazer INTEGER
                             energyToReproduceGrazer INTEGER
                             maintainSpeedGrazer INTEGER
                             maxSpeedGrazer INTEGER
                             maxSpeedHOD INTEGER
                             maxSpeedHOR INTEGER
                             maxSpeedHED INTEGER
                             maintainSpeedPredator INTEGER
                             energyOutputPredator INTEGER
                             energyToReproducePredator INTEGER
                             maxOffspring INTEGER
                             gestation INTEGER
                             offspringEnergy INTEGER
                        )''')
        
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

@app.route('/submitInstructions', methods=['POST'])
def submitInstructions():
    print("Submitting Instructor Limits")
    data = request.json
    name = data.get('name', "AAA")
    growthRate = data.get('growthRate', 1)
    maxSize = data.get('maxSize',1)
    maxSeedCastDistance = data.get('maxSeedCastDistance', 1)
    maxSeedNumber = data.get('maxSeedNumber', 1)
    seedViability = data.get('seedViability', 1)
    energyInputGrazer = data.get('energyInputGrazer', 1)
    energyOutputGrazer = data.get('energyOutputGrazer', 1)
    energyToReproduceGrazer = data.get('energyToReproduceGrazer', 1)
    maintainSpeedGrazer = data.get('maintainSpeedGrazer', 1)
    maxSpeedGrazer = data.get('maxSpeedGrazer', 1)
    maxSpeedHOD = data.get('maxSpeedHOD', 1)
    maxSpeedHOR = data.get('maxSpeedHOR', 1)
    maxSpeedHED = data.get('maxSpeedHED', 1)
    maintainSpeedPredator = data.get('maintainSpeedPredator', 1)
    energyOutputPredator = data.get('energyOutputPredator', 1)
    energyToReproducePredator = data.get('energyToReproducePredator', 1)
    maxOffspring = data.get('maxOffspring', 1)
    gestation = data.get('gestation', 1)
    offspringEnergy = data.get('offspringEnergy', 1)
    
    with sqlite3.connect("instructions.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO instructorSets (name, growthRate, maxSize, maxSeedCastDistance,maxSeedNumber, seedViability, energyInputGrazer, energyOutputGrazer, energyToReproduceGrazer, maintainSpeedGrazer, maxSpeedGrazer, maxSpeedHOD, maxSpeedHOR, maxSpeedHED, maintainSpeedPredator, energyOutputPredator, energyToReproducePredator, maxOffspring, gestation, offspringEnergy) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, growthRate, maxSize, maxSeedCastDistance,maxSeedNumber, seedViability, energyInputGrazer, energyOutputGrazer, energyToReproduceGrazer, maintainSpeedGrazer, maxSpeedGrazer, maxSpeedHOD, maxSpeedHOR, maxSpeedHED, maintainSpeedPredator, energyOutputPredator, energyToReproducePredator, maxOffspring, gestation, offspringEnergy))
        conn.commit()
    
    return jsonify({"message": "score submitted successfully"}), 200 #ok returned in the json

@app.route('/instructions', methods=['GET'])
def getInstructionPresets():
    with sqlite3.connect("instructions.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, growthRate, maxSize, maxSeedCastDistance,maxSeedNumber, seedViability, energyInputGrazer, energyOutputGrazer, energyToReproduceGrazer, maintainSpeedGrazer, maxSpeedGrazer, maxSpeedHOD, maxSpeedHOR, maxSpeedHED, maintainSpeedPredator, energyOutputPredator, energyToReproducePredator, maxOffspring, gestation, offspringEnergy FROM instructorSets ORDER BY name")
        instructorSets = cursor.fetchall()
        
    instructionsList = [{"name": i[0], "growthRate": i[1], "maxSize": i[2], "maxSeedCastDistance": i[3],"maxSeedNumber": i[4], "seedViability": i[5], "energyInputGrazer": i[6], "energyOutputGrazer": i[7], "energyToReproduceGrazer": i[8], "maintainSpeedGrazer": i[9], "maxSpeedGrazer": i[10], "maxSpeedHOD": i[11], "maxSpeedHOR": i[12], "maxSpeedHED": i[13], "maintainSpeedPredator": i[14], "energyOutputPredator": i[15], "energyToReproducePredator": i[16], "maxOffspring": i[17], "gestation": i[18], "offspringEnergy": i[19]} for i in instructorSets]
    return jsonify(instructionsList)

if __name__ == '__main__': #only run if being run on "main", or in other words if run directly
    initialize()
    initializeInstructorDB()
    app.run(host='0.0.0.0', port=5000) #run it on this machine on port 5000