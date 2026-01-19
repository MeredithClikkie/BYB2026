def get_data(full_reference):
    book = full_reference.strip().split()[0].title()

    # Most prophets fall into Pre-Exile, Exile, or Post-Exile
    return {"events": [
        {
            "start_date": {"year": -586},
            "display_date": "The Exile",
            "background": {"color": "#17202a"},
            "text": {"headline": "The Fall of Jerusalem",
                     "text": f"{book} speaks into the era of the Babylonian captivity."}
        },
        {
            "start_date": {"year": -538},
            "display_date": "The Return",
            "background": {"color": "#f1c40f"},
            "text": {"headline": "Restoration", "text": "The remnant returns to rebuild the Temple."}
        }
    ]}