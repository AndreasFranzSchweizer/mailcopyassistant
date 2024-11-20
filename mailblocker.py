import sys
import re
import pyperclip
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QMessageBox

class EmailSplitterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("E-Mail Splitter")
        
        # Layout und Widgets
        layout = QVBoxLayout()
        
        self.label = QLabel("Gib die E-Mail-Adressen ein (optional in Hochkommas oder Anführungszeichen, durch Leerzeichen oder Tabs getrennt):")
        layout.addWidget(self.label)
        
        self.input_field = QTextEdit()
        layout.addWidget(self.input_field)
        
        self.process_button = QPushButton("E-Mails in Gruppen zu je 50 aufteilen")
        layout.addWidget(self.process_button)
        
        self.output_buttons_layout = QHBoxLayout()
        layout.addLayout(self.output_buttons_layout)
        
        self.setLayout(layout)
        
        # Verbindung des Buttons zur Funktion
        self.process_button.clicked.connect(self.split_emails)
    
    def split_emails(self):
        # Text aus dem Eingabefeld holen
        input_text = self.input_field.toPlainText()
        
        # Regex für E-Mail-Adressen mit oder ohne einfache/doppelte Anführungszeichen
        emails = re.findall(r"(?:'([^']*)'|\"([^\"]*)\"|([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}))", input_text)
        
        # Extrahiere die gefundenen E-Mails aus den Gruppen und flache die Liste ab
        emails = [email[0] or email[1] or email[2] for email in emails]
        
        if not emails:
            QMessageBox.warning(self, "Warnung", "Keine gültigen E-Mail-Adressen gefunden.")
            return
        
        # E-Mails in Gruppen von 50 aufteilen
        self.email_groups = [emails[i:i + 50] for i in range(0, len(emails), 50)]
        
        # Vorherige Buttons entfernen, falls vorhanden
        for i in reversed(range(self.output_buttons_layout.count())): 
            widget_to_remove = self.output_buttons_layout.itemAt(i).widget()
            self.output_buttons_layout.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()
        
        # Buttons zum Kopieren jeder Gruppe hinzufügen
        for i, group in enumerate(self.email_groups, start=1):
            button = QPushButton(f"Gruppe {i} kopieren")
            button.clicked.connect(lambda checked, grp=group: self.copy_to_clipboard(grp))
            self.output_buttons_layout.addWidget(button)
    
    def copy_to_clipboard(self, group):
        # E-Mails der Gruppe durch Semikolon getrennt in die Zwischenablage kopieren
        group_text = "; ".join(group)
        pyperclip.copy(group_text)
        QMessageBox.information(self, "Kopiert", "Die Gruppe wurde in die Zwischenablage kopiert.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailSplitterApp()
    window.show()
    sys.exit(app.exec())
