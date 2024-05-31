import sys
from PyQt6.QtWidgets import QApplication, QFileDialog
from PyQt6.QtGui import QPixmap
from VueFirstApp import VueFirstApp
from ModeleFirstApp import ModeleFirstApp
from NewProjectApp import NewProjectApp

class Controller:
    def __init__(self) -> None:

        # Composants de la fenêtre
        self.vue = VueFirstApp()
        self.modele = ModeleFirstApp()
        self.new_window = None

        # Signaux
        self.vue.newClicked.connect(self.new)
        self.vue.loadClicked.connect(self.load)
        self.vue.saveClicked.connect(self.modele.save)
        self.vue.saveasClicked.connect(self.modele.save_as)
        self.vue.openClicked.connect(self.open)
        self.vue.main_widget.options.drawClicked.connect(self.draw_grid)
        self.vue.main_widget.options.clearClicked.connect(self.clear_grid)
        self.vue.main_widget.right.w_slider.gridMoved.connect(self.move_grid)
        self.vue.main_widget.right.h_slider.gridMoved.connect(self.move_grid)



    def new(self):
        self.new_window = NewProjectApp()
        self.new_window.show()

        self.new_window.infosSignal.connect(self.create_project)


    def create_project(self, d:dict):
        self.modele.current_infos = d
        self.update_vue(self.modele.current_infos["image"], self.modele.current_infos["project_name"], self.modele.current_infos["file_path"])


    def load(self):
        if self.modele.load_image():
            self.update_vue()


    def open(self):
        if self.modele.open():
            self.update_vue()


    def update_vue(self):
        self.vue.setWindowTitle(self.modele.current_infos["project_name"] + " - " + self.modele.current_infos["file_path"])

        self.vue.main_widget.right.grid.image = self.modele.current_infos["image"]
        self.vue.main_widget.right.grid.update_image()

        self.vue.main_widget.right.w_slider.setMaximum(self.vue.main_widget.right.grid.pixmap.width())
        self.vue.main_widget.right.h_slider.setMaximum(self.vue.main_widget.right.grid.pixmap.height())

        self.vue.main_widget.right.w_slider.setValue(self.modele.current_infos["x"])
        self.vue.main_widget.right.h_slider.setValue(self.modele.current_infos["y"])

        self.vue.main_widget.right.grid.clear_grid()
        self.vue.main_widget.right.grid.draw_grid(self.modele.current_infos["grid"], self.modele.current_infos["case_size"])

        self.vue.main_widget.options.row_number.setValue(len(self.modele.current_infos["grid"]))
        if self.modele.current_infos["grid"]:
            self.vue.main_widget.options.column_number.setValue(len(self.modele.current_infos["grid"][0]))
            self.vue.main_widget.options.case_size.setValue(self.modele.current_infos["grid"][0][0])


    def draw_grid(self, size:tuple):
        self.clear_grid()

        self.modele.create_grid(size)
        self.vue.main_widget.right.grid.draw_grid(self.modele.current_infos["grid"], self.modele.current_infos["case_size"])


    def clear_grid(self):
        self.vue.main_widget.right.grid.clear_grid()
        self.modele.current_infos["grid"].clear()


    def move_grid(self, value):
        sender = self.vue.sender()
        self.vue.main_widget.right.grid.clear_grid()

        if sender.property("type") == "x":
            self.vue.main_widget.right.grid.x = value
            self.modele.current_infos["x"] = value
        else:
            self.vue.main_widget.right.grid.y = value
            self.modele.current_infos["y"] = value

        self.vue.main_widget.right.grid.draw_grid(self.modele.current_infos["grid"], self.modele.current_infos["case_size"])

if __name__ == "__main__":

    app = QApplication(sys.argv)
    fenetre = Controller()
    sys.exit(app.exec())