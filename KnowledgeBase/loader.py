# Knowledge loader
import os

from .container import Container, Rule


def file_reader(filename):
    with open(filename, encoding="utf8") as file:
        for index, line in enumerate(file):
            line = line.strip()
            if len(line) == 0:
                continue
            if line.startswith('#'):
                continue
            fact = line.split()
            yield index, line, fact
        yield None, None, None


def read_until(reader, stop_tokens):
    content = []
    while True:
        index, line, fact = next(reader)
        if index is None:
            raise Exception("Unexpected end of file!")
        if fact[0] in stop_tokens:
            break
        if line.startswith('!'):
            raise Exception(f"Unexpected command {line} at line {index}")
        content.append(fact)
    return content, fact[0]


def load(filename):
    reader = file_reader(filename)
    container = Container(os.path.basename(filename))
    while True:
        index, line, fact = next(reader)
        if index is None:
            break

        if not line.startswith('!'):
            container.add(fact)
            continue

        if fact[0] == '!include':
            folder = os.path.dirname(filename)
            new_path = os.path.join(folder, fact[1] + '.txt')
            other_container = load(new_path)
            container.add_container(other_container)
            continue

        if fact[0] == '!rule':
            rule = Rule()
            patterns, token = read_until(reader, ['!conclusion', '!exclusion'])
            rule.patterns.extend(patterns)
            if token == '!conclusion':
                conclusions, token = read_until(reader, ['!exclusion', '!rule-end'])
                rule.conclusions.extend(conclusions)
            if token == '!exclusion':
                exclusions, token = read_until(reader, ['!rule-end'])
                rule.exclusions.extend(exclusions)
            rule.update_terms()
            container.add_rule(rule)
            continue

        if fact[0] == '!behaviour':
            print(f"Command !behaviour not implemented at line {index}")
            continue

        raise Exception(f"Unknown command {line} at line {index}")

    return container
