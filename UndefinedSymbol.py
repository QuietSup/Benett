from settings import classes


class UndefinedSymbol(Exception):
    def __init__(self, filepath, line_num, char_num, char, line):
        message = f'\n"{filepath}",\n' \
                  f'стрічка: {line_num}, символ: {char_num}\n' \
                  f'\t***Cимвол {repr(char)} не визначений:\n'
        pointer = ' ' * (char_num - 1) + '^'
        message += line + ('\n' if '\n' not in line else '') + pointer

        super().__init__(message)


class StatementNotExists(Exception):
    def __init__(self, filepath, line_num, char_num, char, line, all_next: list):
        message = f'\n"{filepath}",\n' \
                  f'стрічка: {line_num}, символ: {char_num}\n' \
                  f'***Невизначений вираз\n' \
                  f'\tнеочікуваний символ {repr(char)}:\n'
        pointer = ' ' * (char_num - 1) + '^'
        message += line + ('\n' if '\n' not in line else '') + pointer
        if all_next:
            message += '\nочікується один із наступних:\n'
            for item in all_next:
                chars = [i for i in classes if classes[i] == item.char_class]
                if chars:
                    message += '\t'
                    for char in chars[0]:
                        message += f'{repr(char)} '
                    message += '\n'

        super().__init__(message)
