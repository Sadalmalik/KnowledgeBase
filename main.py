from KnowledgeBase.algorythm import evaluate_rules
from KnowledgeBase.loader import load


def main():
    database = load("content/char_arthur.txt")

    print(f"Before:\n{str(database)}\n")
    evaluate_rules(database)
    print(f"After:\n{str(database)}\n")


if __name__ == '__main__':
    main()
