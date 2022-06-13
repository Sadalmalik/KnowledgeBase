# AAA yourself!
from KnowledgeBase.Algorythm import apply_rules
from KnowledgeBase.Loader import load


def main():
    database = load("content/char_arthur.txt")

    print(f"Before:\n{str(database)}\n")

    i = 0
    while i < 100:
        i += 1
        changes = apply_rules(database)
        if changes == 0:
            break

    print(f"After {i}:\n{str(database)}\n")


if __name__ == '__main__':
    main()
