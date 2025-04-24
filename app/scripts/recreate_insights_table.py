from app.models.analytics import Analytics

def main():
    print("Starting analytics table recreation...")
    Analytics.recreate_table()
    print("Analytics table recreation completed.")

if __name__ == "__main__":
    main() 