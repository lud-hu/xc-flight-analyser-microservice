import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import analyse_flight

# Some configurations
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'igc'}

# init app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper
def generateErrorJson(errorMessage):
    return { 'success': False, 'errorMessage': errorMessage }

@app.route('/')
def index():
    return "Nothing here."

# Route for analyzing a igc flight log file.
# Tries to get file from request, analyses it using xcsoar
# and returns JSON containing all analysed data.
@app.route('/analyse', methods=['POST'])
def analyse():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return str(request.files)
            # return generateErrorJson("No file parts are allowed.")

        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return generateErrorJson("No file was selected.")

        # check if file is not None and extension is allowed
        if file and allowed_file(file.filename):
            # Get file and save it
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            result = None

            # Analyse the file
            try:
                result = analyse_flight.analyse(filepath)
            except:
                return generateErrorJson('The file could not be analysed properly.')

            # Delete file after analyzation
            try:
                os.remove(filepath)
            except:
                return generateErrorJson('Something went wrong while deleting the file.')

            # return result JSON
            return result

        return "jo"


# Run app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))