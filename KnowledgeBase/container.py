# Knowledge container

class Rule:
    def __init__(self):
        self._patterns = []
        self._conclusions = []
        self._exclusions = []
        self._symbols = []

    @property
    def patterns(self):
        return self._patterns

    @property
    def conclusions(self):
        return self._conclusions

    @property
    def exclusions(self):
        return self._exclusions

    @property
    def symbols(self):
        return self._symbols

    def update_symbols(self):
        self._symbols.clear()
        for pattern in self._patterns:
            for token in pattern:
                if not token.startswith('$'):
                    self._symbols.append(token)
    # End of Rule


class Container:
    def __init__(self, name, facts: list = None, rules: list = None):
        self._name = name
        self._terms = dict()
        self._facts = set()
        self._rules = []
        if facts:
            self.add_all(facts)
        if rules:
            self._rules.extend(rules)

    @property
    def name(self):
        return self._name

    @property
    def facts(self):
        return self._facts

    @property
    def rules(self):
        return self._rules

    @property
    def terms(self):
        return self._terms

    def get_term(self, term):
        return self._terms[term]

    def add_all(self, facts):
        for fact in facts:
            self.add(fact)

    def add_container(self, other):
        self.add_all(other.facts)
        self._rules.extend(other.rules)

    def add_rule(self, rule: Rule):
        self._rules.append(rule)

    def add(self, fact):
        if not isinstance(fact, tuple):
            fact = tuple(fact)
        self._facts.add(fact)
        for term in fact:
            if term not in self._terms:
                self._terms[term] = set()
            self._terms[term].add(fact)

    def rem(self, fact):
        if not isinstance(fact, tuple):
            fact = tuple(fact)
        self._facts.remove(fact)
        for term in fact:
            if term not in self._terms:
                continue
            self._terms[term].remove(fact)

    def __str__(self):
        lines = [f'Knowledge \'{self._name}\': {len(self._facts)} facts']
        for fact in self._facts:
            lines.append('  ' + ' '.join(fact))
        return '\n'.join(lines)
# End of Container
