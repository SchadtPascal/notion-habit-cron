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

        # Prüfen auf: Erledigt + Kategorie == Habits
        is_done = props["Erledigt"]["checkbox"]
        is_habit = (
            "Kategorie" in props and
            props["Kategorie"]["type"] == "select" and
            props["Kategorie"]["select"] and
            props["Kategorie"]["select"]["name"] == "Habits"
        )

        if is_done and is_habit:
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


