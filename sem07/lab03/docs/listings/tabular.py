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

        self.position = SYMBOLS_PER_PAGE * page + COLS_PER_ROW * row + column


    def GenerateNumber(self, digits=1):
        num = -1
        with open("randseq/data/digits.txt", "r") as f:
            notRead = True

            while notRead:
                f.seek(self.position, 0)
                num = int(f.read(digits))

                if num // (10 ** (digits - 1)) >= 1:
                   notRead = False

                self.position += COLS_PER_ROW

                if self.position > SYMBOLS_NUMBER - 1:
                    self.position %= SYMBOLS_NUMBER
                    self.position += 1

        return num
