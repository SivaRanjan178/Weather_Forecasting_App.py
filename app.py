import streamlit as st
import pyowm
from datetime import datetime
import matplotlib.pyplot as plt
import time
from weather_details import get_weather_details  # Import additional weather details module

# Replace with your actual OpenWeatherMap API key
API_KEY = "3711e5fb8d3b64e1fd4f17185a819b4b"
owm = pyowm.OWM(API_KEY)
mgr = owm.weather_manager()

st.title("5-Day Weather Forecast 🌤️")
place = st.text_input("Enter City Name:", "")

unit = st.selectbox("Select Temperature Unit", ("Celsius", "Fahrenheit"))
graph_type = st.selectbox("Select Graph Type", ("Line Graph", "Bar Graph"))

if place:
    try:
        # Fetch forecast data
        forecast = mgr.forecast_at_place(place, "3h").forecast

        # Lists for storing temperature data
        days, temp_min, temp_max, feels_like = [], [], [], []

        for weather in forecast:
            day = datetime.utcfromtimestamp(weather.reference_time()).strftime('%Y-%m-%d')
            temp = weather.temperature(unit.lower())

            # Extract min/max temperatures if available, otherwise estimate
            min_temp = temp.get("min", temp.get("temp", 0) - 3)
            max_temp = temp.get("max", temp.get("temp", 0) + 3)

            feels = temp.get("feels_like", "N/A")

            # Ensure min_temp is always less than max_temp
            if min_temp > max_temp:
                min_temp, max_temp = max_temp, min_temp

            # Add to lists if it's a new day
            if day not in days:
                days.append(day)
                temp_min.append(round(min_temp, 2))
                temp_max.append(round(max_temp, 2))
                feels_like.append(feels)

        # ✅ Display Min — Max Temperature Before the Graph
        st.write("### 🌡️ Min - Max Temperatures for 5 Days")
        for i in range(len(days)):
            st.write(f"📅 {days[i]}: **{temp_min[i]}° — {temp_max[i]}°**")

        # ✅ Plot Temperature Graph
        def plot_temperature():
            plt.figure(figsize=(10, 5))

            if not temp_min or not temp_max:
                st.error("⚠️ No temperature data available for plotting!")
                return

            x_indexes = range(len(days))  # Create indexes for bars
            width = 0.4  # Adjust bar width

            if graph_type == "Bar Graph":
                # Plot min and max temperatures side by side
                plt.bar([x - width / 2 for x in x_indexes], temp_min, width=width, label="Min Temp", color="blue", alpha=0.8)
                plt.bar([x + width / 2 for x in x_indexes], temp_max, width=width, label="Max Temp", color="red", alpha=0.8)
                # Add labels on top of bars
                for i, (min_val, max_val) in enumerate(zip(temp_min, temp_max)):
                    plt.text(i - width / 2, min_val + 0.5, f"{min_val:.2f}°", ha="center", fontsize=10, color="white", weight="bold")
                    plt.text(i + width / 2, max_val + 0.5, f"{max_val:.2f}°", ha="center", fontsize=10, color="white", weight="bold")

            else:
                plt.plot(days, temp_min, label="Min Temp", marker="o", linestyle="-", color="blue")
                plt.plot(days, temp_max, label="Max Temp", marker="o", linestyle="-", color="red")

            plt.xticks(ticks=x_indexes, labels=days)  # Set x-axis labels
            plt.xlabel("Date")
            plt.ylabel(f"Temperature ({unit})")
            plt.legend()
            st.pyplot(plt)

        plot_temperature()  # ✅ Show graph first

        # ✅ Fetch Additional Weather Details from `weather_details.py`
        weather_info = get_weather_details(mgr, place)

        # ✅ Temperature Changes Section
        st.write("### 🌡️ Temperature Changes")
        if "error" in weather_info:
            st.error(weather_info["error"])
        else:
            st.write(f"💧 **Humidity:** {weather_info['humidity']}%")
            st.write(f"🌧️ **Will it rain?** {weather_info['rain']}")

        # ✅ Cloud Average & Wind Speed Section
        st.write("### 🌬️ Cloud Coverage & Wind Speed")
        st.write(f"☁️ **The Cloud Coverage for {place.title()} is:** {weather_info['cloud_coverage']}%")
        st.write(f"💨 **The Wind Speed for {place.title()} is:** {weather_info['wind_speed']} m/s")

        # ✅ Sunrise & Sunset Section
        st.write("### 🌅 Sunrise & Sunset Times")
        st.write(f"🌅 **Sunrise time in {place.title()} is:** {weather_info['sunrise_time']} GMT")
        st.write(f"🌇 **Sunset time in {place.title()} is::** {weather_info['sunset_time']} GMT")

        # ✅ Refresh Streamlit
        time.sleep(1)
        st.rerun()

    except Exception as e:
        st.error(f"⚠️ Error fetching weather data: {e}")
