#!/usr/bin/env python3

import json
import logging

from abc import ABC, abstractmethod
from collections import defaultdict
from flask import render_template, request

from .parser import html_parser, widget_parser
from .utils import FlaskAppWrapper
from .widgets import Widget

logger = logging.getLogger('rattle.rattle')


class App(ABC):

    events = defaultdict(lambda: defaultdict(list))

    def __init__(self, title, html=None, css=None):
        self.app = FlaskAppWrapper(__name__)
        self.app.add_endpoint('/', 'http_response', handler=self.http_response,
                              methods=['GET', 'POST'])
        self.title = title
        self.body_src = ''
        self.html_file = html
        self.queue = list()
        self.widgets = dict()
        self.make_widgets()

    def __call__(self, name):
        return self.widgets[name]

    @abstractmethod
    def _setup(self):
        return

    def callback_widget(self, type_, id_, key, value):
        self.queue.append(dict(type_=type_, id_=id_, key=key, value=value))

    def event(_id, action):
        def wrapper(func):
            App.events[_id][action].append(func.__name__)

            def wrapped(self):
                func(self)
            return wrapped
        return wrapper

    def on(self, event, _id):
        try:
            evt = App.events[_id][event][0]
        except IndexError:
            logger.info(f'Event on_{event} for {_id} called but not defined.')
            return None
        return getattr(self, evt)

    def make_widgets(self):
        widget_data = widget_parser('rattle/widgets.json')
        widgets = html_parser(self.html_file, widget_data)
        for w in widgets:
            new_widget = Widget(w[1], widget_data[w[0]], self.callback_widget)
            self.widgets[w[1]] = new_widget

    def make_html_response(self):
        with open(self.html_file, 'r') as f:
            html = f.read()
        for w in self.widgets.values():
            tag = f'{{{{ {w._type}#{w._id} }}}}'
            html = html.replace(tag, str(w))
        self.body_src = html

    def new(self, id_, type_):
        new_widget = self.widget_objs[type_](id_, self.callback_widget)
        self.widgets[id_] = new_widget
        return new_widget

    def run(self):
        self.app.run()

    def http_response(self):
        if not request.form:
            # The very first request or after refresh: build new.
            logger.debug('Received empty request, building inital page.')
            self._setup()
            self.make_html_response()
            return render_template('default.html', title=self.title,
                                   body=self.body_src)
        else:
            event = request.form['event']
            if event != 'None':
                # A 'None' event is send when it doesn't come from a
                # widget (like onload or timers).
                id_ = request.form['id_']
                props = json.loads(request.form['props'])
                widget = self.widgets[id_]
                for prop, value in props.items():
                    # Set all attributes as provided.
                    setattr(widget, prop, value)
                try:
                    # Call a bound function if it exists.
                    self.on(event, id_)()
                except (AttributeError, TypeError):
                    pass
            json_response = json.dumps(self.queue)
            self.queue = list()
            return json_response
