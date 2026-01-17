# books/genesis.py

def get_data():
    """Provides data to the superior script."""
    return [
        {"Event": "Creation/Fall", "Date": -4000},
        {"Event": "The Flood", "Date": -2400},
        {"Event": "Call of Abraham", "Date": -2091},
        {"Event": "Joseph in Egypt", "Date": -1898},
        {"Event": "Jacob Moves to Egypt", "Date": -1876}
    ]

def get_specific_patterns():
    """Patterns unique to Genesis."""
    return [
        {"label": "GPE", "pattern": [{"LOWER": "eden"}]},
        {"label": "GPE", "pattern": [{"LOWER": "ararat"}]}
    ]