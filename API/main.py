from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os

# Add src folder to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import UserOperations, CropsOperations, MarketOperations, WeatherOperations, NegotiationOperations

# ======================
# ===== APP SETUP ======
# ======================
app = FastAPI(title="Smart Farming Portal API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# ===== OPERATIONS =====
# ======================
user_op = UserOperations()
crop_op = CropsOperations()
market_op = MarketOperations()
weather_op = WeatherOperations()
negotiation_op = NegotiationOperations()

# ======================
# ===== SCHEMAS ========
# ======================
class UserCreate(BaseModel):
    name: str
    phone: str
    password: str
    is_admin: bool = False

class UserUpdate(BaseModel):
    data: dict

class CropCreate(BaseModel):
    user_id: int
    crop_name: str
    area: float = None
    sow_date: str = None
    fertilizer: str = None
    expected_yield: float = None

class CropUpdate(BaseModel):
    data: dict

class MarketPriceCreate(BaseModel):
    crop_name: str
    date: str
    price_per_kg: float
    buyer_id: int

class MarketPriceUpdate(BaseModel):
    data: dict

class WeatherCreate(BaseModel):
    date: str
    temperature: str = None
    rainfall: str = None
    humidity: str = None

class WeatherUpdate(BaseModel):
    data: dict

class NegotiationCreate(BaseModel):
    farmer_id: int
    buyer_id: int
    crop_name: str
    quantity_kg: float
    proposed_price: float
    notes: str | None = None

class NegotiationUpdate(BaseModel):
    data: dict

# ======================
# ===== HOME ===========
# ======================
@app.get("/")
def home():
    return {"message": "Smart Farming Portal API is running!"}

# ======================
# ===== USERS ==========
# ======================
@app.get("/users")
def get_all_users():
    result = user_op.get_all()
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.post("/users")
def add_user(user: UserCreate):
    result = user_op.add_user(user.name, user.phone, user.password, user.is_admin)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.put("/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdate):
    result = user_op.update_user(user_id, user_update.data)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    result = user_op.delete_user(user_id)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

# ======================
# ===== CROPS ==========
# ======================
@app.get("/crops/{user_id}")
def get_user_crops(user_id: int):
    result = crop_op.get_crops_by_user(user_id)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.post("/crops")
def add_crop(crop: CropCreate):
    result = crop_op.add_crop(crop.user_id, crop.crop_name, crop.area, crop.sow_date, crop.fertilizer, crop.expected_yield)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.put("/crops/{crop_id}")
def update_crop(crop_id: int, crop_update: CropUpdate):
    result = crop_op.update_crop(crop_id, crop_update.data)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.delete("/crops/{crop_id}")
def delete_crop(crop_id: int):
    result = crop_op.delete_crop(crop_id)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

# ======================
# ===== MARKET PRICES ===
# ======================
@app.get("/market_prices")
def get_market_prices(crop_name: str = None):
    result = market_op.get_prices(crop_name)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.post("/market_prices")
def add_market_price(price: MarketPriceCreate):
    result = market_op.add_price(price.crop_name, price.date, price.price_per_kg, price.buyer_id)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.put("/market_prices/{price_id}")
def update_market_price(price_id: int, price_update: MarketPriceUpdate):
    result = market_op.update_price(price_id, price_update.data)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.delete("/market_prices/{price_id}")
def delete_market_price(price_id: int):
    result = market_op.delete_price(price_id)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

# ======================
# ===== WEATHER ========
# ======================
@app.get("/weather")
def get_weather(date: str = None):
    result = weather_op.get_weather(date)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.post("/weather")
def add_weather(weather: WeatherCreate):
    result = weather_op.add_weather(weather.date, weather.temperature, weather.rainfall, weather.humidity)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.put("/weather/{weather_id}")
def update_weather(weather_id: int, weather_update: WeatherUpdate):
    result = weather_op.update_weather(weather_id, weather_update.data)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.delete("/weather/{weather_id}")
def delete_weather(weather_id: int):
    result = weather_op.delete_weather(weather_id)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

# ======================
# ===== NEGOTIATIONS ===
# ======================
@app.post("/negotiations")
def create_negotiation(neg: NegotiationCreate):
    result = negotiation_op.add_negotiation(neg.farmer_id, neg.buyer_id, neg.crop_name, neg.quantity_kg, neg.proposed_price, neg.notes)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.get("/negotiations")
def get_negotiations(user_id: int, role: str):
    result = negotiation_op.get_negotiations_for_user(user_id, role)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result

@app.put("/negotiations/{neg_id}")
def update_negotiation(neg_id: int, upd: NegotiationUpdate):
    result = negotiation_op.update_negotiation(neg_id, upd.data)
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result
