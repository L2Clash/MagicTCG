def parse_deck(text, profile, cat, DECK_SIZE): #Analyzes pasted decklist into maindeck and sideboard, assigning to 
    #categories provided. Sideboard analysis not implemented yet
    main = []
    sideboard = []
    creature_count = 0
    in_sideboard = False

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.lower().replace(":", "") == "sideboard":
            in_sideboard = True
            continue
        parts = line.split(" ", 1)
        if len(parts) != 2:
            print(f"Skipping invalid line: {line}")
            continue
        amount, name = parts
        amount = int(amount)
        target = sideboard if in_sideboard else main
        if name in profile["special_cards"]:
            category_name = profile["special_cards"][name]
            category_id = cat(category_name)
            target.extend([category_id] * amount)
            if not in_sideboard and category_name in profile["creature_categories"]:
                creature_count += amount
        else:
            if not in_sideboard:
                remaining = max(0, profile["target_creatures"] - creature_count)
                as_creatures = min(amount, remaining)
                as_filler = amount - as_creatures
                target.extend([cat("creature")] * as_creatures)
                target.extend([cat("filler")] * as_filler)
                creature_count += as_creatures
            else:
                target.extend([cat("filler")] * amount)

    if len(main) != DECK_SIZE:
        raise ValueError(f"Main deck has {len(main)} cards, expected {DECK_SIZE}.")
    if sideboard and len(sideboard) != 15:
        raise ValueError(f"Sideboard has {len(sideboard)} cards, expected 15.")
    return tuple(main), tuple(sideboard)