import sys
from PyQt5.QtWidgets import QApplication
from choose import ECommerceWindow

def main():
    app = QApplication(sys.argv)
    
    # Choose platform
    choose_platform = ECommerceWindow()  # Create DateRangeSelector instance
    choose_platform.show()
    
    sys.exit(app.exec_())  # Start event loop

if __name__ == "__main__":
    main()
