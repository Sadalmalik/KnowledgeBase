from knowledge.Combinator import combinator


def apply_rules(facts: list, rules):
    new_facts = []
    for rule in rules:
        apply_rule(facts, rule, new_facts)
    facts.extend(new_facts)


def apply_rule(facts: list, rule, new_facts: list):
    """Применяет правила к списку фактов и добавляет все вновь созданные факты в отдельный список"""
    patterns = rule['patterns']
    size = len(patterns)

    def iterator(idx):
        return match_iterator(facts, patterns[idx])

    for matches in combinator(size, iterator):
        values = try_collapse_dicts(matches)

        if values:
            for prop in rule['conclusions']:
                mew_fact = bind_values(prop, values)
                new_facts.append(mew_fact)


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
    return result


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