# sem_gap_big_lab
## Распознаватель блок-схем
Работу выполняют:
1. Кудрявцева Василиса
2. Пестряков Данил

## Постановка задачи
Разработать модель, которая по данному на вход изображению блок-схемы сгенерирует соответствующий код на языке Python. Модель должна распознавать основные элементы блок-схем, последовательность их расположения, в том числе текст, имеющийся внутри элементов или вблизи них; затем переводить элементы блок-схемы в подходящие языковые команды и собирать рабочую версию кода - прототип функции. Модель рассчитана на простые сценарии, реализуемые в рамках школьной программы. Приложение на основе такой модели может служить тренажером по программированию для формирования логического мышления и навыков реализации простых алгоритмов на языке Python.

### Данные
Ссылка на датасет: https://drive.google.com/drive/folders/1P9_cTfhcmz4IA0D2IqUWvfJURAXG7IUZ (размер датасета на 11.10.22 100 картинок)

### Сделано к текущей итерации
- Детектирование текста
- Распознавание текста 
- Детектирование фигур
- Распознавание фигур
- Детектирование отрезков, составляющих стрелки
- Распознавание отрезков
- Модель хранения данных, получаемых после парсинга блок-схемы
- Генератор кода

### Планируется к следующей итерации
- Генерация схем в нотации ДРАКОН с помощью https://drakonhub.com/ru/ 
- Разработка требований к входному изображению со схемой
- Обновление датасета
- Распознавание характерных элементов стрелок: углов, образуемых отрезками, и треугольных окончаний
- Перенос распаршенных данных в генератор кода

## Реализация
- На вход модели подается изображение блок-схемы
- На выходе получается прототип рабочей функции на языке Python 
___
### Парсинг изображения блок-схемы
Перевод изображения блок-схемы в программный код прототипа функции осуществляется следующим образом:
1. Текст. Требуется распознавать текст, находящийся внутри геометрических фигур (латинские буквы, символы математичсеких/лигических операций, знак вопроса, скобки) или рядом со стрелками (слова Да/Нет, Yes/No). Для детектирования текста используется предобученная модель CRAFT (на основе FCN), которая локализирует отдельные области символов, связывает обнаруженные символы с экземпляром текста и находит баундбоксы текста. Полученные баундбоксы расширяются на 1% для улучшения качества распознавания текста. Затем изображение обрабатывается средствами библиотеки OpenCV. Распознавание текста на изображении и его перевод в строковые символы осуществляется с помощью пакета PyTesseract.  
2. Фигуры. Перед распознаванием фигур происходит обработка изображения средствами OpenCV: стирание всего текста и морфологическая обработка - дилатация (растягивание, операция расширения) и эрозия (размывание, операция сужения). Цель этих операций - удаление шумов, изначально содержащихся в изображении или возникших в результате операции стирания текста. Детектирование фигур происходит путем применения функции findContours из OpenCV, возвращающей сгруппированные наборы точек, которые являются точками контура,  а баундбоксы - функцией minAreaRect, пытающейся найти прямоугольник максимального размера, который может вписаться в заданный замкнутый контур. Для улучшения качества распознавания баундбоксы расширяются нам 3%, затем к вырезанным изображениями добавляются белые поля шириной 20 пикселей. Распознавание фигур происходит так: на вырезанном изображении ищутся контуры разумной для геометрической фигуры площади, последний из таких контуров является минимальным по площади и самым "правильным" - по нему вычисляется аппроксимационный контур функцией approxPolyDP, количество сторон которого определяет форму фигуры (четырехугольник, пятиугольник, шестиугольник, овал)
3. Стрелки. Обнаруженные фигуры закрашиваются белыми прямоугольниками внутри расширенных баундбоксов, и итоговое изображение содержит только отрезки стрелок. Детектирование линий (отрезков) производится с помощью алгоритма Canny, а распознавание - нахождение координат точек начала и конца - с помощью метода Хафа, функцией HoughLinesP 
> Планируется реализация поиска других элементов схемы: угловых точек, образуемых отрезками стрелок и окончаний стрелок, а также перевод распаршенных данных в генератор кода. Угловые точки стрелок планируется рассчитывать путем нахождения ближайших друг к другу концов отрезков. Окончание стрелки планируется находить с помощью описанного выше метода распознавания фигур, либо с помощью темплейтов. Конечной целью является расчет координат центров тяжести элементов блок-схемы при известных баундбоксах - фактически координат расположения элемента. Зная взаимное расположение элементов, можно определить их принадлежность к тому или иному блоку кода. А зная тип фигуры можно восстановить команду или ключевое слово языка Python
___
### Форматы хранения элементов схемы
1. Текст. Координаты баундбоксов: x0 y0 x1 y1 x2 y3 x3 y3 - порядок обхода от верхнего левого угла по часовой стрелке (файл output_text_box.txt). Распознанный текст построчно (файл output_text.txt). Промежуточные данные: auto_text - области с автоматически найденными баундбоксы, corrected_text - области со слегка расширенными баундбоксами
2. Фигуры. Координаты баундбоксов: x0 y0 x1 y1 x2 y3 x3 y3 - порядок обхода от верхнего левого угла по часовой стрелке (файл output_figure_box.txt). Названия фигур построчно (output_figure.txt). Промежуточные данные: corrected_figures - области со слегка расширенными баундбоксами 
3. Стрелки. Координаты начала и конца отрезков, составляющих стрелки: x0 y0 x1 y1 (файл output_lines_box.txt), итоговое изображение edges.png
> Все директории с промежуточными результатами и полезными данными (координаты баундбоксов/линий) создаются автоматически
___
### Генерация кода по элементам схемы
1. Каждый шаг схемы представляется в виде некоторого класса, который наследуется от класса генератора кода
2. Генератор кода представляет собой дерево, которое хранит указатель на начало схемы, а также имеет метод генерации кода
3. Каждый класс, представляющий определенный шаг схемы также имеет метод генерации кода по данным, которые у него есть
4. Общими атрибутами всех классов шагов является указатель на следующий и предыдущий шаг, а также некоторые текстовые данные, нужные для генерации кода
5. По сути генерация кода классом генератора представляет из себя последовательный проход по экземплярам классов шагов и вызова у них встроенного метода генерации кода
6. Отметим, что некоторые шаги (начало условия или начало цикла) поражают новые деревья, поэтому код генерируется рекурсивно
