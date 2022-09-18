

# NAME @: Shruti Sawant
# TOPIC @: Risk Analytics Model Deployment
# DATE @: 17/09/2022


# IMPORT THE DEPENDENCIES 

from flask import (Flask, 
                   render_template, 
                   session, redirect, 
                   url_for, request,
                   jsonify)
 
from helper_functions import (svc_pickle_model,
                              svc_scaler,
                              return_prediction,
                              InfoForm)




app = Flask(__name__)
# Configure a secret SECRET_KEY
app.config['SECRET_KEY'] = 'mysecretkey'



# 1. View point to show the form and collect the data from user 
@app.route('/', methods=['GET', 'POST'])
def index():

    # Create instance of the form.
    form = InfoForm()
    
    # If the form is valid on submission 
    if form.validate_on_submit():
        
        # Grab the data from the  form.
        session['Name'] = form.Name.data
        session['Gender'] = form.Gender.data
        session['Maritual'] = form.Maritual.data
        session['Dependent'] = form.Dependent.data
        session['Education'] = form.Education.data
        session['Employment'] = form.Employment.data
        session['Aincome'] = form.Aincome.data
        session['Cincome'] = form.Cincome.data
        session['LoanAmount'] = form.LoanAmount.data
        session['LoanTerm'] = form.LoanTerm.data
        session['credit'] = form.credit.data
        session['Property'] = form.credit.data

        # Redirect the data to Predictioin function
        return redirect(url_for("prediction"))

    # Show the form for first visit 
    return render_template('home.html', form=form)


# 2. View point to show the result 
@app.route('/prediction')
def prediction():
    
    content = {}

    content['Gender'] = float(session['Gender'])
    content['Married'] = float(session['Maritual'])
    content['Dependents'] = float(session['Dependent'])
    content['Education'] = float(session['Education'])
    content['Self_Employed'] = float(session['Employment'])
    content['ApplicantIncome'] = float(session['Aincome'])
    content['CoapplicantIncome'] = float(session['Cincome'])
    content['LoanAmount'] = float(session['LoanAmount'])
    content['Loan_Amount_Term'] = float(session['LoanTerm'])
    content['Credit_History'] = float(session['credit'])
    content['Property_Area'] = float(session['Property'])



     # PRINT THE DATA PRESENT IN THE REQUEST 
    print("[INFO] WEB Request  - " , content)


    # Actual prediction done by this function 
    results = return_prediction(model=svc_pickle_model, scaler=svc_scaler, sample_json=content)


    # PRINT THE RESULT 
    print("[INFO] WEB Responce - " , results)

    return render_template('thankyou.html', results=results)

# 3. View point to handle the restfull api for prediciton 
@app.route('/api/prediction', methods=['POST'])
def predict_flower():
    
    # RECIEVE THE REQUEST 
    content = request.json
    
    # PRINT THE DATA PRESENT IN THE REQUEST 
    print("[INFO] API Request - " , content)
    
    # PREDICT THE CLASS USING HELPER FUNCTION 
    results = return_prediction(model=svc_pickle_model,scaler=svc_scaler,sample_json=content)
    
    # PRINT THE RESULT 
    print("[INFO] API Responce - " , results)
          
    # SEND THE RESULT AS JSON OBJECT 
    return jsonify(results)




# 4. View Point To handle the 404 Not found Error 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('notfound.html'), 404


if __name__ == '__main__':
    app.run('0.0.0.0',8080,debug=False)
