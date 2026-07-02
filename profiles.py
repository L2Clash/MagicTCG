PROFILES = { #Defines differences between deck archetypes, 
    #"name": {
    #   "title": "___",
    #   "categories": {
    #       "cat_1": 0,...},
    #   "base_deck": {
    #       "card_1": 3, ...},
    #   "special_cards": {
    #       "special_name": "name"},
    #   "target_creatures": ##,
    #   "checks": [
    #   ({minimums:1, (any, of, these):1}, {maximums:1, (these, count, any):1}),...
    #   ]
    #   "check_names": [
    #       "check_name_1",...]
    #},...
    "spy_combo": {
        "title": "Spy Combo",
        "categories": {
            "filler": 0,
            "forest": 1,
            "petal": 2,
            "grant": 3,
            "sagu": 4,
            "gatecreeper": 5,
            "creature": 6,
            "swamp": 7,
            "troll": 8,
            "ent": 9,
        },
        "creature_categories": {
            "creature",
            "ent",
            "sagu",
            "troll",
            "gatecreeper",
        },
        "base_deck": {
            "forest": 3,
            "swamp": 1,
            "petal": 1,
            "grant": 4,
            "sagu": 4,
            "ent": 4,
            "troll": 1,
            "gatecreeper": 3,
            "creature": 25,
        },
        "special_cards": {
            "Forest": "forest",
            "Swamp": "swamp",
            "Lotus Petal": "petal",
            "Land Grant": "grant",
            "Sagu Wildling": "sagu",
            "Gatecreeper Vine": "gatecreeper",
            "Generous Ent": "ent",
            "Troll of Khazad-dum": "troll",
            "Troll of Khazad-dûm": "troll",
            "Troll of Khazad-dÃ»m": "troll",
        },
        "target_creatures": 41,
        "checks": [
            ({"forest/grant/swamp": 1, "ent": 1, "creature": 1}, {}),
            ({"forest/grant": 1, "sagu": 1, "creature": 1}, {}),
            ({"forest/grant": 1, "troll": 1, "creature": 1}, {}),
            ({"petal": 1, "ent/sagu": 2, "creature": 1}, {}),
            ({"petal": 1, "ent/sagu": 1, "troll": 1, "creature": 1}, {}),
            ({"petal": 1, "gatecreeper": 1, "forest/grant/swamp": 1, "creature": 1}, {}),
        ],
        "check_names": [
            "Land + Ent",
            "Land + Sagu",
            "Land + Troll",
            "Petal + Double Payoff",
            "Petal + Troll",
            "Petal + Gatecreeper",
        ],
    }
}