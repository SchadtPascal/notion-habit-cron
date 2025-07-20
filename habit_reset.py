from notion_client import Client
from datetime import datetime, timedelta
import os

# Zugriff auf Umgebungsvariablen
notion = Client(auth=os.environ["NOTION_TOKEN"])
database_id = os.environ["NOTION_DB_ID"]

def update_habits():
    # Abfrage aller Einträge in der Notion-Datenbank
    response = notion.databases.query(database_id=database_id)
    for page in response["results"]:
        props = page["properties"]
        
        # Nur bearbeiten, wenn Checkbox "Erledigt" aktiviert ist
        if props["Erledigt"]["checkbox"]:
            old_date = props["Datum"]["date"]["start"]
            new_date = (datetime.fromisoformat(old_date).date() + timedelta(days=1)).isoformat()
            
            # Update: Datum +1 Tag & Checkbox zurücksetzen
            notion.pages.update(
                page_id=page["id"],
                properties={
                    "Datum": {"date": {"start": new_date}},
                    "Erledigt": {"checkbox": False}
                }
            )

if __name__ == "__main__":
    update_habits()

