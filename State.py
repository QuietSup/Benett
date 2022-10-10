class State:
    def __init__(self, state=0, char_class='', next_state=0, final=False, initial=False):
        self.state = state
        self.char_class = char_class
        self.next_state = next_state
        self.final = final
        self.initial = initial

    def get_next(self, char: str):
        from settings import stf
        if not isinstance(char, str):
            raise TypeError(f'char must be str type\n\tgot {type(char)}')
        for elem in stf:
            if self.next_state == elem.state and (self.get_class(char) or 'other') == elem.char_class:
                return elem

    @staticmethod
    def get_initial():
        from settings import stf
        for elem in stf:
            if elem.initial:
                return elem
        raise ModuleNotFoundError('no initial state found')

    @staticmethod
    def get_class(char):
        if not isinstance(char, str):
            raise TypeError(f'char must be str type\n\tgot {type(char)}')
        from settings import classes
        for key in classes:
            if char in key:
                return classes[key]
        raise Exception(f'class undefined for char {char}')

    def get_all_next(self):
        from settings import stf
        all_next = []
        for elem in stf:
            if self.next_state == elem.state:
                all_next.append(elem)
        return all_next

    # GETTERS
    @property
    def state(self):
        return self.__state

    @property
    def next_state(self):
        return self.__next_state

    @property
    def final(self):
        return self.__final

    @property
    def initial(self):
        return self._initial

    @property
    def char_class(self):
        return self.__char_class

    @state.setter
    def state(self, value):
        if not isinstance(value, int):
            raise TypeError(f'state must be int type\n\tgot {type(value)}')
        self.__state = value

    @next_state.setter
    def next_state(self, value):
        if not isinstance(value, int):
            raise TypeError(f'next_state must be int type\n\tgot {type(value)}')
        self.__next_state = value

    @final.setter
    def final(self, value):
        if not isinstance(value, bool):
            raise TypeError(f'final must be bool type\n\tgot {type(value)}')
        self.__final = value

    @initial.setter
    def initial(self, value):
        if not isinstance(value, int):
            raise TypeError(f'initial must be bool type\n\tgot {type(value)}')
        self._initial = value

    @char_class.setter
    def char_class(self, value):
        if not isinstance(value, str):
            raise TypeError(f'char_class must be str type\n\tgot {type(value)}')
        self.__char_class = value

    def __str__(self):
        out = '  '
        if self.initial:
            out = '▶ '
        if self.final:
            out = out + f'{self.state}--{self.char_class}-->({self.next_state})\n\t'
        else:
            out = out + f'{self.state}--{self.char_class}-->{self.next_state} '
        return out
