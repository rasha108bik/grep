import argparse
import sys
import re

def output(line):
    print(line)

def Index(pattern, lines, b_context, context, a_context):
    index = []
    new_index = []

    for n, line in enumerate(lines):
        find = re.search(pattern, line)
        if find:
            index.append(n)

    if b_context > 0:
        count = b_context
        for x in index:
            for j in range(count + 1):
                y = x - (count - j)
                if not y in new_index:
                    new_index.append(y)

    if a_context > 0:
        count = a_context
        for x in index:
            for j in range(count + 1):
                y = x + j
                if y < len(lines) and not y in new_index:
                    new_index.append(y)

    if context > 0:
        count = context
        for x in index:
            for j in range(count + 1):
                y = x - (count - j)
                if not y in new_index:
                    new_index.append(y)
            for j in range(count + 1):
                y = x + j
                if y < len(lines) and not y in new_index:
                    new_index.append(y)

    return new_index


def compare(pattern, line, case, invert):
    flag = re.IGNORECASE if case else 0
    match = bool(re.search(pattern, line, flag))
    if invert:
        match = not match
    return match


def count(lines, params):
    a = 0
    for line in lines:
        line = line.rstrip()
        if compare(params.pattern, line, params.ignore_case, params.invert):
            a += 1
    output('{}'.format(a))


def grep(lines, params):
    params.pattern = params.pattern.replace('?', '.').replace('*','.*?')

    if params.count:
        count(lines, params)


    else:
        if params.context or params.before_context or params.after_context:
                valid_index = Index(params.pattern, lines, params.before_context,
                                    params.context, params.after_context)

        all_context=(params.context or params.before_context or params.after_context)

        buffer = [None] * all_context

        print(buffer)
        after = 0

        for n, line in enumerate(lines):
            line = line.rstrip()

            if compare(params.pattern, line, params.ignore_case, params.invert):
                if params.line_number:
                    output('{}:{}'.format(n + 1, line))
                else:
                    output('{}'.format(line))

            elif params.context or params.before_context or params.after_context:
                    if n in valid_index:
                        if params.before_context or params.context:
                            for ind_buf,line_buf in enumerate(buffer):
                                if params.line_number:
                                    if compare(params.pattern, line, params.ignore_case, params.invert):
                                        line_buf = ('{}:{}'.format(n+1, line))
                                    else:
                                        line_buf = ('{}-{}'.format(n+1, line))

                                    output(line_buf)
                                else:
                                    line_buf = ('{}'.format(line))
                                    output(line_buf)
                                buffer.pop(0)
                            buffer = [None] * all_context
                            after=params.after_context

                        if params.after_context:
                            after -= 1
                            if params.line_number:
                                line = ('{}-{}'.format(n+1, line))
                            output(line)



def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()
