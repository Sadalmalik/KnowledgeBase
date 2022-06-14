# AAA yourself!
from KnowledgeBase.Algorythm import complete_apply
from KnowledgeBase.Loader import load


def main():
    database = load("content/char_arthur.txt")

    print(f"Before:\n{str(database)}\n")
    complete_apply(database)
    print(f"After:\n{str(database)}\n")


if __name__ == '__main__':
    main()
