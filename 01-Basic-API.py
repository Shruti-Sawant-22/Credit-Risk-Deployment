from flask import Flask, request, jsonify
import numpy as np  
import pickle
import joblib


#### THIS IS WHAT WE DO IN POSTMAN ###
# STEP 1: Create New Request
# STEP 2: Select POST
# STEP 3: Type correct URL (http://127.0.0.1:5000/prediction)
# STEP 4: Select Body
# STEP 5: Select raw and then JSON type
# STEP 6: Type or Paste in example json request
# STEP 7: Run 01-Basic-API.py to launch server and confirm the site is running
# Step 8: Run API request

### IMP NOTES
# Set localhost = '0.0.0.0' and port = 8080 in 01-Basic-API.py 
# To accept the request from other client over a wifi Connection 

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
    
    classes = np.array(['Not-Eligible:- 0', 'Eligible:- 1'])
    
    class_ind = model.predict(person)
    
    return classes[class_ind]
                    
# REMEMBER TO LOAD THE MODEL AND THE SCALER!

# LOAD THE SVC MODEL
pkl_filename = "Models/svc_pickle_model1.pkl"
with open(pkl_filename, 'rb') as file2:
    svc_pickle_model = pickle.load(file2)

# LOAD THE SCLAER OBJECT 
svc_scaler = joblib.load("Models/svm_scaler1.pkl")



app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>FLASK APP IS RUNNING!</h1>'


@app.route('/prediction', methods=['POST'])
def predict_default():
    
    # RECIEVE THE REQUEST 
    content = request.json
    
    # PRINT THE DATA PRESENT IN THE REQUEST 
    print("[INFO] Request: ", content)
    
    # PREDICT THE CLASS USING HELPER FUNCTION 
    results = return_prediction(model=svc_pickle_model,
                                scaler=svc_scaler,
                                sample_json=content)
    
    # PRINT THE RESULT 
    print("[INFO] Responce: ", results)
          
    # SEND THE RESULT AS JSON OBJECT 
    return jsonify(results[0])

if __name__ == '__main__':
    app.run()