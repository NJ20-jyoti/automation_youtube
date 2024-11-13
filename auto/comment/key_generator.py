# import os
# import platform
# import uuid
# import hashlib
# import sqlite3
# from datetime import datetime, timedelta

# def get_hardware_id():
#     # Combine several hardware identifiers
#     identifiers = []

#     # Get the MAC address (works on most platforms)
#     mac_address = hex(uuid.getnode())
#     identifiers.append(f"mac:{mac_address}")

#     # Get the machine name
#     machine_name = platform.node()
#     identifiers.append(f"machine_name:{machine_name}")

#     # Get the system platform
#     system_platform = platform.system()
#     identifiers.append(f"platform:{system_platform}")

#     # Get the system architecture
#     architecture = platform.architecture()[0]
#     identifiers.append(f"architecture:{architecture}")

#     # Get the processor name
#     processor = platform.processor()
#     identifiers.append(f"processor:{processor}")

#     # Combine all identifiers into a single string
#     hardware_id = ''.join(identifiers)
#     return hardware_id

# def generate_key(hardware_id):
#     # Generate a key by hashing the hardware ID
#     key = hashlib.sha256(hardware_id.encode()).hexdigest()  # Hashing for security
#     return key

# def create_database():
#     # Connect to SQLite database (it will create the database if it doesn't exist)
#     conn = sqlite3.connect('keys.db')
#     cursor = conn.cursor()

#     # Create table for keys if it doesn't exist
#     cursor.execute(''' 
#         CREATE TABLE IF NOT EXISTS user_keys (
#             user_id TEXT PRIMARY KEY,
#             key TEXT NOT NULL,
#             expiration_date TEXT NOT NULL,
#             hardware_id TEXT NOT NULL
#         )
#     ''')
#     conn.commit()
#     return conn

# def save_key(conn, user_id, key, expiration_date, hardware_id):
#     # Save the key and hardware ID to the database
#     cursor = conn.cursor()
#     try:
#         cursor.execute('INSERT INTO user_keys (user_id, key, expiration_date, hardware_id) VALUES (?, ?, ?, ?)', 
#                        (user_id, key, expiration_date, hardware_id))
#         conn.commit()
#     except sqlite3.IntegrityError:
#         print("User ID already exists. Please use a different user ID.")

# def load_keys(conn):
#     # Load existing keys from the database
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM user_keys')
#     return {row[0]: (row[1], row[2], row[3]) for row in cursor.fetchall()}  # Return key, expiration date, and hardware ID

# def check_key(conn, user_id, key):
#     # Check if the provided key matches the stored key and is not expired
#     keys = load_keys(conn)
#     stored_key, expiration_date, hardware_id = keys.get(user_id, (None, None, None))
#     if stored_key is None:
#         return None, None  # Key not found

#     # Check if the key is valid and has not expired
#     if stored_key == key:
#         if datetime.now() < datetime.fromisoformat(expiration_date):
#             return True, hardware_id  # Key is valid
#     return False, hardware_id  # Key is invalid or expired

# def main():
#     user_id = input("Enter your user ID: ")

#     # Create or connect to the database
#     conn = create_database()

#     # Check if the user ID already has a valid key
#     keys = load_keys(conn)
#     if user_id in keys:
#         stored_key, expiration_date, hardware_id = keys[user_id]
#         if datetime.now() < datetime.fromisoformat(expiration_date):
#             print("You already have a valid key.")
#             print(f"Your key: {stored_key}")
#             print(f"Expiration date: {expiration_date}")
#             print(f"Hardware ID: {hardware_id}")
#             conn.close()
#             return

#     # Get the hardware ID and generate the key
#     hardware_id = get_hardware_id()
#     generated_key = generate_key(hardware_id)

#     print(f"Generated Key: {generated_key}")

#     # Set the expiration date (3 days from now)
#     expiration_date = (datetime.now() + timedelta(days=3)).isoformat()

#     # Ask if the user wants to save this key
#     save = input("Do you want to save this key? (yes/no): ").strip().lower()

#     if save == 'yes':
#         save_key(conn, user_id, generated_key, expiration_date, hardware_id)
#         print("Key saved successfully.")

#     # Checking the key (for demonstration)
#     check_user = input("Enter your user ID to check the key: ")
#     check_key_input = input("Enter the key to validate: ")

#     is_valid, hw_id = check_key(conn, check_user, check_key_input)

#     if is_valid:
#         print("Key is valid.")
#     elif hw_id is not None:
#         print("Key is invalid or has expired.")
#         print(f"Your hardware ID: {hw_id}")
#     else:
#         print("User ID not found.")

#     # Close the database connection
#     conn.close()

# if __name__ == "__main__":
#     main()
