#Imports 
import os
import pandas as pd
from flask import Flask, render_template, request 


app = Flask(__name__)           # creates the Flask application
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #making the path relative to the location of app.py
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")       # add an uploads folder setting, this stores the uploads folder inside the Flask app
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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
        
        #save the uploaded dataset
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename) # builds the file path. if the uploaded file name is sample_heart_data.csv the file_path becomes uploads/sample_heart_data.csv and file.save saved the uploaded file to the uploads folder
        file.save(file_path)

        #read the dataset 
        df = pd.read_csv(file_path)
        print(df.head())            # first 5 rows

        row_count = df.shape[0]     # get no. of rows
        column_count = df.shape[1]  # get no. of columns
        column_names = df.columns.tolist()
        preview_data = df.head().to_html(classes="data-table", index=False)

        missing_values = df.isnull().sum().to_dict() #check every column for missing values, turns each cell to T/F and counts the T values, then convert to dictionary 

        numeric_summary = df.describe().round(2).to_html(classes="data-table")

        return render_template(
            "results.html",
            filename=file.filename,
            row_count=row_count,
            column_count=column_count,
            column_names=column_names,
            preview_data=preview_data,
            missing_values=missing_values,
            numeric_summary=numeric_summary
        )
        
        print("Uploaded file:", file.filename)
        print("Saved to:", file_path)    # testing, to see in the terminal exactly where the file was saved

    return render_template("upload.html")




if __name__ == "__main__":
    app.run(debug=True)
