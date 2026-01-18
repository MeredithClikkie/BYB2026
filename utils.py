import streamlit as st

# utils.py

# BLACKLIST: Add words here that you want the AI to STOP highlighting
# (Case sensitive usually, so add variations if needed)
BLACKLIST = {
    "faith", "grace", "learn", "seek", "relieve", "amen", "life", "new moons", "sabbaths", "philistines", "behold",
    "lo", "thou"
}

def is_blacklisted(word):
    if not word:
        return False
    # This strips the comma from "Behold," so it becomes "behold"
    clean_word = word.strip(".,!?;:()[]\"' ").lower()
    return clean_word in BLACKLIST


def get_base_patterns():
    return [
        # Define patterns for the "GOD" category
        {"label": "GOD", "pattern": [{"LOWER": "god"}]},
        {"label": "GOD", "pattern": [{"LOWER": "god"}, {"LOWER": "the"}, {"LOWER": "father"}]},
        {"label": "GOD", "pattern": [{"LOWER": "lord"}]},
        {"label": "GOD", "pattern": [{"LOWER": "jesus"}]},
        {"label": "GOD", "pattern": [{"LOWER": "christ"}]},
        {"label": "GOD", "pattern": [{"LOWER": "spirit"}]},
        {"label": "GOD", "pattern": [{"LOWER": "father"}, {"LOWER": "god"}]},
        {"label": "GOD", "pattern": [{"LOWER": "father"}, {"LOWER": "son"}]},
        {"label": "GOD", "pattern": [{"LOWER": "holy"}, {"LOWER": "ghost"}]},
        {"label": "GOD", "pattern": [{"LOWER": "holy"}, {"LOWER": "spirit"}]},
        {"label": "GOD", "pattern": [{"LOWER": "savior"}]},
        {"label": "GOD", "pattern": [{"LOWER": "yahweh"}]},
        {"label": "GOD", "pattern": [{"LOWER": "yahweh"}, {"LOWER": "of"}, {"LOWER": "armies"}]},
        {"label": "GOD", "pattern": [{"LOWER": "holy"}, {"LOWER": "one"}]},
        {"label": "GOD", "pattern": [{"LOWER": "son"}, {"LOWER": "of"}, {"LOWER": "god"}]},
        {"label": "GOD", "pattern": [{"LOWER": "son"}, {"LOWER": "of"}, {"LOWER": "the"}, {"LOWER": "father"}]},
        {"label": "GOD", "pattern": [{"LOWER": "son"}, {"LOWER": "of"}, {"LOWER": "man"}]},
        {"label": "GOD", "pattern": [{"LOWER": "son"}, {"LOWER": "of"}, {"LOWER": "the"}, {"LOWER": "father"}]},
        {"label": "GOD", "pattern": [{"LOWER": "Immanuel"}]},
        {"label": "GOD", "pattern": [{"LOWER": "wonderful"}, {"LOWER": "counselor"}]},
        {"label": "GOD", "pattern": [{"LOWER": "mighty"}, {"LOWER": "god"}]},
        {"label": "GOD", "pattern": [{"LOWER": "mighty"}, {"LOWER": "one"}]},
        {"label": "GOD", "pattern": [{"LOWER": "everlasting"}, {"LOWER": "father"}, {"LOWER": "god"}]},
        {"label": "GOD", "pattern": [{"LOWER": "prince"}, {"LOWER": "of"}, {"LOWER": "peace"}]},
        {"label": "GOD", "pattern": [{"LOWER": "king"}, {"LOWER": "of"}, {"LOWER": "the"}, {"LOWER": "jews"}]},
        {"label": "GOD", "pattern": [{"LOWER": "his"}, {"LOWER": "Son"}]},

        # Add patterns for the "PERSON" category
        {"label": "PERSON", "pattern": [{"LOWER": "jacob"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "ahaz"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "uzziah"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "pekah"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "remaliah"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "tabeel"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "maher"}, {"LOWER": "shalal"}, {"LOWER": "hash"}, {"LOWER": "baz"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "uriah"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "gallim"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "tamar"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "amminadab"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "hezron"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "nahshon"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "salmon"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "boaz"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "obed"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "rehoboam"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "abijah"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "asa"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "jehoshaphat"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "joram"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "shealtiel"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "jechoniah"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "azor"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "zadok"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "eliud"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "eleazer"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "eliakim"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "achim"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "herod"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "moses"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "adam"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "cain"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "irad"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "mehujael"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "adah"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "zillah"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "jubal"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "lamech"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "jabal"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "tubal-cain"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "tubal"}, {"LOWER": "cain"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "kenan"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "mahalalel"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "jared"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "enoch"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "ham"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "job"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "satan"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "eliphaz"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "bildad"}]},


        # Add patterns for the "PEOPLE GROUPS" category
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "philistine"}]},
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "syrians"}]},
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "assyrian"}]},
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "assyrians"}]},
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "jews"}]},
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "the"}, {"LOWER": "jews"}]},
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "jew"}]},
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "nazarene"}]},
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "sabeans"}]},
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "chaldeans"}]},

        # Add patterns for the "GPE" category
        {"label": "GPE", "pattern": [{"LOWER": "sodom"}]},
        {"label": "GPE", "pattern": [{"LOWER": "gomorrah"}]},
        {"label": "GPE", "pattern": [{"LOWER": "zion"}]},
        {"label": "GPE", "pattern": [{"LOWER": "ephraim"}]},
        {"label": "GPE", "pattern": [{"LOWER": "shiloah"}]},
        {"label": "GPE", "pattern": [{"LOWER": "zebulon"}]},
        {"label": "GPE", "pattern": [{"LOWER": "galilee"}]},
        {"label": "GPE", "pattern": [{"LOWER": "manasseh"}]},
        {"label": "GPE", "pattern": [{"LOWER": "arpad"}]},
        {"label": "GPE", "pattern": [{"LOWER": "calno"}]},
        {"label": "GPE", "pattern": [{"LOWER": "carchemish"}]},
        {"label": "GPE", "pattern": [{"LOWER": "hamath"}]},
        {"label": "GPE", "pattern": [{"LOWER": "aiath"}]},
        {"label": "GPE", "pattern": [{"LOWER": "migron"}]},
        {"label": "GPE", "pattern": [{"LOWER": "michmash"}]},
        {"label": "GPE", "pattern": [{"LOWER": "ramah"}]},
        {"label": "GPE", "pattern": [{"LOWER": "gibeah"}]},
        {"label": "GPE", "pattern": [{"LOWER": "gebim"}]},
        {"label": "GPE", "pattern": [{"LOWER": "the"}, {"LOWER": "egyptian"}, {"LOWER": "sea"}]},
        {"label": "GPE", "pattern": [{"LOWER": "babylon"}]},
        {"label": "GPE", "pattern": [{"LOWER": "judea"}]},
        {"label": "GPE", "pattern": [{"LOWER": "bethlehem"}]},
        {"label": "GPE", "pattern": [{"LOWER": "land"}, {"LOWER": "of"}, {"LOWER": "havilah"}]},
        {"label": "GPE", "pattern": [{"LOWER": "land"}, {"LOWER": "of"}, {"LOWER": "cush"}]},
        {"label": "GPE", "pattern": [{"LOWER": "gihon"}]},
        {"label": "GPE", "pattern": [{"LOWER": "hiddekel"}]},
        {"label": "GPE", "pattern": [{"LOWER": "pishon"}]},
        {"label": "GPE", "pattern": [{"LOWER": "euphrates"}]},
        {"label": "GPE", "pattern": [{"LOWER": "tigris"}]},
        {"label": "GPE", "pattern": [{"LOWER": "uz"}]},

        # Define patterns for the "TØP" category
        {"label": "tøp", "pattern": [{"LOWER": "necromancer"}]},
        {"label": "tøp",
         "pattern": [{"LOWER": "dead"}, {"LOWER": "on"}, {"LOWER": "behalf"}, {"LOWER": "of"}, {"LOWER": "the"},
                     {"LOWER": "living"}]}
    ]



def apply_custom_css():
    import streamlit as st
    st.markdown("<style> .main { background-color: #f5f5f5; } </style>", unsafe_allow_html=True)