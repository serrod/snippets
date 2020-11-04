import pyodbc 
import pandas as pd
import json

#CREATE AND OPEN FILE
survey_file = open("survey-export.sql","a", encoding="utf-8")
survey_unit_file = open("survey-unit-export.sql","a", encoding="utf-8")
survey_open_question_file = open("survey-open-question-export.sql","a", encoding="utf-8")
survey_response_file = open("survey-response-export.sql","a", encoding="utf-8")
survey_response_answer_choice_file = open("survey-response-answer-choice-export.sql","a", encoding="utf-8")
survey_response_country_file = open("survey-response-country-export.sql","a", encoding="utf-8")
survey_response_unit_response_file = open("survey-response-unit_response-export.sql","a", encoding="utf-8")


# db connection string
db_connetion = pyodbc.connect("Driver={SQL Server};Server=serverAddr,serverPort; Database=dataBaseName; uid=userId;pwd=serverPassword;")

# fetch pre manipulated data from SQL
sql_query = "SELECT oaa_id, ref_user_survey_table_id, survey_status, survey_results FROM dbo.ref_user_survey WHERE DATALENGTH(survey_results)  > 0"
cursor = db_connetion.cursor()
query = cursor.execute(sql_query)
   

for row in query:
    # COMMON INFORMATION - for all entries
    oaa_id = str(row.oaa_id)[:-2]
    survey_id = str(row.ref_user_survey_table_id)
    
    # GENERAL SURVEY INFORMATION
    survey_status = row.survey_status
    survey_results_json = json.loads(row.survey_results)
    survey_user = survey_results_json["name"]
    survey_start_date = survey_results_json["startDate"]
    survey_end_date = survey_results_json["endDate"]
    survey_organization = survey_results_json["organization"]
    survey_sipr = survey_results_json["siprEmail"]
    survey_nipr = survey_results_json["niprEmail"]
    survey_role = survey_results_json["role"]

    # SURVEY TABLE OUTPUT TABLE
    survey_sql = (  "INSERT INTO " 
                    "survey("
                        "[oaa_id]," 
                        "[survey_id],"  
                        "[survey_organization]," 
                        "[survey_user]," 
                        "[survey_role],"
                        "[survey_sipr]," 
                        "[survey_nipr]," 
                        "[survey_start_date]," 
                        "[survey_end_date]"
                    ") VALUES ( "  
                        + oaa_id + ","  
                        + survey_id + ",'"  
                        + survey_organization + "','"  
                        + survey_user + "','"  
                        + survey_role + "','"   
                        + survey_sipr + "','"   
                        + survey_nipr + "','"  
                        + survey_start_date + "','"  
                        + survey_end_date + 
                    "');")
    
    # WRITE TO FILE - SURVEY TABLE
    survey_file.write(survey_sql)
    survey_file.write("\n")  

    # UNIT 
    for units in survey_results_json["units"]: 
        if units is not None:
            if "Title" in units or not None:
                survey_unit_name = units["Title"]

            if "Status" in units or not None:        
                survey_unit_status = units["Status"]

            if "Author" in units or not None:
                survey_unit_author = units["Author"]["Title"]
                survey_unit_email = units["Author"]["EMail"]
            
            if "HostNation" in units or not None:
                country_id = str(units["HostNation"]["Id"])
                country_name = str(units["HostNation"]["Title"])
            
            # UNIT OUTPUT TABLE
            survey_unit_sql = ( "INSERT INTO " 
                                "survey_unit(" 
                                    "[oaa_id]," 
                                    "[survey_id]," 
                                    "[survey_unit_name]," 
                                    "[survey_unit_email]," 
                                    "[survey_unit_author]," 
                                    "[country_id]," 
                                    "[country_name]," 
                                    "[survey_unit_status]" 
                                ") VALUES ("    
                                    + oaa_id + ","   
                                    + survey_id + ",'"  
                                    + survey_unit_name + "','"  
                                    + survey_unit_email + "','"  
                                    + survey_unit_author + "','" 
                                    + country_id + "','" 
                                    + country_name + "','" 
                                    + survey_unit_status +  
                                "');")
        
            # WIRTE TO UNIT FILE - SURVEY_UNIT TABLE
            survey_unit_file.write(survey_unit_sql)
            survey_unit_file.write("\n")  

    # OPEN ENDED QUESTIONS
    for open_questions in survey_results_json["openEndedQuestions"]: 
        if open_questions is not None:
            survey_question = open_questions["text"]
            survey_reponse = open_questions["response"]

            survey_open_question_sql = ("INSERT INTO " 
                                            "survey_open_question(" 
                                            "[oaa_id]," 
                                            "[survey_id]," 
                                            "[survey_question]," 
                                            "[survey_reponse]" 
                                        ") VALUES (" 
                                            + oaa_id + "," 
                                            + survey_id + ",'" 
                                            + survey_question.replace("'","''") + "','" 
                                            + survey_reponse.replace("'","''") + 
                                    "');")

            # OPEN ENDED QUESTIONS OUTPUT TABLE - SURVEY_OPEN_QUESTION TABLE
            survey_open_question_file.write(survey_open_question_sql)
            survey_open_question_file.write("\n")

    # RESPONSES
    for responses in survey_results_json["responses"]:
        survey_response_indicator = responses["indicatorTitle"]
        survey_response_moe = responses["moeTitle"]      
        survey_response_effect = responses["effectTitle"]
        survey_response_objective = (responses["objectiveTitle"])

        survey_response = ("INSERT INTO " 
                                "survey_response(" 
                                "[oaa_id]," 
                                "[survey_id],"  
                                "[survey_response_objective]," 
                                "[survey_response_effect]," 
                                "[survey_response_moe]," 
                                "[survey_response_indicator]"   
                           ") VALUES ( " 
                                + oaa_id + "," 
                                + survey_id + ",'"  
                                + survey_response_objective.replace("'","''") + "','" 
                                + survey_response_effect.replace("'","''") + "','" 
                                + survey_response_moe.replace("'","''") + "','" 
                                + survey_response_indicator.replace("'","''") + 
                         "');")
            
        # OUTPUT  SURVEY RESPONSE TABLE
        survey_response_file.write(survey_response)
        survey_response_file.write("\n")

        # ANSWER CHIOCE
        if "answerChoices" in responses or not None:
            for answerChoices in responses["answerChoices"]:
                survey_response_answer_choice_text = str(answerChoices["text"])
                
                if "enabled" in answerChoices:
                    survey_response_answer_choice_enable = str(answerChoices["enabled"])

                if "points" in answerChoices:
                    survey_response_answer_choice_points = str(answerChoices["points"])
                
                # OUTPUT ANSWER CHIOCE TABLE
                survey_response_answer_choice_sql = ("INSERT INTO " 
                                                        "survey_response_answer_choice(" 
                                                        "[oaa_id]," 
                                                        "[survey_id],"  
                                                        "[survey_response_objective]," 
                                                        "[survey_response_effect]," 
                                                        "[survey_response_moe]," 
                                                        "[survey_response_indicator],"
                                                        "[survey_answer_choice],"
                                                        "[survey_answer_points],"
	                                                    "[survey_answer_enabled]" 
                                                    ") VALUES ( " 
                                                        + oaa_id + "," 
                                                        + survey_id + ",'"  
                                                        + survey_response_objective.replace("'","''") + "','" 
                                                        + survey_response_effect.replace("'","''") + "','" 
                                                        + survey_response_moe.replace("'","''") + "','" 
                                                        + survey_response_indicator.replace("'","''") + "','"
                                                        + survey_response_answer_choice_text + "','"  
                                                        + survey_response_answer_choice_points + "','"  
                                                        + survey_response_answer_choice_enable +
                                                    "');")

                # WRITE OUTPUT SURVEY_RESPONSE_ANSWER_CHIOCE TABLE
                survey_response_answer_choice_file.write(survey_response_answer_choice_sql)
                survey_response_answer_choice_file.write("\n")

        if "countries" in responses or not None:
             for countries in responses["countries"]:
                 survey_country_name = str(countries["Title"])
                 country_id = str(countries["value"])
                 
                 # OUTPUT COUNTRY RESPONSE TABLE 
                 survey_response_country_sql = ("INSERT INTO " 
                                                    "survey_response_country(" 
                                                    "[oaa_id]," 
                                                    "[survey_id],"  
                                                    "[survey_response_objective]," 
                                                    "[survey_response_effect]," 
                                                    "[survey_response_moe]," 
                                                    "[survey_response_indicator],"
                                                    "[survey_country_name],"
                                                    "[country_id]"
                                                 ") VALUES ( " 
                                                    + oaa_id + "," 
                                                    + survey_id + ",'"  
                                                    + survey_response_objective.replace("'","''") + "','" 
                                                    + survey_response_effect.replace("'","''") + "','" 
                                                    + survey_response_moe.replace("'","''") + "','" 
                                                    + survey_response_indicator.replace("'","''") + "','"
                                                    + survey_country_name + "','"  
                                                    + country_id +
                                                 "');")
                 
                 # OUTPUT COUNTRY SURVEY_RESPONSE_COUNTRY
                 survey_response_country_file.write(survey_response_country_sql)
                 survey_response_country_file.write("\n")

        if "unitResponseValues" in responses or not None:
            for unitResponseValues in responses["unitResponseValues"]:
                survey_response_unit = unitResponseValues["unit"]["Title"]
                
                # SET DEFAULT. INCONSISTENT  DATA SET                
                survey_response_unit_answer_choice_enable = "NULL"
                survey_response_unit_comment = "NOT PROVIDED"
                survey_response_unit_answer_choice_point = "0"

                if "responseComments" in unitResponseValues: 
                    survey_response_unit_comment = unitResponseValues["responseComments"]   
        
                if unitResponseValues["answerChoice"] is not None:
                    survey_response_unit_answer_choice_enable = str(unitResponseValues["answerChoice"]["enabled"])
                    survey_response_unit_answer_choice_text = unitResponseValues["answerChoice"]["text"]

                    if "points" in unitResponseValues["answerChoice"]:
                        survey_response_unit_answer_choice_point = str(unitResponseValues["answerChoice"]["points"])


                #OUTPUT UNIT RESPONSE TABLE
                survey_response_unit_response_file_sql = ("INSERT INTO " 
                                                            "survey_response_unit(" 
                                                            "[oaa_id]," 
                                                            "[survey_id],"  
                                                            "[survey_response_objective]," 
                                                            "[survey_response_effect]," 
                                                            "[survey_response_moe]," 
                                                            "[survey_response_indicator],"
                                                            "[survey_response_unit_name],"
                                                            "[survey_response_unit_comment],"
                                                            "[survey_response_unit_answer],"
                                                            "[survey_response_unit_enable],"
                                                            "[survey_response_unit_points]"
                                                         ") VALUES ( " 
                                                            + oaa_id + "," 
                                                            + survey_id + ",'"  
                                                            + survey_response_objective.replace("'","''") + "','" 
                                                            + survey_response_effect.replace("'","''") + "','" 
                                                            + survey_response_moe.replace("'","''") + "','" 
                                                            + survey_response_indicator.replace("'","''") + "','"
                                                            + survey_response_unit + "','"
                                                            + survey_response_unit_comment.replace("'","''") + "','" 
                                                            + survey_response_unit_answer_choice_text.replace("'","''") + "','" 
                                                            + survey_response_unit_answer_choice_enable + "'," 
                                                            + survey_response_unit_answer_choice_point +
                                                         ");")

                # OUTPUT COUNTRY SURVEY_RESPONSE_COUNTRY
                survey_response_unit_response_file.write(survey_response_unit_response_file_sql)
                survey_response_unit_response_file.write("\n")

# CLOSED ALL OPEN FILE
survey_file.close()
survey_unit_file.close()
survey_open_question_file.close()
survey_response_file.close()
survey_response_answer_choice_file.close()
survey_response_country_file.close()
survey_response_unit_response_file.close()
