#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 1 - fall
# 2- winter
# 3 - spring
# 4- summer


# In[2]:


import pyodbc
import pandas as pd


# In[3]:


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


# In[4]:


config = dict(server= '65.175.68.34',
                  port= 1433,
              database= 'VsaDev',
              username= 'sa',
              password= 'H4ZXZy-vRZwL#9A')


# In[5]:


conn_str = ('SERVER={server},{port};'   +
            'DATABASE={database};'      +
            'UID={username};'           +
            'PWD={password}')


# In[6]:


conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 13 for SQL Server};' +
    conn_str.format(**config)
    )


# In[7]:


class ModifySequence():
    def modify_list(self,classList=['a'], quarterList=[1], summerPref=False, startQuarter=[1]):
        count = int(startQuarter[0])
        if(len(classList)!= len(quarterList)):
            raise ValueError(
            "The class length does not match the quarter length")
        if(summerPref is False and startQuarter[0] == 4):
            raise ValueError(
            "Starting quarter and SummerPref should match")
        resultList = []
        for i in range(len(quarterList)):
            if(quarterList[i] == 4 and summerPref is False):
                raise ValueError(
                "Invalid class List")
            if(count == 4 and summerPref is False):
                count = 1
            elif(count == 5):
                count = 1
            if(quarterList[i] != count):
                resultList.append("breaks")
                resultList.append(classList[i].strip())
                count = count +1
            else:
                resultList.append(classList[i].strip())
                count = count + 1
        return resultList


# In[8]:


quarterList = [3, 1, 2, 3]
classList = ['MATH& 163 ', 'MATH& 264 ', 'MATH 260  ', 'MATH 261  ']
summerPref = False
actualstartQtr = [2]


# In[9]:


x = ModifySequence()


# In[10]:


x.modify_list(classList,quarterList,summerPref,actualstartQtr)


# In[11]:


class Graph:
    def __init__(self,vertices):
        from collections import defaultdict
        
        self.graph = defaultdict(list)
        self.visited = defaultdict()
        self.v = vertices
        self.score = 0
        
    def addEdge(self,u,v):
        self.graph[u].append(v)
        self.visited[u] = False

    def getSequenceBreak(self,s,d,courses):
        from collections import defaultdict
        path = []
        self.score =0
        self.getSequenceBreakUtil(s,d,path,courses)
        return self.score
  
    def getSequenceBreakUtil(self,c,d,path,courses):
        from fuzzywuzzy import fuzz
        self.visited[c] = True
        path.append(c)
        if(c==d or c=='end'):
#             print("path=", path)
            s1 = fuzz.ratio(path,courses)
            if(s1 > self.score):
                self.score = s1
#             print(self.score)
        else:
            for i in self.graph[c]:
                if(i=='end'):
                    break
                if(self.visited[i] == False):
                    self.getSequenceBreakUtil(i,d,path,courses)
        path.pop()
        self.visited[c] = False
           


# In[12]:


class generateSequence():
    def __init__(self,seed = None):
        self.math_list = self._initialize_math_list()
        self.eng_list = self._initialize_english_list()
        self.math_graph = self._initialize_math_graph()
        self.english_graph = self._initialize_english_graph()
        
        
    def _initialize_math_list(self):
        x = ("select c.CourseNumber as Course,        c2.CourseNumber as PreReqCourse        from Prerequisite as p        join Course as c on c.CourseID = p.CourseID        join Course as c2 on c2.CourseID = p.PrerequisiteCourseID        where c.CourseNumber like 'MATH%';")
        
        math = pd.read_sql(x, conn)
        return math
    
    def _initialize_english_list(self):
        x = ("select c.CourseNumber as Course,        c2.CourseNumber as PreReqCourse        from Prerequisite as p        join Course as c on c.CourseID = p.CourseID        join Course as c2 on c2.CourseID = p.PrerequisiteCourseID        where c.CourseNumber like 'ENGL%';")
        
        english = pd.read_sql(x,conn)
        return english
    
    def _initialize_math_graph(self):
        testset = {}
        testset = set()
        v = self.math_list.shape[0]
        for i in range(v):
            testset.add(self.math_list.iloc[i]['PreReqCourse'].strip())
        v= len(testset)
        math = Graph(v)
        for i in range(v):
            math.addEdge(self.math_list.iloc[i]['PreReqCourse'].strip(),self.math_list.iloc[i]['Course'].strip())
        math.addEdge('MATH 261','end')
        math.addEdge('MATH 260','end')
        math.addEdge('MATH& 264','end')
        math.addEdge('MATH 146','end')
        math.addEdge('MATH& 148','end')
        math.addEdge('MATH 153','end')
        return math
    
    def _initialize_english_graph(self):
        testset ={}
        testset = set()
        v = self.eng_list.shape[0]
        for i in range(v):
            testset.add(self.eng_list.iloc[i]['PreReqCourse'].strip())
        v = len(testset)
        eng = Graph(v)
        for i in range(v):
            eng.addEdge(self.eng_list.iloc[i]['PreReqCourse'].strip(),self.eng_list.iloc[i]['Course'].strip())
        eng.addEdge('ENGL& 230','end')
        eng.addEdge('ENGL& 102','end')
        return eng
        
    def getMathSequenceBreak(self,mathStart,mathEnd,courseList):
        return(self.math_graph.getSequenceBreak(mathStart,mathEnd,courseList))
    
    def getEnglishSequenceBreak(self,engStart,engEnd,courseList):
        return(self.english_graph.getSequenceBreak(engStart,engEnd,courseList))

    
 


# In[13]:


g = generateSequence()
# c = ClassSequence()
# read the class list from the data frame
# use modify from classSequence to modify
# send it over to calculate the sequence break
# for testing purpose, we shall use courseList..
courseList = ['MATH& 163','MATH 261']

courseListEnglish = ['ENGL& 230']
print("math break=",g.getMathSequenceBreak('MATH& 152','MATH 261',courseList))
print("english break =",g.getEnglishSequenceBreak('ENGL& 101','ENGL& 230',courseListEnglish))


# In[14]:


class CalculateSequenceBreak:
    def __init__(self,seed = None):
        self.mathData = self._initialize_get_mathData()
        self.engData = self._initialize_get_engData()
    
    
    def _initialize_get_mathData(self):
#      need generated plan id to join with the complete feature list
        x = ('select s.GeneratedPlanID,                s.QuarterID,                s.CourseID,                c3.CourseNumber                from StudyPlan as s                join VsaDev.dbo.Course as c3                on c3.CourseID = s.CourseID                where s.CourseID In                (select c.CourseID from VsaDev.dbo.Course as c                join VsaDev.dbo.StudyPlan as sp on sp.CourseID=c.CourseID                where c.CourseNumber like \'MATH%\');')
        classes = pd.read_sql(x,conn)
    
        plans = {plan : g["CourseNumber"].tolist() for plan,g in classes.groupby("GeneratedPlanID")}
        quarter = {plan : g["QuarterID"].tolist() for plan,g in classes.groupby("GeneratedPlanID")}
        planID = {coll : (g["GeneratedPlanID"].drop_duplicates().values.tolist()) for coll,g in classes.groupby("GeneratedPlanID")}

        y = ('select vw.GeneratedPlanID,        min(vw.StartingQuarter) as ActualStart from (select s.GeneratedPlanID,        FIRST_VALUE(s.QuarterID)        OVER(PARTITION BY s.GeneratedPlanID ORDER BY s.YearID )as StartingQuarter        from StudyPlan as s) as vw        group by vw.GeneratedPlanID;')
        
        actual = pd.read_sql(y,conn)
        actualStart = {ac : g["ActualStart"].tolist() for ac,g in actual.groupby("GeneratedPlanID")}

        start = ('select sw.GeneratedPlanID,        sw.MathStartCourse,        c4.CourseNumber as MathStart from        Course as c4 join(select vw.GeneratedPlanID, min(vw.MathStartCourse)as MathStartCourse        from (select s.GeneratedPlanID,        FIRST_VALUE(s.CourseID)        OVER(PARTITION BY s.GeneratedPlanID ORDER BY s.YearID )as MathStartCourse        from StudyPlan as s where s.CourseID In         (select c.CourseID from Course as c        join StudyPlan as sp on sp.CourseID=c.CourseID        where c.CourseNumber like \'MATH%\') ) as vw        group by vw.GeneratedPlanID)as sw on sw.MathStartCourse = c4.CourseID;')
        
        m1 = pd.read_sql(start,conn)
        
        mathStart = {ms :g["MathStart"].tolist() for ms,g in m1.groupby("GeneratedPlanID")}
        
        end =('select sw.GeneratedPlanID,        sw.MathEndCourse,        c4.CourseNumber as MathEnd from        Course as c4 join(select vw.GeneratedPlanID, max(vw.MathEndCourse)as MathEndCourse        from (select s.GeneratedPlanID,        LAST_VALUE(s.CourseID)        OVER(PARTITION BY s.GeneratedPlanID ORDER BY s.YearID )as MathEndCourse        from StudyPlan as s where s.CourseID In         (select c.CourseID from Course as c        join StudyPlan as sp on sp.CourseID=c.CourseID        where c.CourseNumber like \'MATH%\') ) as vw        group by vw.GeneratedPlanID)as sw on sw.MathEndCourse = c4.CourseID;')
        
        e1 = pd.read_sql(end,conn)
        mathEnd = {ms :g["MathEnd"].tolist() for ms,g in e1.groupby("GeneratedPlanID")}
        
        sm1 = ('select gp1.GeneratedPlanID,        ps.SummerPreference        from GeneratedPlan as gp1        join ParameterSet as ps on ps.ParameterSetID = gp1.ParameterSetID        where gp1.GeneratedPlanID in        (select sp1.GeneratedPlanID        from StudyPlan as sp1        join GeneratedPlan as gp on gp.GeneratedPlanID = sp1.GeneratedPlanID);')
   
        s2 = pd.read_sql(sm1,conn)
        summerPref2 = {sp :(g["SummerPreference"].drop_duplicates().values.tolist()) for sp,g in s2.groupby("GeneratedPlanID")}
        
        from collections import defaultdict
        dd = defaultdict(list)
        for d in (planID,plans,quarter,actualStart,mathStart,mathEnd,summerPref2): # you can list as many input dicts as you want here
            for key, value in d.items():
                dd[key].append(value)

        import pandas
        
        data = pandas.DataFrame.from_dict(dd,orient = 'index')
        filtered_df = data[data[6].notnull()]
        filtered_df = filtered_df[filtered_df.index < 546]
        filtered_df.rename(columns={0: 'GeneratedPlanID', 1: 'ClassList'}, inplace=True)
        filtered_df.rename(columns={2:'Quarters',3:'ActualStartQuarter',4:'SubjectStart',5:'SubjectEnd'},inplace = True)
        filtered_df.rename(columns={6:'SummerPref'},inplace = True)
#         filtered_df.drop(filtered_df[filtered_df.GeneratedPlanID >= [546]].index, inplace=True)
        return filtered_df
        
        
    def _initialize_get_engData(self):
        x = ('select s.GeneratedPlanID,            s.QuarterID,            s.CourseID,            c3.CourseNumber            from StudyPlan as s            join VsaDev.dbo.Course as c3            on c3.CourseID = s.CourseID            where s.CourseID In            (select c.CourseID from VsaDev.dbo.Course as c            join VsaDev.dbo.StudyPlan as sp on sp.CourseID=c.CourseID            where c.CourseNumber like \'ENGL%\');')
    
        classes = pd.read_sql(x,conn)
    
        plans = {plan : g["CourseNumber"].tolist() for plan,g in classes.groupby("GeneratedPlanID")}
        quarter = {plan : g["QuarterID"].tolist() for plan,g in classes.groupby("GeneratedPlanID")}
        planID = {coll : (g["GeneratedPlanID"].drop_duplicates().values.tolist()) for coll,g in classes.groupby("GeneratedPlanID")}

        y = ('select vw.GeneratedPlanID,            min(vw.StartingQuarter) as ActualStart from (select s.GeneratedPlanID,            FIRST_VALUE(s.QuarterID)            OVER(PARTITION BY s.GeneratedPlanID ORDER BY s.YearID )as StartingQuarter            from StudyPlan as s) as vw            group by vw.GeneratedPlanID;')
        actual = pd.read_sql(y,conn)
        actualStart = {ac : g["ActualStart"].tolist() for ac,g in actual.groupby("GeneratedPlanID")}
#         print(actualStart)
        
        start = ('select sw.GeneratedPlanID,            sw.EngStartCourse,            c4.CourseNumber as EngStart from            Course as c4 join(select vw.GeneratedPlanID, min(vw.EngStartCourse)as EngStartCourse            from (select s.GeneratedPlanID,            FIRST_VALUE(s.CourseID)            OVER(PARTITION BY s.GeneratedPlanID ORDER BY s.YearID )as EngStartCourse            from StudyPlan as s where s.CourseID In             (select c.CourseID from Course as c            join StudyPlan as sp on sp.CourseID=c.CourseID            where c.CourseNumber like \'ENGL%\') ) as vw            group by vw.GeneratedPlanID)as sw on sw.EngStartCourse = c4.CourseID;')
        
        m1 = pd.read_sql(start,conn)
        
        engStart = {ms :g["EngStart"].tolist() for ms,g in m1.groupby("GeneratedPlanID")}
        
        end =('select sw.GeneratedPlanID,            sw.EngEndCourse,            c4.CourseNumber as EngEnd from            Course as c4 join(select vw.GeneratedPlanID, max(vw.EngEndCourse)as EngEndCourse            from (select s.GeneratedPlanID,            LAST_VALUE(s.CourseID)            OVER(PARTITION BY s.GeneratedPlanID ORDER BY s.YearID )as EngEndCourse            from StudyPlan as s where s.CourseID In             (select c.CourseID from Course as c            join StudyPlan as sp on sp.CourseID=c.CourseID            where c.CourseNumber like \'ENGL%\') ) as vw            group by vw.GeneratedPlanID)as sw on sw.EngEndCourse = c4.CourseID;')
        
        e1 = pd.read_sql(end,conn)
        engEnd = {ms :g["EngEnd"].tolist() for ms,g in e1.groupby("GeneratedPlanID")}
        sm1 = ('select gp1.GeneratedPlanID,        ps.SummerPreference        from GeneratedPlan as gp1        join ParameterSet as ps on ps.ParameterSetID = gp1.ParameterSetID        where gp1.GeneratedPlanID in        (select sp1.GeneratedPlanID        from StudyPlan as sp1        join GeneratedPlan as gp on gp.GeneratedPlanID = sp1.GeneratedPlanID);')
   
        s2 = pd.read_sql(sm1,conn)
        summerPref2 = {sp :(g["SummerPreference"].drop_duplicates().values.tolist()) for sp,g in s2.groupby("GeneratedPlanID")}
        
        from collections import defaultdict
        dd = defaultdict(list)
        for d in (planID,plans,quarter,actualStart,engStart,engEnd,summerPref2): # you can list as many input dicts as you want here
            for key, value in d.items():
                dd[key].append(value)
        import pandas
        data = pandas.DataFrame.from_dict(dd,orient = 'index')
        filtered_df = data[data[6].notnull()]
#         filtered_df.drop(filtered_df[filtered_df.ClassList < 50].index, inplace=True)
        
        filtered_df.rename(columns={0: 'GeneratedPlanID', 1: 'ClassList'}, inplace=True)
        filtered_df.rename(columns={2: 'Quarters',3: 'ActualStartQuarter',4: 'SubjectStart',5: 'SubjectEnd'},inplace=True)
        filtered_df.rename(columns={6:'SummerPref'},inplace = True)
        return filtered_df
    
    def get_math_seqBreak(self):
        c = ModifySequence()
        g = generateSequence()
        mathBreak = []
        for index,row in self.mathData.iterrows():
            modified = c.modify_list(row['ClassList'],row['Quarters'],row['SummerPref'],row['ActualStartQuarter'])
            r = []
            r.append(row['GeneratedPlanID'][0])
            r.append(g.getMathSequenceBreak(row['SubjectStart'][0].strip(),row['SubjectEnd'][0].strip(),modified))
            mathBreak.append(r)
        return mathBreak
    
    def get_eng_seqBreak(self):
        c = ModifySequence()
        g = generateSequence()
        engBreak = []
        for index,row in self.engData.iterrows():
            modified = c.modify_list(row['ClassList'],row['Quarters'],row['SummerPref'],row['ActualStartQuarter'])
            r = []
            r.append(row['GeneratedPlanID'][0])
            r.append(g.getEnglishSequenceBreak(row['SubjectStart'][0].strip(),row['SubjectEnd'][0].strip(),modified))
            engBreak.append(r)
        return engBreak
            
        
        


# In[15]:


# c = CalculateSequenceBreak()


# In[16]:


# mathSequenceBreak = c.get_math_seqBreak()
# englishSequenceBreak = c.get_eng_seqBreak()
# # print(len(mathSequenceBreak[0]))
# labels = ['GeneratedPlanID','MathSequenceBreak']
# math_df = pd.DataFrame.from_records(mathSequenceBreak,columns = labels)
# print(math_df)
# labels = ['GeneratedPlanID','EnglishSequenceBreak']
# eng_df = pd.DataFrame.from_records(englishSequenceBreak,columns = labels)
# print(eng_df)


# In[19]:


# result = pd.merge(math_df, eng_df,on='GeneratedPlanID',how='outer')
# #####df_merge_col = pd.merge(df_row, df3, on='id')


# In[20]:


# result.to_csv("sequenceBreaks.csv")


# In[ ]:




