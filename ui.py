from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Process the uploaded file
        file_read = pd.read_excel(filepath)
        clean_file = file_read.dropna()
        
        age_cols = clean_file["age"].tolist()
        speed_cols = clean_file["speed"].tolist()
        
        # Perform linear regression
        slope, intercept, r, p, std_error = stats.linregress(age_cols, speed_cols)
        
        def myfile(x):
            return slope * x + intercept
        
        model = list(map(myfile, age_cols))
        
        # Plot the data
        plt.scatter(age_cols, speed_cols, label='Data Points')
        plt.plot(age_cols, model, color='red', label='Regression Line')
        plt.xlabel('Age')
        plt.ylabel('Speed')
        plt.legend()
        
        # Save the plot to a file
        plot_filename = 'static/plot.png'
        plt.savefig(plot_filename)
        plt.close()
        
        return render_template('results.html', plot_url=plot_filename, slope=slope, intercept=intercept, r=r, p=p, std_error=std_error)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
