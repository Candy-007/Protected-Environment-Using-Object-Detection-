import streamlit as st
import requests

def get_current_location():
    try:
        response = requests.get('http://ip-api.com/json/')
        data = response.json()
        
        if data['status'] == 'success':
            # Perform a Google search for places near the current location
            police_station_search_url = f"https://www.google.com/maps/search/police+stations+near+me"
            fire_brigade_search_url = f"https://www.google.com/maps/search/fire+brigade+near+me"

            st.subheader("Search for Police Stations near your location:")
            st.write(f"[Google Maps - Police Stations]({police_station_search_url})")

            st.subheader("Search for Fire Brigades near your location:")
            st.write(f"[Google Maps - Fire Brigades]({fire_brigade_search_url})")

            st.subheader("Current Location:")
            st.write("Latitude:", data['lat']) 
            st.write("Longitude:", data['lon'])
            st.write("City:", data['city'])
            st.write("Zip Code:", data['zip'])
            st.write("Region:", data['regionName'])
            st.write("Country:", data['country'])
        else:
            st.write("Unable to fetch the current location.")
    except Exception as e:
        st.write("An error occurred:", e)
