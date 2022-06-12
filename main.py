# AAA yourself!
import json
from knowledge.Algorythm import apply_rules
from knowledge.Database import load_knowledge_base


test = {
    'facts': [
        ['Human', 'isa', 'Mortal'],
        ['Socrat', 'isa', 'Human'],
    ],
    'rules': [
        {
            'patterns': [
                ['$A', 'isa', '$B'],
                ['$B', 'isa', '$C'],
            ],
            'conclusions': [
                ['$A', 'isa', '$C']
            ]
        }
    ]
}


def dump_facts(facts, tag=""):
    print(f"Facts {tag}:")
    for fact in facts:
        print('  ' + ' '.join(fact))


def main():
    database = load_knowledge_base("content/char_arthur.txt")

    print(f"First:\n{test}")
    print(f"Second:\n{database}\n")

    dump_facts(test['facts'], "before")
    apply_rules(test['facts'], test['rules'])
    dump_facts(test['facts'], "after")


if __name__ == '__main__':
    main()
