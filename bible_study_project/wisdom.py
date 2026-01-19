def get_data(full_reference):
    book = full_reference.strip().split()[0].title()

    # Era of Solomon (Proverbs, Ecclesiastes, Song of Solomon)
    if book in ["Proverbs", "Ecclesiastes", "Song"]:
        return {"events": [{
            "start_date": {"year": -970},
            "display_date": "10th Century BC",
            "background": {"color": "#9a7d0a"},
            "text": {"headline": f"The Wisdom of {book}", "text": "Written during the Golden Age of Israel's Monarchy."}
        }]}

    # Era of David (Psalms)
    if book == "Psalms":
        return {"events": [{
            "start_date": {"year": -1010},
            "display_date": "The United Kingdom",
            "background": {"color": "#1e8449"},
            "text": {"headline": "The Songs of Israel",
                     "text": "Poetry collected largely during the reign of King David."}
        }]}

    return {"events": []}