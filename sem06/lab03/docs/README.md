# Вопросы при защите

> Если ответить почти сразу и почти правильно, долго мучить не будут

## В чем будет проблема, если левое краевое условие станет нелинейным?

Решаем задачу методом прогонки, поэтому, если левое краевное условие будет
нелинейным, мы не сможем определить начальные значения коэффициентов прогонки
(ksi и eta).

## Что тогда делать?

Пойти справа.

## А если справа тоже нелинейное?

~~Грустить~~

Тогда решать итерационно. Взять какое-то начальное распределение `y` (в лекциях
написано, что произвольно, но так, чтобы соотносилось с ожидаемым решением, как
это сделать я не знаю), расчитать начальные значения коэффициентов A, B, C, D.
На каждой следующей итерации использовать коэффициенты предыдущей, расчитывая
новые значения `y` и новые значения коэффициентов. Когда заканчивать итерации
приведено в
[лекции](https://github.com/Sunshine-ki/BMSTU6_Modeling/blob/main/lectures/01-04-2021-Лекция__8_Модели_ОДУ_Краевая_задача_Квазилинейные_схемы.pdf)

