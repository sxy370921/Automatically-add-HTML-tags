def lines(file):
    for line in file:
        yield line
    yield '\n'


def blocks(file):
    block = []
    for line in lines(file):
        if line.strip():  # strip会去掉最后的\n
            block.append(line)   # 如果有内容就加到列表内
        elif block:
            yield ''.join(block).strip()
            block = []
