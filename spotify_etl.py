import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
from requests import post, get
import json
from datetime import datetime,timedelta
import sqlite3
from urllib.parse import urlencode, urlparse, parse_qs
import base64
from dotenv import  load_dotenv
load_dotenv()
import os
import secrets
import hashlib



# WebDriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC





# Generate code verifier
def generate_random_string(length):
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789' #Note this code is nothing special but a placeholder.
    values = [secrets.randbelow(len(possible)) for _ in range(length)]
    return ''.join([possible[x % len(possible)] for x in values])


# Generate code challenge
def sha256(plain):
    return hashlib.sha256(plain.encode('utf-8')).digest()


# Generate a base64 encode
def base64encode(input):
    return base64.urlsafe_b64encode(input).rstrip(b'=').decode()


# Generate access token Finally
def get_token(code):
    code_ver = os.getenv('CODE_VERIFIER')
    
    url = 'https://accounts.spotify.com/api/token'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    data = {
        'client_id': CLIENT_ID,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'code_verifier': code_ver
    }
    
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    # print('\n\n\n', json_result)
    token = json_result['access_token']
    
    return token


# Get hearder for API calls
def get_auth_header(token):
    return {'Authorization': f'Bearer {token}'}


# Get recently play tracks of user
def recently_played_tracks(token):
    today = datetime.now()
    two_days_ago = today - timedelta(days=1)
    two_days_ago_unix_timestamp = int(two_days_ago.timestamp()) * 1
    # ten_mins = today - timedelta(minutes=10)
    # ten_mins_unix_timestamp = int(ten_mins.timestamp()) * 1
    url = 'https://api.spotify.com/v1/me/player/recently-played'
    headers = get_auth_header(token)
    query = f'?after={two_days_ago_unix_timestamp}'
    query_url = url+query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    # print('\n\n\n', json_result['items'])
    return json_result


# Check data validity then transform
def check_data_validity(df: pd.DataFrame) -> bool:
    # check if dataframe is empty
    if df.empty:
        print("No track data extracted. Finishing execution...")
        return False
    
    # Primary key selection check
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception('Primary Key check violated')
    
    # Check for null values
    if df.isnull().values.any():
        raise Exception("Null values found")
    
    # # Check for duplicates
    # if df.duplicated().any():
    #     df.drop_duplicates(inplace=True)
    
    # check that data timestamps are from yesterdays date
    # yesterday = datetime.now() - timedelta(days=1)
    # yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # timestamps = df['timestamp'].to_list()
    # for timestamp in timestamps:
    #     if datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
    #         raise Exception('At least one of the songs is not fro last 24 hours')
        
    return True





# DATABASE_LOCATION = "sqlite:///nathan_played_tracks.sqlite"

# # Supplying Credentials client ID and redirect URI
# CLIENT_ID = os.getenv("CLIENT_ID")
# REDIRECT_URI = os.getenv("REDIRECT_URI")
# # CLIENT_SECRET = os.getenv("CLIENT_SECRETE")








def autorun_spotify_etl():
    
    DATABASE_LOCATION = "sqlite:///nathan_played_tracks.sqlite"

    # Supplying Credentials client ID and redirect URI
    CLIENT_ID = os.getenv("CLIENT_ID")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    # CLIENT_SECRET = os.getenv("CLIENT_SECRETE")

    code_verifier = generate_random_string(64)  # Replace with your actual code verifier
    hashed = sha256(code_verifier)
    code_challenge = base64encode(hashed)  # Replace with the actual code challenge calculated in Python
    # print(f"Code Challenge: {code_challenge}")


    # Store code_verifier (this would be more secure in a real application)
    # For this example, we're just storing it in a variable
    # You might want to use a more secure method, such as a secure database or session management
    os.environ['CODE_VERIFIER'] = code_verifier


    # Construct the authorization URL
    auth_url = "https://accounts.spotify.com/authorize"
    scope = 'user-read-private user-read-email user-read-recently-played'


    # Prepare parameters for the URL
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': scope,
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge,
        'redirect_uri': REDIRECT_URI,
    }


    # Append parameters to the URL
    auth_url_with_params = f"{auth_url}?{urlencode(params)}"

    # # Redirect to the authorization URL
    # webbrowser.open(auth_url_with_params)
    # Redirect to the authorization URL

    # print(f"Authorization URL: {auth_url_with_params}")



    # Once the user grants permission and is redirected back to the redirect_uri,
    # you can extract the 'code' parameter from the URL and use it to request the access token.

    # In a real application, you might want to handle the authorization callback in a web server,
    # but for this example, let's assume the user manually retrieves the code from the redirect URL.
    # You would get the 'code' parameter using a similar approach to the JavaScript example.

    # Now, you can use the following function to request the access token:

    # os.system(f"open {auth_url_with_params}")

    # Open the authorization URL in the default web browser
    # webbrowser.open(auth_url_with_params)









    # Set the path to your WebDriver executable
    # webdriver_path = '/Users/nate/Documents/Projects/chromedriver-mac-x64/chromedriver'

    # Create Chrome options
    chrome_options = Options()

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=chrome_options) #executable_path=webdriver_path,

    # Wait for 5 seconds (adjust the timeout as needed)
    wait = WebDriverWait(driver, 10)

    # Navigate to your authorization URL
    driver.get(auth_url_with_params)
    wait


    # Locate the username and password input fields, and the login button
    username_input = driver.find_element(By.ID, 'login-username')  # Replace 'your_username_input_id' with the actual ID
    password_input = driver.find_element(By.ID, 'login-password')  # Replace 'your_password_input_id' with the actual ID
    login_button = driver.find_element(By.ID, 'login-button')  # Replace 'your_login_button_id' with the actual ID

    # Input username and password
    username_input.send_keys(os.getenv("USERNAME"))
    WebDriverWait(driver, 2)
    password_input.send_keys(os.getenv("PASSWORD"))
    WebDriverWait(driver, 2)

    # Click the login button
    login_button.click()


    # Wait for the verify button to be clickable
    verify_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="auth-accept"]')))

    # Locate the verify button
    # verify_button = driver.find_element(By.CLASS_NAME, 'Button-sc-qlcn5g-0 ikLBZY') 

    # Click the verify button
    verify_button.click()

    # Wait for the user to perform the authorization process (you might need to customize this)
    # input("Perform the authorization in the browser, then press Enter in this terminal.")


    # Get the current URL from the browser's address bar
    reload_button = wait.until(EC.element_to_be_clickable((By.ID, 'reload-button')))
    current_url = driver.current_url

    # Close the browser window
    driver.quit()

    # Now 'current_url' contains the URL you want
    # print('\n\n\n',f"Authorization URL: {current_url}")

    # Parse the URL
    parsed_url = urlparse(current_url)

    # Extract the 'code' parameter from the query string
    code = parse_qs(parsed_url.query).get('code', None)
    # print('\n\n\n',code)


    recent_play_list = recently_played_tracks(get_token(code))



    print('Extracting names and info now')

    # # Now lets extract information

    song_names = []
    song_ids = []
    song_popularitys = []
    artist_names = []
    artist_ids = []
    release_date = []
    played_at = []
    timestamp = []
    duration = []
    album_name = []
    album_id = []


    for song in recent_play_list['items']:
        song_names.append(song['track']['name'])
        song_ids.append(song['track']['id'])
        song_popularitys.append(song['track']['popularity'])
        artist_names.append(song['track']['artists'][0]['name'])
        artist_ids.append(song['track']['artists'][0]['id'])
        release_date.append(song['track']['album']['release_date'])
        played_at.append(song['played_at'])
        timestamp.append(song['played_at'][0:10])
        duration.append(song['track']['duration_ms'])
        album_name.append(song['track']['album']['name'])
        album_id.append(song['track']['album']['id'])


    song_object = {
        'song_name': song_names,
        'song_id': song_ids,
        'song_popularity': song_popularitys,
        'artist_name': artist_names,
        'artist_id': artist_ids,
        'release_date': release_date,
        'played_at': played_at,
        'timestamp': timestamp,
        'duration': duration,
        'album_name': album_name,
        'album_id': album_id,
    }

    data = pd.DataFrame(song_object, 
        columns = ['song_name','song_id', 'song_popularity',
                'artist_name', 'artist_id', 'release_date', 'played_at',
                'timestamp', 'duration', 'album_name', 'album_id' ])

    # print ('\n\n\n', data.isnull())


    if check_data_validity(data):
        print('\n\n','Data is valid, proceed to load stage....')
        
    # Time to LOAD

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('nathan_played_tracks')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS nathan_played_tracks(
        song_name VARCHAR(200),
        song_id VARCHAR(200),
        song_popularity VARCHAR(200),
        artist_name VARCHAR(200),
        release_date VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        duration VARCHAR(200),
        album_name VARCHAR(200),
        album_id VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    cursor.execute(sql_query) 
    print('\n\n','Opened Database successfully')

    try:
        return data.to_sql('nathan_played_tracks', engine, index=False, if_exists='append')
    except:
        print('\n\n','Data already exist in the database')

    conn.close()    

    # print('DONE RUNNIG DAG...')
    












# code_verifier = generate_random_string(64)  # Replace with your actual code verifier
# hashed = sha256(code_verifier)
# code_challenge = base64encode(hashed)  # Replace with the actual code challenge calculated in Python
# # print(f"Code Challenge: {code_challenge}")


# # Store code_verifier (this would be more secure in a real application)
# # For this example, we're just storing it in a variable
# # You might want to use a more secure method, such as a secure database or session management
# os.environ['CODE_VERIFIER'] = code_verifier


# # Construct the authorization URL
# auth_url = "https://accounts.spotify.com/authorize"
# scope = 'user-read-private user-read-email user-read-recently-played'


# # Prepare parameters for the URL
# params = {
#     'response_type': 'code',
#     'client_id': CLIENT_ID,
#     'scope': scope,
#     'code_challenge_method': 'S256',
#     'code_challenge': code_challenge,
#     'redirect_uri': REDIRECT_URI,
# }


# # Append parameters to the URL
# auth_url_with_params = f"{auth_url}?{urlencode(params)}"

# # # Redirect to the authorization URL
# # webbrowser.open(auth_url_with_params)
# # Redirect to the authorization URL

# # print(f"Authorization URL: {auth_url_with_params}")



# # Once the user grants permission and is redirected back to the redirect_uri,
# # you can extract the 'code' parameter from the URL and use it to request the access token.

# # In a real application, you might want to handle the authorization callback in a web server,
# # but for this example, let's assume the user manually retrieves the code from the redirect URL.
# # You would get the 'code' parameter using a similar approach to the JavaScript example.

# # Now, you can use the following function to request the access token:

# # os.system(f"open {auth_url_with_params}")

# # Open the authorization URL in the default web browser
# # webbrowser.open(auth_url_with_params)









# # Set the path to your WebDriver executable
# # webdriver_path = '/Users/nate/Documents/Projects/chromedriver-mac-x64/chromedriver'

# # Create Chrome options
# chrome_options = Options()

# # Create a new instance of the Chrome driver
# driver = webdriver.Chrome(options=chrome_options) #executable_path=webdriver_path,

# # Navigate to your authorization URL
# driver.get(auth_url_with_params)

# # Wait for the user to perform the authorization process (you might need to customize this)
# input("Perform the authorization in the browser, then press Enter in this terminal.")

# # Get the current URL from the browser's address bar
# current_url = driver.current_url

# # Close the browser window
# driver.quit()

# # Now 'current_url' contains the URL you want
# # print('\n\n\n',f"Authorization URL: {current_url}")

# # Parse the URL
# parsed_url = urlparse(current_url)

# # Extract the 'code' parameter from the query string
# code = parse_qs(parsed_url.query).get('code', None)
# # print('\n\n\n',code)


# recent_play_list = recently_played_tracks(get_token(code))





# # # Now lets extract information

# song_names = []
# song_ids = []
# song_popularitys = []
# artist_names = []
# artist_ids = []
# release_date = []
# played_at = []
# timestamp = []
# duration = []
# album_name = []
# album_id = []


# for song in recent_play_list['items']:
#     song_names.append(song['track']['name'])
#     song_ids.append(song['track']['id'])
#     song_popularitys.append(song['track']['popularity'])
#     artist_names.append(song['track']['artists'][0]['name'])
#     artist_ids.append(song['track']['artists'][0]['id'])
#     release_date.append(song['track']['album']['release_date'])
#     played_at.append(song['played_at'])
#     timestamp.append(song['played_at'][0:10])
#     duration.append(song['track']['duration_ms'])
#     album_name.append(song['track']['album']['name'])
#     album_id.append(song['track']['album']['id'])


# song_object = {
#     'song_name': song_names,
#     'song_id': song_ids,
#     'song_popularity': song_popularitys,
#     'artist_name': artist_names,
#     'artist_id': artist_ids,
#     'release_date': release_date,
#     'played_at': played_at,
#     'timestamp': timestamp,
#     'duration': duration,
#     'album_name': album_name,
#     'album_id': album_id,
# }

# data = pd.DataFrame(song_object, 
#     columns = ['song_name','song_id', 'song_popularity',
#                'artist_name', 'artist_id', 'release_date', 'played_at',
#                'timestamp', 'duration', 'album_name', 'album_id' ])

# # print ('\n\n\n', data.isnull())


# if check_data_validity(data):
#     print('\n\n','Data is valid, proceed to load stage....')
    
# # Time to LOAD

# engine = sqlalchemy.create_engine(DATABASE_LOCATION)
# conn = sqlite3.connect('nathan_played_tracks')
# cursor = conn.cursor()

# sql_query = """
# CREATE TABLE IF NOT EXISTS nathan_played_tracks(
#     song_name VARCHAR(200),
#     song_id VARCHAR(200),
#     song_popularity VARCHAR(200),
#     artist_name VARCHAR(200),
#     release_date VARCHAR(200),
#     played_at VARCHAR(200),
#     timestamp VARCHAR(200),
#     duration VARCHAR(200),
#     album_name VARCHAR(200),
#     album_id VARCHAR(200),
#     CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
# )
# """

# cursor.execute(sql_query) 
# print('\n\n','Opened Database successfully')

# try:
#     data.to_sql('nathan_played_tracks', engine, index=False, if_exists='append')
# except:
#     print('\n\n','Data already exist in the database')

# conn.close()    






























    


    


    

    






    




# Run the asynchronous function from the top-level code
# if __name__ == "__main__":
#     asyncio.run(main())
    
    
    
    





# CLIENT_SECRET = os.getenv("CLIENT_SECRET")


# def get_token():
#     auth_string = f'{CLIENT_ID}:{CLIENT_SECRET}'
#     auth_bytes = auth_string.encode("utf-8")
#     auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    
#     url = 'https://accounts.spotify.com/api/token'
    
#     headers = {
#         "Authorization": f'Basic {auth_base64}',
#         'Content-Type': 'application/x-www-form-urlencoded',
#     }
    
#     data = {'grant_type': 'client_credentials'}
    
#     result = post(url, headers=headers, data=data)
#     json_result = json.loads(result.content)
#     token = json_result['access_token']
    
#     return token


# def get_auth_header(token):
#     return {'Authorization': f'Bearer {token}'}


# def search_for_artist(token, artistname):
#     url = 'https://api.spotify.com/v1/search'
#     headers = get_auth_header(token)
#     query = f'?q={artistname}&type=artist&limit=1'
#     query_url = url+query
#     result = get(query_url, headers=headers)
    
#     json_result = json.loads(result.content)['artists']['items']
    
#     if len(json_result)==0:
#         print('No artist with this name exist')
#         return None
    
#     return json_result[0]


# # result = search_for_artist(get_token(), 'ACDC')
# # print(result)


# def recently_played_tracks(token):
#     today = datetime.now()
#     ten_mins = today - timedelta(minutes=10)
#     ten_mins_unix_timestamp = int(ten_mins.timestamp()) * 1
#     url = 'https://api.spotify.com/v1/me/player/recently-played'
#     headers = get_auth_header(token)
#     query = f'?after={ten_mins_unix_timestamp}'
#     query_url = url+query
#     result = get(query_url, headers=headers)
#     print(result)
    
    
#     json_result = json.loads(result.content)
    
#     print(json_result.keys())
    
#     return json_result
    
    
    
    
    
    
    
# recent_play = recently_played_tracks(get_token())
# print(recent_play)
# token = get_token()
# print('\n\n\n\n', token)


# if __name__ == "__main__":
    
#     headers = {
#         "Authorization": "Bearer {token}".format(token=get_token())
#     }
    

# today = datetime.now()
# yesterday = today - timedelta(days=1)
# yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

# r = requests.get("https://api.spotify/v1/me/player/recently-played?after={time}".format(time = yesterday_unix_timestamp), headers = headers)


# data = r.json()


# print(data)


# AT 30January2024 I finally got the installatin of airflow correctly. WEBSERVER & SCHEDULER working perfectly.
# Configure my airflow to see /Users/nate/Documents/Projects/DATA_ENGINEERING_PROJECTS/ETL_Spotify_Data/dags as the location