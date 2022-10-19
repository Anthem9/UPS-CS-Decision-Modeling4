from random import randint
from itertools import permutations
import vote
import pandas as pd


def generating_preferences():
    total_number = 0
    while not (40 < total_number < 100):
        groups_number = [randint(1, 15) for i in range(6)]
        total_number = sum(groups_number)

    groups_order_all = [i for i in permutations("abcdef", 6)]
    best_percentage = 1
    while best_percentage > 0.7:
        groups_order = ["".join(list(groups_order_all[randint(0, 719)])) for i in range(6)]

        best = {candidate: 0 for candidate in "abcdef"}
        for number, order in zip(groups_number, groups_order):
            best[order[0]] += number

        best_order = sorted(best.items(), key=lambda kv: (kv[1], kv[0]))
        highest = best_order.pop()[1]
        best_percentage = highest / total_number

    return [(number, order) for number, order in zip(groups_number, groups_order)], total_number, best_percentage


if __name__ == "__main__":
    candidates = "".join("abcdef")
    groups_name = ["group_{}".format(i) for i in range(6)]
    while True:
        preferences, total_number, best_percentage = generating_preferences()
        groups = [vote.VotersGroup(order, number) for (number, order) in preferences]
        Plurality_winner = vote.Plurality(candidates=candidates, groups=groups)
        PluralityRunoff_winner = vote.PluralityRunoff(candidates=candidates, groups=groups)
        CondorcetVoting_winner = vote.CondorcetVoting(candidates=candidates, groups=groups)
        BordaVoting_winner = vote.BordaVoting(candidates=candidates, groups=groups)
        if CondorcetVoting_winner is None:
            continue
        if Plurality_winner[0] == PluralityRunoff_winner[0] == CondorcetVoting_winner[0] == BordaVoting_winner[0]:
            break

    print("For Question 6:")
    print("We have 6 groups with preferences:")
    for group in groups:
        print(group)
    print("There are {} voter in total.".format(total_number))
    print("There is at most {:.2f}% of voters has the same “best candidate”.".format(best_percentage*100))
    print("In four different vote rules, the same winner is {}.".format(Plurality_winner[0]))

    result = {group_name: {'number': number, 'order': order} for (number, order), group_name, in
              zip(preferences, groups_name)}
    pd.DataFrame(result).to_csv("Q6.csv")
    print()

    while True:
        preferences, total_number, best_percentage = generating_preferences()
        groups = [vote.VotersGroup(order, number) for (number, order) in preferences]
        Plurality_winner = vote.Plurality(candidates=candidates, groups=groups)
        PluralityRunoff_winner = vote.PluralityRunoff(candidates=candidates, groups=groups)
        CondorcetVoting_winner = vote.CondorcetVoting(candidates=candidates, groups=groups)
        BordaVoting_winner = vote.BordaVoting(candidates=candidates, groups=groups)
        if CondorcetVoting_winner is None:
            continue
        all_different = Plurality_winner[0] != PluralityRunoff_winner[0] \
                    and Plurality_winner[0] != CondorcetVoting_winner[0] \
                    and Plurality_winner[0] != BordaVoting_winner[0] \
                    and PluralityRunoff_winner[0] != CondorcetVoting_winner[0] \
                    and PluralityRunoff_winner[0] != BordaVoting_winner[0] \
                    and CondorcetVoting_winner[0] != BordaVoting_winner[0]
        if all_different:
            break

    print("For Question 7:")
    print("We have 6 groups with preferences:")
    for group in groups:
        print(group)
    print("There are {} voter in total.".format(total_number))
    print("There is at most {:.2f}% of voters has the same “best candidate”.".format(best_percentage*100))
    print("In four different vote rules:")
    print("{} is Plurality winner.".format(Plurality_winner[0]))
    print("{} is PluralityRunoff winner.".format(PluralityRunoff_winner[0]))
    print("{} is CondorcetVoting winner.".format(CondorcetVoting_winner[0]))
    print("{} is BordaVoting winner.".format(BordaVoting_winner[0]))
    result = {group_name: {'number': number, 'order': order} for (number, order), group_name, in
              zip(preferences, groups_name)}
    pd.DataFrame(result).to_csv("Q7.csv")

