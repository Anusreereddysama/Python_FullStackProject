import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)


# USERS
class DatabaseManager:
    # -------- USERS --------
    def add_user(self, name, phone, password, is_admin: bool = False):
        return supabase.table("users").insert({
            "name": name,
            "phone": phone,
            "password": password,
            "is_admin": is_admin
        }).execute()

    def get_user_by_phone(self, phone):
        return supabase.table("users").select("*").eq("phone", phone).execute()

    def get_all(self):
        return supabase.table("users").select("*").execute()

    def update_user(self, user_id, update_data):
        return supabase.table("users").update(update_data).eq("id", user_id).execute()

    def delete_user(self, user_id):
        return supabase.table("users").delete().eq("id", user_id).execute()

    # -------- CROPS --------
    def add_crop(self, user_id, crop_name, area, sow_date, fertilizer, expected_yield):
        return supabase.table("crops").insert({
            "user_id": user_id,
            "crop_name": crop_name,
            "area": area,
            "sow_date": sow_date,
            "fertilizer": fertilizer,
            "expected_yield": expected_yield
        }).execute()

    def get_crops_by_user(self, user_id):
        return supabase.table("crops").select("*").eq("user_id", user_id).execute()

    def update_crop(self, crop_id, update_data):
        return supabase.table("crops").update(update_data).eq("id", crop_id).execute()

    def delete_crop(self, crop_id):
        return supabase.table("crops").delete().eq("id", crop_id).execute()

    # -------- MARKET PRICES --------
    def add_market_price(self, crop_name, date, price_per_kg, buyer_id):
        return supabase.table("market_prices").insert({
            "crop_name": crop_name,
            "date": date,
            "price_per_kg": price_per_kg,
            "buyer_id": buyer_id
        }).execute()

    def get_market_prices(self, crop_name: str = None):
        query = supabase.table("market_prices").select("*")
        if crop_name:
            query = query.eq("crop_name", crop_name)
        return query.execute()

    def update_market_price(self, price_id, update_data):
        return supabase.table("market_prices").update(update_data).eq("id", price_id).execute()

    def delete_market_price(self, price_id):
        return supabase.table("market_prices").delete().eq("id", price_id).execute()

    # -------- NEGOTIATIONS --------
    def add_negotiation(self, farmer_id, buyer_id, crop_name, quantity_kg, proposed_price, notes):
        return supabase.table("negotiations").insert({
            "farmer_id": farmer_id,
            "buyer_id": buyer_id,
            "crop_name": crop_name,
            "quantity_kg": quantity_kg,
            "proposed_price": proposed_price,
            "notes": notes,
            "status": "pending"
        }).execute()

    def get_negotiations_for_user(self, user_id, role):
        table = supabase.table("negotiations").select("*")
        if role == "buyer":
            table = table.eq("buyer_id", user_id)
        else:
            table = table.eq("farmer_id", user_id)
        return table.execute()

    def update_negotiation(self, negotiation_id, update_data):
        return supabase.table("negotiations").update(update_data).eq("id", negotiation_id).execute()

    # -------- WEATHER --------
    def add_weather(self, date, temperature, rainfall, humidity):
        return supabase.table("weather").insert({
            "date": date,
            "temperature": temperature,
            "rainfall": rainfall,
            "humidity": humidity
        }).execute()

    def get_weather(self, date: str = None):
        query = supabase.table("weather").select("*")
        if date:
            query = query.eq("date", date)
        return query.execute()

    def update_weather(self, weather_id, update_data: dict):
        return supabase.table("weather").update(update_data).eq("id", weather_id).execute()

    def delete_weather(self, weather_id):
        return supabase.table("weather").delete().eq("id", weather_id).execute()
