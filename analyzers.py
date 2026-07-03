import random
from collections import Counter
from math import comb
from itertools import product

def compile_check(check): #Turns checks from profiles into lists to compare hands against
    #checks more efficiently, makes easier to manually add checks in the profiles
    minimums, maximums = check
    min_list = []
    max_list = []

    for card, amount in minimums.items():
        min_list.append((card, amount))
    for card, amount in maximums.items():
        max_list.append((card, amount))
    return (min_list, max_list)

def count_group(counts, group):
    if isinstance(group, tuple):
        return sum(counts[c] for c in group)

    return counts[group]


def distinct_requirements(counts, required, group):
    if count_group(counts, required) < 1:
        return False

    # Temporarily consume one card from required.
    if isinstance(required, tuple):
        for card in required:
            if counts[card] > 0:
                counts[card] -= 1
                result = count_group(counts, group) >= 1
                counts[card] += 1
                return result
    else:
        counts[required] -= 1
        result = count_group(counts, group) >= 1
        counts[required] += 1
        return result

    return False

def contains(check, counts): #Returns True if the hand validates any of the checks
    minimums, maximums = check
    for card, amount in minimums:
        if isinstance(card, tuple) and card[0] == "distinct":
            required = card[1]
            group = card[2]
            if not distinct_requirements(counts, required, group):
                return False
        elif isinstance(card, tuple):
            if sum(counts[c] for c in card) < amount:
                return False
        else:
            if counts[card] < amount:
                return False
    for card, amount in maximums:
        if isinstance(card, tuple):
            if sum(counts[c] for c in card) > amount:
                return False
            else:
                if counts[card] > amount:
                    return False
    return True

def exact_sample(deck, compiled_checks, hand_size=7): #Uses hypergeometric distribution to compute
    #every possible hand composition based on the categories provided
    #Often faster than simulation, and gives precise mathematics compared to simulation
    deck_counts = Counter(deck)
    categories = sorted(deck_counts)
    total_hands = comb(len(deck), hand_size)
    keep_hands = 0
    mulligan_hands = 0
    check_hits = [0] * len(compiled_checks)

    ranges = [
        range(min(deck_counts[card], hand_size) + 1)
        for card in categories
    ]

    for values in product(*ranges):
        if sum(values) != hand_size:
            continue

        ways = 1
        counts = [0] * (max(deck) + 1)

        for card, amount in zip(categories, values):
            ways *= comb(deck_counts[card], amount)
            counts[card] = amount

        hand_keep = False

        for i, check in enumerate(compiled_checks):
            if contains(check, counts):
                hand_keep = True
                check_hits[i] += ways

        if hand_keep:
            keep_hands += ways
        else:
            mulligan_hands += ways

    keep_rate = keep_hands / total_hands
    mulligan_rate = mulligan_hands / keep_hands

    return keep_rate, mulligan_rate, check_hits

def sim_sample(deck, compiled_checks, trials): #Monte Carlo simulation, drawing hands
    #from the deck [trials] times, and checking hand against the list of
    #checks for that deck. Slower and less accurate than exact, can later
    #be upgraded to allow simulations of turn and play after
    keep = 0
    mulligan_count = 0
    check_hits = [0] * len(compiled_checks)

    for _ in range(trials):
        hand = random.sample(deck, 7)
        counts = [0] * (max(deck) + 1)

        for card in hand:
            counts[card] += 1

        hand_keep = False

        for i, check in enumerate(compiled_checks):
            if contains(check, counts):
                hand_keep = True
                check_hits[i] += 1

        if hand_keep:
            keep += 1
        else:
            mulligan_count += 1

    keep_rate = keep / trials
    mulligan_rate = mulligan_count / keep

    return keep_rate, mulligan_rate, check_hits

def analyze(deck, compiled_checks, method, trials): #Provides check for which method to analyze
    if method == "simulation":
        return sim_sample(deck, compiled_checks, trials)

    elif method == "exact":
        return exact_sample(deck, compiled_checks)

    else:
        raise ValueError(f"Unknown method '{method}'")