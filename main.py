from profiles import PROFILES
from analyzers import analyze
from deck_parser import parse_deck
from deck_builder import build_deck, make_variant, compile_profile_checks
from math import comb

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#SETTINGS BEGIN
PASTE_DECK = False #False or True
METHOD = "exact" #"exact" or "simulation"
TRIALS = 1_000_000 #any number, low end PC's should set to 100_000
ACTIVE_PROFILE = "spy_combo" #change profile to use, currently no others implemented,
                            #if you have added your own, change here
HAND_SIZE = 8 #Opening hand size
#SETTINGS END
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

profile = PROFILES[ACTIVE_PROFILE]

def cat(name):
    return profile["categories"][name]

names = profile["check_names"]
compiled_checks = compile_profile_checks(profile, cat)

manual_decks = [
    #make_variant("Wall Combo", {}, profile, cat)
    #make_variant("4 lands, 0 petal", {"forest": 3, "swamp": 1, "petal": 0}, profile, cat),
    make_variant("4 lands, 1 petal, 0 troll", {"forest": 3, "swamp": 1, "petal": 1, "troll": 0}, profile, cat),
    #make_variant("4 lands, 2 petal", {"forest": 3, "swamp": 1, "petal": 2}, profile, cat),
    #make_variant("4 lands, 1 petal, 1 troll", {"forest": 3, "swamp": 1, "petal": 1, "troll": 1}, profile, cat),
    #make_variant("4 lands, 3 petal", {"forest": 3, "swamp": 1, "petal": 3}, profile, cat),
    #make_variant("4 lands, 4 petal", {"forest": 3, "swamp": 1, "petal": 4}, profile, cat),
    #make_variant("5 lands, 0 petal", {"forest": 4, "swamp": 1, "petal": 0}, profile, cat),
    #make_variant("5 lands, 1 petal", {"forest": 4, "swamp": 1, "petal": 1}, profile, cat),
    #make_variant("5 lands, 2 petal", {"forest": 4, "swamp": 1, "petal": 2}, profile, cat),
    #make_variant("5 lands, 3 petal", {"forest": 4, "swamp": 1, "petal": 3}, profile, cat),
    #make_variant("5 lands, 4 petal", {"forest": 4, "swamp": 1, "petal": 4}, profile, cat),
]

def analyze_deck(name, deck):
    keep_rate, mull, keep_reasons = analyze(deck, compiled_checks, METHOD, TRIALS, HAND_SIZE)

    print(f"\n{name}")
    print(f"Keep: {keep_rate:.4%}")
    print(f"Mulligan: {mull:.4f}")

    total_keeps = keep_rate * (TRIALS if METHOD == "simulation" else comb(len(deck), HAND_SIZE))

    for reason, amount in zip(names, keep_reasons):
        print(f"{reason:<25}: {amount / total_keeps:.2%} of keeps")

if PASTE_DECK:
    print("Paste your decklist.")
    print("Type END when finished.\n")

    lines = []

    while True:
        line = input()
        if line == "END":
            break
        lines.append(line)

    main, sideboard = parse_deck("\n".join(lines), profile, cat)
    analyze_deck(profile["title"], main)

else:
    for name, deck in manual_decks:
        analyze_deck(name, deck)