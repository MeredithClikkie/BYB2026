# data_manager.py
import requests

def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        response = requests.get(url)
        return response.json()['text'] if response.status_code == 200 else "Text not found."
    except:
        return "Connection error."

def get_master_data(wave_name, chapter = "1"):
    """
    Returns the full database for a specific 'Wave' (Book).
    """
    # --- GENESIS DATA ---
    if wave_name == "Genesis":
        return {
                # --- CHAPTER 1: CREATION ---
            "1": [
                {
                    "start_date": {"year": -4004},
                    "display_date": "Day 1-3",
                    "background": {"color": "#000000"},
                    "media": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/6/6d/The_Creation_of_Light_by_Gustave_Dore.jpg",
                        "type": "image"},
                    "text": {"headline": "Forming the World",
                             "text": f"<b>Day 1:</b> Light out of Darkness.<br><b>Day 2:</b> The Firmament.<br><b>Day 3:</b> Dry land and seas."}
                },
                {
                    "start_date": {"year": -4004},
                    "display_date": "Day 4-6",
                    "background": {"color": "#1a365d"},
                    "media": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Creation_of_the_Sun_and_Moon_by_Dore.jpg",
                        "type": "image"},
                    "text": {"headline": "Filling the World",
                             "text": f"<b>Day 4:</b> Sun, Moon, and Stars.<br><b>Day 5:</b> Creatures of Sky and Sea.<br><b>Day 6:</b> Land animals and Mankind."}
                }
            ],

            # --- CHAPTER 7: THE FLOOD BEGINS ---
            "7": [
                # --- MASORETIC TEXT (Standard Tradition) ---
                {
                    "start_date": {"year": -2348, "month": 2, "day": 17},
                    "display_date": "2348 BC (Masoretic)",
                    "background": {"color": "#1a365d"},
                    "media": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/5/5a/The_Deluge_by_Francis_Danby.jpg",
                        "type": "image",
                        "caption": "Date calculated by Archbishop James Ussher."
                    },
                    "text": {"headline": "The Great Flood", "text": "The traditional Masoretic timeline."}
                },

                # --- SAMARITAN PENTATEUCH ---
                {
                    "start_date": {"year": -3145, "month": 2, "day": 17},
                    "display_date": "3145 BC (Samaritan)",
                    "background": {"color": "#2d3748"},
                    "media": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Noahs_Ark.jpg",
                        "type": "image"},
                    "text": {"headline": "Samaritan Chronology", "text": "This tradition places the flood earlier."}
                },

                # --- SEPTUAGINT (Greek Tradition) ---
                {
                    "start_date": {"year": -3298, "month": 2, "day": 17},
                    "display_date": "3298 BC (Septuagint)",
                    "background": {"color": "#000000"},
                    "media": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Noahs_Ark.jpg",
                        "type": "image"},
                    "text": {"headline": "Septuagint Chronology", "text": "The oldest biblical manuscript tradition."}
                }
            ],


            # --- CHAPTER 8: THE WATERS RECEDE ---
            "8": [
                {
                    "start_date": {"year": -2348, "month": 7, "day": 17},
                    "display_date": " 2348 BC, Month 7, Day 17",
                    "background": {"color": "#2d3748"},
                    "media": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Simon_de_Myle_-_Noah%27s_ark_on_Mount_Ararat.jpg/800px-Simon_de_Myle_-_Noah%27s_ark_on_Mount_Ararat.jpg",
                        "type": "image"},
                    "text": {"headline": "The Ark Rests", "text": get_bible_text("Genesis 8:4")}
                },
                {
                    "start_date": {"year": -2347, "month": 2, "day": 27},
                    "display_date": "2347 BC, Mo 2, Day 27",
                    "background": {"color": "#22543d"},
                    "media": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/The_Exit_from_the_Ark.jpg/800px-The_Exit_from_the_Ark.jpg",
                        "type": "image"},
                    "text": {"headline": "A New Beginning", "text": get_bible_text("Genesis 8:14")}
                }
            ]
        }

    # --- EXODUS DATA ---
    elif wave_name == "Exodus":
        return {
            "3": [
                {
                    "start_date": {"year": -1446},
                    "display_date": "1446 BC (Early Date)",
                    "background": {"color": "#744210"},
                    "media": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Simeon_Solomon_Moses_and_the_Burning_Bush.jpg/440px-Simeon_Solomon_Moses_and_the_Burning_Bush.jpg",
                        "type": "image"},
                    "text": {
                        "headline": "🔥 The Burning Bush",
                        "text": "The 15th-century date based on 1 Kings 6:1, placing the Exodus during the 18th Dynasty of Egypt."
                    }
                },
                {
                    "start_date": {"year": -1250},
                    "display_date": "c. 1250 BC (Late Date)",
                    "background": {"color": "#4a5568"},
                    "media": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Simeon_Solomon_Moses_and_the_Burning_Bush.jpg/440px-Simeon_Solomon_Moses_and_the_Burning_Bush.jpg",
                        "type": "image"},
                    "text": {
                        "headline": "🔥 The Burning Bush (Ramesside)",
                        "text": "The 13th-century date often favored by archaeologists, placing the Exodus during the reign of Ramesses II."
                    }
                }
            ],

            # --- CHAPTER 12: THE PASSOVER ---
            "12": [
                {
                    "start_date": {"year": -1446, "month": 1, "day": 14},
                    "display_date": "1446 BC, Nisan 14",
                    "background": {"color": "#000000"},
                    "media": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Charles_Foster_The_Signs_on_the_Door.jpg/440px-Charles_Foster_The_Signs_on_the_Door.jpg",
                        "type": "image"},
                    "text": {"headline": "🌑 The Tenth Plague",
                             "text": "The final plague on Egypt and the institution of the Passover."}
                }
            ],

            # --- CHAPTER 14: THE RED SEA ---
            "14": [
                {
                    "start_date": {"year": -1446, "month": 1, "day": 20},
                    "display_date": "1446 BC, The Crossing",
                    "background": {"color": "#2c5282"},
                    "media": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/The_Seventh_Plague_by_John_Martin.jpg/800px-The_Seventh_Plague_by_John_Martin.jpg",
                        "type": "image"},
                    "text": {"headline": "🌊 Crossing the Red Sea", "text": "Israel is delivered from Pharaoh's army."}
                }
            ]
        }

    # --- ERA OF SOLOMON (Proverbs, Ecclesiastes, Song of Solomon) ---
    elif wave_name in ["Proverbs", "Ecclesiastes", "Song of Solomon"]:
        # We return a dictionary where the key is "All" so the timeline loads automatically
        return {
            "All": [{
                "start_date": {"year": -970},
                "display_date": "10th Century BC",
                "background": {"color": "#9a7d0a"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Solomon_by_Simeon_Solomon.jpg/440px-Solomon_by_Simeon_Solomon.jpg",
                    "type": "image"},
                "text": {"headline": f"The Wisdom of {wave_name}",
                         "text": "Written during the Golden Age of Israel's Monarchy."}
            }]
        }

    # --- ERA OF DAVID (Psalms) ---
    elif wave_name == "Psalms":
        return {
            "All": [{
                "start_date": {"year": -1010},
                "display_date": "The United Kingdom",
                "background": {"color": "#1e8449"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/King_David_by_Guido_Reni.jpg/440px-King_David_by_Guido_Reni.jpg",
                    "type": "image"},
                "text": {"headline": "The Songs of Israel",
                         "text": "Poetry and worship collected largely during the reign of King David."}
            }]
        }


        # --- PROPHETS WAVE ---
    elif wave_name in ["Isaiah", "Jeremiah", "Ezekiel", "Daniel", "Malachi"]:
        return {
            "All": [
                {
                    "start_date": {"year": -586},
                    "display_date": "The Exile",
                    "background": {"color": "#17202a"},
                    "text": {"headline": "The Fall of Jerusalem",
                             "text": f"{wave_name} speaks into the era of the Babylonian captivity."}
                },
                {
                    "start_date": {"year": -538},
                    "display_date": "The Return",
                    "background": {"color": "#f1c40f"},
                    "text": {"headline": "Restoration", "text": "The remnant returns to rebuild the Temple."}
                }
            ]
        }

    # --- GOSPEL HARMONY WAVE ---
    elif wave_name in ["Matthew", "Mark", "Luke", "John"]:
        all_events = []

        # John 1: Prologue
        if chapter == "1" and wave_name == "John":
            all_events.append({
                "start_date": {"year": -4004},
                "display_date": "Eternity Past",
                "background": {"color": "#000000"},
                "text": {"headline": "The Word", "text": "In the beginning was the Word..."}
            })

        # Nativity
        if (wave_name == "Matthew" and chapter == "2") or (wave_name == "Luke" and chapter == "2"):
            all_events.append({
                "start_date": {"year": -4},
                "display_date": "4 BC",
                "background": {"color": "#1a202c"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/The_Nativity_by_Federico_Barocci.jpg/440px-The_Nativity_by_Federico_Barocci.jpg",
                    "type": "image"},
                "text": {"headline": "✨ The Nativity", "text": "The birth of Jesus in Bethlehem."}
            })

        # Baptism
        if chapter == "3" and wave_name in ["Matthew", "Mark", "Luke"]:
            all_events.append({
                "start_date": {"year": 26},
                "display_date": "AD 26",
                "background": {"color": "#2d3748"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Baptism_of_Christ_by_Piero_della_Francesca.jpg/440px-Baptism_of_Christ_by_Piero_della_Francesca.jpg",
                    "type": "image"},
                "text": {"headline": "🌊 Baptism of Jesus", "text": "Ministry begins at the Jordan River."}
            })

        # Crucifixion
        passion_chapters = {"Matthew": "27", "Mark": "15", "Luke": "23", "John": "19"}
        if chapter == passion_chapters.get(wave_name):
            all_events.append({
                "start_date": {"year": 30, "month": 4, "day": 7},
                "display_date": "AD 30",
                "background": {"color": "#000000"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Crucifixion_Dali.jpg/440px-Crucifixion_Dali.jpg",
                    "type": "image"},
                "text": {"headline": "🌑 The Crucifixion", "text": "The sacrifice at Calvary."}
            })

        return {"current_chapter": all_events}

    return {}


def get_timeline_events(book, chapter):
    # Ensure events starts as a list!
    # Sort everything by year before returning

    events = []
    # Step 1: Get data from master
    wave_data = get_master_data(book, chapter)

    if not wave_data:
        return [], 0

    # Handle the key structure
    if chapter == "All":

        for ch_events in wave_data.values():
            events.extend(ch_events)
    else:
        # Check for specific chapter or the Gospel harmony key
        events = wave_data.get(str(chapter), wave_data.get("current_chapter", []))

    # Step 2: ADD PERMANENT JOURNEYS (For Acts & Epistles)
    # Note: We only add these for New Testament books to keep the timeline relevant
    nt_books = ["Acts", "Romans", "Galatians", "Ephesians", "Philippians", "Colossians", "Hebrews", "James"]

    if book in nt_books or book in ["Matthew", "Mark", "Luke", "John"]:
        journeys = [
            {"year": 46, "head": "⛵ 1st Journey (Acts 13-14)", "color": "#1b4f72",
             "text": "Paul & Barnabas sent from Antioch to Cyprus and Galatia."},
            {"year": 49, "head": "🗺️ 2nd Journey (Acts 15-18)", "color": "#1e8449",
             "text": "The Gospel enters Europe; ministry in Philippi and Corinth."},
            {"year": 53, "head": "📖 3rd Journey (Acts 19-21)", "color": "#9a7d0a",
             "text": "Paul's extensive ministry in Ephesus."},
            {"year": 59, "head": "⚓ Voyage to Rome (Acts 27-28)", "color": "#212f3d",
             "text": "Paul travels as a prisoner to stand trial before Caesar."}
        ]

        for j in journeys:
            events.append({
                "start_date": {"year": j["year"]},
                "display_date": f"AD {j['year']}",
                "background": {"color": j["color"]},
                "text": {"headline": j["head"], "text": j["text"]}
            })

    # Step 3: ADD EPISTLE DATA
    epistle_context = {
        "Galatians": {"year": 48, "loc": "Antioch", "context": "Regarding the Gospel of Grace."},
        "Romans": {"year": 57, "loc": "Corinth", "context": "Paul's masterwork on salvation."},
        "Ephesians": {"year": 61, "loc": "Rome (Prison)", "context": "Written during house arrest."},
        "Philippians": {"year": 61, "loc": "Rome (Prison)", "context": "The 'Epistle of Joy'."},
        "Colossians": {"year": 61, "loc": "Rome (Prison)", "context": "Supremacy of Christ."}
    }

    if book in epistle_context:
        ctx = epistle_context[book]
        events.append({
            "start_date": {"year": ctx["year"]},
            "display_date": f"AD {ctx['year']}",
            "background": {"color": "#FCE300"},
            "text": {
                "headline": f"📬 CURRENT INTEL: Letter to the {book}",
                "text": f"<b>Written from:</b> {ctx['loc']}<br><br>{ctx['context']}"
            }
        })

    # Step 4: SORTING & INDEXING
    if not events:
        return [], 0

    # Sort by year
    events = sorted(events, key=lambda x: x["start_date"]["year"])

    # Find the "Current Intel" index to center the timeline
    start_index = 0
    for i, event in enumerate(events):
        if "CURRENT INTEL" in event.get("text", {}).get("headline", ""):
            start_index = i
            break

    # Return the list. In biblestudy_gpp.py, you will wrap this in {"events": events, "start_at_slide": start_index}
    return events, start_index
