# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException


# # List of accounts (username, password)
# accounts = [
#     ('your_email1@gmail.com', 'your_password1'),
#     ('your_email2@gmail.com', 'your_password2'),
#     # Add more accounts as needed
# ]

# # Video URL where you want to comment
# video_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

# # Comment to post
# comment_text = "Your automated comment here!"

# def login_and_comment(email, password):
#     # Set up the driver
#     driver = uc.Chrome()

#     try:
#         # Open YouTube and log in
#         # driver.get("https://www.youtube.com")
#         time.sleep(2)

#         # Click on the Sign In button
#         driver.find_element(By.XPATH, '//*[text()="Sign in"]').click()
#         time.sleep(2)

#         # Enter email
#         email_field = driver.find_element(By.XPATH, '//*[@type="email"]')
#         email_field.send_keys(email)
#         email_field.send_keys(Keys.RETURN)
#         time.sleep(2)

#         # Enter password
#         password_field = driver.find_element(By.XPATH, '//*[@type="password"]')
#         password_field.send_keys(password)
#         password_field.send_keys(Keys.RETURN)
#         time.sleep(5)

#         # Navigate to the video
#         driver.get(video_url)
#         time.sleep(5)

#         # Scroll to the comments section
#         driver.execute_script("window.scrollTo(0, 500);")
#         time.sleep(2)

#         # Locate the comment box and post the comment
#         comment_box = driver.find_element(By.XPATH, '//*[@id="simple-box"]/yt-formatted-string')
#         comment_box.click()
#         time.sleep(1)
#         comment_box.send_keys(comment_text)
#         comment_box.send_keys(Keys.RETURN)

#         print(f"Comment posted by {email}!")

#     except Exception as e:
#         print(f"Error for {email}: {e}")
#     finally:
#         driver.quit()

# # Loop through accounts and post comments
# for email, password in accounts:
#     login_and_comment(email, password)
#     time.sleep(5)  # Wait a bit between accounts to avoid getting flagged

