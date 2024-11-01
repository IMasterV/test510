import pytest


@pytest.fixture(scope="module")
def some():
    print('Начало')
    yield
    print('Конец')


# @pytest.fixture()
# def set_up():
#     print('Вход в систему')
#     yield
#     print('Выход из системы')