#!/usr/bin/env python
# coding: utf-8

# In[144]:


import pandas as pd
import numpy as np
import random


# In[145]:


# i = 1
# five = 0
# four = 0
# three =0
# two = 0
# one = 0
# minus =0
# max_num = 0
# min_num =500
# for index,row in df.iterrows():
#     penalty = 0
#     if(row['ActualNumberQuarters'] < 6 and row['ActualNumberQuarters'] > 20):
#         penalty = penalty + 15
#     if(row['JobType'] == 'Full Time' and row['EnrollmentType'] =='Full Time'
#            and row['ActualNumberofCore'] >4):
#         penalty = penalty + 15
#     elif(row['JobType'] == 'Unemployed' and row['EnrollmentType'] == 'Full Time' 
#            and row['ActualNumberofCore'] < 4):
#         penalty = penalty +15
#     if(row['SummerPref'] != row['ActualSummerPref']):
#         penalty = penalty +8
#     if(row['ActualStartQuarter'] != row['PreferedStartQuarter']):
#         penalty = penalty +7
#     if (row['EnrollmentType'] == 'Full Time' and row['ActualNumberofCore'] <4):
#         penalty = penalty + 6
#     elif(row['EnrollmentType'] == 'Part Time' and row['ActualNumberofCore']<2):
#         penalty = penalty + 6
#     if(row['JobType']=='Full Time' and row['ActualNumberofCore']>4):
#         penalty = penalty +6
#     if(row['ActualNumberQuarters'] is not None and row['PreferedNumberQuarters'] is not None):
#         if(abs(row['PreferedNumberQuarters'] - row['ActualNumberQuarters'] >2)):
#             penalty = penalty +3*2
#         elif(abs(row['PreferedNumberQuarters'] - row['ActualNumberQuarters'] >4)):
#             penalty = penalty +3*4
#         elif(abs(row['PreferedNumberQuarters'] - row['ActualNumberQuarters'] >6)):
#             penalty = penalty +3*6
#         elif(abs(row['PreferedNumberQuarters'] - row['ActualNumberQuarters'] >8)):
#             penalty = penalty +3*8
#     if(row['mathSequenceBreak'] >= 0 and row['mathSequenceBreak'] <30.0):
#         penalty = penalty +20*8
#     elif(row['mathSequenceBreak'] >= 30.0 and row['mathSequenceBreak'] <55.0):
#         penalty = penalty+20*6
#     elif(row['mathSequenceBreak'] >= 55 and row['mathSequenceBreak'] <70.0):
#         penalty = penalty +20*4
#     elif(row['mathSequenceBreak'] >= 70.0 and row['mathSequenceBreak'] <90.0):
#         penalty = penalty +20*2
#     elif(row['mathSequenceBreak'] >= 90):
#         penalty = penalty +0
#     if(row['englishSequenceBreak'] >= 30.0 and row['englishSequenceBreak'] <50.0):
#         penalty = penalty+20*6
#     elif(row['englishSequenceBreak'] >= 50 and row['englishSequenceBreak'] <70.0):
#         penalty = penalty +20*4
#     elif(row['englishSequenceBreak'] >= 70.0 and row['englishSequenceBreak'] <80.0):
#         penalty = penalty +20*2
#     elif(row['englishSequenceBreak'] >= 80):
#         penalty = penalty +0
#     if(max_num<penalty):
#         max_num = penalty
#     if(min_num>penalty):
#         min_num = penalty
#     if(penalty >= 275 and penalty <330):
#         minus = minus +1
#     elif(penalty >=220 and penalty <275):
#         one = one+1
#     elif(penalty >=165 and penalty <220):
#         two = two+1
#     elif(penalty >=110 and penalty <165):
#         three = three+1
#     elif(penalty >=55 and penalty <110):
#         four = four+1
#     elif(penalty >=0 and penalty <150):
#         five = five+1
# print("maax penalty = ",max_num," min penalty = ",min_num)  
# print('275-330  ',minus)
# print('220-275  ',one)
# print('165-220  ',two)
# print('110-165  ',three)
# print('55-110  ',four)
# print('0-55   ',five)


# In[146]:


class LabelData:
    def label_data(self, df):
        label = []
        for index,row in df.iterrows():
            penalty = 0
            if(row['ActualNumberQuarters'] < 8 and row['ActualNumberQuarters'] > 18):
                penalty = penalty + 15
            if(row['JobType'] == 'Full Time' and row['EnrollmentType'] =='Full Time'
                   and row['ActualNumberofCore'] >3):
                penalty = penalty + 15
            elif(row['JobType'] == 'Unemployed' and row['EnrollmentType'] == 'Full Time' 
                   and row['ActualNumberofCore'] < 4):
                penalty = penalty +15
            if(row['SummerPref'] != row['ActualSummerPref']):
                penalty = penalty +8
            if(row['ActualStartQuarter'] != row['PreferedStartQuarter']):
                penalty = penalty +7
            if (row['EnrollmentType'] == 'Full Time' and row['ActualNumberofCore'] <4):
                penalty = penalty + 6
            elif(row['EnrollmentType'] == 'Part Time' and row['ActualNumberofCore']<2):
                penalty = penalty + 6
            if(row['JobType']=='Full Time' and row['ActualNumberofCore']>4):
                penalty = penalty +6
            if(row['ActualNumberQuarters'] is not None and row['PreferedNumberQuarters'] is not None):
                if(abs(row['PreferedNumberQuarters'] - row['ActualNumberQuarters'] >2)):
                    penalty = penalty +3*2
                elif(abs(row['PreferedNumberQuarters'] - row['ActualNumberQuarters'] >4)):
                    penalty = penalty +3*4
                elif(abs(row['PreferedNumberQuarters'] - row['ActualNumberQuarters'] >6)):
                    penalty = penalty +3*6
                elif(abs(row['PreferedNumberQuarters'] - row['ActualNumberQuarters'] >8)):
                    penalty = penalty +3*8
            if(row['PreferedMajor'] is 'Aeronautical Engineering' or row['PreferedMajor'] is'Business'
            or row['PreferedMajor'] is'Graphic Design' or row['PreferedMajor']is'Nursing'
            or row['PreferedMajor']is'Pre-Engineering - General Engineering Transfer'):
                penalty = penalty + 0;
            else:
                if(row['mathSequenceBreak'] >= 0 and row['mathSequenceBreak'] <30.0):
                    penalty = penalty +20*8
                elif(row['mathSequenceBreak'] >= 30.0 and row['mathSequenceBreak'] <55.0):
                    penalty = penalty+20*6
                elif(row['mathSequenceBreak'] >= 55 and row['mathSequenceBreak'] <70.0):
                    penalty = penalty +20*4
                elif(row['mathSequenceBreak'] >= 70.0 and row['mathSequenceBreak'] <90.0):
                    penalty = penalty +20*2
                elif(row['mathSequenceBreak'] >= 90):
                    penalty = penalty + 0;
                if(row['englishSequenceBreak'] >= 30.0 and row['englishSequenceBreak'] <50.0):
                    penalty = penalty+20*6
                elif(row['englishSequenceBreak'] >= 50 and row['englishSequenceBreak'] <70.0):
                    penalty = penalty +20*4
                elif(row['englishSequenceBreak'] >= 70.0 and row['englishSequenceBreak'] <80.0):
                    penalty = penalty +20*2
                elif(row['englishSequenceBreak'] >= 80):
                    penalty = penalty +0
                
                
#             if(max_num<penalty):
#                 max_num = penalty
#             if(min_num>penalty):
#                 min_num = penalty
            if(penalty >= 275 and penalty <330):
                label.append(-1)
            elif(penalty >=220 and penalty <275):
                label.append(1)
            elif(penalty >=165 and penalty <220):
                label.append(2)
            elif(penalty >=110 and penalty <165):
                label.append(3)
            elif(penalty >=55 and penalty <110):
                label.append(4)
            elif(penalty >=0 and penalty <55):
                label.append(5)
#         label2 = label
#         rank = [-1,1,2,3,4,5]
#         for index, x in enumerate(label):
#             if random.randint(0, 1):
#                 label2[index] = random.choice(rank)

# this part of the code can be used to analyze the number of labels which are deviating from the ideal labels
#         count = 0
#         for i, j in zip(label, label2):
#             if (i == j):
#                 count = count +1
#         print(count)


#         https://stackoverflow.com/questions/46157755/how-to-randomly-replace-elements-of-list-with-another-list-elements

        return label
#     print("maax penalty = ",max_num," min penalty = ",min_num)  
#     print('275-330  ',minus)
#     print('220-275  ',one)
#     print('165-220  ',two)
#     print('110-165  ',three)
#     print('55-110  ',four)
#     print('0-55   ',five)


# In[153]:


# lb = LabelData()


# In[154]:


# df = pd.read_csv('test.csv')

# df = df.drop('Unnamed: 0',1)
# print(df.head(2))
# print(df.shape)


# In[155]:


# labels = lb.label_data(df)


# In[156]:


# print(len(labels))


# In[ ]:




