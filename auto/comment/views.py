import time
import random
import pandas as pd
import openpyxl
import json
import undetected_chromedriver as uc
from django.shortcuts import render
from django.http import HttpResponse
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from .models import Cookie  # Import the Cookie model
from django.shortcuts import render, redirect
# import hashlib
# from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from .models import UserKey
import json

# def generate_key(hardware_id):
#     # Generate a key by hashing the hardware ID
#     return hashlib.sha256(hardware_id.encode()).hexdigest()

# def key_generator_view(request):
#     return render(request, 'key.html')  # Render the key.html page

# @csrf_exempt  # Disable CSRF for simplicity; use with caution in production!
# def generate_key_endpoint(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         hardware_id = data.get('hardwareId')

#         if not hardware_id:
#             return JsonResponse({'error': 'Hardware ID is required'}, status=400)

#         # Generate the software key
#         generated_key = generate_key(hardware_id)

#         # Set the expiration date (3 days from now)
#         expiration_date = datetime.now() + timedelta(days=3)

#         # Save the key in the database
#         user_key, created = UserKey.objects.update_or_create(
#             hardware_id=hardware_id,
#             defaults={'key': generated_key, 'expiration_date': expiration_date}
#         )

#         # Instead of returning an HTML page here, return the key and expiration date in JSON
#         return JsonResponse({
#             'key': generated_key,
#             'expiration_date': expiration_date.isoformat()
#         })

#     return JsonResponse({'error': 'Invalid request'}, status=400)

# Function to read accounts from the uploaded Excel file
def read_accounts_from_excel(file_path):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()  # Strip whitespace from column headers

    if df.shape[1] < 2:
        raise ValueError("Excel file must contain at least two columns for email and password.")

    accounts = []
    for index, row in df.iterrows():
        email = row.iloc[0]
        password = row.iloc[1]

        if pd.isnull(email) or pd.isnull(password):
            print(f"Warning: Missing email or password in row {index + 1}. Skipping this row.")
            continue  # Skip rows with missing values

        accounts.append((email, password))

    print(f"Total accounts read: {len(accounts)}")
    
    return accounts

# Function to create a Chrome driver
def create_driver():
    options = uc.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")
    return uc.Chrome(options=options)

# Function to load comments from the uploaded Excel file
def load_comments_from_excel(file_path):
    comments = []
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        for row in sheet.iter_rows(values_only=True):
            if row[0]:  # Ensure the first cell is not empty
                comments.append(row[0])

        if not comments:
            print("Warning: No comments found in the Excel file.")
        else:
            print(f"Comments loaded: {comments}")

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while loading comments: {e}")

    return comments

# Function to save cookies to the database
# Function to save cookies to the database
def save_cookies_to_db(cookies, account_email):
    try:
        # Ensure cookies are JSON serializable
        cookie_data = json.dumps(cookies)

        # Check if cookies already exist for the email
        cookie_instance = Cookie.objects.filter(email=account_email).first()
        
        if cookie_instance:
            # Update existing cookie instance
            cookie_instance.cookies = cookie_data
            cookie_instance.save()
            print(f"Updated cookies for {account_email} in the database.")
        else:
            # Create a new cookie instance
            cookie_instance = Cookie.objects.create(
                email=account_email,
                cookies=cookie_data
            )
            print(f"Cookies saved for {account_email} in the database.")
    except Exception as e:
        print(f"Error saving cookies for {account_email}: {e}")

# Function to load cookies from the database
def load_cookies_from_db(driver, email):
    try:
        cookie_instance = Cookie.objects.get(email=email)
        cookies = json.loads(cookie_instance.cookies)
        for cookie in cookies:
            if 'domain' in cookie and 'youtube.com' in cookie['domain']:
                driver.add_cookie(cookie)
        driver.refresh()  # Refresh to apply cookies
        print(f"Cookies loaded for {email} from the database.")
        return True  # Indicate that cookies were loaded
    except Cookie.DoesNotExist:
        print(f"No cookies found for {email} in the database.")
    except Exception as e:
        print(f"Error loading cookies for {email}: {e}")
    
    return False  # Indicate that no cookies were loaded

# Function to login to YouTube and save cookies
def login_and_save_cookies(account):
    email, password = account
    driver = create_driver()
    
    try:
        driver.get("https://accounts.google.com/ServiceLogin?service=youtube")
        time.sleep(2)

        email_field = driver.find_element(By.ID, 'identifierId')
        email_field.send_keys(email)
        email_field.send_keys(Keys.RETURN)
        time.sleep(2)

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'Passwd'))
        )
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for sign-in to complete

        if "youtube.com" in driver.current_url:  # Confirm we are logged in
            save_cookies_to_db(driver.get_cookies(), email)
        else:
            print(f"Login failed for {email}: Redirected to {driver.current_url}")
    except Exception as e:
        print(f"Login failed for {email}: {e}")
    finally:
        driver.quit()  # Ensure the driver is closed after use

# Function to post a random comment on a given video
def post_comment(driver, url, comments):
    driver.get(url)
    time.sleep(7)  # Wait for the video page to load

    try:
        play_button = driver.find_element(By.CSS_SELECTOR, '#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > button')
        play_button.click()
        time.sleep(3)
    except Exception as e:
        print("Could not play the video: ", e)

    driver.execute_script("window.scrollTo(0, 600);")
    time.sleep(1)

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-comments ytd-comment-simplebox-renderer")))
        driver.find_element(By.CSS_SELECTOR, "ytd-comments ytd-comment-simplebox-renderer div#placeholder-area").click()

        comment = random.choice(comments)
        driver.find_element(By.CSS_SELECTOR, "#contenteditable-root").send_keys(comment)
        time.sleep(2)
        driver.find_element(By.ID, "submit-button").click()
        print(f"Posted comment: {comment}")
        time.sleep(4)
    except Exception as e:
        print(f"An error occurred while posting comment: {e}")

    time.sleep(3)  # Wait before moving to the next account

# Function to run the automation for a single account

# def run_for_account(cookie_file, video_url, comments):
#     driver = create_driver()
#     try:
#         load_cookies(driver, cookie_file)
#         post_random_comments(driver, video_url, comments)
#     finally:
#         driver.quit()

# Main function to handle YouTube automation
def youtube_automation(request):
    if request.method == "POST":
        video_link = request.POST.get('videoLink')
        num_comments = int(request.POST.get('numComments', 1))  # Number of comments per account
        comments_file_path = request.FILES['commentsFile']  # Load comments from uploaded file

        # Save the uploaded comments file
        with open('uploaded_comments.xlsx', 'wb+') as f:
            for chunk in comments_file_path.chunks():
                f.write(chunk)

        # Read comments from the uploaded Excel file
        comments = load_comments_from_excel('uploaded_comments.xlsx')

        # List of account cookie files
        accounts = [
            "cookies_account_1.pkl",
            "cookies_account_2.pkl",
            "cookies_account_4.pkl",
            "cookies_account_5.pkl",
            "cookies_account_6.pkl",
            "cookies_account_7.pkl",
            "cookies_account_9.pkl",
            "cookies_account_10.pkl",
            "cookies_account_11.pkl",
            "cookies_account_12.pkl",
            "cookies_account_13.pkl", 
            "cookies_account_15.pkl",
            "cookies_account_16.pkl",
            "cookies_account_17.pkl",
            "cookies_account_21.pkl",
            "cookies_account_22.pkl",
            "cookies_account_23.pkl",
            "cookies_account_24.pkl",
            "cookies_account_25.pkl",
            "cookies_account_26.pkl",
            "cookies_account_27.pkl",
            "cookies_account_29.pkl",
            "cookies_account_30.pkl",
            "cookies_account_31.pkl",
            "cookies_account_34.pkl",
            "cookies_account_35.pkl",
            "cookies_account_36.pkl",
            "cookies_account_37.pkl",
            "cookies_account_38.pkl",
            "cookies_account_39.pkl",
            "cookies_account_40.pkl",
            "cookies_account_41.pkl",
            "cookies_account_42.pkl",
            "cookies_account_43.pkl",
            "cookies_account_45.pkl",
            "cookies_account_46.pkl",
            "cookies_account_47.pkl",
            "cookies_account_48.pkl",
            "cookies_account_49.pkl",
            "cookies_account_53.pkl"
        ]

        # Use ThreadPoolExecutor to manage multiple browsers for commenting
        with ThreadPoolExecutor(max_workers=1) as executor:
            for cookie_file in accounts:
                executor.submit( cookie_file, video_link, comments,accounts, num_comments)
                # run_for_account,
        return HttpResponse("Automation process initiated!")
    else:
        return render(request, 'index.html')
