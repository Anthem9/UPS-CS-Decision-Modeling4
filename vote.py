from math import floor
from itertools import permutations
import pandas as pd


class VotersGroup:

    def __init__(self, order, number):
        self.order = list(order)
        self.number = number

    def __str__(self):
        return "Order: {}. Number: {}".format(self.order, self.number)


def MajorityRule(candidates, groups, two_candidates=True):
    if two_candidates:
        if len(candidates) != 2:
            return "Candidates should be TWO!"
    votes = {candidate: 0 for candidate in candidates}
    for group in groups:
        for candidate_order in group.order:
            if candidate_order in candidates:
                # print(group.number)
                votes[candidate_order] += group.number
                break
    votes_order = sorted(votes.items(), key=lambda kv: (kv[1], kv[0]))
    if votes_order:
        return votes_order.pop()
    else:
        return None


def Plurality(candidates, groups):
    return MajorityRule(candidates, groups, two_candidates=False)


def PluralityRunoff(candidates, groups):
    votes = {candidate: 0 for candidate in candidates}
    for group in groups:
        for candidate_order in group.order:
            if candidate_order in candidates:
                votes[candidate_order] += group.number
                break
    votes_order = sorted(votes.items(), key=lambda kv: (kv[1], kv[0]))
    if votes_order:
        most = votes_order.pop()
        if most[1] >= floor(sum(votes.values())/2) + 1:
            # print(most)
            # print(floor(sum(votes.values())/2) + 1)
            return most
        else:
            second_candidates = [most[0], votes_order.pop()[0]]
            # print(second_candidates)
            return MajorityRule(candidates=second_candidates, groups=groups)
    else:
        return None


def CondorcetVoting(candidates, groups):
    win = {candidate: 0 for candidate in candidates}
    compare = [i for i in permutations(candidates, 2)]
    for c in compare:
        winner = MajorityRule(list(c), groups)
        if c[0] == winner[0]:
            win[c[0]] += 1
            if win[c[0]] == len(candidates) -1:
                return c[0]
    return None


def BordaVoting(candidates, groups):
    ranks = {candidate: 0 for candidate in candidates}
    for group in groups:
        for i, candidate_order in enumerate(group.order):
            ranks[candidate_order] += group.number * (i+1)
    ranks_order = sorted(ranks.items(), key=lambda kv: (kv[1], kv[0]))
    if ranks_order:
        return ranks_order.pop(0)
    else:
        return None


if __name__ == "__main__":

    data = pd.read_csv("example.csv", index_col=0).to_dict()

    groups = [VotersGroup(data[group]['order'], int(data[group]['number'])) for group in data]

    candidates = ['c', 'b', 'a', 'd']

    print(MajorityRule(candidates=['a', 'b'], groups=groups))
    print(Plurality(candidates=candidates, groups=groups))
    print(PluralityRunoff(candidates=candidates, groups=groups))
    print(CondorcetVoting(candidates=candidates, groups=groups))
    print(BordaVoting(candidates=candidates, groups=groups))
