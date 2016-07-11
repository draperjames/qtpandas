# -*- coding: utf-8 -*-

import os
import pytest

FIXTUREDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')

@pytest.fixture()
def csv_file():
    return os.path.join(FIXTUREDIR, 'csv_file.csv')

@pytest.fixture()
def csv_file_utf8():
    return os.path.join(FIXTUREDIR, 'csv_file_utf8.csv')