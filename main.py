# AAA yourself!
from KnowledgeBase.Algorythm import apply_rules
from KnowledgeBase.Loader import load


def main():
    database = load("content/char_arthur.txt")

    print(f"Before:\n{str(database)}\n")

    i = 100
    while i > 0:
        i -= 1
        changes = apply_rules(database)
        if changes == 0:
            break

    print(f"After {100 - i}:\n{str(database)}\n")
    # print(f"\n\n")
    # dump_facts(test['facts'], "before")
    # apply_rules(test['facts'], test['rules'])
    # dump_facts(test['facts'], "after")
    #
    # print(f"\n\n")
    # dump_facts(database['facts'], "before")
    # i = 100
    # while i > 0:
    #     i -= 1
    #     if 0 == apply_rules(database['facts'], database['rules']):
    #         break
    #     dump_facts(database['facts'], f"inner {i}")
    # print(f"Steps: {i}")
    # dump_facts(database['facts'], "after")


if __name__ == '__main__':
    main()
