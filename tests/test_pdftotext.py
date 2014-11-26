from unittest import TestCase

__author__ = 'oier'

import pytest
import pdftoexcel as p2e


class TestGetfromjava(TestCase):
    def test_getfromjava(self):
        p2e.getfromjava("./data/ExampleTest.pdf")