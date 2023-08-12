# coding = UTF-8
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDesktopWidget, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QFont
# run platform
from taobao import taobao
from jd import jd
from pdd import pdd
from qt5 import DateRangeSelector

# Replace these with your actual functions
class ECommerceWindow(QMainWindow):
    def __init__(self, start_date, end_date):
        super().__init__()
        self.setWindowTitle("请选择您想要收集数据的电商平台")
        self.start_date = start_date
        self.end_date = end_date

        # Calculate the position to center the window
        self.center_window()

        # Set font for buttons
        font = QFont()
        font.setPointSize(16)  # Adjust the font size as desired

        self.taobao_button = QPushButton("淘宝/天猫", self)
        self.taobao_button.setFont(font)
        self.taobao_button.clicked.connect(self.run_taobao)

        self.jd_button = QPushButton("京东", self)
        self.jd_button.setFont(font)
        self.jd_button.clicked.connect(self.run_jd)

        self.pdd_button = QPushButton("拼多多", self)
        self.pdd_button.setFont(font)
        self.pdd_button.clicked.connect(self.run_pdd)

        # Use a vertical layout to center the buttons
        layout = QVBoxLayout()
        layout.addStretch()  # Add stretching space at the top
        layout.addWidget(self.taobao_button)
        layout.addWidget(self.jd_button)
        layout.addWidget(self.pdd_button)
        layout.addStretch()  # Add stretching space at the bottom

        # Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def center_window(self):
        # Calculate the position to center the window
        screen_geometry = QDesktopWidget().screenGeometry()
        window_size = self.geometry()
        x = (screen_geometry.width() - window_size.width()) // 2
        y = (screen_geometry.height() - window_size.height()) // 2
        self.setGeometry(x, y, window_size.width(), window_size.height())

    def run_taobao(self):
        self.close()
        self.show_finish_message("淘宝/天猫")
        app.exit()
        taobao(start_date, end_date)
        
    def run_jd(self):
        self.close()
        self.show_finish_message("京东")
        app.exit()
        jd(start_date, end_date)

        
    def run_pdd(self):
        self.close()
        self.show_finish_message("拼多多")
        app.exit()
        pdd(start_date, end_date)


    def show_finish_message(self, platform):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("开始自动化操作")
        if platform != "拼多多":
            msg_box.setText(f"我们将自动为您打开{platform}的登录界面\n请使用{platform}app内的扫码功能扫码登录您的账号!")
        else:
            msg_box.setText(f"我们将自动为您打开{platform}的登录界面\n请使用您拼多多账号绑定的手机号进行登录！（如果您还未绑定手机号,请先绑定）")
        msg_box.exec_()

if __name__ == "__main__":
    # Init the app
    app = QApplication(sys.argv)

    # Select date range
    window = DateRangeSelector()
    window.show()
    window.resize(600, 300)
    app.exec_()
    start_date, end_date = window.pick_dates()
    
    # Message about chosen date
    msg_box = QMessageBox()
    msg_box.setWindowTitle("日期选择结果")
    msg_box.setText(f"开始日期为{start_date}\n结束日期为{end_date}")
    msg_box.exec_()

    # Choose platform
    window = ECommerceWindow(start_date, end_date)
    window.show()
    app.exec_()

    