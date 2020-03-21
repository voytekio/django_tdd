import pytest
import os
import sys

@pytest.fixture()
def my_fixture():
    print('FIXTURE SETUP(my_fixture)')
    yield 'my_fixture_result'
    print('FIXTURE TEARDOWN(my_fixture)')

