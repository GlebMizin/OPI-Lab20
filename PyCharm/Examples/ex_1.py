#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


if __name__ == '__main__':
    print("The keys and values of all environment variables:")
    for key in os.environ:
        print(key, '=>', os.environ[key])
    print("The value of HOME is: ", os.environ['home'])
