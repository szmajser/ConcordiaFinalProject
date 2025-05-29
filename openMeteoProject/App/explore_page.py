import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

##################################################################################################
# Load Dataset
##################################################################################################
@st.cache_data
def load_data():
    df = pd.read_csv('./openMeteoProject/Data/quebec_hourly_weather_2017_2024_after_EDA.csv')
    return df

# Call Load Data Function to load CSV information
df = load_data()

##################################################################################################
# Show Explore Page
##################################################################################################
def show_explore_page():
    st.title("Explore Weather Events Data Location: Quebec Province")

    st.write("## Information from Open Meteo API")

    # Links to OpenMete API Docs and Weather codes source
    url_api_docs = "https://open-meteo.com/en/docs"
    url_weather_codes = "https://www.nodc.noaa.gov/archive/arc0021/0002199/1.1/data/0-data/HTML/WMO-CODE/WMO4677.HTM"
    st.write("- API Docs - [api_docs](%s)" % url_api_docs)
    st.write("- National Centers for Environmental Information - Weather Codes used - [weather_codes](%s)" % url_weather_codes)

    # Tab - Show Weather used codes for Snow / Rain / Hail
    tab1, tab2, tab3 = st.tabs(["Snow Weather Codes", "Rain Weather Codes", "Hail Weather Codes"])
    with tab1:
        #####################################################
        # Snow Weather codes used
        #####################################################
        #st.write(" 71 - Continuous fall of snowflakes")
        #st.write(" 73 - Continuous fall of snowflakes")
        #st.write(" 75 - Continuous fall of snowflakes")
        #st.write(" 77 - Snow grains (with or without fog)")
        #st.write(" 85 - Snow shower(s), slight")
        #st.write(" 86 - Snow shower(s), moderate or heavy")
        #st.write(" ")
        #st.write("### Snow - Weather codes used")
        st.write("- 71 - Continuous fall of snowflakes")
        st.write("- 73 - Continuous fall of snowflakes")
        st.write("- 75 - Continuous fall of snowflakes")
        st.write("- 77 - Snow grains (with or without fog)")
        st.write("- 85 - Snow shower(s), slight")
        st.write("- 86 - Snow shower(s), moderate or heavy")
    with tab2:
        #####################################################
        # Rain Weather codes used
        #####################################################
        # 61	Rain, not freezing, continuous
        # 63	Rain, not freezing, continuous
        # 65	Rain, not freezing, continuous
        # 80	Rain shower(s), slight
        # 81	Rain shower(s), moderate or heavy
        # 82	Rain shower(s), violent
        #st.write("### Rain - Weather codes used")
        st.write("- 61 - Rain, not freezing, continuous")
        st.write("- 63 - Rain, not freezing, continuous")
        st.write("- 65 - Rain, not freezing, continuous")
        st.write("- 80 - Rain shower(s), slight)")
        st.write("- 81 - Rain shower(s), moderate or heavy")
        st.write("- 82 - Rain shower(s), violent")
         
    with tab3:
        #####################################################
        # Hail Weather codes used
        #####################################################
        # 96	Thunderstorm, slight or moderate, with hail 
        # 99	Thunderstorm, heavy, with hail* 
        #st.write("### Hail - Weather codes used")
        st.write("- 96 - Thunderstorm, slight or moderate, with hail")
        st.write("- 99 - Thunderstorm, heavy, with hail")

    if st.checkbox("Show Raw Dataset"):
        st.write(df)

    st.write("### Weather Event Distribution")
    event_counts = {
        "Rain": df["rain"].sum(),
        "Snow": df["snow"].sum(),
        "Hail": df["hail"].sum()
    }

    fig1, ax1 = plt.subplots()
    ax1.pie(event_counts.values(), labels=event_counts.keys(), autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

    selected_year = st.selectbox("Select a year", df["year"].unique())
    filtered = df[df["year"] == selected_year]
    
    # Rain by Year by Month
    monthly_rain = filtered.groupby("month")["rain"].sum()
    st.write("### Rain by year " + str(selected_year))
    st.bar_chart(monthly_rain)

    # Snow by Year by Month
    monthly_snow = filtered.groupby("month")["snow"].sum()
    st.write("### Snow by year " + str(selected_year))
    st.bar_chart(monthly_snow)

    # Hail by Year by Month
    monthly_hail = filtered.groupby("month")["hail"].sum()
    st.write("### Hail by year " + str(selected_year))
    st.bar_chart(monthly_hail)

    # Monthly events by Rain / Snow / Hail
    event = st.selectbox("Select event type:", ["rain", "snow", "hail"])
    event_per_month = df.groupby("month")[event].sum()

    st.write(f"### Monthly {event.capitalize()} Events")
    st.bar_chart(event_per_month)