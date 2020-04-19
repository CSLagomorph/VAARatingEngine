

import pyodbc
import pandas as pd



(r'DRIVER={ODBC Driver 17 for SQL Server};' +
        ('SERVER={server},{port};'   +
        'DATABASE={database};'      +
        'UID={username};'           +
        'PWD={password}').format(
                server= '65.175.68.34',
                  port= 1433,
              database= 'VsaDev',
              username= 'sa',
              password= 'pwd')
        )

config = dict(server= '65.175.68.34',
                  port= 1433,
              database= 'VsaDev',
              username= 'sa',
              password= 'pwd')

conn_str = ('SERVER={server},{port};'   +
            'DATABASE={database};'      +
            'UID={username};'           +
            'PWD={password}')
conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 13 for SQL Server};' +
    conn_str.format(**config)
    )



data = ("SELECT g.GeneratedPlanID,
        g.ParameterSetID,        
        p.MajorID,        
        m.Name as PreferedMajor,         
        p.SchoolID,        
        s.Name as PreferedSchool,        
        p.JobTypeID,        
        j.JobType,        
        QuarterPreferenceID,        
        q.Quarter as PreferedStartQuarter,        
        gp.StartingQuarter,        
        q1.Quarter as ActualStartQuarter,        
        NumberCoreCoursesPerQuarter,        
        gp3.NumberOfCorePerQuarter as ActualNumberofCore,        
        MaxNumberOfQuarters as PreferedNumberQuarters,        
        gp.NumberOfQuarters as ActualNumberQuarters,        
        CreditsPerQuarter,        
        SummerPreference as SummerPref,        
        gp2.SummerClass as ActualSummerPref,        
        p.EnrollmentTypeID,        
        e.EnrollmentDescription as EnrollmentType,        
        gp.TotalNumberOfCourses,        
        m1.MathStarting,        
        eng.EnglishStarting,        
        g.MachineScore        
        FROM VsaDev.dbo.ParameterSet as p        
        # join on major table to get major name
        INNER JOIN VsaDev.dbo.Major as m ON p.MajorID = m.MajorID 
              # join on school table to get school name
        INNER JOIN VsaDev.dbo.School as s ON p.SchoolID = s.SchoolID 
               # get job type description
        INNER Join VsaDev.dbo.JobType as j on p.JobTypeID = j.JobTypeID
                # join to  get quarter description
        INNER JOIN VsaDev.dbo.Quarter as q on p.QuarterPreferenceID = q.QuarterID   
             #  join to get enrollment type
        INNER JOin VsaDev.dbo.EnrollmentType as e on p.EnrollmentTypeID = e.EnrollmentTypeID 
               # join on generatedplan to get the information for correspoding study plan
        Inner join VsaDev.dbo.GeneratedPlan as g on g.ParameterSetID = p.ParameterSetID
        # get information about the study plan -- the above lines capture user parameters along with some others which can be directly read from the ParameterSet table
        Inner JOin         
        (select s.GeneratedPlanID,        
          Count (distinct s.QuarterID) as NumberOfQuarters,        
          Count(s.CourseID)  as TotalNumberOfCourses,         
          MIN(QuarterID) as StartingQuarter        
          from VsaDev.dbo.StudyPlan as s        
          GROUP by s.GeneratedPlanID ) as gp on gp.GeneratedPlanID = g.GeneratedPlanID
                  # join to  get actual start quarter understood from the study plan 
        Inner join VsaDev.dbo.Quarter as q1 on gp.StartingQuarter = q1.QuarterID
                # check if the original plan actually has a class scheduled in summer
        Full join         
        (select * from         
        (select  s.GeneratedPlanID,case when s.QuarterID = 4 then 'Yes'        
          end as SummerClass        
          from StudyPlan as s        
          GROUP by s.QuarterID,s.GeneratedPlanID)        
        as d where d.SummerClass = 'Yes') as gp2 on gp2.GeneratedPlanID = g.GeneratedPlanID 
               # calculate number of core courses per quarter ( core = english and math)
        full JOIN        
        (select  s1.GeneratedPlanID, Count(s1.NumberOfCoursesPerQuarter)as NumberOfCorePerQuarter        
          from (        
            select  s.GeneratedPlanID,        
            s.QuarterID,        
            count(s.CourseID) as NumberOfCoursesPerQuarter        
            FROM VsaDev.dbo.StudyPlan as s        
            where s.CourseID in 
            (select CourseID from Course as c where c.CourseNumber like 'MATH%' UNION select CourseID from Course as co1 where co1.CourseNumber like 'ENGL%')        
            GROUP by s.QuarterID,s.GeneratedPlanID)as s1        
          GROUP by s1.GeneratedPlanID) as gp3 on gp3.GeneratedPlanID = g.GeneratedPlanID
                  # find the math starting point
        FULL JOIN        
        (select  s.GeneratedPlanID,        
          MIN(s.CourseID) as MathStarting        
          FROM VsaDev.dbo.StudyPlan as s        
          where s.CourseID in (select CourseID from Course as c where        
            c.CourseNumber like 'MATH%')        
          GROUP by s.GeneratedPlanID) as m1 on m1.GeneratedPlanID = g.GeneratedPlanID 
                 # find the english starting point
        full JOIN        
        (select  s.GeneratedPlanID,        
          MIN(s.CourseID) as EnglishStarting        
          FROM VsaDev.dbo.StudyPlan as s        
          where s.CourseID in (select CourseID from Course as c where c.CourseNumber like 'ENGL%')        
          GROUP by s.GeneratedPlanID) as eng on eng.GeneratedPlanID = g.GeneratedPlanID;")



vaaData = pd.read_sql(data, conn) 




vaaData.shape


# dropped the ids as they dont serve much purpose to my work.

vaaData = vaaData.drop('ParameterSetID',1)
vaaData = vaaData.drop('MajorID',1)
vaaData = vaaData.drop('SchoolID',1)
vaaData = vaaData.drop('JobTypeID',1)
vaaData = vaaData.drop('QuarterPreferenceID',1)
vaaData = vaaData.drop('StartingQuarter',1)
vaaData = vaaData.drop('EnrollmentTypeID',1)

# calculated sequence break which is another feature -- we need math and english starting points for this. Added the .py file.


import CalculateSequenceBreak as cb




c = cb.CalculateSequenceBreak()





mathSequenceBreak = c.get_math_seqBreak()
englishSequenceBreak = c.get_eng_seqBreak()
# print(len(mathSequenceBreak[0]))
labels = ['GeneratedPlanID','mathSequenceBreak']
math_df = pd.DataFrame.from_records(mathSequenceBreak,columns = labels)
# print(math_df)
labels = ['GeneratedPlanID','englishSequenceBreak']
eng_df = pd.DataFrame.from_records(englishSequenceBreak,columns = labels)
# print(eng_df)





math_merged = pd.merge(vaaData, math_df, on='GeneratedPlanID',how = 'outer')





eng_merged = pd.merge(math_merged, eng_df, on='GeneratedPlanID',how = 'outer')


# adding the below file as well, for u to observe.
# this is how the data which is being fed into my classifiers mostly looks like
# i say mostly coz I do some data pre processing.


eng_merged.to_csv("getVAAData_may6.csv")







