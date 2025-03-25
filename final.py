import streamlit as st
import google.generativeai as genai
import requests
from datetime import datetime

st.set_page_config(page_title="GoExplore", page_icon="🌍")


gemini_api_key = st.secrets["GEMINI_API_KEY"]
weather_api_key = st.secrets["WEATHER_API_KEY"]


genai.configure(api_key=gemini_api_key)

def get_weather(Destination):
    """Fetches real-time weather details for the given destination."""
    try:
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={Destination}&appid={weather_api_key}&units=metric"
        response = requests.get(weather_url)
        weather_data = response.json()

        if response.status_code == 200 and "main" in weather_data:
            temp = weather_data["main"]["temp"]
            description = weather_data["weather"][0]["description"]
            return f"🌤️ **Weather:** {temp}°C, {description.capitalize()}"
        else:
            return "⚠️ Unable to fetch weather data. Please try again."
    except Exception as e:
        return f"❌ Weather API error: {str(e)}"

def get_travel_plan(Destination, Departure, travellers, budget, start_date, end_date,restaurant_preference,Interest):
    """Generates a detailed travel plan using Gemini AI."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")

        prompt = f"""
        Plan a well-detailed trip from {Departure} to {Destination} for {travellers} travellers, with a budget of {budget} USD.
        Travel dates: {start_date} to {end_date}.
        The travelers are interested in {Interest}. Please include activities and sightseeing recommendations based on this interest.
        Include:
        - Day-wise itinerary
        - Accommodation options based on {hotel_type} hotels
        - Flight recommendations based on {flight_type} class
        - Sightseeing recommendations
        - Local transport details
        - Food recommendations with {restaurant_preference} restaurants
       **Do NOT include any disclaimers or notes about budgeting, itinerary customization.**

        """

        response = model.generate_content(prompt)

        return response.text if response else "⚠️ AI couldn't generate travel suggestions. Try again later."
    except Exception as e:
        return f"❌ Gemini AI error: {str(e)}"

st.title("✈️ Travel & Exploration Bot")
st.write("Get real-time travel insights, recommendations!")

col1, col2 = st.columns(2)
with col1:
    Destination = st.text_input("✈️ Destination", placeholder="e.g., Rome")
    Departure = st.text_input("🏡 Departure City", placeholder="e.g., Mumbai")
    Start_date = st.date_input("📅 Start Date")
    End_date = st.date_input("📅 End Date")
    restaurant_preference = st.radio("🍽️ Restaurant Preference", ["Veg", "Non-Veg"], horizontal=True)

with col2:
    Number_of_Travellers = st.number_input("👥 Travellers", min_value=1, value=1)
    Budget_level = st.number_input("💰 Budget (INR)", min_value=100, value=1000)
    Interest = st.selectbox("🎯 Interest", ["All", "Adventure", "Culture", "Relaxation", "Wildlife", "Food & Wine", "History", "Shopping", "Nightlife"])
    hotel_type = st.selectbox("🏨 Hotel Type", ["Budget", "Mid-range", "Luxury"])
    flight_type = st.selectbox("🛫 Flight Class", ["Economy", "Business", "First Class"])

if st.button("🔍 Get Travel Info"):
    if Destination and Departure and Start_date and End_date:
        with st.spinner("Fetching travel insights..."):
            weather = get_weather(Destination)
            suggestions = get_travel_plan(Destination, Departure, Number_of_Travellers, Budget_level, Start_date, End_date,restaurant_preference,Interest)

        st.subheader(f"🌍 Travel Insights for {Destination}")
        st.write(weather)
        st.markdown(f"📜 **Travel Plan:**\n\n{suggestions}")
    else:
        st.warning("⚠️ Please enter all the required details!")

