from sqlalchemy import  text
import logging
from datetime import datetime
import pandas as pd
from ..schemas.patientSchemas import UserData, PatientDetails
from ..utils.encoder import Encode_password, verify_password
from ..utils.Utils import parse_header, createconnection, patient_id_generator, jsonCommonStatus


def Account_Creation(req):
    logging.info('Received New Request For Account Creation')
    req_body = dict(req)
    print(req)
    required_fields = ["username","email","dob","gender","mobile","rtype","education","ssn","insuranceurl","password"]
    if not all(key_ in req_body for key_ in required_fields):
        missing_fields = set(required_fields) - set(req_body.keys())
        return jsonCommonStatus(f"Missing Fields :- [ {', '.join(map(str, missing_fields))} ] in the body.",None, 400, False)
    req_body["dob"] = datetime.strptime(req_body["dob"], "%Y-%m-%d")
    tp,main_ = Encode_password(req_body["password"])
    req_body["salt"],req_body["password"] = main_[0],main_[1]
    try:
        session = createconnection()
        result = session.execute(text(f"SELECT patient_id,activestat FROM patient_details WHERE email='{req_body['email']}'"))
        for row in result:
            if row[1] == True:
                return jsonCommonStatus("Account with this email already exist. Please try another email", None, 400, False)
        patient_id = patient_id_generator(req_body)
        user_data = UserData(
            patient_id=patient_id,
            salt = req_body["salt"],
            password = req_body["password"]
        )
        patient_details = PatientDetails(
            patient_id = patient_id,
            username = req_body["username"],
            email = req_body["email"],
            dob = req_body["dob"],
            gender = req_body["gender"],
            mobile = req_body["mobile"],
            rtype = req_body["rtype"],
            education = req_body["education"],
            ssn = req_body["ssn"],
            insuranceurl = req_body["insuranceurl"],
            activestat = 1
        )
        session.add(user_data)
        session.add(patient_details)
        session.commit()
        session.close()
    except Exception as e:
        logging.error("Failed to add data to sql database :- " + str(e))
        return jsonCommonStatus("Internal server error",None,500, False)
    return jsonCommonStatus("Account Created Successfully! Thank You", None, 200, True)


def Update_User_Details(req):
    req_body = req
    if "email" not in req_body.keys():
        return jsonCommonStatus("Email is compulsory for updating details.", None, 400, False)
    if len(req_body) == 1:
        return jsonCommonStatus("No Parameters found to update", None, 200, True)
    main_query = "UPDATE patient_details SET"
    cn = 0
    for key_ in req_body.keys():
        if key_ == "email":
            continue
        if cn != 0:
            main_query += " ,"
        main_query += f" {key_} = '{req_body[key_]}'"
        cn += 1
    main_query += f" WHERE email = '{req_body['email']}';"
    session = createconnection()
    try:
            results = session.execute(text(main_query))
            session.commit()
            print(results)
    except Exception as e:
            logging.error("Code failed with:- " + str(e))
            return jsonCommonStatus("Internal server error", None, 500, False)
    return jsonCommonStatus("Details Updated Succefully.", None, 200, True)
    
    
    
def Get_User_Details(req):
        valdata = {"userName":"", "email":"", "D.O.B":"", "gender":"", "mobile":"", "residentType":"", "education":"", "ssn":"", "insurance":'', "patientId":"", "AccoutStatus":""}
        print(req)
        try:
            req_body = req
        except:
            req_body = {}
        if "password" in req_body.keys():
            return jsonCommonStatus("Can not view accounts on the basis of Password.", None, 400, False)
        main_query = "SELECT * FROM patient_details"
        if len(req_body) > 0:
            for cn, key_ in enumerate(req_body.keys()):
                if cn == 0:
                    if key_ == 'activestat':
                        main_query += f" WHERE {key_} = {req_body[key_]}"
                        continue
                    main_query += f" WHERE {key_} = '{req_body[key_]}'"
                    continue
                if key_ == 'activestat':
                    main_query += f" AND {key_} = {req_body[key_]}"
                    continue
                main_query += f" AND {key_} = '{req_body[key_]}'"
        main_query += ";"
        try:
            session= createconnection()
            out = []
            results = session.execute(text(main_query))
            for row in results:
                row = list(row)
                row[2] = pd.to_datetime(row[2]).strftime("%d/%m/%y")
                result = {key: row[index] for index, key in enumerate(valdata.keys())}
                out.append(result)
            return jsonCommonStatus("Accounts fetched successfully", out, 200, True)
        except Exception as e:
            logging.error("Code failed with:- " + str(e))
            return jsonCommonStatus("Internal server error", None, 500, False)
        
        
        
def Delete_User(req):
    req_body = req
    if "email" not in req_body.keys():
        return jsonCommonStatus("Email is compulsory for updating details.", None, 400, False)
    checker_query = f"SELECT username FROM patient_details WHERE email='{req_body['email']}';"
    main_query = f"UPDATE patient_details SET activestat = 0 WHERE email = '{req_body['email']}'"
    session = createconnection()
    try:
        results = session.execute(text(checker_query))
        count = 0
        for val in results:
                patient_id = val[0]
                count+=1
        main_query = f"UPDATE patient_details SET activestat = 0 WHERE patient_id = '{patient_id}';"
        user_query = f"DELETE FROM user_data WHERE patient_id = '{patient_id}';"            
        if count != 0:
                session.execute(text(main_query))
                session.execute(text(user_query))
                session.commit()
        else:
            return jsonCommonStatus("User Account with email :- " + req_body["email"] + " Does not exsist", None, 400, False)
                
    except Exception as e:
        logging.error("Delete account:- " + str(e))
        return jsonCommonStatus("Internal server error", None, 500, False)
    return jsonCommonStatus("User Account Deleted Successfully. Thank You", None, 200, True)


def User_Login(req):
    req_body = req
    if "@" in req_body["Username"]:
        query = f"SELECT patient_id from patient_details WHERE email = '{req_body['Username']}' AND activestat = 1"
        session = createconnection()
        try:
            results = session.execute(text(query))
            for row in results:
                user_query = f"SELECT salt,password from user_data WHERE patient_id = '{row[0]}'"
                result = session.execute(text(user_query))
                for main in result:
                    if verify_password(req_body["Password"],main[0],main[1]):
                        return jsonCommonStatus("User authenticated succesfully!", None, 200, True)
                    else:
                        return jsonCommonStatus("Incorrect password or Incorrect Username", None, 400, False)
        except Exception as e:
            logging.error("login account username:- " + str(e))
            return jsonCommonStatus("Internal server error", None, 500, False)
    else:
        query = f"SELECT password from user_data WHERE mobile = '{req_body['Username']}'"
        session = createconnection()
        try:
            results = session.execute(text(query))
            for row in results:
                if verify_password(req_body["Password"]):
                    return jsonCommonStatus("User authenticated succesfully!", None, 200, True)
                else:
                    return jsonCommonStatus("Incorrect password or Incorrect Username", None, 400, False)
        except Exception as e:
            logging.error("login account:- " + str(e))
            return jsonCommonStatus("Internal server error", None, 500, False)


def sym_adder(req):
    req_body = req
    required_fields = ["patient_id","weight","height","bloodP","pulse","vitals"]
    if not all(key_ in req_body for key_ in required_fields):
        missing_fields = set(required_fields) - set(req_body.keys())
        return jsonCommonStatus(f"Missing Fields :- [ {', '.join(map(str, missing_fields))} ] in the body.", None, 400, False)
    timestamp = pd.Timestamp('now')
    query = f"INSERT INTO patient_symp (tdate, patient_id, weight, height, bloodP, pulse, ctimestamp, vitals) " \
            f"VALUES ('{timestamp.date().strftime('%m-%d-%y')}', '{req_body['patient_id']}', {req_body['weight']}, {req_body['height']}, " \
            f"{req_body['bloodP']}, {req_body['pulse']}, '{timestamp.strftime('%m-%d-%y %X')}', '{req_body['vitals']}');"
    try:
        session = createconnection()
        result = session.execute(text(query))
        session.commit()
        return jsonCommonStatus("The Symptoms for :- " + str(timestamp) + " Were noted successfully", None, 200, True)
    except Exception as e:
        logging.error("Error in Add_symptoms:" + str(e))
        return jsonCommonStatus("Internal server error", None, 500, False)
    

def sym_getter(req):
    req_body = req
    current_date = pd.Timestamp('now').strftime("%Y-%m-%d")
    vitaldatas = {
                    "Infirnity":"",
                    "NSynacpe":"",
                    "TiredNessAfirnity":"",
                    "BreathnessDA":"",
                    "BreathnessEA":"",
                    "Dizziness" :"",
                    "Col Swet": "",
                    "Tiredness" : "",
                    "chest_pain" : "",
                    "pressureChest" : "",
                    "worry" : "",
                    "weakness" : "",
                }
    try:
        #Check any of these key available in the req_body
        if("email" in req_body.keys()) or ("mobile" in req_body.keys()) or ("patient_id" in req_body.keys()):
            main_query = f"SELECT * FROM patient_symp"
            if len(req_body) >= 1:
                for cn, key_ in enumerate(req_body.keys()):
                    #First index will create a where clause
                    if cn == 0:
                        if key_ == 'activestate':
                            main_query += f" WHERE {key_} = {req_body[key_]}"
                            continue
                        main_query += f" WHERE {key_} = '{req_body[key_]}'"
                        continue
                    # All other will append in mainquery with AND operatior
                    if key_ == 'activestate':
                        # Avoiding Start_date and end_date
                        if key_ != "start_date" and key_ != "end_date":
                            main_query += f" AND {key_} = {req_body[key_]}"
                            continue
                    # Avoiding Start_date and end_date
                    if key_ != "start_date" and key_ != "end_date":
                        main_query += f" AND {key_} = {req_body[key_]}"

            #Start date and end date from request
            start_date = req_body.get('start_date')
            end_date = req_body.get('end_date')

           # Date based filter
            if (start_date and pd.to_datetime(start_date).strftime("%Y-%m-%d") > current_date) or (end_date and pd.to_datetime(end_date).strftime("%Y-%m-%d") > current_date):
                return jsonCommonStatus("Future date cannot be accessible",None,400, True)
            else:
                if start_date:
                    main_query += f" AND tdate >= '{start_date}'"
                if end_date:
                    main_query += f" AND tdate <= '{end_date}'"

            #Sorting the OUTPUT
            main_query += " ORDER BY ctimestamp DESC;"
            output = []
            session = createconnection()
            results = session.execute(text(main_query))
            for row in results:
                data = {
                            "date" : pd.to_datetime(row[0]).strftime("%d-%m-%y"),
                            "symptoms": {key: row[7][index] for index, key in enumerate(vitaldatas.keys())}
                            }
                data["Weight"] = row[2]
                data["B.P"] = row[4]
                data["Height"] = row[3]
                data["Pulse"]  = row[5]
                output.append(data)    
            return jsonCommonStatus("Sympotms fetched succesfully!", output, 200, True)
        else:
            return jsonCommonStatus("Email or Phone-Number or patient_id is required", None, 400, False)
    except Exception as e:
        logging.error("An error occurred in query_symptoms: " + str(e))
        return jsonCommonStatus("Internal server error", None, 500, False)
