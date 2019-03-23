#!/usr/bin/env python3

import time

from rattle.rattle import App


class MyApp(App):

    def _setup(self):
        self('result').innerText = 'Please enter a number.'
        self('dropdown').append(['en', 'English'])
        self('dropdown').append(['de', 'German'])
        self('sample_link').html('This is a sample link')
        self('files').append(['ID', 'Name', 'Phone'], category='header')
        self('files').append(['1', 'John', '555-34124'])
        self('files').append(['2', 'Jane', '555-09812'])
        self('loading').value = '20'
        self('gauge').html('Click me to load.')

        link_index = self.new('link_index', 'a')
        link_index.html('Main Settings')
        link_index.attr('href', 'index')
        self('menu').append(link_index)

        link_advanced = self.new('link_advanced', 'a')
        link_advanced.html('Advanced Settings')
        link_advanced.attr('href', 'advanced')
        self('menu').append(link_advanced)
        
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

    @App.event('gauge', 'click')
    def fill_bar(self):
        for i in range(20, 102, 1):
            self('loading').value = str(i)
            time.sleep(0.1)


src = 'example/'
myapp = MyApp('my_app: Testing widgets', src=src)
myapp.run()
