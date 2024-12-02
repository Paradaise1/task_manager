import json

from main import TaskManager

from conftest import TEST_DATA_FILENAME


class TestTaskManager():
    '''Класс для тестирования функционала класса TaskManager.'''
    # Создаем эксземпляер тестируемого класса
    tm = TaskManager()
    tm.FILENAME = TEST_DATA_FILENAME

    OUTPUT_TASK = ('id - 1;\n'
                   'title - test_title;\n'
                   'description - test description;\n'
                   'category - test_category;\n'
                   'time_to_complete - 10;\n'
                   'priority - низкий;\n'
                   'status - не выполнена;\n\n')
    ERROR_MESSAGE = ('Такого статуса/категории/ключевого '
                     'слова не существует/не найдено.\n')

    def test_add_task(self, monkeypatch, create_statuses, create_priorities):
        '''Тест создания задачи.'''
        STATUSES = create_statuses
        PRIORITIES = create_priorities
        monkeypatch.setattr(
            'builtins.input',
            lambda _: ('test_title, test description, '
                       f'test_category, 10, {PRIORITIES[0]}')
        )
        self.tm.add_task()
        with open(TEST_DATA_FILENAME, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]['id'] == 1
        assert data[0]['title'] == 'test_title'
        assert data[0]['description'] == 'test description'
        assert data[0]['category'] == 'test_category'
        assert data[0]['time_to_complete'] == 10
        assert data[0]['priority'] == PRIORITIES[0]
        assert data[0]['status'] == STATUSES[0]

    def test_find_task_by_status(self, monkeypatch, create_statuses, capfd):
        '''Тест поиска задачи по id.'''
        STATUSES = create_statuses
        monkeypatch.setattr('builtins.input', lambda _: f'{STATUSES[0]}')
        self.tm.find_task()
        out, err = capfd.readouterr()
        assert out == self.OUTPUT_TASK

    def test_find_task_by_category(self, monkeypatch, capfd):
        '''Тест поиска задачи по id.'''
        monkeypatch.setattr('builtins.input', lambda _: 'test_category')
        self.tm.find_task()
        out, err = capfd.readouterr()
        assert out == self.OUTPUT_TASK

    def test_find_task_by_key_word(self, monkeypatch, capfd):
        '''Тест поиска задачи по id.'''
        monkeypatch.setattr('builtins.input', lambda _: 'description')
        self.tm.find_task()
        out, err = capfd.readouterr()
        assert out == self.OUTPUT_TASK

    def test_find_task_with_invalid_args(self, monkeypatch, capfd):
        '''Тест поиска задачи по id.'''
        monkeypatch.setattr('builtins.input', lambda _: 'invalid_word')
        self.tm.find_task()
        out, err = capfd.readouterr()
        assert out == self.ERROR_MESSAGE

    def test_change_to_valid_status(self, monkeypatch, create_statuses):
        '''Тест изменения статуса задачи на доступный статус.'''
        STATUSES = create_statuses
        monkeypatch.setattr('builtins.input', lambda _: '1')
        self.tm.change_status()
        with open(TEST_DATA_FILENAME, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert data[0]['status'] == STATUSES[1]

    def test_delete_task_with_invalid_args(self, monkeypatch):
        '''Тест удаления несуществующей задачи.'''
        monkeypatch.setattr('builtins.input', lambda _: '100')
        self.tm.delete_task()
        with open(TEST_DATA_FILENAME, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert len(data) == 1

    def test_delete_task(self, monkeypatch):
        '''Тест удаления существующей задачи.'''
        monkeypatch.setattr('builtins.input', lambda _: '1')
        self.tm.delete_task()
        with open(TEST_DATA_FILENAME, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert len(data) == 0

    def test_add_task_with_invalid_args(self, monkeypatch):
        '''Тест создания задачи с невалидными аргументами.'''
        monkeypatch.setattr(
            'builtins.input', lambda _: 'invalid_args'
        )
        with open(TEST_DATA_FILENAME, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert len(data) == 0
