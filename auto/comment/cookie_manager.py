import undetected_chromedriver as uc
import pickle
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os


import undetected_chromedriver as uc
import pickle
import time

# List of accounts with (email, password)
accounts = [
    ("dudhaneraj031@gmail.com", "rajdudhane036"),
    ("punia4517@gmail.com", "1133912444sahil"),
    ("qwsahil22@gmail.com","1133912444sahil"),
    ("isush9176@gmail.com","1133912444sahil"),
    ("kidoqowi@gmail.com","1133912444sahil"),
    ("8wjwuhzhs@gmail.com","1133912444sahil"),
    ("Popis8170@gmail.com","1133912444sahil"),
    ('Vermaparas402@gmail.com',"1133912444sahil"),
    ("p7502515@gmail.com","1133912444sahil"),
    ('parasverma400.0@gmail.com',"1133912444sahil"),
    ("Parasvera50@gmail.com","1133912444sahil"),
    ("Ukopois602@gmail.com","1133912444sahil"),
    ("ji9999385@gmail.com","1133912444sahil"),
    ("sahiljaathghg@gmail.com","1133912444sahil"),
    ("Sop145832@gmail.com","1133912444sahil"),
    ("Poiuyhjiwh@gmail.com","1133912444sahil"),
    ("sj3140678@gmail.com","1133912444sahil"),
    ("jyosiljaat@gmail.com","1133912444sahil") ,
    ("aakashpunia27@gmail.com","1133912444sahil"),
    ("kushaljaat230@gmail.com","1133912444sahil"),
    ("aakashpunia297@gmail.com","1133912444sahil"),
    ("aakashpunia60@gmail.com","1133912444sahil") ,
    ("puniaaakash213@gmail.com","1133912444sahil"),
    ("opram5726@gmail.com","1133912444sahil"),
    ("rsa350120@gmail.com","1133912444sahil"),
    ("s63692331@gmail.com","1133912444sahil"),
    ("r48373712@gmail.com","1133912444sahil"),
    ("aakashpunia077@gmail.com","1133912444sahil"),
    ("ytgdio@gmail.com","1133912444sahil"),
    ("pj2789264@gmail.com","1133912444sahil"),
    ("jaatshail64@gmail.com","1133912444sahil"),
    ("qrfwfjshs@gmail.co","1133912444sahil"),
    ("gggfgfd712@gmail.com","1133912444sahil"),
    ("shbshuwuw@gmail.com","1133912444sahil"),
    ("qtfsgbeb@gmail.com","1133912444sahil"),
    ("rretwt0@gmail.com","1133912444sahil"),
    ("djaat6826@gmail.com","1133912444sahil"),
    ("fcfffeed@gmail.com","1133912444sahil"),
    ("kushalgill29@gmail.com","1133912444sahil"),
    ("uwhwhwhg@gmail.com","1133912444sahil"),
    ("dddggfddss@gmail.com","1133912444sahil"),
    ("r83355710@gmail.com","1133912444sahil"),
    ("cmsahil33@gmail.com","1133912444sahil"),
    ("dark72223@gmail.com","1133912444sahil"),
    ("s81060402@gmail.com","1133912444sahil"),
    ("uahshhshs256@gmail.com","1133912444sahil"),
    ("s86425567@gmail.com","1133912444sahil"),
    ("omb7658@gmail.com","1133912444sahil"),
    ("gamepinta2@gmail.com","1133912444sahil"),
    ("s63692331@gmail.com","1133912444sahil"),
]
def create_driver(port):
    options = uc.ChromeOptions()
    options.add_argument(f"--remote-debugging-port={port}")  # Set the debugging port
    return uc.Chrome(options=options)

def save_cookies(driver, cookie_file):
    cookies = driver.get_cookies()
    with open(cookie_file, 'wb') as file:
        pickle.dump(cookies, file)
    print(f"Cookies saved to {cookie_file}")

def sign_in_youtube(driver, email, password):
    driver.get("https://accounts.google.com/ServiceLogin?service=youtube")
    time.sleep(2)  # Wait for the page to load

    # Enter email
    email_field = driver.find_element(By.ID, 'identifierId')
    email_field.send_keys(email)
    email_field.send_keys(Keys.RETURN)
    time.sleep(2)

    # Enter password
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'Passwd'))  # Corrected name to 'password'
    )
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)  # Wait for sign-in to complete

def main():
    start_port = 9222  # Starting port number
    for i, (email, password) in enumerate(accounts):
        port = start_port + i  # Unique port for each account
        cookie_file = f"cookies_account_{i + 1}_port_{port}.pkl"  # File name for each account
        
        # Check if the cookie file already exists
        if os.path.exists(cookie_file):
            print(f"Cookie file for account {email} already exists. Skipping sign-in.")
            continue  # Skip to the next account if the cookie file exists

        driver = create_driver(port)
        try:
            sign_in_youtube(driver, email, password)
            save_cookies(driver, cookie_file)  # Save cookies after sign-in
        except Exception as e:
            print(f"Error for account {email}: {e}")
        finally:
            driver.quit()  # Ensure the driver is closed

if __name__ == "__main__":
    main()


# import undetected_chromedriver as uc
# import pickle
# import time
# import pandas as pd  # Import pandas for handling Excel files
# import os  # Import os for file operations
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Function to read accounts from an Excel file
# def read_accounts_from_excel(file_path):
#     df = pd.read_excel(file_path)  # Read the Excel file into a DataFrame
#     df.columns = df.columns.str.strip()  # Clean up column names (remove leading/trailing whitespace)

#     # Check if the DataFrame has at least 2 columns
#     if df.shape[1] < 2:
#         raise ValueError("Excel file must contain at least two columns for email and password.")
    

#     # Use the first two columns for accounts
#     accounts = [(row[0], row[1]) for index, row in df.iterrows()]
#     return accounts

# def create_driver():
#     options = uc.ChromeOptions()
#     # options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'  # Update path if necessary
#     return uc.Chrome(options=options)

# def save_cookies(driver, email):
#     cookies = driver.get_cookies()
#     cookie_file = f'cookies_{email}.pkl'
    
#     # Ensure unique cookie file name
#     count = 1
#     while os.path.exists(cookie_file):
#         cookie_file = f'cookies_{email}_{count}.pkl'
#         count += 1

#     with open(cookie_file, 'wb') as file:
#         pickle.dump(cookies, file)
#     print(f"Cookies saved to {cookie_file}")

# def sign_in_youtube(driver, email, password):
#     driver.get("https://accounts.google.com/ServiceLogin?service=youtube")
#     time.sleep(2)  # Wait for the page to load

#     # Enter email
#     email_field = driver.find_element(By.ID, 'identifierId')
#     email_field.send_keys(email)
#     email_field.send_keys(Keys.RETURN)
#     time.sleep(2)

#     # Enter password
#     password_field = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.NAME, 'Passwd'))
#     )
#     password_field.send_keys(password)
#     password_field.send_keys(Keys.RETURN)
#     time.sleep(5)  # Wait for sign-in to complete

#     # Check if the login was successful
#     if "YouTube" in driver.title:  # Check if the title contains 'YouTube'
#         print(f"Successfully signed in with {email}")
#         save_cookies(driver, email)  # Save cookies only if signed in
#     else:
#         print(f"Failed to sign in with {email}")

# # Path to your Excel file
# excel_file_path = 'a1.xlsx'  # Update with your actual Excel file path

# # Read accounts from Excel
# try:
#     accounts = read_accounts_from_excel(excel_file_path)
# except ValueError as e:
#     print(e)
#     exit(1)  # Exit the program if the Excel file is not valid

# # Example of using the accounts to log in
# for email, password in accounts:
#     driver = create_driver()
#     try:
#         sign_in_youtube(driver, email, password)
#     except Exception as e:
#         print(f"Error logging in with {email}: {e}")
#     finally:
#         driver.quit()  # Close the driver
# import os

# def delete_cookies_in_folder(folder_path):
#     # Check if the provided folder path exists
#     if not os.path.exists(folder_path):
#         print(f"Folder not found: {folder_path}")
#         return

#     # Iterate through all files in the specified folder
#     for filename in os.listdir(folder_path):
#         # Check if the file ends with .pkl (cookie files)
#         if filename.endswith('.pkl'):
#             file_path = os.path.join(folder_path, filename)
#             try:
#                 os.remove(file_path)  # Remove the file
#                 print(f"Deleted cookie file: {file_path}")
#             except Exception as e:
#                 print(f"Error deleting file {file_path}: {e}")

# # Specify the folder containing the cookie files
# cookies_folder_path = r'C:\Users\Hp\Documents\auto_youtube\Youtube-auto-comments-using-multiple-accounts-main\auto\comment'  # Update this path

# # Call the function to delete cookies
# delete_cookies_in_folder(cookies_folder_path)
