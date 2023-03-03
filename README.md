[![fastapi-test-ci](https://github.com/BigDataIA-Spring2023-Team-08/assignment03-data-as-a-service/actions/workflows/fastapi-test.yml/badge.svg)](https://github.com/BigDataIA-Spring2023-Team-08/assignment03-data-as-a-service/actions/workflows/fastapi-test.yml)

# Assignment 03: Data as a Service

> ✅ Active status <br>
> [🚀 Application link](http://34.73.90.193:8076/) <br>
> [🧑🏻‍💻 FastAPI](http://34.73.90.193:8002/docs) <br>
> [⏱ Airflow](http://34.73.90.193:9000) <br>
> [🎬 Codelab Slides](https://codelabs-preview.appspot.com/?file_id=1JnHebupGexcMGBsASIkyiD3i3Ll14ISlHGPMQ6wKoWU#0) <br>
> 🐳 Docker Hub Images: [FastAPI](https://hub.docker.com/repository/docker/mashruwalav/daas_api_v2/general), [Streamlit](https://hub.docker.com/repository/docker/mashruwalav/daas_streamlit_v2/general)

----- 

## Index
  - [Objective](#objective)
  - [Abstract 📝](#abstract)
  - [Architecture Diagram](#architecture-diagram)
  - [Project Components 💽](#project-components)
  - [FastAPI](#fast-api)
  - [Streamlit](#streamlit) 
  - [Unit Testing ⚒️](#unit-testing)
  - [Steps to run application](#steps-to-run-application)


## Objective
Providing Data as a Service of a Data Exploration Tool for Satellite Imagery Data (NOAA's NexRad and GOES Satellite). Construct a decoupled application with microservices of FastAPI and Streamlit, both published as an image on Docker Hub. Use docker compose to host both services and run live for users to access. 


## Abstract
The task involves decoupling the client and server from our data exploration tool and to host a private streamlit client
This work can help one: 

- Access the publicly available SEVIR satellite radar data in a highly interactive & quick way
- Scrap the data from public AWS S3 buckets to store them into a personal S3 bucket making it convenient to then perform additional tasks or use these saved files from your personal bucket. Government’s public data can always be hard to navigate across but we make it easy with our application
- Get files through the application by 2 options: searching by fields or directly entering a filename to get the URL from the source
- View the map plot of all the NEXRAD satellite locations in the USA


## Architecture Diagram
This architecture diagram depicts the flow of the application and the relationships between services. NOTE: Our proposed diagram is same our final implemented framework

![Architecure Diagram](architectural_diagram_for_assignment_2.png)


## Project Components
- FastAPI: REST API endpoints for the application
- Streamlit: Frontend interface for the Data as a Service application
- Airflow: DAG to scrape & load metadata every midnight into a S3 bucket. Second DAG to perform data quality check of the metadata scraped using Great Expectations
- Docker images: Both FastAPI and Streamlit images have been put on Docker Hub. These images have been pulled using the docker-compose.yml and the application is deployed through GCP live on URL specified above


## Fast API


## Streamlit
The data exploration tool for the Geospatial startup uses the Python library [Streamlit](https://streamlit.iohttps://streamlit.io) for its user interface. The tool offers a user-friendly experience with three distinct pages, each dedicated to NexRad, GOES, and NexRad location maps. On each page, users can choose between downloading satellite data based on filename or specific field criteria. The UI then displays a download link to the S3 bucket, enabling users to successfully retrieve the desired satellite images.

### Streamlit UI layout:

  - Login/ Signup Functionality
    - Login page for returning users to enter username and password to get access to the data exploration application
    - Signup page for new users to enter name, username, password and confirm password to access the application
  - Logout
    - Logout users to end session and return to Login/ Signup page
  - GOES18 data downloader page
      - Download file by entering field values
      - Get public URL by entering filename
  - NEXRAD data downloaded page
      - Download file by entering field values
      - Get public URL by entering filename
  - NEXRAD Maps Location page
  - Analytics Dashboard
      - Plotting a line chart of count of request by each user against time (date)
      - Metric for total API calls the previous day
      - Metric to show total average calls during the last week
      - Comparison of Success ( 200 response code) and Failed request calls(ie non 200 response codes)
      - Each endpoint total number of calls


## Unit Testing
[PyTest](https://docs.pytest.org/en/7.1.x/contents.html) framework implemented to write tests which is easy to use but can be scaled to support functional testing for applications and libraries.
* Create a new file [test_main.py](test_main.py), containing test functions
* Implemented testing functions for all API endpoints. The tests have also been integrated to git actions and run on every commit. The workflow is present at [test_main.py](fastapi-test.yml)

## Steps to run application
1. Download app files
2. Have a ```.env``` file with necessary AWS credentials



-----
> WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK.
> 
> Vraj: 25%, Poojitha: 25%, Merwin: 25%, Anushka: 25%
-----


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

