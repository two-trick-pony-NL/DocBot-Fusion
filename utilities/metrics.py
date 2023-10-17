# utils.py
import pandas as pd
from datetime import datetime
import streamlit as st
import os

# Define the folder for CSV files
ANALYTICS_FOLDER = 'analytics'

def get_csv_path(filename):
    return os.path.join(ANALYTICS_FOLDER, filename)

def read_csv_to_df(filename):
    csv_path = get_csv_path(filename)
    return pd.read_csv(csv_path, parse_dates=['timestamp'])

def add_question_row(count):
    filename = 'questions.csv'
    csv_path = get_csv_path(filename)
    questions_df = read_csv_to_df(filename)
    new_row = {'timestamp': datetime.now(), 'question_count': count}
    questions_df = questions_df.append(new_row, ignore_index=True)
    questions_df.to_csv(csv_path, index=False)
    return questions_df

def add_file_row(count):
    filename = 'files.csv'
    csv_path = get_csv_path(filename)
    files_df = read_csv_to_df(filename)
    new_row = {'timestamp': datetime.now(), 'upload_count': count}
    files_df = files_df.append(new_row, ignore_index=True)
    files_df.to_csv(csv_path, index=False)
    return files_df

def add_pageview_row(count):
    filename = 'pageviews.csv'
    csv_path = get_csv_path(filename)
    pageviews_df = read_csv_to_df(filename)
    new_row = {'timestamp': datetime.now(), 'pageview_count': count}
    pageviews_df = pageviews_df.append(new_row, ignore_index=True)
    pageviews_df.to_csv(csv_path, index=False)
    return pageviews_df
