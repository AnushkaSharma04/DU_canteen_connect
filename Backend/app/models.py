import mysql.connector
from app.logging_config import setup_logging
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
import uuid
from flask import jsonify
from flask_bcrypt import Bcrypt
import os
import re
import logging
import base64
import random

bcrypt = Bcrypt()

def get_db_connection():

    try:
        db_host = os.getenv('DB_HOST', 'localhost')
        db_user = os.getenv('DB_USER', 'root')
        db_password = os.getenv('DB_PASSWORD', '')
        db_name = os.getenv('DB_NAME', 'du_canteen_hub')

        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        logging.info("Database connection established.")
        return connection
    except mysql.connector.Error as err :
        print(f"Error: {err}")
        logging.error("Error connecting to the database: %s", err)
        return None
    
def check_user_exists(phone_number, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE phone_number=%s AND role=%s"
    cursor.execute(query, (phone_number, role))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

def add_user(user_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO users (name, phone_number, password_hash, role, email)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        user_data['name'],
        user_data['phone_number'],
        user_data['password'],
        user_data['role'],
        user_data['email']
    ))
    conn.commit()

    # Fetch the auto-generated user_id
    user_id = cursor.lastrowid

    cursor.close()
    conn.close()
    return user_id


def add_canteen_profile(profile_data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO canteens (
                owner_id, name, location, description, contact_no,
                days_open, opening_time, closing_time, peak_hr_start_time, peak_hr_end_time
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            profile_data["owner_id"],
            
            profile_data["canteen_name"],
            profile_data["location"],
            profile_data["description"],
            profile_data["contact_number"],
            profile_data["days_open"],
            profile_data["opening_time"],
            profile_data["closing_time"],
            profile_data["peak_hr_start_time"],
            profile_data["peak_hr_end_time"]
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Canteen profile created successfully"}
    except Exception as e:
        logging.error(f"Error adding canteen profile: {str(e)}")
        return {"message": "Failed to create canteen profile"}, 500

    

def get_user_by_phone(phone_number):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT user_id, name, phone_number, password_hash, role, email FROM users WHERE phone_number = %s"
        cursor.execute(query, (phone_number,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return {
                "user_id": user[0],
                "name": user[1],
                "phone_number": user[2],
                "password": user[3],
                "role": user[4],
                "email": user[5]
            }
        return None

    except Exception as e:
        logging.error(f"Error fetching user: {str(e)}")
        return None
    
def get_all_canteens_from_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  

        query = """
            SELECT 
                canteen_id,
                name,
                location,
                days_open,
                opening_time,
                closing_time,
                overall_rating
            FROM canteens
        """
        cursor.execute(query)
        canteens = cursor.fetchall()

        cursor.close()
        conn.close()

        return canteens

    except Exception as e:
        logging.error(f"Error fetching canteens from DB: {str(e)}")
        return None

def get_canteen_info_from_db(canteen_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  

        query = """
            SELECT 
                canteen_id,
                name,
                location,
                description,
                contact_no,
                days_open,
                opening_time,
                closing_time,
                peak_hr_start_time,
                peak_hr_end_time,
                overall_rating
            FROM canteens
            WHERE canteen_id = %s
        """
        cursor.execute(query, (canteen_id,))
        canteen_info = cursor.fetchone()

        cursor.close()
        conn.close()

        return canteen_info

    except Exception as e:
        logging.error(f"Error fetching canteen info from DB: {str(e)}")
        return None

def get_canteen_reviews_and_ratings_from_db(canteen_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

    
        query_canteen = """
            SELECT 
                canteen_id,
                name,
                overall_rating,
                overall_food,
                overall_hygiene,
                overall_staff,
                overall_facilities
            FROM canteens
            WHERE canteen_id = %s
        """
        cursor.execute(query_canteen, (canteen_id,))
        canteen = cursor.fetchone()

        if not canteen:
            cursor.close()
            conn.close()
            return None  

        query_reviews = """
            SELECT 
                review_id,
                overall_rating,
                review_text,
                image_1,
                image_2,
                image_3,
                created_at
            FROM canteen_reviews
            WHERE canteen_id = %s
            ORDER BY created_at DESC
            LIMIT 5
        """
        cursor.execute(query_reviews, (canteen_id,))
        reviews = cursor.fetchall()

        cursor.close()
        conn.close()

        
        import base64
        for review in reviews:
            if review["image"]:
                review["image"] = base64.b64encode(review["image"]).decode("utf-8")

        return {
            "canteen_id": canteen["canteen_id"],
            "canteen_name": canteen["name"],
            "overall_rating": canteen["overall_rating"],
            "overall_food": canteen["overall_food"],
            "overall_hygiene": canteen["overall_hygiene"],
            "overall_staff": canteen["overall_staff"],
            "overall_facilities": canteen["overall_facilities"],
            "top_reviews": reviews
        }

    except Exception as e:
        logging.error(f"Error fetching reviews and ratings for canteen_id {canteen_id}: {str(e)}")
        return None
    
def get_canteen_menu_from_db(canteen_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Step 1: Fetch the menu row for this canteen
        query_menu = """
            SELECT *
            FROM menu
            WHERE canteen_id = %s
        """
        cursor.execute(query_menu, (canteen_id,))
        menu = cursor.fetchone()

        if not menu:
            cursor.close()
            conn.close()
            return {"message": "Menu not found for this canteen"}

        # Step 2: If menu_file exists, return it directly
        if menu["menu_file"]:
            encoded_file = base64.b64encode(menu["menu_file"]).decode("utf-8")
            cursor.close()
            conn.close()
            return {
                "canteen_id": canteen_id,
                "menu_type": "file",
                "menu_file": encoded_file
            }

        menu_id = menu["menu_id"]

        # Step 3: If menu_file is null, handle based on day_wise
        if menu["day_wise"].lower() == "yes":
            day_columns = [
                ("Monday", "monday_price"),
                ("Tuesday", "tuesday_price"),
                ("Wednesday", "wednesday_price"),
                ("Thursday", "thursday_price"),
                ("Friday", "friday_price"),
                ("Saturday", "saturday_price"),
                ("Sunday", "sunday_price")
            ]
            day_wise_menu = {}

            for day, price_col in day_columns:
                food_ids_text = menu.get(day)
                prices_text = menu.get(price_col)

                if not food_ids_text:
                    continue

                # Convert comma-separated food_ids into list
                food_ids = [fid.strip() for fid in food_ids_text.split(",") if fid.strip().isdigit()]

                if not food_ids:
                    continue

                # Fetch food item names
                format_strings = ','.join(['%s'] * len(food_ids))
                query_foods = f"SELECT name FROM food_items WHERE food_id IN ({format_strings}) AND menu_id = %s"
                cursor.execute(query_foods, (*food_ids, menu_id))
                food_names = [row["name"] for row in cursor.fetchall()]

                # Combine food names with price info
                day_wise_menu[day] = {
                    "items": ", ".join(food_names),
                    "price": prices_text
                }

            cursor.close()
            conn.close()

            return {
                "canteen_id": canteen_id,
                "menu_type": "day_wise",
                "menu": day_wise_menu
            }

        else:
            # Step 4: If day_wise = no, return full food list for that menu
            query_food_items = """
                SELECT name, price
                FROM food_items
                WHERE menu_id = %s
            """
            cursor.execute(query_food_items, (menu_id,))
            items = cursor.fetchall()

            cursor.close()
            conn.close()

            return {
                "canteen_id": canteen_id,
                "menu_type": "standard",
                "menu": items
            }

    except Exception as e:
        logging.error(f"Error fetching canteen menu for canteen_id {canteen_id}: {str(e)}")
        return None