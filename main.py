# AAA yourself!

test = {
    'facts': [
        ['isa', 'Human', 'Mortal'],
        ['isa', 'Socrat', 'Human'],
    ],
    'rules': [
        {
            'patterns': [
                ['isa', '$A', '$B'],
                ['isa', '$B', '$C'],
            ],
            'proposition': [
                ['isa', '$A', '$C']
            ]
        }
    ]
}


def ApplicateRules(facts: list, rules):
    new_facts = []
    for rule in rules:
        ApplyRule(facts, rule, new_facts)
    facts.extend(new_facts)


def ApplyRule(facts: list, rule, new_facts: list):
    stack = []
    for pattern in rule['patterns']:
        stack.append(MatchIterator(facts, pattern))
    l = len(stack)
    matches = []
    for i in range(l):
        m = next(stack[i])
        if m is None:
            return
        matches.append(m)
    work = True
    while work:
        values = TryCollapseDicts(matches)

        if values:
            for prop in rule['proposition']:
                mew_fact = BindValues(prop, values)
                new_facts.append(mew_fact)

        signal = True
        for i in range(l):
            if not signal:
                break
            matches[i] = next(stack[i])
            if matches[i] is None:
                signal = True
                stack[i] = MatchIterator(facts, rule['patterns'][i])
            else:
                signal = False
            if i == l-1:
                work = False


def TryCollapseDicts(dicts):
    keys = set()
    for d in dicts:
        keys |= d.keys()
    result = dict()
    for d in dicts:
        for k in keys:
            if k not in d:
                continue
            if k not in result:
                result[k] = d[k]
                continue
            if result[k] != d[k]:
                return None
    return result


def BindValues(pattern, values):
    l = len(pattern)
    result = [None] * l
    for i in range(l):
        p = pattern[i]
        result[i] = values[p] if p[0] == '$' else p
    return result


def MatchIterator(facts, pattern):
    for fact in facts:
        m = Match(fact, pattern)
        if m is None:
            continue
        yield m
    yield None


def Match(fact, pattern):
    if len(fact) != len(pattern):
        return None
    values = dict()
    for f, p in zip(fact, pattern):
        if f == p:
            continue
        if p[0] == '$':
            values[p] = f
            continue
        if f != p:
            return None
    return values


def main():
    print(test)
    ApplicateRules(test['facts'], test['rules'])
    print(test)


if __name__ == '__main__':
    main()
