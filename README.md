# 🌾 Smart Farming Portal

**Smart Farming Portal** is a full-stack web application built with **Python and Supabase** that allows farmers to digitally manage crops, track farming activities, and view daily market prices and weather updates. Admins can update market data, and the system ensures each farmer’s data remains private and secure.

---

## 🌱 Key Features

### 1️⃣ User Management

* Farmer registration and login
* Secure authentication
* Each farmer can access only their own data

### 2️⃣ Crop Management

* Add, edit, and delete crop records
* Track crop details: name, area, sowing date, fertilizer, expected yield
* View crop history like a digital farming diary

### 3️⃣ Market Prices

* Admin can update daily crop market prices
* Farmers can view latest prices to make selling decisions

### 4️⃣ Weather Updates

* Display daily temperature, humidity, and rainfall
* Can use live weather API for real-time updates
* Optional: store weather history for reports

### 5️⃣ Reports & Insights

* Generate crop summary reports
* Downloadable as CSV or PDF
* Analyze trends: most planted crops, average yield

### 6️⃣ Security & Access Control

* Only authorized admins can update market prices
* Row-Level Security ensures farmers see only their crops

---

## 🛠 Technologies Used

* **Backend:** Python (Flask or Django)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** Supabase (PostgreSQL)
* **APIs:** OpenWeatherMap (optional for live weather updates)
* **Other Tools:** VS Code, Git, GitHub

---

## ⚙ Technical Details

* **Database Structure:**

  * `users` table: stores farmer/admin info
  * `crops` table: stores crop records linked to users
  * `market_prices` table: stores daily crop prices
  * Optional `weather` table for storing historical weather data

* **Authentication & Security:**

  * Passwords should be hashed before storing
  * Row-Level Security (RLS) ensures farmers access only their own crops

* **Admin Controls:**

  * Admins can add, edit, or delete market prices
  * Admin dashboard is protected via `is_admin` flag in the users table

---

## 📂 Project Structure

```
Python_FullStackProject/
├── src/                 # Core application logic
│   ├── logic.py         # Application logic and task operations
│   └── db.py            # Database operations (CRUD with Supabase/Postgres)
├── API/                 # Backend API
│   └── main.py          # FastAPI endpoints
├── Frontend/            # Frontend web application
│   └── app.py           # Streamlit web interface
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .env                 # Environment variables (API keys, database URL, secrets)
```

---

## Quick Start

### Prerequisites

* Python 3.8 or higher
* Supabase account

### 1️⃣ Clone the Project

```bash
# Clone with git
git clone https://github.com/Anusreereddysama/Python_FullStackProject.git
cd Python_FullStackProject

# OR download ZIP and extract
```

### 2️⃣ Create & Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Database Tables in Supabase

#### Users Table

```sql
CREATE TABLE users (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name text NOT NULL,
    phone text UNIQUE NOT NULL,
    password text NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at timestamp DEFAULT now()
);
```

#### Crops Table

```sql
CREATE TABLE crops (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id uuid REFERENCES users(id) ON DELETE CASCADE,
    crop_name text NOT NULL,
    area numeric,
    sow_date date,
    fertilizer text,
    expected_yield numeric,
    created_at timestamp DEFAULT now()
);
```

#### Market Prices Table

```sql
CREATE TABLE market_prices (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    crop_name text NOT NULL,
    date date NOT NULL,
    price_per_kg numeric NOT NULL
);
```

#### Weather Table (Optional)

```sql
CREATE TABLE weather (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    date date NOT NULL,
    temperature text,
    rainfall text,
    humidity text,
    created_at timestamp DEFAULT now()
);
```

### 5️⃣ Run the Application

#### FastAPI Backend

```bash
cd API
python main.py
```

* API will be available at: `http://localhost:8080`

#### Streamlit Frontend

```bash
cd Frontend
streamlit run app.py
```

---

## ⚠️ Common Issues

* `code` command not found → Install VS Code command in PATH: `Cmd + Shift + P → Shell Command: Install 'code' command in PATH`
* Database connection errors → Ensure Supabase URL and API key are correct
* Password issues → Use hashed passwords when storing in DB
* API errors (Weather/Market) → Verify internet connection and API key validity

---

## Future Enhancements

* AI Crop Health Monitoring (image-based disease detection)
* IoT sensor integration for real-time soil and weather data
* Automated Market Price Updates via scraping or API
* Mobile application version for field access
* Multi-language support for regional farmers

---

## 🆘 Support

For questions, bug reports, or feature requests:

**Anusree S** – [anusreereddysama@gmail.com](mailto:anusreereddysama@gmail.com)

```
```
