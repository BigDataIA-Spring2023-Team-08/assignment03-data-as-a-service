import os
import boto3
import time
import pandas as pd
from datetime import datetime, timedelta
import re
import requests
import sqlite3
from sqlite3 import Connection
import schema, userdb, db_model, oauth2
from fastapi import FastAPI, APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from get_database_file import get_database_file, get_userdb_file
from dotenv import load_dotenv

#load env variables
load_dotenv()

#create router object
router = APIRouter(
    prefix="/logs",
    tags=['logs']
)

@router.get('/admin', status_code=status.HTTP_200_OK)
async def get_admin_logs(current_user: schema.User = Depends(oauth2.get_current_user), userdb_conn : Connection = Depends(get_userdb_file)):

    #define the log client
    clientLogs = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_LOG_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_LOG_SECRET_KEY')
                        )

    #define log group and stream names
    log_group_name = 'assignment-03'
    log_stream_name = 'api'
    query = f"fields @timestamp, @message | sort @timestamp asc | filter @logStream='{log_stream_name}'" #define a log query to get the required logs from the given log stream
    response = clientLogs.start_query(
        logGroupName=log_group_name,
        startTime=0,
        endTime=int(time.time() * 1000),
        queryString=query,
        limit=10000
    )

    #wait for query to complete
    query_id = response['queryId']
    response = None
    while response is None or response['status'] == 'Running':
        print('Waiting for query to complete...')
        time.sleep(1)
        response = clientLogs.get_query_results(    #get all logs
            queryId=query_id
        )

    #parse log events and create DataFrame
    events = []
    for event in response['results']:
        timestamp = datetime.strptime(event[0]['value'], '%Y-%m-%d %H:%M:%S.%f')    #change the timestamp column from millisecond format to datetime
        message = event[1]['value']
        split_msg = message.split(":")  #define strategy to capture endpoint name, user, response code from the log message
        endpoint = split_msg[1].strip().split()[0]  #capture the string for endpoint
        user = split_msg[2].strip().split()[0]   #capture the string for user
        response = split_msg[3].strip().split()[0]  #capture the string for response code
        events.append((timestamp, message, endpoint, user, response))    #store every detail in events
    df_requests = pd.DataFrame(events, columns=['timestamp', 'message', 'endpoint', 'user', 'response'])    #create df from events

    return df_requests


@router.get('/user', status_code=status.HTTP_200_OK)
async def get_user_logs(username : str, current_user: schema.User = Depends(oauth2.get_current_user), userdb_conn : Connection = Depends(get_userdb_file)):

    #define the log client
    clientLogs = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_LOG_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_LOG_SECRET_KEY')
                        )

    #define log group and stream names
    log_group_name = 'assignment-03'
    log_stream_name = 'api'
    query = f"fields @timestamp, @message | sort @timestamp asc | filter @logStream='{log_stream_name}'"    #define a log query to get the required logs from the given log stream
    response = clientLogs.start_query(  #run a logs insights query
        logGroupName=log_group_name,
        startTime=0,    #start time is beginning of the logs file
        endTime=int(time.time() * 1000),    #end time is current time
        queryString=query,  #query defined above
        limit=10000 #in case the number of events returned is huge limit to 10000
    )

    #wait for query to complete
    query_id = response['queryId']
    response = None
    while response is None or response['status'] == 'Running':
        print('Waiting for query to complete...')
        time.sleep(1)
        response = clientLogs.get_query_results(    #get all logs
            queryId=query_id
        )

    #parse log events and create DataFrame
    events = []
    for event in response['results']:
        timestamp = datetime.strptime(event[0]['value'], '%Y-%m-%d %H:%M:%S.%f')    #change the timestamp column from millisecond format to datetime
        message = event[1]['value']
        split_msg = message.split(":")  #define strategy to capture endpoint name, user, response code from the log message
        user = split_msg[2].strip().split()[0]  #capture the string for user
        if (user == username):  #before adding any log event check if the user in the event is equal to current user's username
            #after filtering user
            endpoint = split_msg[1].strip().split()[0]  #capture the string for endpoint
            response = split_msg[3].strip().split()[0]  #capture the string for response code
            events.append((timestamp, message, endpoint, user, response))   #store every detail in events
        else:
            #if user is different
            pass
    df_requests = pd.DataFrame(events, columns=['timestamp', 'message', 'endpoint', 'user', 'response'])    #create df from events

    return df_requests



@router.get('/latest', status_code=status.HTTP_200_OK)
async def get_latest_user_logs(username : str, current_user: schema.User = Depends(oauth2.get_current_user), userdb_conn : Connection = Depends(get_userdb_file)):

    #define the log client
    clientLogs = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_LOG_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_LOG_SECRET_KEY')
                        )

    #define log group and stream names
    log_group_name = 'assignment-03'
    log_stream_name = 'api'
    #calculate start time of filtering log records as 1 hour ago
    start_time = datetime.utcnow() - timedelta(hours=1)
    startTime = int(start_time.timestamp() * 1000)
    query = f"fields @timestamp, @message | sort @timestamp asc | filter @logStream='{log_stream_name}'"    #define a log query to get the required logs from the given log stream
    response = clientLogs.start_query(  #run a logs insights query
        logGroupName=log_group_name,
        startTime=startTime,    #start time is 1 hour ago
        endTime=int(time.time() * 1000),    #end time is current time
        queryString=query,  #query defined above
        limit=10000 #in case the number of events returned is huge limit to 10000
    )

    #wait for query to complete
    query_id = response['queryId']
    response = None
    while response is None or response['status'] == 'Running':
        print('Waiting for query to complete...')
        time.sleep(1)
        response = clientLogs.get_query_results(    #get all logs
            queryId=query_id
        )

    #parse log events and create DataFrame
    events = []
    for event in response['results']:
        timestamp = datetime.strptime(event[0]['value'], '%Y-%m-%d %H:%M:%S.%f')    #change the timestamp column from millisecond format to datetime
        message = event[1]['value']
        split_msg = message.split(":")  #define strategy to capture endpoint name, user, response code from the log message
        user = split_msg[2].strip().split()[0]  #capture the string for user
        if (user == username):  #before adding any log event check if the user in the event is equal to current user's username
            #after filtering user
            endpoint = split_msg[1].strip().split()[0]  #capture the string for endpoint
            response = split_msg[3].strip().split()[0]  #capture the string for response code
            events.append((timestamp, message, endpoint, user, response))   #store every detail in events
        else:
            #if user is different
            pass
    df_requests = pd.DataFrame(events, columns=['timestamp', 'message', 'endpoint', 'user', 'response'])    #create df from events

    return df_requests