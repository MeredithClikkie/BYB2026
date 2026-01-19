import streamlit as st


def get_data(full_reference):
    try:
        parts = full_reference.strip().split()
        book = parts[0].title()
        chapter = parts[1].split(":")[0]
    except:
        return {"events": []}

    events = []

    if book == "Acts":
        # CHAPTER 1-8: JERUSALEM
        if int(chapter) <= 8:
            events.append({
                "start_date": {"year": 30},
                "display_date": "AD 30-33",
                "background": {"color": "#7b241c"},
                "text": {"headline": "The Jerusalem Church", "text": "The apostles witness in Jerusalem and Judea."}
            })

        # CHAPTER 13-14: 1ST MISSIONARY JOURNEY
        elif int(chapter) in [13, 14]:
            events.append({
                "start_date": {"year": 46},
                "display_date": "AD 46-48",
                "background": {"color": "#1b4f72"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/First_missionary_journey_of_Paul.svg/800px-First_missionary_journey_of_Paul.svg.png",
                    "type": "image"},
                "text": {"headline": "⛵ 1st Missionary Journey",
                         "text": "Paul and Barnabas are sent out from Antioch to Cyprus and Galatia."}
            })

        # CHAPTER 15-18: 2ND MISSIONARY JOURNEY
        elif int(chapter) >= 15 and int(chapter) <= 18:
            events.append({
                "start_date": {"year": 49},
                "display_date": "AD 49-52",
                "background": {"color": "#1e8449"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Second_missionary_journey_of_Paul.svg/800px-Second_missionary_journey_of_Paul.svg.png",
                    "type": "image"},
                "text": {"headline": "🗺️ 2nd Missionary Journey",
                         "text": "The Gospel enters Europe (Philippi, Thessalonica, Athens, Corinth)."}
            })

        # CHAPTER 19-21: 3RD MISSIONARY JOURNEY
        elif int(chapter) >= 19 and int(chapter) <= 21:
            events.append({
                "start_date": {"year": 53},
                "display_date": "AD 53-57",
                "background": {"color": "#9a7d0a"},
                "text": {"headline": "📖 3rd Missionary Journey",
                         "text": "Paul spends three years in Ephesus, strengthening the churches."}
            })

        # CHAPTER 27-28: VOYAGE TO ROME
        elif int(chapter) >= 27:
            events.append({
                "start_date": {"year": 59},
                "display_date": "AD 59-62",
                "background": {"color": "#212f3d"},
                "text": {"headline": "⚓ Voyage to Rome",
                         "text": "Shipwreck at Malta and arrival in Rome under house arrest."}
            })

    return {"events": events}