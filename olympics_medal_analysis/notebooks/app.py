import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Olympics Medal Analysis",
    page_icon="🏅",
    layout="wide"  
)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f8ff; /* light blue */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Custom CSS for sidebar width
st.markdown(
    """
    <style>
    /* Reduce sidebar width */
    [data-testid="stSidebar"] {
        min-width: 200px;
        max-width: 300px;
    }
    </style>
    """,
    unsafe_allow_html=True
)



options = st.sidebar.radio(
    "Choose an option ",
    ("Overall Analysis", "Country-wise Analysis", "Medals by Year","Medals by Gender","Medals Tally","Total Medals","About the developer")
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("olympics_medal_analysis/data/Athletes_summer_games.csv")
    df_medals = df.dropna(subset=['Medal'])  # keep only medal winners
    return df, df_medals

df, df_medals = load_data()

# ---- Medals by Year ----
if options == 'Medals by Year':
    st.header("Medals by Year")
    medals_by_year = df_medals.groupby('Year').size().reset_index(name='medal_count')

    st.write("### Data Preview")
    st.dataframe(medals_by_year)

    if not medals_by_year.empty:
        fig = px.line(
            medals_by_year,
            x='Year',
            y='medal_count',
            title='Medals by Year',
            markers=True
        )
        st.plotly_chart(fig)
    else:
        st.warning("No medal data found.")

# ---- Overall Analysis ----
elif options == 'Overall Analysis':
    st.header("Overall Analysis")
    total_athletes = df['Name'].nunique()
    total_countries = df['NOC'].nunique()
    total_sports = df['Sport'].nunique()
    total_events = df['Event'].nunique()
    total_medals = df_medals.shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Athletes", total_athletes)
        st.metric("Total Sports", total_sports)
    with col2:
        st.metric("Total Countries", total_countries)
        st.metric("Total Events", total_events)
    with col3:
        st.metric("Total Medals", total_medals)

#Country-wise Analysis
elif options == 'Country-wise Analysis':
    st.header("Country-wise Analysis")
    country = st.sidebar.selectbox("Select Country", df['NOC'].unique())
    
    # Keep only medal winners from the chosen country
    country_data = df_medals[df_medals['NOC'] == country]

    # ✅ Deduplicate by Games + Event + Medal (team medals only once)
    country_unique_medals = country_data.drop_duplicates(subset=['Games', 'Event', 'Medal'])

    st.write(f"### Medal Tally for {country}")
    medal_tally = country_unique_medals['Medal'].value_counts().reset_index()
    medal_tally.columns = ['Medal', 'Count']
    st.dataframe(medal_tally)

    if not country_unique_medals.empty:
        # Medals by year (deduplicated)
        medals_by_year = (
            country_unique_medals
            .groupby('Year')
            .size()
            .reset_index(name='medal_count')
        )

        fig = px.line(
            medals_by_year,
            x='Year',
            y='medal_count',
            title=f'Medals by Year for {country}',
            markers=True
        )
        st.plotly_chart(fig)
    else:
        st.warning(f"No medal data found for {country}.")

#Medals by gender
elif options == 'Medals by Gender':
    st.header("Medals by Gender")

    # Deduplicate to avoid team medals inflating counts
    medals_unique = df_medals.drop_duplicates(subset=['Games', 'Event', 'Medal', 'NOC'])

    # Group by gender
    medals_by_gender = (
        medals_unique.groupby('Sex')
        .size()
        .reset_index(name='medal_count')
    )

    st.write("### Medal Distribution by Gender")
    st.dataframe(medals_by_gender)

    # Plot
    if not medals_by_gender.empty:
        fig = px.pie(
            medals_by_gender,
            names='Sex',
            values='medal_count',
            title='Medals Distribution by Gender'
        )
        st.plotly_chart(fig)
    else:
        st.warning("No gender data available.")


# ---- Medals Tally ----
elif options == 'Medals Tally':
    st.header("Medals Tally")
    year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique(), reverse=True))
    country = st.sidebar.selectbox("Select Country", sorted(df['NOC'].unique()))

    # Filter data based on selections
    filtered_data = df_medals[(df_medals['Year'] == year) & (df_medals['NOC'] == country)]

    # Deduplicate by Games + Event + Medal (team medals only once)
    filtered_unique_medals = filtered_data.drop_duplicates(subset=['Games', 'Event', 'Medal'])

    st.write(f"### Medal Tally for {country} in {year}")
    medal_tally = filtered_unique_medals['Medal'].value_counts().reset_index()
    medal_tally.columns = ['Medal', 'Count']
    st.dataframe(medal_tally)

    if medal_tally.empty:
        st.warning(f"No medals found for {country} in {year}.")

# ---- Total Medals ----
elif options == 'Total Medals':
    st.header("Total Medals by Country")
    total_medals_by_country = (
        df_medals.groupby('NOC')
        .size()
        .reset_index(name='total_medals')
        .sort_values(by='total_medals', ascending=False)
    )

    st.write("### Total Medals by Country")
    st.dataframe(total_medals_by_country)

    if not total_medals_by_country.empty:
        fig = px.bar(
            total_medals_by_country.head(20),
            x='NOC',
            y='total_medals',
            title='Top 20 Countries by Total Medals',
            labels={'NOC': 'Country', 'total_medals': 'Total Medals'}
        )
        st.plotly_chart(fig)
    else:
        st.warning("No medal data available.")

# ---- About the developer ----
elif options == 'About the developer':
    st.header("About the Developer")
    st.markdown("""
    **Name:** Fawas Anayat   
    **Role:** Data Scientist | Machine Learning Engineer | AI Enthusiast\n
    **Contact** [Linkedin](linkedin.com/in/fawas-anayat-32b120261) \n
    **Portfolio** [Github](https://github.com/Fawas-Anayat)""")
    