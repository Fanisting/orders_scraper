import sys
from PyQt5.QtWidgets import QApplication
from qt5 import DateRangeSelector

def main():
    app = QApplication(sys.argv)
    window = DateRangeSelector()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
