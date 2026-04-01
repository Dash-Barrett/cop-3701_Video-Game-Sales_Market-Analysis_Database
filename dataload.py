import oracledb
import csv

# --- SETUP ---
LIB_DIR = r"C:\basic light package\instantclient_23_0"  # Your Instant Client Path
DB_USER = "cop3710"
DB_PASS = "sp2026"
DB_DSN  = "127.0.0.1:1521/XE"

# Initialize Thick Mode (Required for FreeSQL/Cloud)
oracledb.init_oracle_client(lib_dir=LIB_DIR)

def bulk_load_csv(file_path, table_type):
    try:
        # 1. Connect
        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        cursor = conn.cursor()
        
        # 2. Read CSV Data into a List
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            data_to_insert = [row for row in reader]

        # 3. Prepare Bulk Insert SQL
        # :1 and :2 correspond to the values in each row of your list
        if(table_type == "GameRegionSales"):
            sql = "INSERT INTO GAME_SALES_REGION (Game_ID, Platform_Name, Sales_Rank, Region, Region_Sales) VALUES (:1, :2, :3, :4, :5)"

        elif(table_type == "Game"):
            sql = "INSERT INTO GAME (Game_ID, Game_Name, Release_Year, Publisher_Name) VALUES (:1, :2, :3, :4)"

        elif(table_type == "GameSpecs"):
            sql = "INSERT INTO GAME_SPECS (Game_ID, Game_Spec_ID, Genre_Name, Launch_Price, Current_Price) VALUES (:1, :2, :3, :4, :5)"

        elif(table_type == "Platforms"):
            sql = "INSERT INTO PLATFORMS (Platform_Name, Platform_Holder, Launch_Year) VALUES (:1, :2, :3)"

        elif(table_type == "PublisherPlatform"):
            sql = "INSERT INTO PUBLISHER_PLATFORM (Publisher_Name, Platform_Name, Exclusive_Contract) VALUES (:1, :2, :3)"

        elif(table_type == "Publisher"):
            sql = "INSERT INTO PUBLISHER (Publisher_Name, Founding_Year, Total_Games) VALUES (:1, :2, :3)"

        # 4. Execute Batch
        print(f"Starting bulk load of {len(data_to_insert)} rows...")
        cursor.executemany(sql, data_to_insert)
        
        # 5. Commit Changes
        conn.commit()
        print(f"Successfully loaded {cursor.rowcount} rows into the database.")

    except Exception as e:
        print(f"Error during bulk load: {e}")
        if 'conn' in locals():
            conn.rollback() # Undo changes if an error occurs

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# Run the function
print("\nLoading Publisher Data...\n")
bulk_load_csv('data\PublisherTable.csv', "Publisher")
print("\nLoading Game Data...\n")
bulk_load_csv('data\GamesTable.csv', "Game")
print("\nLoading GameSpecs Data...\n")
bulk_load_csv('data\GameSpecsTable.csv', "GameSpecs")
print("\nLoading Platform Data...\n")
bulk_load_csv('data\PlatformTable.csv', "Platforms")
print("\nLoading Publisher-Platform Data...\n")
bulk_load_csv('data\PublisherPlatformTable.csv', "PublisherPlatform")
print("\nLoading Game Region Sales Data....\n")
bulk_load_csv('data\GameRegionSalesTable.csv', "GameRegionSales")
