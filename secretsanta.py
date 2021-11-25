import os
import random

import qrcode


def parseInput(path):
    with open(path) as f:
        participants = f.read().strip('\n"')
    couplesDict = {}
    santas = []
    for p in participants.split('","'):
        split = p.split(", ")
        if len(split) == 2:
            p0, p1 = split[0], split[1]
            couplesDict[p0] = p1
            couplesDict[p1] = p0
        santas += split
    return (santas, couplesDict)


def hohoho(santas, couplesDict):
    results = {}
    selected = []
    random.shuffle(santas)
    for santa in santas:
        toSubtract = selected.copy()
        toSubtract.append(santa)
        partner = couplesDict.get(santa)
        if partner is not None:
            toSubtract.append(partner)
        pool = list(set(santas) - set(toSubtract))
        random.shuffle(pool)
        picked = False
        while not picked:
            if len(pool) == 0:
                return hohoho(santas, couplesDict)
            recipient = random.choice(pool)
            results[santa] = recipient
            selected.append(recipient)
            picked = True
    return results


def secretSanta(santas, couplesDict):
    if not os.path.exists("codes"):
        os.mkdir("codes")
    for (santa, recipient) in hohoho(santas, couplesDict).items():
        img = qrcode.make(recipient)
        img.save(f"./codes/{santa}.png")


def main():
    santas, couplesDict = parseInput("./participants.csv")
    secretSanta(santas, couplesDict)


if __name__ == "__main__":
    main()
