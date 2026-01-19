import streamlit as st


def get_data(full_reference):
    try:
        parts = full_reference.strip().split()
        book = parts[0].title()
        chapter = parts[1].split(":")[0]
    except:
        return {"events": []}

    events = []

    # Acts - The Holy Spirit & The Early Church
    if book == "Acts":
        if chapter == "2":
            events.append({
                "start_date": {"year": 30},
                "display_date": "Pentecost",
                "background": {"color": "#7b241c"},
                "text": {"headline": "🔥 Pentecost", "text": "The Holy Spirit descends; 3,000 baptized."}
            })
        if chapter in ["13", "14", "15"]:
            events.append({
                "start_date": {"year": 46},
                "display_date": "AD 46-48",
                "background": {"color": "#1b4f72"},
                "text": {"headline": "⛵ Paul's 1st Journey", "text": "Mission to Cyprus and Galatia."}
            })

        # ... (Keep your Acts 2 and Acts 13 logic here)

        # NEW: If no chapter-specific events were added, add a general book event
        if not events:
            if book == "Acts":
                events.append({
                    "start_date": {"year": 30},
                    "display_date": "AD 30 - 62",
                    "background": {"color": "#1b4f72"},
                    "text": {"headline": "The Acts of the Apostles",
                             "text": "The era of the early church spreading from Jerusalem to Rome."}
                })
            elif book == "Revelation":
                events.append({
                    "start_date": {"year": 95},
                    "display_date": "AD 95",
                    "background": {"color": "#4a235a"},
                    "text": {"headline": "The Apocalypse of John",
                             "text": "Written by the Apostle John during his exile on the island of Patmos."}
                })

        return {"events": events}