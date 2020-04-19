#!/usr/bin/env python
# coding: utf-8

# In[1]:


# https://www.toolsqa.com/postman/post-request-in-postman/  ------- how to post request using Postman
# https://auth0.com/blog/developing-restful-apis-with-python-and-flask/#L-span-id--why-flask----span--Why-Flask- ---- why flask. 
# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask#designing-requests


# In[1]:


from flask import Flask, jsonify, request
from flask import make_response
from flask import request
import pandas as pd
import pyodbc
import pandas as pd
from itertools import groupby
import json
from collections import defaultdict


# In[2]:


app = Flask(__name__) 


# In[6]:


(r'DRIVER={ODBC Driver 17 for SQL Server};' +
        ('SERVER={server},{port};'   +
        'DATABASE={database};'      +
        'UID={username};'           +
        'PWD={password}').format(
                server= '65.175.68.34',
                  port= 1433,
              database= 'VsaDev',
              username= 'sa',
              password= 'H4ZXZy-vRZwL#9A')
        )

config = dict(server= '65.175.68.34',
                  port= 1433,
              database= 'VsaDev',
              username= 'sa',
              password= 'H4ZXZy-vRZwL#9A')

conn_str = ('SERVER={server},{port};'   +
            'DATABASE={database};'      +
            'UID={username};'           +
            'PWD={password}')
conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 13 for SQL Server};' +
    conn_str.format(**config)
    )


# In[7]:


def read_data():
    data = ("SELECT g.GeneratedPlanID,            g.ParameterSetID,            p.MajorID,            m.Name as PreferedMajor,             p.SchoolID,            s.Name as PreferedSchool,            p.JobTypeID,            j.JobType,            QuarterPreferenceID,            q.Quarter as PreferedStartQuarter,            gp.StartingQuarter,            q1.Quarter as ActualStartQuarter,            NumberCoreCoursesPerQuarter,            gp3.NumberOfCorePerQuarter as ActualNumberofCore,            MaxNumberOfQuarters as PreferedNumberQuarters,            gp.NumberOfQuarters as ActualNumberQuarters,            CreditsPerQuarter,            SummerPreference as SummerPref,            gp2.SummerClass as ActualSummerPref,            p.EnrollmentTypeID,            e.EnrollmentDescription as EnrollmentType,            gp.TotalNumberOfCourses,            m1.MathStarting,            eng.EnglishStarting,            g.MachineScore            FROM VsaDev.dbo.ParameterSet as p            INNER JOIN VsaDev.dbo.Major as m ON p.MajorID = m.MajorID            INNER JOIN VsaDev.dbo.School as s ON p.SchoolID = s.SchoolID            INNER Join VsaDev.dbo.JobType as j on p.JobTypeID = j.JobTypeID            INNER JOIN VsaDev.dbo.Quarter as q on p.QuarterPreferenceID = q.QuarterID            INNER JOin VsaDev.dbo.EnrollmentType as e on p.EnrollmentTypeID = e.EnrollmentTypeID            Inner join VsaDev.dbo.GeneratedPlan as g on g.ParameterSetID = p.ParameterSetID             Inner JOin             (select s.GeneratedPlanID,            Count (distinct s.QuarterID) as NumberOfQuarters,            Count(s.CourseID)  as TotalNumberOfCourses,            MIN(QuarterID) as StartingQuarter            from VsaDev.dbo.StudyPlan as s            GROUP by s.GeneratedPlanID ) as gp on gp.GeneratedPlanID = g.GeneratedPlanID            Inner join VsaDev.dbo.Quarter as q1 on gp.StartingQuarter = q1.QuarterID            Full join             (select * from             (select  s.GeneratedPlanID,case when s.QuarterID = 4 then 'Yes'            end as SummerClass            from StudyPlan as s            GROUP by s.QuarterID,s.GeneratedPlanID)            as d where d.SummerClass = 'Yes') as gp2 on gp2.GeneratedPlanID = g.GeneratedPlanID            full JOIN            (select  s1.GeneratedPlanID, Count(s1.NumberOfCoursesPerQuarter)as NumberOfCorePerQuarter            from (            select  s.GeneratedPlanID,            s.QuarterID,            count(s.CourseID) as NumberOfCoursesPerQuarter            FROM VsaDev.dbo.StudyPlan as s            where s.CourseID in (select CourseID from Course as c where c.CourseNumber like 'MATH%' UNION select CourseID from Course as co1 where co1.CourseNumber like 'ENGL%')            GROUP by s.QuarterID,s.GeneratedPlanID)as s1            GROUP by s1.GeneratedPlanID) as gp3 on gp3.GeneratedPlanID = g.GeneratedPlanID            FULL JOIN            (select  s.GeneratedPlanID,            MIN(s.CourseID) as MathStarting            FROM VsaDev.dbo.StudyPlan as s            where s.CourseID in (select CourseID from Course as c where            c.CourseNumber like 'MATH%')            GROUP by s.GeneratedPlanID) as m1 on m1.GeneratedPlanID = g.GeneratedPlanID            full JOIN            (select  s.GeneratedPlanID,            MIN(s.CourseID) as EnglishStarting            FROM VsaDev.dbo.StudyPlan as s            where s.CourseID in (select CourseID from Course as c where c.CourseNumber like 'ENGL%')            GROUP by s.GeneratedPlanID) as eng on eng.GeneratedPlanID = g.GeneratedPlanID;")
    vaaData = pd.read_sql(data, conn)
    import CalculateSequenceBreak as cb
    c = cb.CalculateSequenceBreak()
    mathSequenceBreak = c.get_math_seqBreak()
    englishSequenceBreak = c.get_eng_seqBreak()

    labels = ['GeneratedPlanID','mathSequenceBreak']
    math_df = pd.DataFrame.from_records(mathSequenceBreak,columns = labels)

    labels = ['GeneratedPlanID','englishSequenceBreak']
    eng_df = pd.DataFrame.from_records(englishSequenceBreak,columns = labels)
    math_merged = pd.merge(vaaData, math_df, on='GeneratedPlanID',how = 'outer')
    data1 = pd.merge(math_merged, eng_df, on='GeneratedPlanID',how = 'outer')
    data1['NumberCoreCoursesPerQuarter'] = data1['NumberCoreCoursesPerQuarter'].fillna(6)
# filling missing values with the mean of the distribution
    data1['ActualSummerPref'] = data1['ActualSummerPref'].fillna('No')
    data1['ActualNumberofCore'] = data1['ActualNumberofCore'].fillna(4)
    data1['CreditsPerQuarter'] = data1['CreditsPerQuarter'].fillna(20)
    import LabelData as lb
    l = lb.LabelData()
    labels = l.label_data(data1)

    data1['Rating'] = labels
    data1['SummerPref'] = data1['SummerPref'].str.lower()
    data1['ActualSummerPref'] = data1['SummerPref'].str.lower()

    return data1


# In[8]:


data = read_data()
# data


# In[9]:


# data['NumberCoreCoursesPerQuarter'] = data['NumberCoreCoursesPerQuarter'].fillna(6)
# # filling missing values with the mean of the distribution
# data['ActualSummerPref'] = data['ActualSummerPref'].fillna('No')
# data['ActualNumberofCore'] = data['ActualNumberofCore'].fillna(4)
# data['CreditsPerQuarter'] = data['CreditsPerQuarter'].fillna(20)


# In[10]:


# print (data.isnull().sum())


# In[11]:


import json
class Decoder(json.JSONDecoder):
    def decode(self, s):
        result = super().decode(s)  # result = super(Decoder, self).decode(s) for Python 2.x
        return self._decode(result)

    def _decode(self, o):
        if isinstance(o, str) or isinstance(o, unicode):
            try:
                return int(o)
            except ValueError:
                return o
        elif isinstance(o, dict):
            return {k: self._decode(v) for k, v in o.items()}
        elif isinstance(o, list):
            return [self._decode(v) for v in o]
        else:
            return o


# In[12]:


@app.route('/getRecommendationPlan', methods=['POST'])
def get_plan():
    if not request.json or not 'major' or not 'school' in request.json:
        abort(400)

# additional things that can be done are do clustering on the data to improve the 
# speed at which recommendations are generated. 
    parameter = {
        'name': 'Student',
        'Prefered Major': request.json['major'],
        'Prefered School': request.json['school'],
        'Summer Preference': request.json['summer'],
        'NumberOfCourses' : int(request.json['courses']),
        'NumberOfQuarters' : int(request.json['quarters']),
        'PreferedStartQuarter' : request.json['quarter'],
        'Enrollment' : request.json['enrollment'],
        'Job' : request.json['job'],
        'NumberOfCredits':int(request.json['credits']),
        
        
        
    }
    column=['PlanId','Distance'];
    recommendation = pd.DataFrame()
#     count = 0
    for test_index,test_row in data.iterrows():
        if(test_row['Rating'] < 5):
            pass
        else : 
            distance=0
#         major
            if(parameter['Prefered Major'] is not test_row['PreferedMajor']):
                distance=distance + 1000
#           School
            if(parameter['Prefered School']!= test_row['PreferedSchool']):
                distance=distance + 1000
            if(parameter['Summer Preference'] != test_row['SummerPref']):
                distance = distance + 10
            if(parameter['PreferedStartQuarter'] != test_row['PreferedStartQuarter']):
                distance = distance + 10
            if(parameter['Enrollment'] != test_row['EnrollmentType']):
                distance = distance + 10
            if(parameter['Job'] != test_row['JobType']):
                distance = distance + 10
            distance = distance + (abs(parameter['NumberOfCourses']-int(test_row['NumberCoreCoursesPerQuarter'])))
            distance = distance + (abs(parameter['NumberOfCredits'] - int(test_row['CreditsPerQuarter'])))
            distance = distance + (abs(parameter['NumberOfQuarters'] - int(test_row['PreferedNumberQuarters'])))
            if(distance < 2000):
                score = pd.DataFrame({'PlanId':test_row['GeneratedPlanID'],'Distance':[distance]})
                recommendation=recommendation.append(score,ignore_index = True,)
#                     count = count + 1
            
    plans = pd.DataFrame()  
    
    
    cursor = conn.cursor()

    rating = []
    recommendation=recommendation.sort_values(by=['Distance'])
    for test_index,test_row in recommendation.head(3).iterrows():

        number = int(test_row['PlanId'])
        sql = ("select s.GeneratedPlanID as GeneratedPlanID,RTRIM(q.Quarter) as Quarter,RTRIM(c.CourseNumber) as CourseNumber,gp.MachineScore from StudyPlan as s                join Course as c on c.CourseID = s.CourseID                join Quarter as q on q.QuarterID = s.QuarterID                join GeneratedPlan as gp on gp.GeneratedPlanID=s.GeneratedPlanID                where s.GeneratedPlanID =?")

        
        
        df = (pd.read_sql_query(sql, conn, params=(number,)))
        plans = pd.concat([plans,df],ignore_index =True)
        
    
    
        
    course = {plan : g["CourseNumber"].tolist() for plan,g in plans.groupby("GeneratedPlanID")}
    quarter = {plan : g["Quarter"].tolist() for plan,g in plans.groupby("GeneratedPlanID")}

    
 
 
    dd = defaultdict(list)
 
    for d in (course,quarter): # you can list as many input dicts as you want here
        for key, value in d.items():
            dd[key].append(value)
 

            
      
    return json.dumps(dict(dd))


# In[13]:


app.run(port = 8443) 


# In[15]:


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Parameters dont match'}), 404)


# In[ ]:





# In[ ]:





# In[ ]:




