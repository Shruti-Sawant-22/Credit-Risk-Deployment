from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
import pickle
import joblib
import numpy as np
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,StringField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired


app = Flask(__name__)
# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!
app.config['SECRET_KEY'] = 'mysecretkey'

# Now create a WTForm Class
# Lots of fields available:
# http://wtforms.readthedocs.io/en/stable/fields.html
class InfoForm(FlaskForm):
    '''
    This general class to accept form data
    '''
    
    Name = StringField('Enter Your Full Name',validators=[DataRequired()])
    
    Gender = RadioField('Please choose your Gender:', choices=[('1','Male'),('0','Female')])
    
    Maritual = RadioField('Please choose your marital status:', choices=[('1','Mrried'),('0','Un-Married')])
    
    Dependent = StringField('Enter Total Number Of Dependent People',validators=[DataRequired()])
    
    Education = RadioField('Educational Details :', choices=[('1','Not-Graduate'),('0','Graduate')])
    
    Employment = RadioField('Are you self Employed :', choices=[('1','Yes'),('0','No')])
    
    Aincome = StringField('Applicatin Income In Digits ',validators=[DataRequired()])
    
    Cincome = StringField('Coapplicant Income In Digits ',validators=[DataRequired()])
    
    LoanAmount = StringField('Total Loan Amount ',validators=[DataRequired()])
    
    LoanTerm = StringField('Loan Term In  Digits ',validators=[DataRequired()])
    
    credit = RadioField('Do You Have Any Credit Histoy :', choices=[('1','Yes'),('0','No')])
    
    
    Property = SelectField(u'Pick Your Property Area :',
                          choices=[('0', 'Rural'), ('1', 'Semiurban'),
                                   ('2', 'Urban')])
   
    
    
    feedback = TextAreaField()
    
    submit = SubmitField('Submit')





def return_prediction(model,scaler,sample_json):
    
    # For larger data features, you should probably write a for loop
    # That builds out this array for you
    
    gen = sample_json['Gender']
    mar = sample_json['Married']
    dep = sample_json['Dependents']
    edu = sample_json['Education']
    sle = sample_json['Self_Employed']
    api = sample_json['ApplicantIncome']
    cpi = sample_json['CoapplicantIncome']
    lam = sample_json['LoanAmount']
    lat = sample_json['Loan_Amount_Term']
    crh = sample_json['Credit_History']
    pra = sample_json['Property_Area']
    
    person = [[gen,mar,dep,edu,sle,api,cpi,lam,lat,crh,pra]]
    
    person = scaler.transform(person)
    
    classes = np.array(['Not-Eligible', 'Eligible'])
    
    class_ind = model.predict(person)
    
    return classes[class_ind[0]]



# REMEMBER TO LOAD THE MODEL AND THE SCALER!

# LOAD THE SVC MODEL
pkl_filename = "Models/svc_pickle_model1.pkl"
with open(pkl_filename, 'rb') as file2:
    svc_pickle_model = pickle.load(file2)

# LOAD THE SCLAER OBJECT 
svc_scaler = joblib.load("Models/svm_scaler1.pkl")



@app.route('/', methods=['GET', 'POST'])
def index():

    # Create instance of the form.
    form = InfoForm()
    # If the form is valid on submission 
    if form.validate_on_submit():
        # Grab the data from  form.

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

        return redirect(url_for("prediction"))


    return render_template('home.html', form=form)


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


    results = return_prediction(model=svc_pickle_model, scaler=svc_scaler, sample_json=content)

    

    return render_template('thankyou.html', results=results)


if __name__ == '__main__':
    app.run('0.0.0.0',port = 8080 , debug=True)
