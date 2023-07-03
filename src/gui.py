from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog, \
    QFormLayout, QVBoxLayout, QWidget, QGroupBox, QComboBox
import sys
import json
from scrape_engine import ScrapeEngine, ScrapeEngineException


def load_user_agents(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        user_agents = data.get("user_agents", [])
        return user_agents


class ScrapeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scrap")
        self.setGeometry(100, 100, 500, 200)  # Set the window size

        # Create the main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Create form layout for input elements
        form_layout = QFormLayout()

        # URL input
        self.label_url = QLabel("Enter the URL to scrape:")
        self.entry_url = QLineEdit()
        self.entry_url.setPlaceholderText("URL")
        form_layout.addRow(self.label_url, self.entry_url)

        # Element name input
        self.label_element = QLabel("Enter the element name:")
        self.entry_element = QLineEdit()
        self.entry_element.setPlaceholderText("Element Name")
        form_layout.addRow(self.label_element, self.entry_element)

        # Class name input
        self.label_class = QLabel("Enter the class name (optional):")
        self.entry_class = QLineEdit()
        self.entry_class.setPlaceholderText("Class Name (Optional)")
        form_layout.addRow(self.label_class, self.entry_class)

        # ID name input
        self.label_id = QLabel("Enter the ID name (optional):")
        self.entry_id = QLineEdit()
        self.entry_id.setPlaceholderText("ID Name (Optional)")
        form_layout.addRow(self.label_id, self.entry_id)

        # User agent dropdown
        self.label_user_agent = QLabel("Select User Agent:")
        self.combo_user_agent = QComboBox()
        form_layout.addRow(self.label_user_agent, self.combo_user_agent)

        self.user_agents = load_user_agents("src/user_agents.json")
        self.combo_user_agent.addItems(self.user_agents)

        # Create a group box and set the form layout as its layout
        group_box = QGroupBox()
        group_box.setLayout(form_layout)

        # Create the scrape button
        self.button_scrape = QPushButton("Scrape")
        self.button_scrape.clicked.connect(self.scrape)

        # Set the button background color
        self.button_scrape.setStyleSheet("background-color: #4CAF50; color: white;")

        # Add the elements to the main layout
        main_layout.addWidget(group_box)
        main_layout.addWidget(self.button_scrape)

        # Set the main layout as the layout for the main widget
        main_widget.setLayout(main_layout)

        # Set the central widget for the main window
        self.setCentralWidget(main_widget)

    def scrape(self):
        # Get user input
        url = self.entry_url.text()
        element_name = self.entry_element.text()
        class_name = self.entry_class.text()
        id_name = self.entry_id.text()
        user_agent = self.combo_user_agent.currentText()

        # Create an instance of the ScrapeEngine class
        engine = ScrapeEngine()
        engine.url = url
        engine.element_name = element_name
        engine.class_name = class_name
        engine.id_name = id_name
        engine.user_agent = user_agent

        try:
            # Prompt user to select output file
            file_dialog = QFileDialog()
            file_dialog.setDefaultSuffix(".csv")
            file_dialog.setNameFilter("CSV Files (*.csv);;All Files (*)")
            file_dialog.setAcceptMode(QFileDialog.AcceptSave)
            if file_dialog.exec_():
                filenames = file_dialog.selectedFiles()
                if filenames:
                    engine.filename = filenames[0]

            # Perform scraping and save to CSV
            engine.request()

            # Show a message box indicating completion
            QMessageBox.information(self, "Scraping Complete", "Scraping has been completed successfully.")

            # Clear the entry fields
            self.entry_url.clear()
            self.entry_element.clear()
            self.entry_class.clear()
            self.entry_id.clear()

        except ScrapeEngineException as e:
            # Show an error message box with the exception message
            QMessageBox.critical(self, "Scraping Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = ScrapeGUI()
    gui.show()
    sys.exit(app.exec_())
