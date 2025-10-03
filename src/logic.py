from src.db import DatabaseManager


# ===================== USERS =====================
class UserOperations:
    """Bridge between frontend/FastAPI and Users table"""

    def __init__(self):
        self.db = DatabaseManager()

    def add_user(self, name, phone, password, is_admin: bool = False):
        if not name or not phone or not password:
            return {"success": False, "message": "name, phone and password are required"}

        try:
            result = self.db.add_user(name, phone, password, is_admin)
        except Exception as exc:
            return {"success": False, "message": str(exc)}

        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "message": "User added successfully", "data": getattr(result, "data", None)}

    def get_all(self):
        result = self.db.get_all()
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "data": getattr(result, "data", None)}

    def update_user(self, user_id, data: dict):
        result = self.db.update_user(user_id, data)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "message": "User updated successfully", "data": getattr(result, "data", None)}

    def delete_user(self, user_id):
        result = self.db.delete_user(user_id)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "message": "User deleted successfully"}


# ===================== CROPS =====================
class CropsOperations:
    """Bridge between frontend/FastAPI and Crops table"""

    def __init__(self):
        self.db = DatabaseManager()

    def add_crop(self, user_id, crop_name, area=None, sow_date=None, fertilizer=None, expected_yield=None):
        if not user_id or not crop_name:
            return {"success": False, "message": "user_id and crop_name are required"}
        
        result = self.db.add_crop(user_id, crop_name, area, sow_date, fertilizer, expected_yield)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "message": "Crop added successfully", "data": getattr(result, "data", None)}

    def get_crops_by_user(self, user_id):
        result = self.db.get_crops_by_user(user_id)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "data": getattr(result, "data", None)}

    def update_crop(self, crop_id, data: dict):
        result = self.db.update_crop(crop_id, data)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "message": "Crop updated successfully", "data": getattr(result, "data", None)}

    def delete_crop(self, crop_id):
        result = self.db.delete_crop(crop_id)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "message": "Crop deleted successfully"}


# ===================== MARKET PRICES =====================
class MarketOperations:
    """Bridge between frontend/FastAPI and Market Prices table"""

    def __init__(self):
        self.db = DatabaseManager()

    def add_price(self, crop_name, date, price_per_kg, buyer_id):
        if not crop_name or not date or price_per_kg is None or not buyer_id:
            return {"success": False, "message": "All fields are required"}
        
        result = self.db.add_market_price(crop_name, date, price_per_kg, buyer_id)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "message": "Market price added successfully", "data": getattr(result, "data", None)}

    def get_prices(self, crop_name=None):
        result = self.db.get_market_prices(crop_name)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "data": getattr(result, "data", None)}

    def update_price(self, price_id, data: dict):
        result = self.db.update_market_price(price_id, data)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "message": "Market price updated successfully", "data": getattr(result, "data", None)}

    def delete_price(self, price_id):
        result = self.db.delete_market_price(price_id)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "message": "Market price deleted successfully"}


# ===================== WEATHER =====================
class WeatherOperations:
    """Bridge between frontend/FastAPI and Weather table"""

    def __init__(self):
        self.db = DatabaseManager()

    def add_weather(self, date, temperature=None, rainfall=None, humidity=None):
        if not date:
            return {"success": False, "message": "Date is required"}
        
        result = self.db.add_weather(date, temperature, rainfall, humidity)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "message": "Weather data added successfully", "data": getattr(result, "data", None)}

    def get_weather(self, date=None):
        result = self.db.get_weather(date)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "data": getattr(result, "data", None)}

    def update_weather(self, weather_id, data: dict):
        result = self.db.update_weather(weather_id, data)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "message": "Weather updated successfully", "data": getattr(result, "data", None)}

    def delete_weather(self, weather_id):
        result = self.db.delete_weather(weather_id)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "message": "Weather deleted successfully"}


# ===================== NEGOTIATIONS =====================
class NegotiationOperations:
    """Bridge between frontend/FastAPI and Negotiations table"""

    def __init__(self):
        self.db = DatabaseManager()

    def add_negotiation(self, farmer_id, buyer_id, crop_name, quantity_kg, proposed_price, notes=None):
        if not farmer_id or not buyer_id or not crop_name or quantity_kg is None or proposed_price is None:
            return {"success": False, "message": "All fields are required"}
        result = self.db.add_negotiation(farmer_id, buyer_id, crop_name, quantity_kg, proposed_price, notes)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "message": "Negotiation created", "data": getattr(result, "data", None)}

    def get_negotiations_for_user(self, user_id, role):
        result = self.db.get_negotiations_for_user(user_id, role)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "data": getattr(result, "data", None)}

    def update_negotiation(self, negotiation_id, data: dict):
        result = self.db.update_negotiation(negotiation_id, data)
        if getattr(result, "error", None):
            return {"success": False, "message": str(result.error)}
        return {"success": True, "message": "Negotiation updated", "data": getattr(result, "data", None)}
