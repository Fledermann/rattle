#!/usr/bin/env python3

import re
import json
from abc import ABC, abstractmethod
from collections import defaultdict
from flask import render_template, request
from .widgets import Input, Label, Link, Select, Table
from .utils import FlaskAppWrapper


class App(ABC):

    events = defaultdict(lambda: defaultdict(list))

    def __init__(self, title, html=None, css=None):
        self.app = FlaskAppWrapper(__name__)
        self.app.add_endpoint('/', 'http_response', handler=self.http_response,
                              methods=['GET', 'POST'])
        self.title = title
        self.html = ''
        self.html_src = html
        self.queue = list()
        self.widgets = dict()
        self.widget_objs = {'input': Input, 'label': Label, 'link': Link,
                            'select': Select, 'table': Table}
        self.make_widgets()

    def __call__(self, name):
        return self.widgets[name]

    @abstractmethod
    def __setup__(self):
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
            return None
        return getattr(self, evt)

    def make_widgets(self):
        with open(self.html_src, 'r') as f:
            html = f.read()
        pattern = re.compile(r'{{ (.*?) }}')
        widgets = re.findall(pattern, html)
        for w in widgets:
            type_, id_ = w.split('#')
            new_widget = self.widget_objs[type_](id_, self.callback_widget)
            self.widgets[id_] = new_widget

    def make_html_response(self):
        with open(self.html_src, 'r') as f:
            html = f.read()
        for w in self.widgets.values():
            tag = f'{{{{ {w._type}#{w._id} }}}}'
            html = html.replace(tag, str(w))
        self.html = html

    def new(self, id_, type_):
        new_widget = self.widget_objs[type_](id_, self.callback_widget)
        self.widgets[id_] = new_widget
        return new_widget

    def run(self):
        self.app.run()

    def http_response(self):
        if not request.form:
            # The very first request or after refresh: build new.
            self.setup()
            self.make_html_response()
            return render_template('default.html', title=self.title,
                                   body=self.html)
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
