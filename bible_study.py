# %% [markdown]
# # Isaiah
# %% [markdown]
# ### BYBW1 Relationship Between God and Humanity
# ### D6 Isaiah 1-6
# %% [markdown]
# https://biblehub.com/esv/isaiah/1.htm
# %%
import pandas as pd
import re
# %%
 # Thematic configuration
THEMES = {
    "Attributes of God": {
        "keywords": ["holy", "eternal", "almighty", "faithful", "love", "sovereign"],
        "color": "#FFC0CB"  # Pink
    },
    "Commands": {
        "keywords": ["thou shalt", "repent", "follow", "do not", "go", "pray"],
        "color": "#ADD8E6"  # Light Blue
    },
    "Promises": {
        "keywords": ["will give", "inheritance", "peace", "not be shaken", "with you"],
        "color": "#90EE90"  # Light Green
    },
    "People": {
        "keywords": ["Isaiah"],
        "color": "#FFC0CB"
    },
}

def highlight_verse(text):
    for theme, data in THEMES.items():
        # Check if any keyword from the theme is in the verse (case-insensitive)
        if any(word.lower() in text.lower() for word in data['keywords']):
            return f'<div style="background-color: {data["color"]}; padding: 10px; border-radius: 5px; margin: 5px 0;">' \
                   f'<strong>[{theme}]</strong> {text}</div>'

    # Return plain text if no theme matches
    return f'<div style="padding: 10px;">{text}</div>'


import streamlit as st

st.title("📖 Thematic Bible Dashboard")
st.write("Enter verses below to see them automatically categorized.")

# Input area
input_text = st.text_area("""1The vision of Isaiah the son of Amoz, which he saw concerning Judah and Jerusalem in the days of Uzziah, Jotham, Ahaz, and Hezekiah, kings of Judah.

The Wickedness of Judah

2Hear, O heavens, and give ear, O earth;
for the Lord has spoken:
“Childrena have I reared and brought up,
but they have rebelled against me.
3The ox knows its owner,
and the donkey its master’s crib,
but Israel does not know,
my people do not understand.”

4Ah, sinful nation,
a people laden with iniquity,
offspring of evildoers,
children who deal corruptly!
They have forsaken the Lord,
they have despised the Holy One of Israel,
they are utterly estranged.

5Why will you still be struck down?
Why will you continue to rebel?
The whole head is sick,
and the whole heart faint.
6From the sole of the foot even to the head,
there is no soundness in it,
but bruises and sores
and raw wounds;
they are not pressed out or bound up
or softened with oil.

7Your country lies desolate;
your cities are burned with fire;
in your very presence
foreigners devour your land;
it is desolate, as overthrown by foreigners.
8And the daughter of Zion is left
like a booth in a vineyard,
like a lodge in a cucumber field,
like a besieged city.

9If the Lord of hosts
had not left us a few survivors,
we should have been like Sodom,
and become like Gomorrah.

10Hear the word of the Lord,
you rulers of Sodom!
Give ear to the teachingb of our God,
you people of Gomorrah!
11“What to me is the multitude of your sacrifices?
says the Lord;
I have had enough of burnt offerings of rams
and the fat of well-fed beasts;
I do not delight in the blood of bulls,
or of lambs, or of goats.

12“When you come to appear before me,
who has required of you
this trampling of my courts?
13Bring no more vain offerings;
incense is an abomination to me.
New moon and Sabbath and the calling of convocations—
I cannot endure iniquity and solemn assembly.
14Your new moons and your appointed feasts
my soul hates;
they have become a burden to me;
I am weary of bearing them.
15When you spread out your hands,
I will hide my eyes from you;
even though you make many prayers,
I will not listen;
your hands are full of blood.
16Wash yourselves; make yourselves clean;
remove the evil of your deeds from before my eyes;
cease to do evil,
17learn to do good;
seek justice,
correct oppression;
bring justice to the fatherless,
plead the widow’s cause.

18“Come now, let us reasonc together, says the Lord:
though your sins are like scarlet,
they shall be as white as snow;
though they are red like crimson,
they shall become like wool.
19If you are willing and obedient,
you shall eat the good of the land;
20but if you refuse and rebel,
you shall be eaten by the sword;
for the mouth of the Lord has spoken.”

The Unfaithful City

21How the faithful city
has become a whore,d
she who was full of justice!
Righteousness lodged in her,
but now murderers.
22Your silver has become dross,
your best wine mixed with water.
23Your princes are rebels
and companions of thieves.
Everyone loves a bribe
and runs after gifts.
They do not bring justice to the fatherless,
and the widow’s cause does not come to them.

24Therefore the Lord declares,
the Lord of hosts,
the Mighty One of Israel:
“Ah, I will get relief from my enemies
and avenge myself on my foes.
25I will turn my hand against you
and will smelt away your dross as with lye
and remove all your alloy.
26And I will restore your judges as at the first,
and your counselors as at the beginning.
Afterward you shall be called the city of righteousness,
the faithful city.”

27Zion shall be redeemed by justice,
and those in her who repent, by righteousness.
28But rebels and sinners shall be broken together,
and those who forsake the Lord shall be consumed.
29For theye shall be ashamed of the oaks
that you desired;
and you shall blush for the gardens
that you have chosen.
30For you shall be like an oak
whose leaf withers,
and like a garden without water.
31And the strong shall become tinder,
and his work a spark,
and both of them shall burn together,
with none to quench them.""")

if st.button("Analyze & Highlight"):
    # Splitting by lines or periods to simulate verse-by-verse analysis
    verses = input_text.split('.')

    for verse in verses:
        if verse.strip():
            highlighted_html = highlight_verse(verse.strip())
            st.markdown(highlighted_html, unsafe_allow_html=True)