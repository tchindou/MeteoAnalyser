import sys
import sqlite3
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QComboBox, QMessageBox
from PySide6.QtGui import QIcon
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class DataAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Analyseur de Données')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.load_button = QPushButton('Charger un fichier TXT', self)
        self.load_button.clicked.connect(self.load_data)
        layout.addWidget(self.load_button)

        self.process_button = QPushButton('Traiter les données', self)
        self.process_button.clicked.connect(self.process_data)
        self.process_button.setEnabled(False)
        layout.addWidget(self.process_button)

        self.combo_box = QComboBox()
        self.combo_box.addItems(['Par heure', 'Par jour', 'Par mois'])
        self.combo_box.activated.connect(self.update_graph)
        layout.addWidget(self.combo_box)

        self.canvas = FigureCanvas(plt.figure(figsize=(8, 4)))
        layout.addWidget(self.canvas)

        self.central_widget.setLayout(layout)

        self.conn = sqlite3.connect('donnees.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS donnees (
                Date TEXT,
                Heures TEXT,
                Param1 REAL,
                Param2 REAL,
                Param3 REAL,
                Param4 REAL
            )
        ''')
        self.conn.commit()

    def load_data(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Charger un fichier TXT', '', 'Text Files (*.txt)',
                                                    options=options)
        if file_name:
            try:
                # Charger les données depuis le fichier TXT
                self.data = pd.read_csv(file_name, sep='|', header=None,
                                        names=['Date', 'Heures', 'Param1', 'Param2', 'Param3', 'Param4'])

                self.data['Date'] = self.data['Date'].str.strip()

                # Afficher un message de succès
                QMessageBox.information(self, 'Succès', 'Données chargées avec succès.')

                # Enregistrer les données dans la base de données (si nécessaire)
                self.data.to_sql('donnees', self.conn, if_exists='replace', index=False)

                # Activer le bouton de traitement (si nécessaire)
                self.process_button.setEnabled(True)
            except Exception as e:
                QMessageBox.warning(self, 'Erreur', f"Erreur lors du chargement des données : {e}")
        else:
            QMessageBox.warning(self, 'Avertissement', 'Aucun fichier chargé. Veuillez sélectionner un fichier TXT.')


    def process_data(self):
        if hasattr(self, 'data'):
            self.plot_data()

    def plot_data(self):
        if hasattr(self, 'data'):
            if 'Heures' in self.data.columns:
                fig, axes = plt.subplots(2, 1, figsize=(8, 6))

                axes[0].plot(self.data['Heures'], self.data['Param2'], label='Température')
                axes[0].plot(self.data['Heures'], self.data['Param3'], label='Humidité')
                axes[0].set_xlabel('Heures')
                axes[0].set_ylabel('Valeurs')
                axes[0].set_title('Variation de la température et de l\'humidité')
                axes[0].legend()

                axes[1].plot(self.data['Heures'], self.data['Param4'], label='Rayonnement')
                axes[1].set_xlabel('Heures')
                axes[1].set_ylabel('Rayonnement')
                axes[1].set_title('Variation du rayonnement')
                axes[1].legend()

                plt.tight_layout()

                self.canvas.figure = fig
                self.canvas.draw()
            else:
                QMessageBox.warning(self, 'Erreur', "La colonne 'Heures' n'existe pas dans les données.")
        else:
            QMessageBox.warning(self, 'Erreur', 'Aucune donnée à afficher.')

    def update_graph(self):
        selected_option = self.combo_box.currentText()

        if selected_option == 'Par heure':
            self.plot_data_by_hour()
        elif selected_option == 'Par jour':
            self.plot_data_by_day()
        elif selected_option == 'Par mois':
            self.plot_data_by_month()

    def plot_data_by_hour(self):
        if hasattr(self, 'data'):
            if 'Heures' in self.data.columns:
                fig, axes = plt.subplots(2, 1, figsize=(8, 6))

                axes[0].plot(self.data['Heures'], self.data['Param2'], label='Température')
                axes[0].plot(self.data['Heures'], self.data['Param3'], label='Humidité')
                axes[0].set_xlabel('Heures')
                axes[0].set_ylabel('Valeurs')
                axes[0].set_title('Variation de la température et de l\'humidité')
                axes[0].legend()

                axes[1].plot(self.data['Heures'], self.data['Param4'], label='Rayonnement')
                axes[1].set_xlabel('Heures')
                axes[1].set_ylabel('Rayonnement')
                axes[1].set_title('Variation du rayonnement')
                axes[1].legend()

                plt.tight_layout()

                self.canvas.figure = fig
                self.canvas.draw()
            else:
                QMessageBox.warning(self, 'Erreur', "La colonne 'Heures' n'existe pas dans les données.")
        else:
            QMessageBox.warning(self, 'Erreur', 'Aucune donnée à afficher.')

    def plot_data_by_day(self):
        if hasattr(self, 'data'):
            if 'Date' in self.data.columns:

                # Création du graphique
                fig, axes = plt.subplots(2, 1, figsize=(8, 6))
                axes[0].plot(self.data['Date'], self.data['Param2'], label='Température')
                axes[0].plot(self.data['Date'], self.data['Param3'], label='Humidité')
                axes[0].set_xlabel('Jours')
                axes[0].set_ylabel('Valeurs moyennes')
                axes[0].set_title('Variation moyenne de la température et de l\'humidité par jour')
                axes[0].legend()

                axes[1].plot(self.data['Date'], self.data['Param4'], label='Rayonnement')
                axes[1].set_xlabel('Jours')
                axes[1].set_ylabel('Rayonnement moyen')
                axes[1].set_title('Variation moyenne du rayonnement par jour')
                axes[1].legend()

                plt.tight_layout()

                self.canvas.figure = fig
                self.canvas.draw()
            else:
                QMessageBox.warning(self, 'Erreur', "La colonne 'Date' n'existe pas dans les données.")
        else:
            QMessageBox.warning(self, 'Erreur', 'Aucune donnée à afficher.')



    def plot_data_by_month(self):
        if hasattr(self, 'data'):
            if 'Date' in self.data.columns:

                self.data['Date'] = self.data['Date'].str.strip()
                self.data['Date'] = pd.to_datetime(self.data['Date'], format='%d/%m/%Y', dayfirst=True)

                print(self.data['Date'].dtype)

                monthly_data = self.data.groupby(self.data['Date'].dt.month).agg(
                    {
                        'Param2': 'mean',
                        'Param3': 'mean',
                        'Param4': 'mean',
                    }
                )

                fig, axes = plt.subplots(2, 1, figsize=(8, 6))

                axes[0].plot(monthly_data.index, monthly_data['Param2'], label='Température')
                axes[0].plot(monthly_data.index, monthly_data['Param3'], label='Humidité')
                axes[0].set_xlabel('Mois')
                axes[0].set_ylabel('Valeurs moyennes')
                axes[0].set_title('Variation moyenne de la température et de l\'humidité par mois')
                axes[0].legend()

                axes[1].plot(monthly_data.index, monthly_data['Param4'], label='Rayonnement')
                axes[1].set_xlabel('Mois')
                axes[1].set_ylabel('Rayonnement moyen')
                axes[1].set_title('Variation moyenne du rayonnement par mois')
                axes[1].legend()

                plt.tight_layout()

                self.canvas.figure = fig
                self.canvas.draw()
            else:
                QMessageBox.warning(self, 'Erreur', "La colonne 'Date' n'existe pas dans les données.")
        else:
            QMessageBox.warning(self, 'Erreur', 'Aucune donnée à afficher.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataAnalyzer()
    app.setWindowIcon(QIcon('./image/logo.jpg'))  # Remplacez './image/logo.jpg' par le chemin vers votre propre logo
    window.show()
    sys.exit(app.exec())

