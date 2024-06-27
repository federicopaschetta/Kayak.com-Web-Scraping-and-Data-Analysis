# Kayak Flight Tickets Analysis

## Overview
This project analyzes flight ticket data from Kayak.com, focusing on the top 10 airports in Europe by passenger traffic. The analysis includes web scraping, data preprocessing, and trend analysis of flight prices and routes.

## Team Members
- Federico Paschetta
- Karla Gonzalez Romero
- Yacine Merioua
- Arth Jain

## Project Structure
The project is divided into three main parts:

1. Web Scraping
2. Data Preprocessing
3. Data Analysis

### Part 1: Web Scraping

#### Data Source
- Website: www.kayak.com
- Airports: Top 10 in Europe by passenger traffic
  - LHR: London
  - CDG: Paris
  - AMS: Amsterdam
  - FRA: Frankfurt
  - MAD: Madrid
  - BCN: Barcelona
  - IST: Istanbul
  - MUC: Munich
  - FCO: Rome
  - DUB: Dublin

#### Scraping Details
- Dates: 19th of each month for a year (April 2024 to March 2025)
- Generated 10 CSV files (one for each airport)
- Over 3000 flight data entries per airport

#### Data Structure
Each row contains:
- DepAirport
- ArrAirport
- Carrier
- DepTime
- ArrTime
- Price
- Day
- DayAfter (Boolean)
- Duration

### Part 2: Data Preprocessing

#### Cleaning and Transformation
- Convert price text to numerical values
- Unify carrier names (e.g., 'Wizz Air', 'Wizz Air UK', 'Wizz Air Brussels' -> 'Wizz Air')
- Remove non-airline services (e.g., 'ALSA', 'RENFE')

### Part 3: Data Analysis

#### Key Analyses
1. Price Distribution by Carrier
   - Most Expensive: United Airlines
   - Least Expensive: RyanAir

2. Price Trends Over Time
   - Most Expensive Season: Spring (March-May)
   - Least Expensive Season: Winter (October-February)

3. Longest Routes and Average Prices
   - Found direct correlation between flight duration and price

#### Key Findings
- Flight prices depend on distance, booking time, and airline
- United Airlines and RyanAir are the most and least expensive airlines, respectively
- Spring is the most expensive season to fly, while Winter is the cheapest
- Longer flights generally have higher prices

## Recommendations
- Check websites in advance to avoid surcharge pricing

## Tools and Technologies Used
- Python
- Web scraping library (selenium)
- Data analysis libraries (Pandas and Matplotlib)
