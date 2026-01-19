import streamlit as st


def get_data(full_reference):
    try:
        parts = full_reference.strip().split()
        book = parts[0].title()
        # We don't need chapter for the 'Letters', but we keep it for 'Acts' logic
        chapter = parts[1].split(":")[0]
    except:
        return {"events": []}

    # --- STEP 1: INITIALIZE LIST ---
    events = []


    # --- Step 2: ADD PERMANENT JOURNEYS ---
    # These stay on the timeline regardless of which book you are in
    journeys = [
        {"year": 46, "head": "⛵ 1st Journey (Acts 13-14)",
         "text": "Paul & Barnabas sent from Antioch to Cyprus and Galatia.", "color": "#1b4f72"},
        {"year": 49, "head": "🗺️ 2nd Journey (Acts 15-18)",
         "text": "The Gospel enters Europe; ministry in Philippi and Corinth.", "color": "#1e8449"},
        {"year": 53, "head": "📖 3rd Journey (Acts 19-21)", "text": "Paul's extensive ministry in Ephesus.",
         "color": "#9a7d0a"},
        {"year": 59, "head": "⚓ Voyage to Rome (Acts 27-28)",
         "text": "Paul travels as a prisoner to stand trial before Caesar.", "color": "#212f3d"}
    ]

    for j in journeys:
        events.append({
            "start_date": {"year": j["year"]},
            "display_date": f"AD {j['year']}",
            "background": {"color": j["color"]},
            "text": {"headline": j["head"], "text": j["text"]}
        })

    # --- STEP 3: ADD EPISTLE DATA ---
    epistle_context = {
        "Galatians": {"year": 48, "loc": "Antioch",
                      "context": "Written shortly after the 1st Journey regarding the Gospel of Grace."},
        "Romans": {"year": 57, "loc": "Corinth",
                   "context": "Paul's masterwork on salvation, written toward the end of his 3rd Journey."},
        "Ephesians": {"year": 61, "loc": "Rome (Prison)", "context": "Written during his first Roman house arrest."},
        "Philippians": {"year": 61, "loc": "Rome (Prison)", "context": "The 'Epistle of Joy' written while in chains."},
        "Colossians": {"year": 61, "loc": "Rome (Prison)", "context": "Focusing on the supremacy of Christ."}
    }

    if book in epistle_context:
        ctx = epistle_context[book]
        events.append({
            "start_date": {"year": ctx["year"]},
            "display_date": f"AD {ctx['year']}",
            "background": {"color": "#FCE300"},  # Bandito Yellow makes the 'current book' stand out
            "text": {
                "headline": f"📬 CURRENT INTEL: Letter to the {book}",
                "text": f"<b>Written from:</b> {ctx['loc']}<br><br>{ctx['context']}"
            }
        })


# --- STEP 4: SORTING & INDEXING ---
    # We sort NOW after all events have been added to the list
    events = sorted(events, key=lambda x: x["start_date"]["year"])

    start_index = 0
    for i, event in enumerate(events):
        if "CURRENT INTEL" in event.get("text", {}).get("headline", ""):
            start_index = i
            break

    # --- STEP 5: RETURN PAYLOAD ---
    return {
        "events": events,
        "start_at_slide": start_index
    }