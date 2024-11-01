from sys import getsizeof
#
# def get_min_max(iterable):
#     some_iter = iter(iterable)
#     try:
#         for i in some_iter:
#             if start <= i:
#             start = i
#         return (next(some_iter), max(some_iter))
#     except StopIteration:
#         return None


# massiv = [(1,2,3), (4,5,6), (7,8,9)]
#
# # можно и так сразу развернуть в каждую переменную если количество переменных фиксировано
# for data, state, status in massiv:
#     print(data, state, status)



# wr_data = (16, 8, 16, 2)
# rd_data_state = (1, 17, None, 2)
# rd_data_status = (0, 17, None, 0)
#
# massiv = [(16, 8, 16, 2), (1, 17, None, 2), (0, 17, None, 0)]
# for data, state, status, r in massiv:
#     print(data, state, status, r)

# def is_palindrome(text):
#     list = []
#
#     for i in text:
#         if i.isalpha():
#             list.append(i)
#     result = ''.join(list)
#
#     if result.lower() == result.lower()[::-1]:
#         return True
#     else:
#         return False
#
# # считываем данные
# txt = input()
#
# # вызываем функцию
# print(is_palindrome(txt))


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Point{(self.x, self.y, self.z)}"

    def __iter__(self):
        yield from (self.x, self.y, self.z)


points = [Point(4, 7, 0), Point(1, 5, 10), Point(12, 23, 44)]
print(points)

#print(date(2022, 3, 8) + timedelta(days=1))

# import argparse
#
# parser = argparse.ArgumentParser(description="Ввод входных аргументов")
#
# parser.add_argument('arg1', type=str, help='COM порт')
# parser.add_argument('arg2', type=str, help='Адрес прибора')
#
# parser.add_argument('--ip', type=str, help="Опциональный аргумент", default="10.2.25.78")
#
# args = parser.parse_args()
#
# print(f"COM{args.arg1}")
# print(f"Адрес {args.arg2}")
# print(f"IP-адрес: {args.ip}")

#print(get_min_max(iterable))
#     min = range(100_000_000)[0]
#     max = range(100_000_000)[-1]
# print(min, max)
# def add(a, b):
#     '''sum of two numbers'''
#     return a + b
#
#
# print(add.__name__)
# print(add.__doc__)
# print(add(10, b=20))


# try:
#     while True:
#         try:
#             port = int(input('Номер COM-порта: '))
#         except ValueError:
#             print('Значение должно быть целочисленным')
#         else:
#             break
#
#     while True:
#         try:
#             id = int(input('Адрес прибора: '))
#         except ValueError:
#             print('Значение должно быть целочисленным')
#         else:
#             break
# except EOFError:
#     mu_210.wr_holding_registers(address=470, values=[0], id=1)
#подключаемся к модулю 510


# def initialization_values():
#     parser = argparse.ArgumentParser(description="Ввод входных аргументов")
#
#     parser.add_argument('port', type=str, help='COM порт')
#     parser.add_argument('id', type=str, help='Адрес прибора')
#
#     parser.add_argument('--ip', type=str, help="Опциональный аргумент", default="10.2.25.78")
#
#     args = parser.parse_args()
#
#     print(f"COM{args.port}")
#     print(f"Адрес {args.id}")
#     print(f"IP-адрес: {args.ip}")
#     return args.port, args.id, args.ip
#
# com_port, id, ip_address = initialization_values()