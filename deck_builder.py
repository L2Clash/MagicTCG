from analyzers import compile_check

def build_deck(deck_definition, cat, deck_size): #Creates deck tuple from profile deck definition
    deck = []
    for category_name, amount in deck_definition.items():
        deck.extend([cat(category_name)] * amount)
    if len(deck) > deck_size:
        raise ValueError(f"Deck has {len(deck)} cards, but size is only {deck_size}.")
    deck.extend([cat("filler")] * (deck_size - len(deck)))
    return tuple(deck)

def make_variant(name, changes, profile, cat, deck_size): #Copies over testdeck, replaces with new imported
    #quantities, and rebuilds
    deck_def = profile["base_deck"].copy()

    for category_name, new_amount in changes.items():
        deck_def[category_name] = new_amount

    return name, build_deck(deck_def, cat, deck_size)

def parse_group(group, cat):
    parts = group.split("/")
    ids = tuple(cat(part) for part in parts)

    if len(ids) == 1:
        return ids[0]

    return ids


def parse_check_key(key, cat):
    if key.startswith("distinct:"):
        _, required, group = key.split(":", 2)

        return (
            "distinct",
            parse_group(required, cat),
            parse_group(group, cat),
        )

    return parse_group(key, cat)

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