def combinator(size, get_iterator):
    stack = [None] * size
    content = [None] * size

    for i in range(size):
        stack[i] = get_iterator(i)
        content[i] = next(stack[i])

    complete = False
    while not complete:
        yield content

        signal = True
        for k in range(size):
            if not signal:
                break
            content[k] = next(stack[k])
            if content[k] is None:
                signal = True
                stack[k] = get_iterator(k)
                content[k] = next(stack[k])
                if k == size - 1:
                    complete = True
            else:
                signal = False
    # end of while


def test():
    def iterator(idx):
        for t in range(4):
            yield "ABCD"[t]
        yield None

    for x in combinator(3, iterator):
        print("".join(x))


if __name__ == "__main__":
    test()
