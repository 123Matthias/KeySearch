from View.main_page import MainPage
from Controller.main_page_controller import MainPageController


class Main:
    def __init__(self):
        self.main_page_controller = MainPageController()
        self.main_page = MainPage(self.main_page_controller)




if __name__ == "__main__":
    main_app = Main()  # mainloop läuft jetzt in der View