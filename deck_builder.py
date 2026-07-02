from analyzers import compile_check

def build_deck(deck_definition, cat, size=60): #Creates deck tuple from profile deck definition
    deck = []
    for category_name, amount in deck_definition.items():
        deck.extend([cat(category_name)] * amount)
    if len(deck) > size:
        raise ValueError(f"Deck has {len(deck)} cards, but size is only {size}.")
    deck.extend([cat("filler")] * (size - len(deck)))
    return tuple(deck)

def make_variant(name, changes, profile, cat, size=60): #Copies over testdeck, replaces with new imported
    #quantities, and rebuilds
    deck_def = profile["base_deck"].copy()

    for category_name, new_amount in changes.items():
        deck_def[category_name] = new_amount

    return name, build_deck(deck_def, cat, size)

def parse_check_key(key, cat): #Reads tuples of cards in check, allows "ent"/"grant"/"troll" to
    #function as an "or"
    parts = key.split("/")
    ids = tuple(cat(part) for part in parts)
    if len(ids) == 1:
        return ids[0]
    return ids

def compile_profile_checks(profile, cat): #Converts typed profiles into more efficient system to
    #evaluate. Allows user to input strings in profiles instead of ID numbers
    converted_checks = []
    for minimums, maximums in profile["checks"]:
        converted_minimums = {}
        converted_maximums = {}
        for key, amount in minimums.items():
            converted_minimums[parse_check_key(key, cat)] = amount
        for key, amount in maximums.items():
            converted_maximums[parse_check_key(key, cat)] = amount
        converted_checks.append(
            compile_check((converted_minimums, converted_maximums))
        )
    return converted_checks