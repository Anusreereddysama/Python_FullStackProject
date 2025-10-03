import streamlit as st
import requests
from datetime import date

API_URL = "http://127.0.0.1:8000"

# -------------------------
# Page Config & Branding
# -------------------------
st.set_page_config(
    page_title="Smart Farming Portal",
    page_icon="🌾",
    layout="wide"
)

BRAND_NAME = "Smart Farming Portal"
PRIMARY_COLOR = "#1B5E20"
ACCENT_COLOR = "#2E7D32"
LIGHT_BG = "#F6FFF6"

st.markdown(
    f"""
    <style>
        .app-header {{
            background: linear-gradient(90deg, {PRIMARY_COLOR}, {ACCENT_COLOR});
            color: #ffffff;
            padding: 18px 24px;
            border-radius: 8px;
            margin-bottom: 16px;
        }}
        .app-footer {{
            color: #777;
            font-size: 12px;
            text-align: center;
            margin-top: 28px;
        }}
        .kpi-card {{
            background: {LIGHT_BG};
            border: 1px solid #e6f2e6;
            padding: 16px;
            border-radius: 8px;
        }}
        .stButton>button {{
            background-color: {ACCENT_COLOR} !important;
            color: white !important;
            border: 0 !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(f"<div class='app-header'><h2 style='margin:0'>{BRAND_NAME}</h2><div>Official services for our farming community</div></div>", unsafe_allow_html=True)

# -------------------------
# Session state
# -------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'active_page' not in st.session_state:
    st.session_state.active_page = "Home"

# -------------------------
# API Helpers
# -------------------------
def api_get(path, params=None):
    try:
        res = requests.get(f"{API_URL}{path}", params=params or {})
        return res.json()
    except Exception as e:
        return {"success": False, "message": str(e), "data": []}

def api_post(path, payload):
    try:
        res = requests.post(f"{API_URL}{path}", json=payload)
        return res.json()
    except Exception as e:
        return {"success": False, "message": str(e)}

def api_put(path, payload):
    try:
        res = requests.put(f"{API_URL}{path}", json=payload)
        return res.json()
    except Exception as e:
        return {"success": False, "message": str(e)}

def api_delete(path):
    try:
        res = requests.delete(f"{API_URL}{path}")
        return res.json()
    except Exception as e:
        return {"success": False, "message": str(e)}

# -------------------------
# Auth
# -------------------------
def login(phone, password):
    users = api_get("/users")
    if not users.get('success'):
        st.error(users.get('message', 'Unable to fetch users'))
        return False
    for user in users.get('data', []):
        if user.get('phone') == phone and user.get('password') == password:
            st.session_state.logged_in = True
            st.session_state.user = user
            return True
    st.error("Invalid phone or password")
    return False

def register(name, phone, password, is_admin=False):
    payload = {"name": name, "phone": phone, "password": password, "is_admin": is_admin}
    res = api_post("/users", payload)
    if res.get('success'):
        st.success("Registration successful. Logging you in...")
        return login(phone, password)
    st.error(res.get('message', 'Registration failed'))
    return False

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.active_page = "Home"

# -------------------------
# Pages
# -------------------------
def page_home():
    left, right = st.columns([2, 1])
    with left:
        st.subheader("Welcome")
        if st.session_state.logged_in and st.session_state.user:
            name = st.session_state.user.get('name', 'Farmer')
            st.write(f"Hello, {name}. Explore services using the sidebar.")
        else:
            st.write("Login or register to access personalized services.")
        st.markdown("- Manage crops and track your expected yield")
        st.markdown("- Buyers can post prices; farmers compare and negotiate")
        st.markdown("- Check local weather records")
    with right:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.caption("Quick Actions")
        if st.button("Go to Crops"):
            st.session_state.active_page = "Crops"
        if st.button("Market Prices"):
            st.session_state.active_page = "Market"
        if st.button("Weather"):
            st.session_state.active_page = "Weather"
        st.markdown("</div>", unsafe_allow_html=True)

def page_crops():
    st.subheader("My Crops")
    if not st.session_state.logged_in:
        st.info("Please login to manage your crops.")
        return

    user_id = st.session_state.user.get('id')
    crops = api_get(f"/crops/{user_id}")
    if crops.get('success'):
        data = crops.get('data', [])
        if data:
            for c in data:
                with st.container(border=True):
                    st.write(f"Crop: {c.get('crop_name')} | Area: {c.get('area', '-')}")
                    st.caption(f"Sow: {c.get('sow_date', '-')} | Fertilizer: {c.get('fertilizer', '-')} | Expected Yield: {c.get('expected_yield', '-')} kg")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Delete", key=f"del_{c.get('id')}"):
                            del_res = api_delete(f"/crops/{c.get('id')}")
                            if del_res.get('success'):
                                st.success("Deleted.")
                                st.rerun()
                            else:
                                st.error(del_res.get('message', 'Delete failed'))
        else:
            st.write("No crops yet. Add your first crop below.")
    else:
        st.error(crops.get('message', 'Could not fetch crops'))

    st.divider()
    st.subheader("Add a Crop")
    col1, col2 = st.columns(2)
    with col1:
        crop_name = st.text_input("Crop Name")
        area = st.number_input("Area (acres)", min_value=0.0, value=0.0)
        fertilizer = st.text_input("Fertilizer Used")
    with col2:
        sow_dt = st.date_input("Sow Date", value=date.today())
        expected_yield = st.number_input("Expected Yield (kg)", min_value=0.0, value=0.0)

    if st.button("Add Crop", type="primary"):
        payload = {
            "user_id": user_id,
            "crop_name": crop_name,
            "area": area,
            "sow_date": str(sow_dt),
            "fertilizer": fertilizer,
            "expected_yield": expected_yield,
        }
        res = api_post("/crops", payload)
        if res.get('success'):
            st.success(res.get('message', 'Crop added'))
            st.rerun()
        else:
            st.error(res.get('message', 'Add failed'))

def page_market():
    st.subheader("Market Prices")
    col1, col2 = st.columns([2, 1])
    with col1:
        search_crop = st.text_input("Search by Crop Name")
        if st.button("Search"):
            st.session_state["_search_crop"] = search_crop
    with col2:
        st.empty()

    search_value = st.session_state.get("_search_crop", "")
    prices = api_get("/market_prices", params={"crop_name": search_value or None})
    if prices.get('success'):
        for p in prices.get('data', []):
            st.write(f"{p.get('crop_name', '')}: {p.get('date', '')} - ₹{p.get('price_per_kg', '-')}/kg")
    else:
        st.error(prices.get('message', 'Could not fetch prices'))

    # Buyer can add prices
    if st.session_state.logged_in and st.session_state.user.get('is_admin'):
        st.divider()
        st.subheader("Add Market Price (Buyer)")
        c1, c2, c3 = st.columns(3)
        with c1:
            crop_name = st.text_input("Crop Name", key="admin_price_crop")
        with c2:
            dt = st.date_input("Date", key="admin_price_date", value=date.today())
        with c3:
            price = st.number_input("Price per KG (₹)", min_value=0.0, value=0.0, key="admin_price_value")
        if st.button("Add Price"):
            res = api_post("/market_prices", {"crop_name": crop_name, "date": str(dt), "price_per_kg": price, "buyer_id": st.session_state.user.get('id')})
            if res.get('success'):
                st.success(res.get('message', 'Price added'))
                st.rerun()
            else:
                st.error(res.get('message', 'Add failed'))

def page_weather():
    st.subheader("Weather Records")
    col1, col2 = st.columns(2)
    with col1:
        dt = st.date_input("Select Date", value=date.today())
        if st.button("View Weather"):
            st.session_state["_weather_date"] = str(dt)

    q_date = st.session_state.get("_weather_date")
    result = api_get("/weather", params={"date": q_date} if q_date else None)
    if result.get('success'):
        data = result.get('data', [])
        if data:
            for w in data:
                st.write(f"Date: {w.get('date')} | Temp: {w.get('temperature', '-')} | Rainfall: {w.get('rainfall', '-')} | Humidity: {w.get('humidity', '-')}")
        else:
            st.info("No records for selected date.")
    else:
        st.error(result.get('message', 'Could not fetch weather'))

    if st.session_state.logged_in and st.session_state.user.get('is_admin'):
        st.divider()
        st.subheader("Add Weather (Buyer)")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            w_date = st.date_input("Date", key="w_date", value=date.today())
        with c2:
            temp = st.text_input("Temperature", key="w_temp")
        with c3:
            rain = st.text_input("Rainfall", key="w_rain")
        with c4:
            humid = st.text_input("Humidity", key="w_humid")
        if st.button("Add Weather"):
            res = api_post("/weather", {"date": str(w_date), "temperature": temp or None, "rainfall": rain or None, "humidity": humid or None})
            if res.get('success'):
                st.success(res.get('message', 'Weather added'))
                st.rerun()
            else:
                st.error(res.get('message', 'Add failed'))

def page_buyer():
    st.subheader("Buyer Dashboard")
    if not (st.session_state.logged_in and st.session_state.user and st.session_state.user.get('is_admin')):
        st.info("Buyer access only.")
        return
    st.write("Post crop prices, view negotiations, and respond to offers.")
    page_market()
    st.divider()
    st.subheader("Negotiations")
    negs = api_get("/negotiations", params={"user_id": st.session_state.user.get('id'), "role": "buyer"})
    if negs.get('success'):
        for n in negs.get('data', []):
            with st.container(border=True):
                st.write(f"Farmer #{n.get('farmer_id')} offers {n.get('quantity_kg')} kg {n.get('crop_name')} @ ₹{n.get('proposed_price')}/kg")
                st.caption(f"Notes: {n.get('notes', '-')}")
                st.write(f"Status: {n.get('status')}")
    else:
        st.error(negs.get('message', 'Could not fetch negotiations'))

def page_account():
    st.subheader("Account")
    if st.session_state.logged_in and st.session_state.user:
        u = st.session_state.user
        st.write(f"Name: {u.get('name')}")
        st.write(f"Phone: {u.get('phone')}")
        st.write("Role: Buyer" if u.get('is_admin') else "Role: Farmer")
        if st.button("Logout"):
            logout()
            st.success("Logged out")
            st.rerun()
    else:
        st.info("Login to view your account.")

def page_negotiations():
    st.subheader("Negotiations")
    if not (st.session_state.logged_in and st.session_state.user):
        st.info("Login to view negotiations.")
        return
    user = st.session_state.user
    role = "buyer" if user.get('is_admin') else "farmer"
    negs = api_get("/negotiations", params={"user_id": user.get('id'), "role": role})
    if negs.get('success'):
        for n in negs.get('data', []):
            with st.container(border=True):
                st.write(f"Crop: {n.get('crop_name')} | Qty: {n.get('quantity_kg')} kg | Price: ₹{n.get('proposed_price')}/kg")
                st.caption(f"Notes: {n.get('notes', '-')}")
                st.write(f"Status: {n.get('status')}")
    else:
        st.error(negs.get('message', 'Could not fetch negotiations'))

# -------------------------
# Sidebar Navigation & Auth UI
# -------------------------
with st.sidebar:
    st.markdown("### Navigation")
    pages = ["Home", "Crops", "Market", "Weather"]
    if st.session_state.logged_in and st.session_state.user and st.session_state.user.get('is_admin'):
        pages.append("Buyer")
    pages.append("Negotiations")
    pages.append("Account")
    st.session_state.active_page = st.selectbox("Go to", pages, index=pages.index(st.session_state.active_page) if st.session_state.active_page in pages else 0)

    st.divider()
    if not st.session_state.logged_in:
        st.markdown("### Account")
        tab_login, tab_register = st.tabs(["Login", "Register"])
        with tab_login:
            phone = st.text_input("Phone", key="login_phone")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                if login(phone, password):
                    st.success("Welcome back!")
                    # redirect to role page
                    if st.session_state.user.get('is_admin'):
                        st.session_state.active_page = "Buyer"
                    else:
                        st.session_state.active_page = "Crops"
                    st.rerun()
        with tab_register:
            name = st.text_input("Name", key="reg_name")
            phone_r = st.text_input("Phone", key="reg_phone")
            pwd_r = st.text_input("Password", type="password", key="reg_password")
            is_admin = st.checkbox("Register as Buyer", key="reg_is_admin")
            if st.button("Create Account"):
                if register(name, phone_r, pwd_r, is_admin):
                    # redirect to role page
                    if st.session_state.user and st.session_state.user.get('is_admin'):
                        st.session_state.active_page = "Buyer"
                    else:
                        st.session_state.active_page = "Crops"
                    st.rerun()

# -------------------------
# Router
# -------------------------
page_map = {
    "Home": page_home,
    "Crops": page_crops,
    "Market": page_market,
    "Weather": page_weather,
    "Buyer": page_buyer,
    "Negotiations": page_negotiations,
    "Account": page_account,
}

page_map.get(st.session_state.active_page, page_home)()

st.markdown("<div class='app-footer'>© 2025 Smart Farming Portal. All rights reserved.</div>", unsafe_allow_html=True)
