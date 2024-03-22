import datetime

# Создание списка доступных времен (с учетом текущего времени)
def create_available_times():
    now = datetime.datetime.now().time()
    start_time = datetime.time(9, 0)  # Начальное время
    end_time = datetime.time(17, 0)  # Конечное время

    # Начнем с ближайшего к текущему времени интервала
    while start_time <= now:
        start_time = (datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(minutes=30)).time()

    available_times = []
    while start_time < end_time:
        available_times.append(start_time)
        start_time = (datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(minutes=30)).time()

    return available_times

# Пример использования
available_times = create_available_times()
print(available_times)


def get_available_times(start_time, duration):
    available_times = []
    end_time = start_time + duration
    while start_time < end_time:
        available_times.append(start_time)
        start_time += datetime.timedelta(minutes=30)
    return available_times