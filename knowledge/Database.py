import os


def load_knowledge_base(filename):
    facts = []
    rules = []
    rule_mode = None
    active_rule = None
    with open(filename) as file:
        index = 0
        for line in file:
            index += 1
            line = line.strip()
            if len(line) == 0:
                continue
            if line.startswith('#'):
                continue
            tokens = line.split(' ')
            if tokens[0].startswith('!'):
                if tokens[0] == '!include':
                    if rule_mode is not None:
                        print(f'Wrong command {tokens[0]} - can\'t be inside rule! Try skip line!')
                        continue
                    folder = os.path.dirname(filename)
                    new_path = os.path.join(folder, tokens[1] + '.txt')
                    kb = load_knowledge_base(new_path)
                    facts.extend(kb['facts'])
                    rules.extend(kb['rules'])
                    continue
                elif tokens[0] == '!rule':
                    if rule_mode is not None:
                        print(f'Wrong command {tokens[0]} - can\'t be inside rule! Try skip line!')
                        continue
                    rule_mode = 'patterns'
                    active_rule = {
                        'patterns': [],
                        'conclusions': []
                    }
                    continue
                elif tokens[0] == '!conclusion':
                    if rule_mode != 'patterns':
                        print(f'Wrong command {tokens[0]} - can\'t be used twise inside rule! Try skip line!')
                        continue
                    rule_mode = 'conclusions'
                    continue
                elif tokens[0] == '!rule-end':
                    if rule_mode != 'conclusions':
                        print(
                            f'Wrong command {tokens[0]} - can\'t be used end rule without conclusions! Try skip line!')
                        continue
                    rules.append(active_rule)
                    rule_mode = None
                    continue
                else:
                    print(f'Unknown command {tokens[0]} in line {index} will be skipped!')
                    continue
            if rule_mode == 'patterns':
                active_rule['patterns'].append(tokens)
            elif rule_mode == 'conclusions':
                active_rule['conclusions'].append(tokens)
            else:
                facts.append(tokens)
    return {
        'facts': facts,
        'rules': rules
    }
