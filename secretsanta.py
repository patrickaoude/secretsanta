import os
import csv
import random

import networkx as nx
import qrcode


def parseInput(path):
    blacklistDict = {}
    with open(path) as f:
        groups = csv.reader(f)
        # remove leading & trailing white space from names
        groups = [[n.strip() for n in g] for g in groups]
        # create blacklist for all names on same line
        blacklistDict = {n: g for g in groups for n in g}

    participants = blacklistDict.keys()
    # use blacklists to find all possible recipients
    candidatesDict = {
        p: list(set(participants) - set(blacklistDict[p])) for p in participants
    }

    return candidatesDict


def makeAssignments(candidatesDict):
    santaPrefix = "santa_"  # append to names for santa nodes
    names = sorted(set(candidatesDict.keys()))
    santas = [f"{santaPrefix}{n}" for n in names]
    edges = [(n, c) for n, cands in candidatesDict.items() for c in cands]
    random.shuffle(edges)

    # build a graph of names (duplicated for santas/recipients)
    G = nx.Graph()
    G.add_nodes_from(santas, bipartite=0)
    G.add_nodes_from(names, bipartite=1)

    # add edges for allowed pairings (santa -> recipient)
    for n, c in edges:
        G.add_edge(f"{santaPrefix}{n}", c)

    # find maximum matching
    matches = nx.algorithms.bipartite.matching.hopcroft_karp_matching(
        G, top_nodes=santas
    )

    # extract matches
    assignments = {
        santa[len(santaPrefix) :]: recipient
        for santa, recipient in matches.items()
        if santa.startswith(santaPrefix)
    }
    santas = list(assignments.keys())
    recipients = list(assignments.values())

    # assert matches aren't malformed
    if len(assignments) != len(names):
        from pprint import pprint

        pprint(assignments)
        raise AssertionError("Malformed assignments detected")
    if sorted(set(santas)) != names:
        print(santas)
        raise AssertionError("Malformed santas detected")
    if sorted(set(recipients)) != names:
        print(recipients)
        raise AssertionError("Malformed recipients detected")
    for n in names:
        a = assignments[n]
        c = candidatesDict[n]
        if a not in c:
            print(f"{n}: {a}")
            print(f"candidates: {c}")
            raise AssertionError(
                "Assigned recipient not in list of permitted candidates"
            )

    return assignments


def main():
    candidatesDict = parseInput("./participants.csv")
    assignments = makeAssignments(candidatesDict)

    if not os.path.exists("codes"):
        os.mkdir("codes")

    for santa, recipient in assignments.items():
        img = qrcode.make(recipient)
        img.save(f"./codes/{santa}.png")


if __name__ == "__main__":
    main()
