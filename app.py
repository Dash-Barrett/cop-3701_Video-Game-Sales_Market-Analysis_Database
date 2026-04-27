'''
If you are running this code first time, and you don't have streamlit installed, then follow this instruction:
1. open a terminal
2. enter this command
    pip install streamlit
'''

import streamlit as st
import oracledb

# --- DATABASE SETUP ---
# Update this path to your local Instant Client folder
LIB_DIR = # INSTANT CLIENT PATH
DB_USER = # USERNAME
DB_PASS = # PASSWORD
DB_DSN  = # DSN 


# Initialize Oracle Client for Thick Mode
@st.cache_resource
def init_db():
    if LIB_DIR:
        try:
            oracledb.init_oracle_client(lib_dir=LIB_DIR)
        except Exception as e:
            st.error(f"Error initializing Oracle Client: {e}")


init_db()


def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)


# --- STREAMLIT UI ---
st.title("Video Game Sales Market Analysis Database")
st.subheader("Search for & Analysis Info")

menu = ["Region Sales", "Publisher Sales", "Platform Sales", "Average Current Price on Platform", "Price History of a Game"]
choice = st.sidebar.selectbox("Select Action", menu)


if choice == "Region Sales":
    st.write("### Search Region")
    region = st.text_input("Type Here")

    if st.button("Search"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT REGION, SUM(REGION_SALES)*1000000 as REVENUE FROM GAME_SALES_REGION WHERE REGION = :1 GROUP BY REGION", [region])
            conn.commit()
            data = cur.fetchall()
            cur.close()
            conn.close()

            if data:
                st.table(data)
                st.success(f"{region} found!")
            else:
                st.info("Region not found.")
        except Exception as e:
            st.error(f"Error: {e}")


elif choice == "Publisher Sales":
    st.write("### Search Publisher")
    publisher = st.text_input("Type Here")

    if st.button("Search"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT p.PUBLISHER_NAME, SUM(g.REGION_SALES)*1000000 as REVENUE FROM PUBLISHER_PLATFORM p JOIN GAME_SALES_REGION g ON g.PLATFORM_NAME = p.PLATFORM_NAME WHERE p.PUBLISHER_NAME = :1 GROUP BY p.PUBLISHER_NAME", [publisher])
            conn.commit()
            data = cur.fetchall()
            cur.close()
            conn.close()

            if data:
                st.table(data)
                st.success(f"{publisher} found!")
            else:
                st.info("Publisher not found.")
        except Exception as e:
            st.error(f"Error: {e}")



elif choice == "Platform Sales":
    st.write("### Search Platform")
    platform = st.text_input("Type Here")

    if st.button("Search"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT PLATFORM_NAME, SUM(REGION_SALES)*1000000 as REVENUE FROM GAME_SALES_REGION WHERE PLATFORM_NAME = :1 GROUP BY PLATFORM_NAME", [platform])
            conn.commit()
            data = cur.fetchall()
            cur.close()
            conn.close()

            if data:
                st.table(data)
                st.success(f"{platform} found!")
            else:
                st.info("Platform not found.")
        except Exception as e:
            st.error(f"Error: {e}")


elif choice == "Average Current Price on Platform":
    st.write("### Search Platform")
    platform = st.text_input("Type Here")

    if st.button("Search"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT p.PLATFORM_NAME, ROUND(AVG(s.CURRENT_PRICE), 2) FROM PUBLISHER_PLATFORM p JOIN GAME g ON p.PUBLISHER_NAME = g.PUBLISHER_NAME JOIN GAME_SPECS s ON g.GAME_ID = s.GAME_ID WHERE p.PLATFORM_NAME = :1 GROUP BY p.PLATFORM_NAME", [platform])
            conn.commit()
            data = cur.fetchall()
            cur.close()
            conn.close()

            if data:
                st.table(data)
                st.success(f"{platform} found!")
            else:
                st.info("Platform not found.")
        except Exception as e:
            st.error(f"Error: {e}")

elif choice == "Price History of a Game":
    st.write("### Search Game")
    game = st.text_input("Type Here")

    if st.button("Search"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT g.GAME_NAME, s.LAUNCH_PRICE, s.CURRENT_PRICE FROM GAME g JOIN GAME_SPECS s ON g.GAME_ID = s.GAME_ID WHERE g.GAME_NAME = :1", [game])
            conn.commit()
            data = cur.fetchall()
            cur.close()
            conn.close()

            if data:
                st.table(data)
                st.success(f"{game} found!")
            else:
                st.info("Game not found.")
        except Exception as e:
            st.error(f"Error: {e}")

# run using: streamlit run app.py
