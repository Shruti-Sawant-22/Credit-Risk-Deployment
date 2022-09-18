
# NAME @: Shruti Sawant
# TOPIC @: Risk Analytics Model Deployment
# DATE @: 17/09/2022



# IMPORT THE DEPENDENCIES 

import pickle 
import joblib
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
import numpy as np
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,
                     TextAreaField,SubmitField)






# REMEMBER TO LOAD THE MODEL AND THE SCALER!

# 1. LOAD THE SVC MODEL
pkl_filename = "Models/svc_pickle_model1.pkl"
with open(pkl_filename, 'rb') as file2:
    svc_pickle_model = pickle.load(file2)

# 2. LOAD THE SCLAER OBJECT 
svc_scaler = joblib.load("Models/svm_scaler1.pkl")



# 3. CREATE A PREICTION FUNCTION 
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
    
    classes = np.array(['Non-Eligible', 'Eligible'])
    
    class_ind = model.predict(person)
    
    return classes[class_ind[0]]



# 4 . CREATE A FLASK FORM 

class InfoForm(FlaskForm):
    '''
    This general class gets a lot of form data about user.
    Mainly a way to go through many of the WTForms Fields.
    '''
    
    Name = StringField('Enter Your Full Name :    ',validators=[DataRequired()])
    
    Gender = RadioField('Please choose your Gender : ', choices=[('1','Male'),('0','Female')])
    
    Maritual = RadioField('Please choose your Marital status : ', choices=[('1','Married'),('0','Unmarried')])
    
    Dependent = StringField('Enter Total Number Of Dependent People : ',validators=[DataRequired()])
    
    Education = RadioField('Educational Details : ', choices=[('1','Not-Graduate'),('0','Graduate')])
    
    Employment = RadioField('Are you self Employed : ', choices=[('1','Yes'),('0','No')])
    
    Aincome = StringField('Applicant Income In Thousand $ : ',validators=[DataRequired()])
    
    Cincome = StringField('Co-applicant Income In Thousand $ : ',validators=[DataRequired()])
    
    LoanAmount = StringField('Total Loan Amount In Thousand $ :  ',validators=[DataRequired()])
    
    LoanTerm = StringField('Duration Of Loan In No Of Months : ',validators=[DataRequired()])
    
    credit = RadioField('Do You Have Any Credit Histoy : ', choices=[('1','Yes'),('0','No')])
    
    
    Property = SelectField(u'Pick Your Property Area :',
                          choices=[('0', 'Rural'), ('1', 'Semiurban'),
                                   ('2', 'Urban')])
   
    
    
    feedback = TextAreaField()
    
    submit = SubmitField('Submit')
