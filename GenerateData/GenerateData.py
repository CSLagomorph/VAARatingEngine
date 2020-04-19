
import os
import random
from random import randint, choice
import pandas as pd




class datagen():
    def __init__(self,seed = None):
        self.seed = seed
        self.randnum = randint(1, 9)
        self.major_list = self._initialize_major_list()
        self.college_list = self._initialize_college_list()

    def _initialize_major_list(self):
        path = "Majors.txt"
        major_list = []
        with open(path) as fh:
            major_list = [str(line).strip() for line in fh.readlines()]

        return major_list
    
    def _initialize_college_list(self):
        path = "Colleges.txt"
        college_list = []
        with open(path) as fh:
            college_list = [str(line).strip() for line in fh.readlines()]
            
        return college_list

    
    def generate_data(self, num=10, fields=['major'], real_college=True, real_major=True, real_job_type=True, seed=None):
        self._validate_args(num,fields)
        df = pd.DataFrame(data=self.generate_series(num, data_type=fields[0]), columns=[fields[0]])
        for col in fields[1:]:
            if col == 'major' and real_major:
                df['PreferedMajor'] = self.generate_series(num, data_type=col)
            elif col == 'college':
                df['PreferedCollege'] = self.generate_series(num, data_type=col)
            elif col == 'job_type' and real_job_type:
                df['JobType'] = self.generate_series(num, data_type=col)
            elif col =='enrollment_type':
                df['EnrollmentType'] = self.generate_series(num, data_type=col)
            elif col =='quarter':
                df['PreferedStartQuarter'] = self.generate_series(num,data_type = col)
            elif col == 'quarter2':
                df['ActualStartQuarter'] = self.generate_series(num,'quarter')
            elif col =='numQuarters':
                df['PreferedNumberQuarters'] = self.generate_series(num,col)
            elif col =='numQuarters2':
                df['ActualNumberQuarters'] = self.generate_series(num,'numQuarters')
            elif col =='numCore' :
                df['PreferedNumberofCore'] = self.generate_series(num,col)
            elif col =='actualNumCore':
                df['ActualNumberofCore'] = self.generate_series(num,col)
            elif col =='summerPref':
                df['SummerPref'] = self.generate_series(num,col)
            elif col == 'summer':
                df['ActualSummerPref'] = self.generate_series(num,'summerPref')
            elif col == 'mathSequenceBreak':
                df['mathSequenceBreak'] = self.generate_series(num,col)
            elif col == 'englishSequenceBreak':
                df['englishSequenceBreak'] = self.generate_series(num,col)
        return df

    def generate_series(self, num=10, data_type='major', seed=None):
        if type(data_type) != str:
            raise ValueError(
                "Data type must be of type str, found " + str(type(data_type)))
        try:
            num = int(num)
        except:
            raise ValueError(
                'Number of samples must be a positive integer, found ' + num)

        if num <= 0:
            raise ValueError(
                'Number of samples must be a positive integer, found ' + num)

        num = int(num)
        func_lookup = {
            'major': self.major,
            'college': self.college,
            'job_type': self.job_type,
            'enrollment_type': self.enrollment_type,
            'quarter' : self.quarter,
            'numQuarters' : self.numQuarters,
            'numCore':self.numCore,
            'actualNumCore':self.actualNumCore,
            'summerPref':self.summerPref,
            'mathSequenceBreak' : self.mathsequenceBreak,
            'englishSequenceBreak' : self.engsequenceBreak
        }
        if data_type not in func_lookup:
            raise ValueError("Data type must be one of " +
                             str(list(func_lookup.keys())))

        datagen_func = func_lookup[data_type]
        return pd.Series((datagen_func() for _ in range(num)))

    def mathsequenceBreak(self,seed =None):
        random_int = randint(0,100)
        return random_int
#     though it is practically possible to get a sequencebreak 
# less that 30, it was not observed in the real data
    def engsequenceBreak(self,seed =None):
        random_int = randint(30,100)
        return random_int
    def summerPref(self,seed = None):
        summerPref =['yes','no']
        return choice(summerPref)
    def actualNumCore(self,seed = None):
        random_int = randint(0,7)
        return random_int
    def numCore(self,seed=None):
        random_int = randint(1,6)
        return random_int
    def numQuarters(self,seed=None):
        random_int = randint(1,30)
        return random_int
    def major(self, seed=None):
        random.seed(self.seed)
        return choice(self.major_list)
    def college(self, seed = None):
        random.seed(self.seed)
        return choice(self.college_list)
    def enrollment_type(self, seed = None):
        type = ['Full Time','Part Time']
        return choice(type)
    def job_type(self, seed = None):
        type = ['Full Time','Part Time','Unemployed']
        return choice(type)
    def quarter(self,seed = None):
        type = ['Fall','Winter','Spring','Summer']
        return choice(type)
    
    def _validate_args(self, num, fields):
        try:
            num = int(num)
        except:
            raise ValueError(
                'Number of samples must be a positive integer, found ' + num)
        if num <= 0:
            raise ValueError(
                'Number of samples must be a positive integer, found ' + num)

        num_cols = len(fields)
        if num_cols < 0:
            raise ValueError(
                "Please provide at least one type of data field to be generated")
    
    




x = datagen()





# import time
# t1 = time.time()
# x.generate_data(500,['major','college','job_type','enrollment_type','quarter','quarter2','numQuarters',
#                         'numQuarters2','numCore','actualNumCore','summerPref','summer','mathSequenceBreak',
#                     'englishSequenceBreak'])
# t2 = time.time()

# print("500 ",t2-t1)
# t1 = time.time()
# x.generate_data(5000,['major','college','job_type','enrollment_type','quarter','quarter2','numQuarters',
#                         'numQuarters2','numCore','actualNumCore','summerPref','summer','mathSequenceBreak',
#                     'englishSequenceBreak'])
# t2 = time.time()

# print("5000 ", t2-t1)
# t1 = time.time()
# x.generate_data(50000,['major','college','job_type','enrollment_type','quarter','quarter2','numQuarters',
#                         'numQuarters2','numCore','actualNumCore','summerPref','summer','mathSequenceBreak',
#                     'englishSequenceBreak'])
# t2 = time.time()

# print("50k ", t2-t1)
# t1 = time.time()
# x.generate_data(100000,['major','college','job_type','enrollment_type','quarter','quarter2','numQuarters',
#                         'numQuarters2','numCore','actualNumCore','summerPref','summer','mathSequenceBreak',
#                     'englishSequenceBreak'])
# t2 = time.time()

# print("100k ", t2-t1)
    





# t1 = time.time()
# x.generate_data(500000,['major','college','job_type','enrollment_type','quarter','quarter2','numQuarters',
#                         'numQuarters2','numCore','actualNumCore','summerPref','summer','mathSequenceBreak',
#                     'englishSequenceBreak'])
# t2 = time.time()

# print("500k ", t2-t1)
# # 





y = x.generate_data(50000,['major','college','job_type','enrollment_type','quarter','quarter2','numQuarters',
                        'numQuarters2','numCore','actualNumCore','summerPref','summer','mathSequenceBreak',
                    'englishSequenceBreak'])





y.rename(columns={'major': 'PreferedMajor'}, inplace=True)




y.to_csv("Test_Data_may17.csv")

# # The data generation above has more deviation from the original data as we are trying to consider
#  all the possible cases rather than just the cases given in the original data. The original data at 
#  the point of creation was not very diverse and had more plans which fall in an average case. similarly 
#  with the new data.  






# In[ ]:




