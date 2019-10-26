import random
import math
from enum import Enum


class Quality(Enum):
    very_good = 'Очень хорошая погода'
    good = 'Хорошая погода'
    bad = 'Плохая погода'
    very_bad = 'Очень плохая погода'


class Weather:
    dEuq = 0
    dCity = 0
    dHem = 0

    def __init__(self, date, temp, fall, wind, humid, quality=None):
        self.date = date
        self.temp = int(temp)
        self.fall = int(fall)
        self.wind = int(wind)
        self.humid = int(humid)
        self.quality = quality

    def toString(self):
        return 'Дата: ' + self.date + '|Температура:' + str(self.temp) + 'гр.|Осадки: ' + str(self.fall) + 'мм.|Ветер: ' + str(self.wind) + 'м/с|Влажность:' + str(self.humid) + '%|' + str(self.quality.value)

    def toStringWithDistance(self):
        return self.toString() + '||Евклид: ' + str("%.3f" % self.dEuq) + '|Хемминг: ' + str("%.3f" % self.dHem) + '|Город. кварт.: ' + str("%.3f" % self.dCity)


def clasterize(wList):
    clusters = []
    # 1. Берём случайный центр:
    i = random.randint(0, len(wList))
    center = wList[i]
    clusters.append(center)
    wList.pop(i)

    # 2. Ищем образ с наибольшим расстоянием:
    for w in wList:
        w.dEuq = euqlid(wList, center)
    maxEuq = max(wList, key=lambda x: x.dEuq)
    maxEuqIndex = wList.index(maxEuq)
    # 2.1 Переносим его в массив кластеров:
    clusters.append([maxEuq])
    wList.pop(maxEuqIndex)


def euqlid(w1, w2):
    return math.sqrt((w1.temp - w2.temp) ** 2 + (w1.fall - w2.fall)
                     ** 2 + (w1.wind - w2.wind) ** 2 + (w1.humid - w2.humid) ** 2)


def hemming(w1, w2):
    return abs(w1.temp - w2.temp) + abs(w1.fall - w2.fall) + abs(w1.wind - w2.wind) + abs(w1.humid - w2.humid)


def city(w1, w2):
    return max([abs(w1.temp - w2.temp), abs(w1.fall - w2.fall), abs(w1.wind - w2.wind), abs(w1.humid - w2.humid)])


task = -1

print('Введите номер задания:')
print('1. Классификация')
print('2. Кластеризация')
print('3. Метод голосования')
print('0. Завершить программу')
print()

task = input()

while (task != 0):
    # Исходные данные:
    wData = [
        Weather('26 окт', 8, 0.4, 7, 77, Quality.very_good),
        Weather('27 окт', 7, 10.7, 9, 93, Quality.bad),
        Weather('28 окт', 1, 11.5, 5, 87, Quality.bad),
        Weather('29 окт', -5, 0, 3, 72, Quality.very_good),
        Weather('30 окт', -4, 0, 3, 67, Quality.very_good),
        Weather('31 окт', -3, 1.3, 4, 71, Quality.good),
        Weather('1 нояб', -6, 1.8, 5, 72, Quality.good),
        Weather('2 нояб', -3, 7.6, 2, 89, Quality.very_bad),
        Weather('3 нояб', -11, 0, 3, 82, Quality.good),
        Weather('4 нояб', -4, 4.2, 6, 82, Quality.bad)
    ]

    # Ввод погоды для классификации:
    print('Введите погоду для проверки:')
    print('Температура (гр.):')
    t = input()
    print('Количество осадков (мм):')
    fall = input()
    print('Скорость ветра (м/с):')
    wind = input()
    print('Влажность (%):')
    humid = input()
    wUser = Weather('?', t, fall, wind, humid)

    print('Введённая погода:')
    print(wUser.toString())

    if (task == '1'):
        # Вычисление расстояний:
        for w in wData:
            w.dEuq = euqlid(w, wUser)
            w.dHem = hemming(w, wUser)
            w.dCity = city(w, wUser)

        minEuq = min(wData, key=lambda x: x.dEuq)
        minHem = min(wData, key=lambda x: x.dHem)
        minCity = min(wData, key=lambda x: x.dCity)

        # Вывод результатов:
        print('___Метод Евклида___')
        print('Класс: ' + minEuq.quality.value)
        print('Расстояние: ' + str("%.3f" % minEuq.dEuq))
        print('Ближайший сосед: ' + minEuq.date)
        print()
        print('___Метод Хемминга___')
        print('Класс: ' + minHem.quality.value)
        print('Расстояние: ' + str("%.3f" % minHem.dHem))
        print('Ближайший сосед: ' + minHem.date)
        print()
        print('___Метод городских кварталов___')
        print('Класс: ' + minCity.quality.value)
        print('Расстояние: ' + str("%.3f" % minCity.dCity))
        print('Ближайший сосед: ' + minCity.date)
        print()
        print('Расстояния: ')
        for w in wData:
            print(w.toStringWithDistance())

    if task == 2:
        clasterize(wData, wUser)
