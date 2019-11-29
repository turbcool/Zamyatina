import random
import math
from enum import Enum


class Quality(Enum):
    very_good = 'Очень хорошая погода'
    good = 'Хорошая погода'
    bad = 'Плохая погода'
    very_bad = 'Очень плохая погода'
    none = '?'


class Weather:
    lenghts = []
    nearestCenter = []

    dEuq = 0
    dCity = 0
    dHem = 0

    def __init__(self, date, temp, fall, wind, humid, quality=Quality.none):
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

class Row:
    x1 = 0
    x2 = 0
    x3 = 0
    x4 = 0

    def __init__(self, x1, x2, x3, x4):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.x4 = x4

def clasterize(wList):
    centers = []
    ok = True
    # 1. Берём первый (случайный) центр:
    i = random.randint(0, len(wList) - 1)
    center = wList[i]
    centers.append(center)
    wList.pop(i)

    # 2. Ищем второй центр:
    maxEuq = max(wList, key=lambda x: x.dEuq)
    maxEuqIndex = wList.index(maxEuq)
    centers.append(maxEuq)
    wList.pop(maxEuqIndex)

    # 3. Ищем остальные центры:
    while ok:
        for w in wList:
            w.lenghts = []

            for index, c in enumerate(centers):
                w.lenghts.append(euqlid(w, c))
            w.nearestCenter = w.lenghts.index(min(w.lenghts))
        Lw = max(wList, key=lambda w: w.lenghts[w.nearestCenter])
        L = Lw.lenghts[Lw.nearestCenter]
        Lindex = wList.index(max(wList, key=lambda w: w.nearestCenter))
        # max of cross join ^^?
        ok = (L > euqlid(centers[0], centers[1]) / 2)
        if ok:
            centers.append(wList[Lindex])
            wList.pop(Lindex)

    clusters = []
    for index, c in enumerate(centers):
        cluster = [c]
        for w in wList:
            if index == w.nearestCenter:
                cluster.append(w)
        clusters.append(cluster)
    return clusters


def euqlid(w1, w2):
    return math.sqrt((w1.temp - w2.temp) ** 2 + (w1.fall - w2.fall)
                     ** 2 + (w1.wind - w2.wind) ** 2 + (w1.humid - w2.humid) ** 2)


def hemming(w1, w2):
    return abs(w1.temp - w2.temp) + abs(w1.fall - w2.fall) + abs(w1.wind - w2.wind) + abs(w1.humid - w2.humid)


def city(w1, w2):
    return max([abs(w1.temp - w2.temp), abs(w1.fall - w2.fall), abs(w1.wind - w2.wind), abs(w1.humid - w2.humid)])

def compare(testW, testList):
    tPair1 = (testW[0], testW[1])
    tPair2 = (testW[2], testW[3])
    ok1 = 0
    ok2 = 0
    for w in testList:
        t1 = (w[0], w[1])
        t2 = (w[1], w[2])
        if t1 == tPair1:
            ok1=ok1+1
        if t2 == tPair2:
            ok2=ok2+1
    score = ok1 + ok2
    return score

task = -1

while (task != 0):
    clear()
    print('Введите номер задания:')
    print('1. Классификация')
    print('2. Кластеризация')
    print('3. Метод голосования')
    print('4. Посчитать ошибки для метода классификации')
    print('0. Завершить программу')
    print()

    task = int(input())

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

    if task == 1:
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
        clusters = clasterize(wData)

        for index, c in enumerate(clusters):
            for w in c:
                print(w.toString() + '| Кластер: ' + str(index))
    if task == 3:
        # теплая погода, солнечно, низкая влажность, был дождь
        goodWeather = [
            [1, 0, 1, 0],
            [1, 0, 1, 0],
            [0, 1, 1, 1],
            [1, 1, 0, 0],
            [1, 1, 1, 0]
        ]

        badWeather = [
            [1, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 1, 1, 1],
            [1, 1, 0, 0],
            [0, 1, 0, 0]
        ]

        print('Погода была тёплой? (введите 0 или 1)')
        i1 = int(input())
        print('Погода была солнечной? (введите 0 или 1)')
        i2 = int(input())
        print('Была низкая влажность? (введите 0 или 1)')
        i3 = int(input())
        print('Был дождь? (введите 0 или 1)')
        i4 = int(input())

        testW = [i1,i2,i3,i4]

        scoreForGood = compare(testW, goodWeather)
        scoreForBad = compare(testW, badWeather)

        print('За хорошую погоду:' + str(scoreForGood))
        print('За плохую погоду:' + str(scoreForBad))

        if scoreForGood > scoreForBad:
            print('Итог: ваша погода - хорошая')
        else:
            print('Итог: ваша погода - плохая')
    if task == 4:
        print('Ошибки для класса "хорошая погода":')
        wTest = [
            Weather('11 нояб', -10, 10, 2, 89, 'FP'),
            Weather('12 нояб', -3, 0, 0, 71, 'FN'),
            Weather('13 нояб', 2, 5, 2, 92, '?'),
            Weather('14 нояб', -8, 0, 10, 82, '?'),
            Weather('15 нояб', 0, 5, 7, 90, 'FP'),
            Weather('16 нояб', 5, 0, 10, 60, 'FN')
        ]

        FP=0
        FN=0
        for w in wTest:
            if str(w.quality) == 'FP':
                FP=FP+1
            if w.quality == 'FN':
                FN=FN+1
        Nn = FP+FN
        Np=len(wTest)-Nn

        TP=Np-FN
        TN=Nn-FP

        nFN = FN/Np # %
        nFP = FP/Nn # %

        nTN = TN/Nn
        nTP = TP/Np

        precision = TP/(TP+FP) # %
        recall = TP/(TP+FN) # %

        print('FP: ' + str(FP))
        print('FN: ' + str(FN))
        print('Nn: ' + str(Nn))
        print('Np: ' + str(Np))
        print('TP: ' + str(TP))
        print('TN: ' + str(TN))
        print('nFN: ' + str(nFN) + '%')
        print('nFP: ' + str(nFP) + '%')
        print('nTN: ' + str(nTN))
        print('nTP: ' + str(nTP))
        print('precision: ' + str(precision) + '%')
        print('recall: ' + str(recall) + '%')
        
