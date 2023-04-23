import pickle
from pathlib import Path
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth
import yaml
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import altair as alt
from time import strftime
import time
# --- USER AUTHENTICATION ---
with open('/Users/aishworyann/Desktop/Streamlit Authenticator/config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')


def port():
    # Upload CSV
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # Create a dictionary to map boolean values to checkmark or cross symbols
        # status_dict = {True: "✅", False: "❌"}
        # # Replace the boolean values with checkmark or cross symbols
        # df["Enabled"] = df["Enabled"].map(status_dict)
        #Table BG
        st.markdown(
            '<style>div.row-widget.stRadio > div{background-color: #f4f4f4}</style>',
            unsafe_allow_html=True,
        )
        total_ports = len(df)
        open_ports = len(df[df['State'] == 'Open'])
        close_ports = total_ports - open_ports
        open_percentage = round(open_ports / total_ports * 100, 2)
        close_percentage = round(close_ports / total_ports * 100, 2)

        # Create a pie chart to display the data
        data = {'State': ['Open', 'Close'], 'Percentage': [open_percentage, close_percentage]}
        fig = px.pie(data, values='Percentage', names='State')
        left_column, right_column = st.columns(2)
        # Display the pie chart
        with left_column:
            st.write(df)
        with right_column:
            st.plotly_chart(fig)

        # Display table

def firewall():
    # Upload CSV
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Create a dictionary to map boolean values to checkmark or cross symbols
        status_dict = {True: "✅", False: "❌"}

        # Replace the boolean values with checkmark or cross symbols
        df["Enabled"] = df["Enabled"].map(status_dict)

        #Table BG
        st.markdown(
            '<style>div.row-widget.stRadio > div{background-color: #f4f4f4}</style>',
            unsafe_allow_html=True,
        )

        # Display table
        st.write(df)

def netstats():
    file = st.file_uploader("Upload CSV file", type=["csv"])
    if file:
        df = pd.read_csv(file)

        # Create a bar chart of InterfaceAlias and Source
        chart = alt.Chart(df).mark_bar().encode(
            x='InterfaceAlias',
            y='count()',
            color='Source'
        ).properties(
            width=600,
            height=400
        )
        st.altair_chart(chart)

        # Create a table of statistics for each InterfaceAlias
        interfaces = df['InterfaceAlias'].unique()
        for interface in interfaces:
            st.write('## ' + interface)
            subset = df[df['InterfaceAlias'] == interface]
            subset = subset.drop(columns=['ifAlias', 'ifDesc', 'Caption', 'Description', 'ElementName', 'InstanceID',
                                          'InterfaceDescription', 'Name', 'Source', 'SystemName'])
            st.write(subset)

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    # ---- SIDEBAR ----
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    with st.sidebar:
        selected = option_menu(
            menu_title= "Dashboard",
            options=["Home", "Network Audit", "OS Audit", "Vulnerability Assessment", "Malware Logs"],
            icons=["house", "ethernet","motherboard","braces asterisk","envelope"],
            menu_icon="cast",
            default_index=0,
        )
    if selected== "Home":
        st.title(f"{selected}")
        st.subheader('Notifications 🗒')
        with st.spinner("Listening..."):
            time.sleep(3)
        st.error(' Firewall are not enabled for one or more Domains')
        with st.spinner("Listening..."):
            time.sleep(2)
        st.error(' Ports [21] & [22] are open')
        with st.spinner("Listening..."):
            time.sleep(1)
        st.error(' No active backup present')
        with st.spinner("Listening..."):
            time.sleep(2)
        st.success(' System is Up-to Date')
        with st.spinner("Listening..."):
            time.sleep(3)
        st.success(' 2 Active Users Found')

    if selected == "Network Audit":
        select = option_menu(
            menu_title="Network Audit",
            options=["Firewall Stats", "Open-Ports Logs", "Network Stats"],
            icons=["bricks", "displayport", "fire"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"
        )
        # st.title(f"{selected}")
        if select == "Open-Ports Logs":
            st.title(f"{select}")
            port()
        if select == "Firewall Stats":
            st.title(f"{select}")
            firewall()
        if select == "Network Stats":
            st.title(f"{select}")
            netstats()



    if selected == "OS Audit":
        select = option_menu(
            menu_title="OS Audit",
            options=["OS Details", "System Version", "Peripheral Devices"],
            icons=["bricks", "displayport", "fire"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"
        )
        if select == "OS Details":
            st.title(f"{select}")
        if select == "System Version":
            st.title(f"{select}")
        if select == "Peripheral Devices":
            st.title(f"{select}")

    if selected == "Vulnerability Assessment":
        select = option_menu(
            menu_title="Vulnerability Assessment",
            options=["Assessment 1", "Assessment 2", "Assessment 3"],
            icons=["file-bar-graph", "file-bar-graph", "file-bar-graph"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"
        )
        if select == "Assessment 1":
            st.title(f"{select}")
        if select == "Assessment 2":
            st.title(f"{select}")
        if select == "Assessment 3":
            st.title(f"{select}")

    if selected == "Malware Logs":
        st.title(f"{selected}")


