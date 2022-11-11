from datetime import datetime

PAGES_NUMBER = 7
ROWS_PER_PAGE = 50
COLS_PER_ROW = 50

SYMBOLS_PER_PAGE = ROWS_PER_PAGE * COLS_PER_ROW
SYMBOLS_NUMBER = SYMBOLS_PER_PAGE * PAGES_NUMBER

class TabularGenerator:

    def __init__(self):
        page   = datetime.now().microsecond % PAGES_NUMBER
        row    = datetime.now().microsecond % ROWS_PER_PAGE
        column = datetime.now().microsecond % COLS_PER_ROW

        #page = 0
        #row = 0
        #column = 12

        self.position = SYMBOLS_PER_PAGE * page + COLS_PER_ROW * row + column


    def GetNumber(self, digits=1):
        num = -1
        with open("./data/digits.txt", "r") as f:
            notRead = True

            while notRead:
                # двигаем указатель в файле
                f.seek(self.position, 0)
                # читаем число
                num = int(f.read(digits))

                # проверяем не первые ли нули
                if num // (10 ** (digits - 1)) >= 1:
                   notRead = False

                # двигаем позицию
                self.position += COLS_PER_ROW

                if self.position > SYMBOLS_NUMBER - 1:
                    self.position %= SYMBOLS_NUMBER
                    self.position += 1

        return num


def main():
    generator = TabularGenerator()
    for i in range(20):
        print(generator.GetNumber(1))


if __name__ == "__main__":
    main()
