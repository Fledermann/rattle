#!/usr/bin/env python3

import time

from rattle.rattle import App


class MyApp(App):

    def _setup(self):
        self('result').innerText = 'Please enter a number.'
        self('dropdown').append(['en', 'English'])
        self('dropdown').append(['de', 'German'])
        self('sample_link').html('This is a sample link')

    @App.event('number_input', 'input')
    def square(self):
        value = self('number_input').value
        try:
            result = f'n² = {int(value) ** 2}'
        except ValueError:
            result = 'Not a number!'
        self('result').innerText = result

    @App.event('sample_link', 'click')
    def click_sample(self):
        time_ = time.strftime('%H:%M:%S')
        msg = f'You clicked a link on {time_}'
        self('sample_link_label').innerText = msg

    @App.event('dropdown', 'change')
    def select_lang(self):
        value = self('dropdown').value
        output = f'The selected language is: "{value}"'
        self('selected').innerText = output


html = 'my_app.html'
css = 'static/default.css'
myapp = MyApp('my_app: Testing widgets', html=html, css=css)
myapp.run()
