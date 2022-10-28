# Защита

> Вольный пересказ по памяти, скорее всего, с ошибками, возможно грубыми.
> Поэтому данный материал больше для ознакомления и наведения на нужные мысли.

## Какие значения у f(0), f(1), f_max, u(0), u(1)?

Запусти программу на значениях из методы.

## Увеличивайте k = 8e3, 8e2...

На **8e2** появляются отрицательные значения `u`, а по физическому смыслу
объемная плотность не может быть отрицательной.

### Почему? Где ошибка?

Накапливается погрешность в разности `Up - u`.

### Как исправить?

На каждом шаге проверять **неотрицательность???** `u`, если
она не выполняется возвращаемся на шаг назад, полагаем `u_предыдущее = Up` и
повторяем.

> P. S. Вот это по-хорошему надо реализовать в коде до сдачи.

## Как тестируем?

Сравнение с физическими данными (уже не помню про что тут конкретно было).

Сравнеие с другими методами (неявный Эйлера, неявный трапеций).

### Какая система уравнений в итоге получается? Как ее решать?

Получается линейная система уравнений. Для решения много способов:

* метод Гаусса;
* метод Крамера;
* и тд.

(Зашел разговор про определители: какая сложность у стандартного алгоритма
(`n!`), поэтому считаться будет долго (очень долго) даже при малых размерах
матриц, поэтому лучше считать его через приведение к треугольному виду, которого
сложность `n^3`.)

> Теперь можно идти сдавать lisp Юрию Владимировичу ;)

---

Сравнение с аналитическим решением

(Можно использователь ещё приближенные методы (Пикара, например), по этим
методам тоже были вопросы)

### Как получить аналитическое решение?

Надо привести систему к одному дифференциальному уравнению второго порядка.

F у нас выражено, поэтому просто подставляем первое уравнение во второе и
получаем нужное нам уравнение.

### Как решить?

Для аналитического решения надо принять коэффициент k за константу и решить.
(решать не надо)

### Программа все ещё работает с переменным k.
### Как сделать его константой меняя только начальные условия (нельзя делать изменений в коде)?

Можно положить `p=0`.

`k` зависит от температуры, там стоит коэффициент перед `z` `Tw - T0`, если
положить заданные температурами равными, то `T` будет равно `T0`.

### Как теперь выразить краевые условия? F то у нас больше нет.

Используем исходную систему.

`k` считаем константой, поэтому можно просто поставить краевые условия в первое
уравнение системы и выразить `du/dz`.

Должно получиться: `u'(0) = 0` и `u'(1) = C * u(1)`, где `C` -- константа (она
просто выражается из составленного уравнения)

### Подберите функцию u0 для метода коллокаций / метода Галеркина.

Суть в том, что сумма функций с коэффициентами (см. методу) в краевых точках
равна 0.

Поэтому `u` принимается равным `u_0` и надо подобрать функцию, которая
удовлетворяет уравнениям:

```
u_0'(0) = 0
u_0'(1) = C * u_0(1)
```
