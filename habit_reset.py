from notion_client import Client
from datetime import datetime, timedelta
import os

# Zugriff auf Umgebungsvariablen
notion = Client(auth=os.environ["NOTION_TOKEN"])
database_id = os.environ["NOTION_DB_ID"]

def update_habits():
    response = notion.databases.query(database_id=database_id)
    for page in response["results"]:
        props = page["properties"]

        erledigt = props.get("Erledigt", {}).get("checkbox", False)
        gruppe = props.get("Gruppe", {}).get("rich_text", [])
        gruppe_text = gruppe[0]["text"]["content"] if gruppe else ""

        # Nur wenn "Erledigt" aktiviert ist und Gruppe == "Habits"
        if erledigt and gruppe_text == "Habits":
            old_date = props["Datum"]["date"]["start"]
            new_date = (datetime.fromisoformat(old_date).date() + timedelta(days=1)).isoformat()

            notion.pages.update(
                page_id=page["id"],
                properties={
                    "Datum": {"date": {"start": new_date}},
                    "Erledigt": {"checkbox": False}
                }
            )

if __name__ == "__main__":
    update_habits()
