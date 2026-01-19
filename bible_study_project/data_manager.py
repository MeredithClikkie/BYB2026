# data_manager.py
import requests

def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        response = requests.get(url)
        return response.json()['text'] if response.status_code == 200 else "Text not found."
    except:
        return "Connection error."

def get_master_data(wave_name):
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

    return {}  # Return empty dict if no wave found


def get_timeline_events(wave, chapter):
    """
    Filters the data for a specific chapter.
    If chapter is 'All', it combines all chapters in that wave.
    """
    wave_data = get_master_data(wave)

    if chapter == "All":
        all_events = []
        for ch_events in wave_data.values():
            all_events.extend(ch_events)
        return all_events

    return wave_data.get(str(chapter), [])