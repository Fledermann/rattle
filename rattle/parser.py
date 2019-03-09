#!/usr/bin/env python3

import json
import logging
import re

logger = logging.getLogger('rattle.parser')


def html_parser(source_file, widget_data):
    logger.debug(f'Parsing html source file {source_file}.')
    types, ids = [], []
    pattern = re.compile(r'{{ (.*?) }}')
    with open(source_file, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        widgets = re.findall(pattern, line)
        for w in widgets:
            _type, _id = w.split('#')
            if _type not in widget_data:
                logger.error(f'Widget type not found: "{_type}" on line {i}.')
                continue
            if _id in ids:
                logger.error(f'Duplicate widget id: "{_id}" on line {i}.')
                continue
            ids.append(_id)
            types.append(_type)
    return zip(types, ids)


def widget_parser(source_file):
    widgets_indexed = dict()
    with open(source_file, 'r') as f:
        widget_data = json.load(f)
    for w in widget_data:
        widgets_indexed[w['_name']] = w
    return widgets_indexed
