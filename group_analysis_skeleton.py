#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
"""

#%% import block 
import numpy as np
import scipy as sp
import scipy.stats
import os
import shutil


#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename
# I created the paths with variables to take on the iteration value room
testingrooms = ['A','B','C']
for room in testingrooms:
    path_testingroom = 'testingroom' + room + '\experiment_data.csv' 
    path_rawdata = 'rawdata\experiment_data_' + room + '.csv'
    shutil.copy(path_testingroom, path_rawdata)


#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT
#
data = np.empty((0,5))
for room in testingrooms:
    new_path = 'rawdata\experiment_data_' + room + '.csv'
    tmp = sp.loadtxt(new_path, delimiter=',')
    data = np.vstack([data,tmp])
    


#%%
# calculate overall average accuracy and average median RT
# I created a new list, and for each element in 92 elements (since there are
# 92 participants, I want to append the 3rd column of the element row to
# an empty list for accuracy. Same technique for mrt.
# finally, I find the mean and median for the acc and mrt.
acc_list = []
for element in range(92):
    acc_list.append(data[element][3])

mrt_list = []
for element in range(92):
    mrt_list.append(data[element][4])


acc_avg = np.mean(acc_list)*100
mrt_avg = np.median(mrt_list)

#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)
# Similar technique as above, but I want to make sure that if the stimulus
# value is 1 (words), to append the corresponding rt and accuracy to their
# appropriate lists. Else just means 2 (faces) would be appended to
# their appropriate lists.
word_acc = []
word_RT = []
face_acc = []
face_RT = []

for element in range(92):
    stim = int(data[element][1])
    if stim == 1:
        word_acc.append(data[element][3])
        word_RT.append(data[element][4])
    else:
        face_acc.append(data[element][3])
        face_RT.append(data[element][4])
        
        

# words: 88.6%, 489.4ms   
word_acc_avg = np.mean(word_acc)*100
word_mrt_avg = np.mean(word_RT)

#faces: 94.4%, 465.3ms
face_acc_avg = np.mean(face_acc)*100
face_mrt_avg = np.mean(face_RT)

#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)
# Similar method as above, except now looking at white versus black 
# pleasant, and if 1 (white), append to its corresponding lists.
# if it is 2 (black), append to its corresponding list)

acc_wp_list = []
acc_bp_list = []
mrt_wp_list = []
mrt_bp_list = []

for element in range(92):
    stim = int(data[element][2])
    if stim == 1:
        acc_wp_list.append(data[element][3])
        mrt_wp_list.append(data[element][4])
    else:
        acc_bp_list.append(data[element][3])
        mrt_bp_list.append(data[element][4])
        
        

acc_wp = np.mean(acc_wp_list)*100  # 94.0%

acc_bp = np.mean(acc_bp_list)*100  # 88.9%

mrt_wp = np.mean(mrt_wp_list)  # 469.6ms

mrt_bp = np.mean(mrt_bp_list)  # 485.1ms



#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)
# Similar as above, including more conditions. E.g. if stim == 1 and pairing
# == 1, this means words/whitepleasant. And append the corresponding
# values to their lists
words_wp = []
words_bp = []
faces_wp = []
faces_bp = []

for element in range(92):
    stim = int(data[element][1])
    pairing = int(data[element][2])
    if stim == 1 and pairing == 1:
        words_wp.append(data[element][4])
    elif stim == 1 and pairing == 2:
        words_bp.append(data[element][4])
    elif stim == 2 and pairing == 1:
        faces_wp.append(data[element][4])
    elif stim == 2 and pairing == 2:
        faces_bp.append(data[element][4])



# words - white/pleasant: 478.4ms
wwp = np.mean(words_wp)
# words - black/pleasant: 500.3ms
wbp = np.mean(words_bp)
# faces - white/pleasant: 460.8ms
fwp = np.mean(faces_wp)
# faces - black/pleasant: 469.9ms
fbp = np.mean(faces_bp)


#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()
# using the lists of RT for words white pleasant and words black pleasant
# input those into the scipy.stats.ttest_rel() function. 
# same for faces.
import scipy.stats

stats_words = scipy.stats.ttest_rel(words_wp,words_bp)
stats_faces = scipy.stats.ttest_rel(faces_wp,faces_bp)

# words: t=-5.36, p=2.19e-5
# faces: t=-2.84, p=0.0096


#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)
#
print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(acc_avg,mrt_avg))
print('\nAverage reaction time and accuracy for WORDS: {:.2f}%, {:.1f} ms'.format(word_acc_avg,word_mrt_avg))
print('\nAverage reaction time and accuracy for FACES: {:.2f}%, {:.1f} ms'.format(face_acc_avg,face_mrt_avg))
print('\nAverage accuracy for White Pleasant and Black Pleasant: {:.2f}%, {:.2f}%'.format(acc_wp,acc_bp))
print('\nAverage reaction time for White Pleasant and Black Pleasant: {:.1f}ms, {:.1f} ms'.format(mrt_wp,mrt_bp))
print('\nAverage reaction time for WORDS for White Pleasant and Black Pleasant Respectively: {:.1f} ms, {:.1f} ms'.format(wwp,wbp))
print('\nAverage reaction time for FACES for White Pleasant and Black Pleasant Respectively: {:.1f} ms, {:.1f} ms'.format(fwp,fbp))
print('\nt-value and p-value for words respectively: {:.2f}, {:.7f}'.format(stats_words[0],stats_words[1]))
print('\nt-value and p-value for faces respectively: {:.2f}, {:.4f}'.format(stats_faces[0],stats_faces[1]))
