#Imports 
from flask import Flask, render_template, request 

app = Flask(__name__)           # creates the Flask application


@app.route("/")                 # creates a route. "/" is the homepage
def home():                     
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])               
def upload(): 

    if request.method == "POST":

        if "dataset" not in request.files:
            print("No file part")
            return render_template("upload.html")
        
        file = request.files["dataset"] # when file is submitted Flask stores uploaded files in request.files

        if file.filename == "":
            print("No file selected")   # testing, when user uploads a file, the terminal will show the file name
            return render_template("upload.html")
        
        print("Uploaded file:", file.filename)

    return render_template("upload.html")




if __name__ == "__main__":
    app.run(debug=True)