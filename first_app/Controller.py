import sys, os
from PyQt6.QtWidgets import QApplication, QMessageBox
from VueFirstApp import VueFirstApp
from ModeleFirstApp import ModeleFirstApp
from NewProjectApp import NewProjectApp
from Popup import Popup

class Controller:
    def __init__(self) -> None:

        # Composants de la fenêtre
        self.vue = VueFirstApp()
        self.modele = ModeleFirstApp()
        self.new_window = None
        self.popup = None

        # Signaux
        self.vue.newClicked.connect(self.new)
        self.vue.loadClicked.connect(self.load)
        self.vue.saveClicked.connect(self.modele.save)
        self.vue.saveasClicked.connect(self.modele.save_as)
        self.vue.openClicked.connect(self.open)
        self.vue.deleteClicked.connect(self.delete)
        self.vue.main_widget.options.drawClicked.connect(self.draw_grid)
        self.vue.main_widget.options.clearClicked.connect(self.clear_grid)
        self.vue.main_widget.right.w_slider.gridMoved.connect(self.move_grid)
        self.vue.main_widget.right.h_slider.gridMoved.connect(self.move_grid)
        self.vue.main_widget.right.grid.rectClicked.connect(self.new_popup)



    def new(self):
        self.new_window = NewProjectApp()
        self.new_window.show()

        self.new_window.infosSignal.connect(self.create_project)


    def create_project(self, d:dict):
        self.modele.current_infos = d
        self.update_vue()


    def load(self):
        if self.modele.load_image():
            self.update_vue()


    def open(self):
        if self.modele.open():
            self.update_vue()


    def delete(self):
        msgBox = QMessageBox()
        reponse = msgBox.warning(self.vue, "Attention", "Voulez-vous vraiment supprimer le projet en cours ?",
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reponse == QMessageBox.StandardButton.Yes:
            if self.modele.current_infos["file_path"]:
                os.remove(self.modele.current_infos["file_path"])
                self.modele.current_infos = {
                    "project_name": "Sans nom",
                    "project_author": "Sans nom",
                    "shop_name": "Sans nom",
                    "shop_address": "Sans nom",
                    "file_path": "",
                    "image": "../images/vide.png",
                    "case_size": 50,
                    "x": 0,
                    "y": 0,
                    "grid": [],
                    "pattern": {}
                }

                self.update_vue()



    def update_vue(self):
        self.vue.setWindowTitle(self.modele.current_infos.get("project_name", ""))

        self.vue.main_widget.right.grid.image = self.modele.current_infos["image"]
        self.vue.main_widget.right.grid.update_image()

        self.vue.main_widget.right.w_slider.setMaximum(self.vue.main_widget.right.grid.pixmap.width())
        self.vue.main_widget.right.h_slider.setMaximum(self.vue.main_widget.right.grid.pixmap.height())

        self.vue.main_widget.right.w_slider.setValue(self.modele.current_infos["x"])
        self.vue.main_widget.right.h_slider.setValue(self.modele.current_infos["y"])

        self.vue.main_widget.right.grid.clear_grid()
        self.vue.main_widget.right.grid.draw_grid(self.modele.current_infos["grid"], self.modele.current_infos["case_size"])

        self.vue.main_widget.options.case_size.setValue(self.modele.current_infos["case_size"])
        self.vue.main_widget.options.row_number.setValue(len(self.modele.current_infos["grid"]))
        if self.modele.current_infos["grid"]:
            self.vue.main_widget.options.column_number.setValue(len(self.modele.current_infos["grid"][0]))
        else:
            self.vue.main_widget.options.column_number.setValue(0)


    def draw_grid(self, size:tuple):
        self.clear_grid()

        self.modele.create_grid(size)
        self.modele.current_infos["case_size"] = size[2]
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


    def new_popup(self, coordinates:tuple):
        if self.popup:
            self.popup.close()

        self.popup = Popup(coordinates, self.modele.current_infos["pattern"], self.modele.current_infos["grid"][coordinates[0]][coordinates[1]])
        self.popup.show()

        self.popup.confirmClicked.connect(self.update_pattern)

    def update_pattern(self):
        if self.popup.x < len(self.modele.current_infos["grid"][0]) and self.popup.y < len(self.modele.current_infos["grid"]):
            if self.popup.left.products.currentItem():
                self.modele.current_infos["grid"][self.popup.y][self.popup.x] = [self.popup.left.categories.currentText(), self.popup.left.products.currentItem().text()]
            else:
                self.modele.current_infos["grid"][self.popup.y][self.popup.x] = None

            for info in self.popup.right.rect_infos:
                if info[1] == "green":
                    if info[0] == "left":
                        self.modele.current_infos["pattern"][(self.popup.y, self.popup.x)][(self.popup.y, self.popup.x-1)] = 1
                        self.modele.current_infos["pattern"][(self.popup.y, self.popup.x-1)][(self.popup.y, self.popup.x)] = 1
                    if info[0] == "right":
                        self.modele.current_infos["pattern"][(self.popup.y, self.popup.x)][(self.popup.y, self.popup.x+1)] = 1
                        self.modele.current_infos["pattern"][(self.popup.y, self.popup.x+1)][(self.popup.y, self.popup.x)] = 1
                    if info[0] == "down":
                        self.modele.current_infos["pattern"][(self.popup.y, self.popup.x)][(self.popup.y+1, self.popup.x)] = 1
                        self.modele.current_infos["pattern"][(self.popup.y+1, self.popup.x)][(self.popup.y, self.popup.x)] = 1
                    if info[0] == "up":
                        self.modele.current_infos["pattern"][(self.popup.y, self.popup.x)][(self.popup.y-1, self.popup.x)] = 1
                        self.modele.current_infos["pattern"][(self.popup.y-1, self.popup.x)][(self.popup.y, self.popup.x)] = 1
                elif info[1] == "red":
                    if info[0] == "left":
                        if (self.popup.y, self.popup.x-1) in self.modele.current_infos["pattern"][(self.popup.y, self.popup.x)].keys():
                            del self.modele.current_infos["pattern"][(self.popup.y, self.popup.x)][(self.popup.y, self.popup.x-1)]
                        if (self.popup.y, self.popup.x) in self.modele.current_infos["pattern"][(self.popup.y, self.popup.x-1)].keys():
                            del self.modele.current_infos["pattern"][(self.popup.y, self.popup.x-1)][(self.popup.y, self.popup.x)]
                    if info[0] == "right":
                        if (self.popup.y, self.popup.x+1) in self.modele.current_infos["pattern"][(self.popup.y, self.popup.x)].keys():
                            del self.modele.current_infos["pattern"][(self.popup.y, self.popup.x)][(self.popup.y, self.popup.x+1)]
                        if (self.popup.y, self.popup.x) in self.modele.current_infos["pattern"][(self.popup.y, self.popup.x+1)].keys():
                            del self.modele.current_infos["pattern"][(self.popup.y, self.popup.x+1)][(self.popup.y, self.popup.x)]
                    if info[0] == "down":
                        if (self.popup.y+1, self.popup.x) in self.modele.current_infos["pattern"][(self.popup.y, self.popup.x)].keys():
                            del self.modele.current_infos["pattern"][(self.popup.y, self.popup.x)][(self.popup.y+1, self.popup.x)]
                        if (self.popup.y, self.popup.x) in self.modele.current_infos["pattern"][(self.popup.y+1, self.popup.x)].keys():
                            del self.modele.current_infos["pattern"][(self.popup.y+1, self.popup.x)][(self.popup.y, self.popup.x)]
                    if info[0] == "up":
                        if (self.popup.y-1, self.popup.x) in self.modele.current_infos["pattern"][(self.popup.y, self.popup.x)].keys():
                            del self.modele.current_infos["pattern"][(self.popup.y, self.popup.x)][(self.popup.y-1, self.popup.x)]
                        if (self.popup.y, self.popup.x) in self.modele.current_infos["pattern"][(self.popup.y-1, self.popup.x)].keys():
                            del self.modele.current_infos["pattern"][(self.popup.y-1, self.popup.x)][(self.popup.y, self.popup.x)]


        self.popup.close()
        self.update_vue()



if __name__ == "__main__":

    app = QApplication(sys.argv)
    fenetre = Controller()
    sys.exit(app.exec())