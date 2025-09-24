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

   # Clone or Download the project
    ## 1.Clone with git
       git clone https://github.com/Anusreereddysama/Python_FullStackProject.git
    ## 2.Download a zip file

   # Install Dependencies
    -install al required packages with this command
      pip install -r requirements.txt
    
   # Setup Database table in supabase ( users(farmers and admins),crops,market_prices,weather)
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



