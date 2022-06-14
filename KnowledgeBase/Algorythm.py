# Knowledge thinking

from .Combinator import combinator
from .Container import Container, Rule


def complete_apply(container: Container, limit=100):
    while True:
        limit -= 1
        changes = apply_rules(container)
        if changes == 0:
            break
        if limit == 0:
            break


def apply_rules(container: Container):
    add_facts = set()
    rem_facts = set()
    # Apply all  rules
    for rule in container.rules:
        add, rem = apply_rule(container, rule)
        add_facts = add_facts.union(add)
        rem_facts = rem_facts.union(rem)
    # Add new facts
    add_count = len(container.facts)
    for fact in add_facts:
        container.add(fact)
    # Remove old facts
    rem_count = len(container.facts)
    for fact in rem_facts:
        container.rem(fact)
    last_count = len(container.facts)
    # Return amount of changes
    return (rem_count - add_count) + (rem_count - last_count)


def apply_rule(container: Container, rule: Rule):
    # Getting facts slice
    facts = set()
    add_facts = set()
    rem_facts = set()
    for term in rule.terms:
        facts = facts.union(container.terms[term])

    # Memoization of matches for performance
    size = len(rule.patterns)
    matches_memo = [None] * size
    for i in range(size):
        matches_memo[i] = list(match_iterator(facts, rule.patterns[i]))

    # Iterate patterns combinations
    def iterator(idx):
        m = matches_memo[idx]
        for value in m:
            yield value

    # Iterate all matches combinations
    for matches in combinator(size, iterator):
        values = try_collapse_dicts(matches)
        if not values:
            continue

        # If combination is valid - add conclusions and exclusions
        for inc in rule.conclusions:
            add_facts.add(bind_values(inc, values))
        for exc in rule.exclusions:
            rem_facts.add(bind_values(exc, values))

    return add_facts, rem_facts


def try_collapse_dicts(dicts):
    """Объединяет все словари в один при условии что у одинаковых ключей в разных словарях одинаковые значения"""
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


def bind_values(pattern, values):
    """Создаёт на основе паттерна объект-значение, заменяя все переменные в паттерне значениями"""
    l = len(pattern)
    result = [None] * l
    for i in range(l):
        p = pattern[i]
        result[i] = values[p] if p[0] == '$' else p
    return tuple(result)


def match_iterator(facts, pattern):
    """Поочередно находит все совпадающие с паттерном факты"""
    for fact in facts:
        m = match(fact, pattern)
        if m is None:
            continue
        yield m
    yield None


def match(fact, pattern):
    """Находит совпадение факта с паттерном"""
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