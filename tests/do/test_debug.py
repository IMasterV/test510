# test_debug.py
import pytest

class TestDebug:
    def test_one(self):
        """Test number one"""
        print("This is test one")
        assert 1 == 1

    def test_two(self):
        """Test number two"""
        print("This is test two")
        assert 2 == 2

    def test_three(self):
        """Test number three"""
        print("This is test three")
        for i in range(4):
            assert i == 3