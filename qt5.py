import sys
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QComboBox, QHBoxLayout, QDateEdit

class DateRangeSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('选择日期范围')
        self.setGeometry(100, 100, 400, 200)  # Set window size

        self.years = [str(year) for year in range(2020, 2026)]
        self.months = [f"{month:02}" for month in range(1, 13)]

        # Combo boxes
        self.startYearComboBox = QComboBox(self)
        self.startMonthComboBox = QComboBox(self)
        self.startDayComboBox = QComboBox(self)

        self.endYearComboBox = QComboBox(self)
        self.endMonthComboBox = QComboBox(self)
        self.endDayComboBox = QComboBox(self)

        self.startYearComboBox.addItems(self.years)
        self.startMonthComboBox.addItems(self.months)

        self.endYearComboBox.addItems(self.years)
        self.endMonthComboBox.addItems(self.months)

        # Set default date as today
        today = datetime.datetime.today()
        self.startYearComboBox.setCurrentText(str(today.year))
        self.startMonthComboBox.setCurrentText(f"{today.month:02}")
        self.endYearComboBox.setCurrentText(str(today.year))
        self.endMonthComboBox.setCurrentText(f"{today.month:02}")

        # Connect signals
        self.startYearComboBox.currentTextChanged.connect(lambda: self.update_days(self.startYearComboBox, self.startMonthComboBox, self.startDayComboBox))
        self.startMonthComboBox.currentTextChanged.connect(lambda: self.update_days(self.startYearComboBox, self.startMonthComboBox, self.startDayComboBox))

        self.endYearComboBox.currentTextChanged.connect(lambda: self.update_days(self.endYearComboBox, self.endMonthComboBox, self.endDayComboBox))
        self.endMonthComboBox.currentTextChanged.connect(lambda: self.update_days(self.endYearComboBox, self.endMonthComboBox, self.endDayComboBox))

        # Trigger the update once during initialization
        self.update_days(self.startYearComboBox, self.startMonthComboBox, self.startDayComboBox)
        self.update_days(self.endYearComboBox, self.endMonthComboBox, self.endDayComboBox)

        self.resultLabel = QLabel("已选择的日期范围:", self)
        self.submitButton = QPushButton('提交', self)
        self.submitButton.clicked.connect(self.pick_dates)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("开始日期:", self))

        start_date_layout = QHBoxLayout()
        start_date_layout.addWidget(self.startYearComboBox)
        start_date_layout.addWidget(self.startMonthComboBox)
        start_date_layout.addWidget(self.startDayComboBox)

        layout.addLayout(start_date_layout)
        layout.addWidget(QLabel("结束日期:", self))

        end_date_layout = QHBoxLayout()
        end_date_layout.addWidget(self.endYearComboBox)
        end_date_layout.addWidget(self.endMonthComboBox)
        end_date_layout.addWidget(self.endDayComboBox)

        layout.addLayout(end_date_layout)
        layout.addWidget(self.submitButton)
        layout.addWidget(self.resultLabel)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def update_days(self, year_combobox, month_combobox, day_combobox):
        year = int(year_combobox.currentText())
        month = int(month_combobox.currentText())

        if month in [1, 3, 5, 7, 8, 10, 12]:
            days = 31
        elif month in [4, 6, 9, 11]:
            days = 30
        else:
            # February
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):  # leap year
                days = 29
            else:
                days = 28

        day_combobox.clear()
        day_combobox.addItems([f"{day:02}" for day in range(1, days + 1)])

    def pick_dates(self):
        start_date = datetime.date(int(self.startYearComboBox.currentText()), int(self.startMonthComboBox.currentText()), int(self.startDayComboBox.currentText()))
        end_date = datetime.date(int(self.endYearComboBox.currentText()), int(self.endMonthComboBox.currentText()), int(self.endDayComboBox.currentText()))

        if end_date < start_date:
            self.resultLabel.setText("结束日期不能早于开始日期")
        else:
            self.resultLabel.setText(f"已选择的日期范围: {start_date} 到 {end_date}")

            # Return the selected start and end dates
            return start_date, end_date

app = QApplication(sys.argv)
window = DateRangeSelector()
window.show()
sys.exit(app.exec_())
