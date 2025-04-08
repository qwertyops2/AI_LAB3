

## !!!!Программа должна запускаться в режиме интерпретатора построчно или блоками кода!!!!!!!
## !!!!!!!!   Чтиайте комментарии и только после этого запускайте код !!!!!!!!!!!!!


## Перед выполнением убедитесь что у вас установлен pytorch

import torch 
import numpy as np
import pandas as pd

import random

# Основная структура данных pytorch - тензоры
# Основные отличия pytorch-тензоров от numpy массивов:
# 1 Место их хранения можно задать ( память CPU или GPU )
# 2 В отношении тензоров можно задать вычисление и отслеживание градиентов



# Создавать тензоры можно разными способами:
# Пустой тензор
a = torch.empty(5, 3)
print(a) # Пустой тензор обычно содержит "мусор"

b = torch.Tensor(5, 3)
print(b) # Пустой тензор обычно содержит "мусор"

# тензор с нулями
a = torch.zeros(5, 3)
print(a) # тензор заполняем нулями

b = torch.ones(5, 3)
print(b) # тензор заполняем единицами

# можно задать тип тензора
# pytorch поддерживает следующие основные типы тензоров
# 32-bit с плавающей точкой - torch.float32 или torch.float
# 64-bit с плавающей точкой - torch.float64 или torch.double
# 16-bit с плавающей точкой - torch.float16 или torch.half
# 8-bit целый беззнаковый - torch.uint8 
# 8-bit целый - torch.int8
# 16-bit целый - torch.int16 или torch.short
# 32-bit целый - torch.int32 или torch.int
# 64-bit целый - torch.int64 или torch.long
# Булевский бинарный - torch.bool
# квантизованный целый беззнаковый 8-bit - torch.quint8
# квантизованный целый 8-bit - torch.qint8
# квантизованный целый 32-bit - torch.qint32
# квантизованный целый 4-bit - torch.quint4x2

с = torch.ones(5, 3, dtype=torch.int32)
print(с) # тензор заполняем единицами

# кроме того тензоры, используемые для вычислений на GPU имеют свои типы данных
# torch.cuda.FloatTensor, 
# torch.cuda.DoubleTensor, 
# torch.cuda.HalfTensor, 
# torch.cuda.ByteTensor,
# torch.cuda.ShortTensor, 
# torch.cuda.IntTensor, 
# torch.cuda.LongTensor, 
# torch.cuda.BoolTensor


# Можно преобразовать созданный тензор в другой тип
b = b.to(dtype=torch.int32)
print(b)


# Тензор можно заполнить случайными числами
a = torch.rand(5, 3)
print(a) # распределеными по равномерному закону распределения

b = torch.randn(5, 3)
print(b) # распределеными по нормальному закону распределения

# или можем явно указать нужные значения
a = torch.Tensor([[1,2],[3,4]])
print(a) 

# Наиболее часто используемые методы создания тензоров

#    torch.rand: случайные значения из равномерного распределения
#    torch.randn: случайные значения из нормального распределения
#    torch.eye(n): единичная матрица
#    torch.from_numpy(ndarray): тензор на основе ndarray NumPy-массива
#    torch.ones : тензор с единицами
#    torch.zeros_like(other): тензор с нулями такой же формы, что и other
#    torch.range(start, end, step): 1-D тензор со значениями между start и end с шагом steps


# тензоры можно преобразовать к Numpy массивам
# !!! но нужно не забывать про копирование данных !!!
# если не указать метод copy(), обе переменные будут 
# указывать на одну область памяти и изменения в одной из переменных будут 
# вызывать изменения в другой
d = a.numpy().copy()

# тензоры можно "слайсить" как и Numpy массивы, списки или строки
print(a[1,:].numpy())

# Понять можем ли мы использовать графический ускоритель для вычислений поможет функция
print(torch.cuda.is_available())

if torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu' 

# device теперь хранит тип устройства на котором можно проводить вычисления
# создавать тензоры можно в памяти видеокарты, если CUDA доступна
a = torch.Tensor([[1,2],[3,4]]).to(device) 

# Для обучения нейронных сетей некоторые тензоры 
# должны отслеживать градиенты (происходящие с ними изменения)
a = torch.randn(2, 2, requires_grad=False)
a.requires_grad

a.requires_grad=True # Теперь все операци над тензором a будут отслеживаться
print(a)

# выполненные операции хранятся в свойстве grad_fn
print(a.grad_fn) # пока с тензором ничего не делали

# Выполним какую-нибудь операцию с тензором:
a = a + 2
print(a)

# теперь grad_fn, который хранит информацию об операции с тензором
print(a.grad_fn)

a = a * 2
print(a)

print(a.grad_fn)

# Все это нужно для вычисления градиентов
# посмотрим детально как это происходит
# создадим простую последовательность вычислений

x = torch.zeros(2, 2, requires_grad=True)
y = x + 3
z = y**2
out = z.mean()
print(z)
print(out)

# теперь воспользовавшись правилом дифференцирования сложных функций
# продифференцируем полученную последовательность
# для этого вызовем метод .backward(), который проведет дифференцирование в обратном порядке 
# до изначально заданного тензора x
out.backward()
print(x.grad) # градиенты d(out)/dx

# метод .backward() без аргументов работает только для скаляра (например ошибки нейросети)
# чтобы вызвать его для многомерного тензора, внего в качестве параметра необходимо 
# передать значения градиентов с "предыдущего" блока  
x = torch.tensor([[1.,2.],[3.,4.]], requires_grad=True)
print(z)
z = x**2
print(z) 
z.backward(torch.ones(2,2))
print(x.grad) # градиенты d(z)/dx = 2*x


###########                                                        ############
###########    Обучение линейного алгоритма на основе нейронов    #############
###########                                                       #############

# Для работы с нейронными сетями pytorch предоставляет широкий набор инструментов:
# слои, функции активации, функционалы потерь, оптимизаторы
import torch.nn as nn

# Попробуем обучить нейроны решать искусственную задачу
# Создадим 2 тензора:  1 входной размером (10, 3) - наша обучающая выборка 
# из 10 примеров с 3 признаками

X = torch.randn(10, 3)

#  2 выходной тензор - значения, которые мы хотим предсказывать нашим алгоритмом
y = torch.randn(10, 2)


# создадим 3 сумматора без функци активации, это называется полносвязный слой (fully connected layer)
# Отсутствие фунций активаци на выходе сумматора эквивалетно наличию  линейной активации
linear = nn.Linear(3, 2)

# при создании веса и смещения инициализируются автоматически
print ('w: ', linear.weight)
print ('b: ', linear.bias)

# выберем вид функции ошибки и оптимизатор
# фунция ошибки показывает как сильно ошибается наш алгоритм в своих прогнозах
lossFn = nn.MSELoss() # MSE - среднеквадратичная ошибка, вычисляется как sqrt(sum(y^2 - yp^2))


# создадим оптимизатор - алгоритм, который корректирует веса наших сумматоров (нейронов)
optimizer = torch.optim.SGD(linear.parameters(), lr=0.01) # lr - скорость обучения

# прямой проход (пресказание) выглядит так:
yp = linear(X)

# имея предсказание можно вычислить ошибку
loss = lossFn(yp, y)
print('Ошибка: ', loss.item())

# и сделать обратный проход, который вычислит градиенты (по ним скорректируем веса)
loss.backward()

# градиенты по параметрам
print ('dL/dw: ', linear.weight.grad) 
print ('dL/db: ', linear.bias.grad)

# далее можем сделать шаг оптимизации, который изменит веса 
# на сколько изменится каждый вес зависит от градиентов и скорости обучения lr
optimizer.step()

# итерационно повторяем шаги
# в цикле (фактически это и есть алгоритм обучения):
for i in range(0,10):
    pred = linear(X)
    loss = lossFn(pred, y)
    print('Ошибка на ' + str(i+1) + ' итерации: ', loss.item())
    loss.backward()
    optimizer.step()
 
# Задание 2

di = pd.read_csv("data.csv")
X = torch.Tensor(di.iloc[0:100, 0:3].values)
y = di.iloc[0:100, 4].values
y = torch.Tensor(np.where( y == "Iris-setosa", 1, -1).reshape(-1,1))

linear = nn.Linear(3, 1)
print ('w: ', linear.weight)
print ('b: ', linear.bias)

lossFn = nn.MSELoss()

optimizer = torch.optim.SGD(linear.parameters(), lr=0.01)

yp = linear(X)

loss = lossFn(yp, y)
print('Ошибка: ', loss.item())

loss.backward()

print ('dL/dw: ', linear.weight.grad) 
print ('dL/db: ', linear.bias.grad)

optimizer.step()

for i in range(0,10):
    pred = linear(X)
    loss = lossFn(pred, y)
    print('Ошибка на ' + str(i+1) + ' итерации: ', loss.item())
    loss.backward()
    optimizer.step()

with torch.no_grad():
    pred = linear(X)

pred = torch.Tensor(np.where(pred >=0, 1, -1).reshape(-1,1))
err = sum(abs(y-pred))/2
print('\nОшибка (количество несовпавших ответов): ')
print(err)

# Задание 1 (6 вар)
t = torch.rand(5, 3, dtype=torch.float32)
print("t:")
print(t)

t_pow = torch.pow(t, 3)
print("\nt^3:")
print(t_pow)

rand = random.randint(1, 11)
t_mul = t_pow * rand
print("\nt^3 * rand:")
print(t_mul, rand)

t_exp = t_mul.exp()
print("\nexp(t^3 * rand):")
print(t_exp)

t_exp.requires_grad = True

t_exp.sum().backward() 

print("\nПроизводная по х:")
print(t_exp.grad)


