import os

import tabulate

from UndefinedSymbol import UndefinedSymbol, StatementNotExists
from State import State
from settings import tokens, other


class Automata:
    def __init__(self, filename):
        self.line = ''
        self.char_num = 0
        self.line_num = 0
        self.lexeme = ''
        self.filename = filename
        self.state = State().get_initial()
        self.symbol_table = []
        self.ident_table = []
        self.const_table = []
        self.label_table = []

    def process(self):
        with open(self.filename) as file:
            for line in file:
                self.line_num += 1
                self.line = line
                for char_i, char in enumerate(line):
                    self.char_num = char_i + 1
                    try:
                        self.get_tokens(char)
                    except:
                        raise UndefinedSymbol(os.path.abspath(self.filename), self.line_num, char_i + 1, char, line)
                    else:
                        print('*** Лексичний аналіз завершено успішно')
            self.get_tokens('\n')

    def get_tokens(self, char: str):
        if not isinstance(char, str):
            raise TypeError(f'char must be str type\n\tgot {type(char)}')
        next_state = self.state.get_next(char)
        if next_state is not None:
            if not next_state.initial:
                self.lexeme += char
            self.state = next_state
        else:
            if self.state.final:
                if self.lexeme != '':
                    self.identify()
                self.lexeme = ''
                self.state = State().get_initial()
                self.get_tokens(char)
            else:
                raise StatementNotExists(os.path.abspath(self.filename), self.line_num, self.char_num, char, self.line, self.state.get_all_next())

    def identify(self):
        if self.lexeme in tokens:
            token = tokens[self.lexeme]
        else:
            if self.state.next_state in other:
                token = other[self.state.next_state]
            else:
                token = ''
        self.symbol_table.append({
            'line': self.line_num,
            'lexeme': self.lexeme,
            'token': token,
            'index': self.get_index(token)
        })

    def get_index(self, token: str) -> int or None:
        if not isinstance(token, str):
            raise TypeError(f'token must be str type\n\tgot {type(token)}')
        if token == 'ident':
            self.ident_table.append({
                'line': self.line_num,
                'lexeme': self.lexeme,
                'token': token
            })
            return len(self.ident_table)
        if token in ('real', 'int', 'bool'):
            self.const_table.append({
                'line': self.line_num,
                'lexeme': self.lexeme,
                'token': token
            })
            return len(self.const_table)
        if token == 'label':
            self.label_table.append({
                'line': self.line_num,
                'lexeme': self.lexeme,
                'token': token
            })
            return len(self.const_table)
        return None

    def fancy_symbol_table(self):
        if self.symbol_table:
            print('--- Таблиця символів')
            header = self.symbol_table[0].keys()
            rows = [x.values() for x in self.symbol_table]
            print(tabulate.tabulate(rows, header))
        else:
            print('*** Символів не знайдено ***')

    def fancy_ident_table(self):
        if self.ident_table:
            print('--- Таблиця ідентифікаторів')
            header = self.ident_table[0].keys()
            rows = [x.values() for x in self.ident_table]
            print(tabulate.tabulate(rows, header))
        else:
            print('*** Ідентифікаторів не знайдено ***')

    def fancy_const_table(self):
        if self.const_table:
            print('--- Таблиця констант')
            header = self.const_table[0].keys()
            rows = [x.values() for x in self.const_table]
            print(tabulate.tabulate(rows, header))
        else:
            print('*** Констант не знайдено ***')

    def fancy_label_table(self):
        if self.label_table:
            print('--- Таблиця міток')
            header = self.label_table[0].keys()
            rows = [x.values() for x in self.label_table]
            print(tabulate.tabulate(rows, header))
        else:
            print('*** Міток не знайдено ***')

    @property
    def symbol_table(self):
        return self._symbol_table

    @symbol_table.setter
    def symbol_table(self, value):
        if not isinstance(value, list):
            raise TypeError(f'symbol_table must be list type\n\tgot {type(list)}')
        self._symbol_table = value

    @property
    def ident_table(self):
        return self._ident_table

    @ident_table.setter
    def ident_table(self, value):
        if not isinstance(value, list):
            raise TypeError(f'ident_table must be list type\n\tgot {type(value)}')
        self._ident_table = value

    @property
    def const_table(self):
        return self._const_table

    @const_table.setter
    def const_table(self, value):
        if not isinstance(value, list):
            raise TypeError(f'symbol_table must be list type\n\tgot {type(value)}')
        self._const_table = value

    @property
    def label_table(self):
        return self._label_table

    @label_table.setter
    def label_table(self, value):
        if not isinstance(value, list):
            raise TypeError(f'label_table must be list type\n\tgot {type(value)}')
        self._label_table = value
