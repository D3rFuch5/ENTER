import csv
import src.Exceptions


def read_in_csv(data_path):
    """
    Methode liest die Datei unter dem übergebenen Pfad aus und gibt die eingelesenen Daten zurück
    :param data_path: Pfad der zu lesenden csv-Datei
    :return: 2 Elemente: 1. Zeile des eingelesenenen Datensatzes(Header)
                         2. restliche eingelesene Daten als Liste von Listen
    """
    # Öffnet die Datei unter dem übergebenen Pfad
    read_in_data_file = open(data_path, encoding='utf-8')

    # Erstellen des csv-Readers. Das erwartete Trennzeichen lauter ;
    csvreader = csv.reader(read_in_data_file, delimiter=';')

    # Liste zur Speicherung der Daten
    read_in = []

    # Einlesen der Daten
    for row in csvreader:
        read_in.append([data for data in row])

    if not read_in:
        raise src.Exceptions.EmptyFileException

    return read_in[0], read_in[1:]
