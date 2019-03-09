#!/usr/bin/env python3

import logging

logger = logging.getLogger('rattle.widgets')


class Widget:
    """ The Widget abstract base class. Never to be called directly.

    :param str _id: The widgets' id or name.
    :param callable callback: Callback function which receives the instances'
                              attributes when certain attributes are changed.
    """

    def __init__(self, _id, data, callback):
        self._id = _id
        self._data = data
        self._type = data['_name']
        self._callback = callback
        self._gen_code()

    def __setattr__(self, key, value):
        """ Set the attribute and trigger callback when things are changed
        which may require a new render. Make a callback to flask/js if
        it is not a private attribute and not a function (like when
        assigning on_event methods).
        """
        self.__dict__[key] = value
        if key[0] != '_' and not callable(value):
            self._callback('attr', self._id, key, value)
            self._gen_code()

    def __getattr__(self, key):
        """ Return the requested value. If it doesn't exist, pass it on to our
        callback since it is propably a function not defined here. """
        try:
            return self.__dict__[key]
        except KeyError:
            if key.startswith('on_'):
                logger.info(f'Info: Function {key} available but not defined ',
                            f'for {self._type}')
                return None
            self.__dict__['fname'] = key
            return self.return_func

    def __repr__(self):
        self._gen_code()
        return self._code

    def _gen_code(self):
        """ Build the html source for the element. """
        properties = self._data

        if not properties:
            logger.error(f'Widget type {self._type} NA')
            self._code = ''
            return

        attrib = [f'{key}="{value}"' for key, value in
                  properties['extra_attributes'].items()]

        self._code = (f'<{self._type} '  # Opening Tag
                      f'id="{self._id}" '  # DOM id
                      f'class="{properties["events"]}" '  # class
                      f'{" ".join(attrib)}>')  # additional attributes

        if not properties.get('single'):
            self._code += f'</{self._type}>'  # Closing tag

    def return_func(self, *args, fname='', **kwargs):
        """ Pass the parameters to our callback and return nothing. """
        if fname:
            self.fname = fname
        setattr(self, f'_{self.fname}', args)
        try:
            # Process args if function is defined (like table_append())
            args = globals()[f'{self._type}_{self.fname}'](*args, **kwargs)
        except KeyError:
            pass
        self._callback('func', self._id, self.fname, args)


def select_append(args):
    value, name = args
    return f'<option value="{value}">{name}</option>'


def table_append(row, category='default'):
    """ Take any number of string args and put them together as a
    HTML table row.
    """
    html_row = '</td><td>'.join(row)
    html_row = f'<tr><td>{html_row}</td></tr>'
    if category == 'header':
        html_row = html_row.replace('td>', 'th>')
    return html_row


def ul_append(name):
    return f'<li>{name}</li>'
