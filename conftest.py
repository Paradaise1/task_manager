import json
import os
import pytest


TEST_DATA_FILENAME = 'test_data.json'


@pytest.fixture(scope='session', autouse=True)
def create_json_file():
    '''Фикстура для создания json файла.'''
    if not os.path.exists(TEST_DATA_FILENAME):
        with open(TEST_DATA_FILENAME, 'w') as f:
            json.dump([], f)
    yield
    os.remove(TEST_DATA_FILENAME)


@pytest.fixture()
def create_statuses():
    '''Фикстура для создания доступных статусов.'''
    return {0: 'не выполнена', 1: 'выполнена'}


@pytest.fixture()
def create_priorities():
    '''Фикстура для создания доступных приорететов.'''
    return ('низкий', 'средний', 'высокий')
