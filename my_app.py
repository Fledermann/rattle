#!/usr/bin/env python3

import os
import pathlib
import time

from rattle.rattle import App


def square_input(id_):
    value = my_app('number_input').value
    try:
        result = f'n² = {int(value) ** 2}'
    except ValueError:
        result = 'Not a number!'
    my_app('result').innerText = result


def language(id_):
    value = my_app('dropdown').value
    output = f'The selected language is: "{value}"'
    my_app('selected').innerText = output


def link_clicked(id_):
    time_ = time.strftime('%H:%M:%S')
    msg = f'You clicked a link on {time_}'
    my_app('sample_link_label').innerText = msg


def file_browser_build(my_app, directory):
    if not pathlib.Path(directory).is_dir():
        return None
    # Erase the current html and add header.
    my_app('dir_curr').innerText = directory
    my_app('files').html('')
    my_app('files').append('File Name', 'Size (bytes)', category='header')

    # Add a link to parent directory.
    link = my_app.new(f'link_parent', 'link')
    link.html('..')
    link._value = str(pathlib.Path(directory).parent.resolve())
    link.on_click = file_browser_click

    my_app('files').append(repr(link), '4096')

    # Walk through dir and create links.
    for file_ in sorted(pathlib.Path(directory).iterdir())[:6]:
        size = os.stat(file_).st_size
        id_ = str(file_).replace('/', '')
        link = my_app.new(f'link_{id_}', 'link')
        link.html(file_.parts[-1])
        link._value = str(pathlib.Path(file_).resolve())
        link.on_click = file_browser_click
        my_app('files').append(repr(link), str(size))


def file_browser_click(id_):
    directory = my_app(id_)._value
    file_browser_build(my_app, directory)


def setup(my_app):
    my_app('number_input').on_input = square_input
    my_app('result').innerText = 'Please enter a number.'

    my_app('dropdown').append('<option value="en">English</option>')
    my_app('dropdown').append('<option value="de">German</option>')
    my_app('dropdown').on_change = language

    my_app('sample_link').html('This is a sample link')
    my_app('sample_link').on_click = link_clicked

    file_browser_build(my_app, '.')


my_app = App('my_app: Testing widgets', 'my_app.html', setup)

my_app.run()
