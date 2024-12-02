import json
import os
import sys

from typing import Dict


# Все доступные команды
COMMANDS = [
    'add task - добавление задачи по названию, '
    'описанию, категории, сроку выполнения и приоретету.',
    'find task - поиск задачи по '
    'ключевым словам, категории или статусу выполнения.',
    'edit task - редактирование существующей задачи.',
    'change status - отметить задачу как выполненную.'
    'delete task - удаление задачи по id.',
    'show tasks - отображение списка всех доступных задач.',
    'help - список всех доступных команд.',
    'exit - завершение работы программы.'
]

# Название локального хранилища данных
DATA_FILENAME = 'data.json'


class TaskManager():
    '''Класс для работы с задачами.'''
    FILENAME = DATA_FILENAME
    # Статусы
    STATUSES = {0: 'не выполнена', 1: 'выполнена'}
    # Приорететы
    PRIORITIES = ('низкий', 'средний', 'высокий')

    def print_task(self, task: Dict) -> None:
        '''Вспомогательный метод для вывода конкретной задачи.'''
        for key, value in task.items():
            print(f'{key} - {value};')

    def validate(self, val: str, message: str) -> None:
        '''Вспомогательный метод для валидации данных.'''
        try:
            val = int(val)
        except TypeError:
            print(f'{message} должен быть целым числом.')
        return val

    def add_task(self) -> None:
        '''Метод для добавление задачи.'''
        # Запрашиваем данные задачи
        try:
            task_data = input(
                'Введите название, описание, категорию, срок выполнения '
                '(в днях) и приоретет задачи через запятую.\n'
                f'Доступные приорететы: {", ".join(self.PRIORITIES)}.\n'
            ).split(',')
        except ValueError:
            print('Неверное количество аргументов.')
            return
        task_data = list(map(str.strip, task_data))
        task_data[3] = self.validate(task_data[3], 'Cрок выполнения')
        if task_data[4] not in self.PRIORITIES:
            print('Такого приоритета не существует.')
            return
        # Читаем файл, создаем и добавлем задачу, перезаписываем файл
        with open(self.FILENAME, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            if data:
                current_id = data[-1]['id'] + 1
            else:
                current_id = 1
            task = {
                'id': current_id,
                'title': task_data[0],
                'description': task_data[1],
                'category': task_data[2],
                'time_to_complete': task_data[3],
                'priority': task_data[4],
                'status': self.STATUSES[0]
            }
            data.append(task)
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
        print('Задача успешно добавлена!')

    def find_task(self, flag: bool = True) -> int | None:
        '''
        Метод для поиска задачи по ключевым словам,
        категории или статусу выполнения.
        А так же по id для других методов.
        '''
        if not flag:
            # Запрашиваем id задачи при поиске по id
            current_id = input('Введите id задачи: ')
            current_id = self.validate(current_id, 'Индентификатор')
            # Открываем файл, ищем задачу, если нашли - возвращаем ее index
            # Иначе - None
            with open(self.FILENAME, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data:
                    for index, task in enumerate(data):
                        if task['id'] == current_id:
                            return index
                print('Такой задачи не существует.')
                return
        else:
            # Запрашиваем данные поиска
            text = input(
                'Введите ключевое слово, категорию или статусу выполнения: '
            )
            # Получаем данные из хранилища
            with open(self.FILENAME, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Формируем данные среди которых будем искать задачи
            categories = {}
            descriptions = []
            for index, task in enumerate(data):
                if task['category'] in categories.keys():
                    categories[task['category']] += [index]
                else:
                    categories[task['category']] = [index]
                descriptions.append(task['description'])
            # Если критерий поиска - статус
            if text in self.STATUSES.values():
                task_is_found = False
                for task in data:
                    if text == task['status']:
                        task_is_found = True
                        self.print_task(task)
                        print()
                if not task_is_found:
                    print('Задач с таким статусом не найдено.')
                return
            # Если критерий поиска - категория
            elif text in categories.keys():
                for index in categories[task['category']]:
                    self.print_task(data[index])
                    print()
                return
            else:
                # Если критерий поиска - ключевое слово
                task_is_found = False
                for index, desc in enumerate(descriptions):
                    if text in desc:
                        task_is_found = True
                        self.print_task(data[index])
                        print()
                # Если ничего не совпало - ошибка
                if not task_is_found:
                    print('Такого статуса/категории/ключевого '
                          'слова не существует/не найдено.')
                return

    def edit_task(self) -> None:
        '''Метод для редактирования задачи по id.'''
        # Находим задачу уже существующим методом
        current_id = self.find_task(flag=False)
        if current_id is None:
            return
        # Запрашиваем новые данные задачи
        try:
            new_data = input(
                'Введите новые название, описание, категорию, срок выполнения '
                '(в днях) и приоретет задачи через запятую.\n'
                'Чтобы не изменять какое-то значение, введите "-"\n'
                f'Доступные приорететы: {", ".join(self.PRIORITIES)}.\n'
            ).split(',')
        except ValueError:
            print('Неверное количество аргументов.')
            return
        new_data = list(map(str.strip, new_data))
        if new_data[3] != '-':
            new_data[3] = self.validate(new_data[3], 'Cрок выполнения')
        if new_data[4] != '-':
            if new_data[4] not in self.PRIORITIES:
                print('Такого приоритета не существует.')
                return
        # Читаем файл, изменяем данные задачи, перезаписываем файл
        with open(self.FILENAME, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            index = 0
            task_data = list(data[current_id].keys())
            task_data.pop(0)
            task_data.pop(-1)
            for key in task_data:
                if new_data[index] != '-':
                    data[current_id][key] = new_data[index]
                index += 1
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()
        print('Задача успешно изменена!')

    def delete_task(self) -> None:
        '''Метод для удаления задачи по id.'''
        # Находим задачу уже существующим методом
        current_id = self.find_task(flag=False)
        if current_id is None:
            return
        # Открываем файл, удаляем задачу
        with open(self.FILENAME, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data.pop(current_id)
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()
        print('Задача успешно удалена!')

    def show_tasks(self) -> None:
        '''Метод для вывода информации о всех задачах.'''
        # Открваем файл, читаем информацию, выводим ее
        with open(self.FILENAME, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if data:
            for task in data:
                self.print_task(task)
                print()
        else:
            print('Задач нет.')

    def change_status(self) -> None:
        '''Метод для изменения статуса конкретной задачи.'''
        # Находим задачу уже существующим методом
        current_id = self.find_task(flag=False)
        if current_id is None:
            return
        # Читаем файл, меняем статус, перезаписываем файл
        with open(self.FILENAME, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            if data[current_id]['status'] == self.STATUSES[1]:
                print('Эта задача уже завершена.')
            else:
                data[current_id]['status'] = self.STATUSES[1]
                print(f'Здача {data[current_id]["id"]}: '
                      f'{data[current_id]["title"]} завершена!')
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()


class CommandsManager():
    '''Класс для управления командами,
    не относящимися к работе с библиотекой.'''
    def helping(self) -> None:
        '''Команда для вывода списка всех доступных команд.'''
        print('Все доступные команды:')
        for cmd in COMMANDS:
            print(cmd)

    def exiting(self) -> None:
        '''Команда для выхода из бесконечного цикла.'''
        print('Выход...')
        sys.exit()


def main() -> None:
    '''Основная логика программы.'''
    # Инициализируем все необходимое для работы программы
    if not os.path.exists(DATA_FILENAME):
        with open(DATA_FILENAME, 'w') as f:
            json.dump([], f)

    tm = TaskManager()
    cm = CommandsManager()
    commands = {
        'add task': tm.add_task,
        'find task': tm.find_task,
        'edit task': tm.edit_task,
        'delete task': tm.delete_task,
        'show tasks': tm.show_tasks,
        'change status': tm.change_status,
        'help': cm.helping,
        'exit': cm.exiting
    }

    # Выводим приветсвие
    print('Привет пользователь! Данное консольное приложение '
          'разработано для управления '
          'списком задач на твоем компьютере.')
    cm.helping()

    # Запрашиваем команды, пока пользователь не введет exit
    while True:
        cmd = input('Введите команду: ')
        try:
            commands[cmd]()
        except KeyError:
            print('Такой команды не существует. '
                  'Попробуйте help для просмотра всех доступных команд.')


if __name__ == '__main__':
    main()
