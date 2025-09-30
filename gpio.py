# import time
#
# gpio_in1 = "/sys/class/gpio/GPIO_in1/value"
#
# with open(gpio_in1, "r") as f:
#     value = f.read().strip()
# print(f"gpio_in1: {value}")
#
# gpio_out1 = "/sys/class/gpio/GPIO_out1/value"
#
# with open(gpio_out1, "w") as f:
#     f.write("1")
#
#



def gpio_access(path, mode = "r", value = None):
    """
    Универсальная функция для работы с GPIO через sysfs.

    :param path: путь к файлу (например, /sys/class/gpio/GPIO_in1/value)
    :param mode: режим - "r" (чтение) или "w" (запись)
    :param value: строка для записи ("0" или "1"), если mode="w"
    :return: строка со значением при чтении, None при записи
    """

    if mode == "r":
        with open(path, "r") as file:
            return file.read().strip()

    elif mode == "w":
        if value is None:
            raise ValueError("Для записи нужно указать value")

        with open(path, "w") as file:
            file.write(value)
        return None
    else:
        raise ValueError("mode должен быть 'r' или 'w'")


gpio_in1 = "/sys/class/gpio/GPIO_in1/value"
gpio_out1 = "/sys/class/gpio/GPIO_out1/value"

result = gpio_access(gpio_in1, mode='r')
print(result)


