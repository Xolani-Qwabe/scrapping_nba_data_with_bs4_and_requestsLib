import os
import pandas as pd


def convert_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

#
#This will take minutes convert to int
# basic['MP'] = basic['MP'].apply(convert_to_minutes)
#
#This will only grab the row where staters == Devin Vassell
# basic[basic['Starters'] == 'Devin Vassell']
