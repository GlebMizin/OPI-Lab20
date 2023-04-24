#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


if __name__ == '__main__':
    if os.environ.get('DEBUG') == 'True':
        print('Debug mode is on')
    else:
        print('Debug mode is off')