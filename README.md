# 🌾 Smart Farming Portal
Smart Farming Portal: A full-stack web application built with Python and Supabase that allows farmers to digitally manage their crops, track farming activities, and view daily market prices and weather updates. Admins can update market data, and the system ensures each farmer’s data remains private and secure.

## 🌱 Key Features
1️⃣ User Management

Farmer registration and login

Secure authentication

Each farmer can access only their own data

2️⃣ Crop Management

Add, edit, and delete crop records

Track crop details: crop name, area, sowing date, fertilizer, expected yield

View crop history like a digital farming diary

3️⃣ Market Prices

Admin can update daily crop market prices

Farmers can view latest prices to make selling decisions

4️⃣ Weather Updates

Display daily temperature, humidity, and rainfall

Can use live weather API for real-time updates

Optional: store weather history for reports

5️⃣ Reports & Insights

Generate crop summary reports

Downloadable as CSV or PDF

Analyze trends: most planted crops, average yield, etc.

6️⃣ Security & Access Control

Only authorized admins can update market prices

Row-Level Security ensures farmers see only their crops

## Technologies Used

- **Backend:** Python (Flask or Django)  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** Supabase (PostgreSQL)  
- **APIs:** OpenWeatherMap (optional for live weather updates)  
- **Other Tools:** VS Code, Git, GitHub  

---

## Technical Details

- **Database Structure:**  
  - `users` table: stores farmer/admin info  
  - `crops` table: stores crop records linked to users  
  - `market_prices` table: stores daily crop prices  
  - Optional `weather` table for storing historical weather data  
- **Authentication & Security:**  
  - Passwords should be hashed before storing  
  - Row-Level Security (RLS) ensures farmers access only their own crops  
- **Admin Controls:**  
  - Admins can add, edit, or delete market prices  
  - Admin dashboard is protected via `is_admin` flag in the users table  

---

## How to Use

### Farmer
1. Register or log in as a farmer  
2. Add crop details: crop name, area, sowing date, fertilizer, expected yield  
3. View your crop records in the dashboard  
4. Check daily market prices and weather updates  
5. Generate reports for analysis (CSV or PDF)  

### Admin
1. Log in as an admin (is_admin = TRUE)  
2. Add or update daily market prices  
3. View all farmers’ crop records (optional)  
4. Manage reports or data updates  

# Project Structure

Python_FullStackProject/
|
|--src/                     # Core apllication logic
|   |---logic.py            #Apllication logic and task
operations
|   |--db.pyn               #Database Operations
|
|--API/                    #Backend API
|   |--main.py             #Fast API end points
|
|--Frontend/               #Frontend web application
|   |--app.py              #Streamlit web interface
|
|--requirements.txt        #Python Dependencies
|
|--Readme.md               #Project Documentation
|
|.env                      #Python Environmet Variables

# Quick Start
  ## Prerequisites
   -python 3.8 or higher
   -A Supabase account

   # 1.Clone or Download the project
    ## 1.Clone with git
       git clone https://github.com/Anusreereddysama/Python_FullStackProject.git
    ## 2.Download a zip file
   # 2.Create & activate virtual environment:
      python3 -m venv venv
      source venv/bin/activate
   # 3.Install Dependencies
    -install al required packages with this command
      pip install -r requirements.txt
    
   # 4.Setup Database tables in supabase(users(farmers and admins),crops,market_prices,weather)
    Run this SQL commands in Supabase SQL editor
    # USER TABLE 
       create table users (
        id uuid primary key default uuid_generate_v4(), 
        name text not null,
        phone text unique not null,
        password text not null, 
        is_admin BOOLEAN DEFAULT FALSE,
        created_at timestamp default now()
        );

    # CROPS TABLE
      create table crops (
        id uuid primary key default uuid_generate_v4(),
        user_id uuid references users(id) on delete cascade, 
        crop_name text not null,
        area numeric,
        sow_date date,
        fertilizer text,
        expected_yield numeric,
        created_at timestamp default now()
        );

    #MARKET_PRICES TABLE
       create table market_prices (
        id uuid primary key default uuid_generate_v4(),
        crop_name text not null,
        date date not null,
        price_per_kg numeric not null
        );

    #WEATHER TABLE
       create table weather (
        id uuid primary key default uuid_generate_v4(),
        date date not null,
        temperature text,
        rainfall text,
        humidity text,
        created_at timestamp default now()
        );
   
   # Run the Application
     #FastAPI backend
       cd API
       python main.py
       The API will available at 'http://localhost:8080'

   # Common Issues
     code command not found: Install VS Code command in PATH via Cmd + Shift + P → Shell Command: Install 'code' command in PATH.
     Database connection errors: Ensure Supabase URL and API key are correct.
     Password issues: Use hashed passwords when storing in DB.
     API errors (Weather/Market): Verify internet connection and API key validity.

   # Future Enhancements

     AI Crop Health Monitoring (image-based disease detection)
     IoT sensor integration for real-time soil and weather data
     Automated Market Price Updates via scraping or API
     Mobile application version for field access
     Multi-language support for regional farmers
   # Support 
     For questions, bug reports, or feature requests:
     Your Name – anusreereddysama@gmail.com