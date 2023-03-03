import typer
import requests
import json
from schema import Plan
from wsgiref import headers


#API_URL = "http://127.0.0.1:8080" 
API_URL = "http://34.73.90.193:8002"

app = typer.Typer()
users_app = typer.Typer()
app.add_typer(users_app, name="users")
session =requests.session() #creating session
headers = session.headers  #declaring headers as global variable

@users_app.command("create")
def create_user(name: str = typer.Option(..., prompt= "Enter your name"), username: str = typer.Option(..., prompt= "Enter your username"), password : str = typer.Option(...,prompt = "Please enter your password",confirmation_prompt= True), plan :  Plan = typer.Option(..., prompt = "Please choose a plan"), user_type : str = typer.Option(["user, admin"], prompt="Are you a user or admin?") ):
    '''
    Create an account by entering name, username, password and choose a plan
    '''
    payload = {'name': name, 'username': username, 'password': password, 'plan': plan, 'user_type' : user_type}
    response = requests.request("POST", f"{API_URL}/user/create", json=payload)  #referencing fastapi to create a user in the database
    print(response)
    print(f"Creating user: {username} in plan: {plan}")   

@users_app.command("login")
def login(username : str = typer.Option(...,prompt="Enter Username"), password: str = typer.Option(..., prompt="Enter Password")):
    '''
    Login using username and password to be granted an access token in order to perform authorized tasks
    '''
    global headers
    payload = {'username' : username, 'password' : password}
    response = requests.request("POST",f"{API_URL}/login",data=payload)
    json_data = json.loads(response.text)
    #print(json_data['access_token'])
    if response.status_code ==200:
        access_token = json_data['access_token']
        #headers = {'User-Agent': 'python-requests/2.26.0', 'Accept-Encoding': 'gzip, deflate, br', 'Accept': '*/*', 'Connection': 'keep-alive'}
        #print('Before adding Authorization:', headers)
        headers['Authorization'] = f"Bearer {access_token}"  #always throws error here!
        #print('After adding Authorization:', headers)
        session.headers.update({'Authorization': 'Bearer ' + access_token})  
        print(session.headers)
        #print("working")
    else:
        print("Incorrect username or password.")

@users_app.command("changepassword")
def change_password(username: str = typer.Option(...,prompt = "Enter username"),new_password: str = typer.Option(...,prompt="Enter new password", confirmation_prompt=True) ):
    '''
    Change password by entering your username and new password
    '''
    payload = {'password' : new_password}
    response = requests.request("PATCH", f"{API_URL}/user/update?username={username}", json=payload, headers=headers) #referencing fastapi to change a user's password in the database 
    if response.status_code == 200:
        print("Password updated successfully!")
    else:
        print(response)

@users_app.command("download")
def download_by_filename(username : str = typer.Option(...,prompt="Enter Username to login"), password: str = typer.Option(..., prompt="Enter Password"), dataset : str = typer.Option(...,prompt="Choose one- GOES18 or NEXRAD")):
    '''
    Download files from goes18 or nexrad by entering the filename
    '''

    payload = {'username' : username, 'password' : password}
    login_resp = requests.request("POST",f"{API_URL}/login",data=payload)
    if(login_resp.status_code==200):
        json_data = json.loads(login_resp.text)
        json_data['access_token']
        access_token = json_data['access_token']
        global headers
        headers['Authorization'] = f"Bearer {access_token}"
        if dataset == "GOES18":
            file_name=input("Enter file name: ")
            response = requests.request("POST", f"{API_URL}/fetchfile/goes18?file_name={file_name}", headers=headers)   #api request to get file from nexrad 
            if response.status_code == 200:
                json_data = json.loads(response.text)
                final_url = json_data   #store reponse data
                print("Found URL of the file available on GOES18 bucket!")     #display success message
                print("URL to file: ", final_url)
                return
            else:
                print("Incorrect file name given, please change!")
                return
        elif dataset == "NEXRAD":
            file_name=input("Enter file name: ")
            response = requests.request("POST", f"{API_URL}/fetchfile/nexrad?file_name={file_name}", headers=headers)   #api request to get file from nexrad 
            if response.status_code == 200:
                json_data = json.loads(response.text)
                final_url = json_data   #store reponse data
                print("Found URL of the file available on NEXRAD bucket!")     #display success message
                print("URL to file: ", final_url)
                return
            else:
                print("Incorrect file name given, please change!")
                return
        else:
            print("Please enter one of the 2 options above")
            return
    else:
        print("Incorrect username or password.")
        return

    payload = {file_name : file_name}
    if dataset == "goes18":
        response = requests.request("GET", f"{API_URL}/fetchfile/goes18",json=payload) #api request to get file from goes18
    elif dataset == "nexrad":
        response = requests.request("POST", f"{API_URL}/fetchfile/nexrad?file_name={file_name}", headers=header)   #api request to get file from nexrad 
    print(response)
    print("Download link!")

@users_app.command("fetch")
def list_files(username : str = typer.Option(...,prompt="Enter Username to login"), password: str = typer.Option(..., prompt="Enter Password"), dataset : str = typer.Option(...,prompt="Choose one- GOES18 or NEXRAD")):

    '''
    List all files in a bucket. 
    The format for choosing for GOES18 is : GOES18 Product Year Day Hour 
    The format for choosing for NEXRAD is : NEXRAD Year Month Day Ground Station
    '''

    payload = {'username' : username, 'password' : password}
    login_resp = requests.request("POST",f"{API_URL}/login",data=payload)
    if(login_resp.status_code==200):
        json_data = json.loads(login_resp.text)
        json_data['access_token']
        access_token = json_data['access_token']
        global headers
        headers['Authorization'] = f"Bearer {access_token}"
        if dataset == "GOES18":
            year=input("Enter year: ")
            day=input("Enter day: ")
            hour=input("Enter hour: ")
            print("Product is ABI-L1b-RadC by default")
            product = "ABI-L1b-RadC"
            response = requests.request("GET",f"{API_URL}/s3/goes18?year={year}&day={day}&hour={hour}&product={product}", headers=headers)
            if response.status_code == 200:
                json_data = json.loads(response.text)
                files_in_selected_hour = json_data  #store response data
                print("List of files loading...")
                print(files_in_selected_hour)
                return
            else:
                print("Incorrect input given, please change the inputs!")
                return
        elif dataset == "NEXRAD":
            year=input("Enter year: ")
            month=input("Enter month: ")
            day=input("Enter day: ")
            ground_station=input("Enter ground station: ")
            response = requests.request("GET",f"{API_URL}/s3/nexrad?year={year}&month={month}&day={day}&ground_station={ground_station}", headers=headers)
            if response.status_code == 200:
                json_data = json.loads(response.text)
                files_in_selected_hour = json_data  #store response data
                print("List of files loading...")
                print(files_in_selected_hour)
                return
            else:
                print("Incorrect input given, please change the inputs!")
                return
        else:
            print("Please enter one of the 2 options above")
            return
    else:
        print("Incorrect username or password.")
        return

if __name__ == "__main__":
    app()