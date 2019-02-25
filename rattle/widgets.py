#!/usr/bin/env python3

from abc import ABC, abstractmethod


class Widget(ABC):
    """ The Widget abstract base class. Never to be called directly.

    :param str _id: The widgets' id or name.
    :param callable callback: Callback function which receives the instances'
                              attributes when certain attributes are changed.
    """

    def __init__(self, _id, callback):
        self._id = _id
        self._callback = callback
        self._init_local()
        self._gen_code()

    def __setattr__(self, key, value):
        """ Set the attribute and trigger callback when things are changed
        which may require a new render. """
        self.__dict__[key] = value
        if key[0] != '_':
            self._callback('attr', self._id, key, value)
            self._gen_code()

    def __getattr__(self, key: str):
        """ Return the requested value. If it doesn't exist, pass it on to our
        callback since it is propably a function not defined here. """
        try:
            return self.__dict__[key]
        except KeyError:
            self.__dict__['fname'] = key
            return self.return_func

    def __repr__(self):
        return self._code

    @abstractmethod
    def _init_local(self):
        return

    @abstractmethod
    def _gen_code(self):
        return

    def return_func(self, *args, **kwargs):
        """ Pass the parameters to our callback and return nothing. """
        self.__dict__[f'_{self.fname}'] = args
        self._callback('func', self._id, self.fname, args)


class Table(Widget):

    def _init_local(self):
        self._type = 'table'

    def _gen_code(self):
        self._code = f'<table id="{self._id}" class="widget"></table>'


class Link(Widget):

    def _init_local(self):
        self._type = 'link'
        self._html = tuple([''])

    def _gen_code(self):
        html = self._html[0]
        self._code = f'<a id="{self._id}" class="widget-cl" href="#">{html}</a>'


class Input(Widget):

    def _init_local(self):
        self._type = 'input'

    def _gen_code(self):
        self._code = f'<input type="text" id="{self._id}" class="widget-ch-in">'


class Label(Widget):

    def _init_local(self):
        self._type = 'label'
        self._innerText = ''

    def _gen_code(self):
        self._code = f'<p id="{self._id}" class="widget">{self._innerText}</p>'


class Select(Widget):

    def _init_local(self):
        self._type = 'select'

    def _gen_code(self):
        self._code = f'<select id="{self._id}" class="widget-ch-cl"></select>'
