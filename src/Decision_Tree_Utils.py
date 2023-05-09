import copy
import math


def calculate_best_attribute(split_criterion, header, data):
    """
    Bestimmt aus den übergebenen Daten das beste Attribut für den Split und gibt dieses zurück
    :param split_criterion: Splitkriterium, nach welchem dar Informationsgewinn berechnet werden soll
    :param header: Liste der betrachteten Attribute
    :param data: zu den Attributen gehörende Spalten mit den Attributwerten
    :return: bestes Attribut
    """
    information_gains = calculate_information_gains(split_criterion=split_criterion,
                                                    header=header, data=data)
    return max(information_gains, key=information_gains.get), information_gains


def split_data_by_attribute(dataset, split_attribute):
    """
    Teilt den übergebenenen Datensatz(header und data) entsprechend der Attributwerte des split_attribut auf und
    gibt eine Liste mit den Teildatensätzen zurück
    :param dataset: Aufzuteilender Datensatz bestehend aus Headerzeile und Daten
    :param split_attribute: Attribut nach dessen Attributwerten aufgeteilt werden soll
    :return: Liste der aufgeteilten Datendatensätze (header und data)
    """
    # Zelegen des Datensatzes in Header-Zeile und Daten
    header = [x for x in dataset[0]]
    data = copy.deepcopy(dataset[1:])

    # Bestimmen des Index des Attributs, nach dem aufgeteilt werden soll
    index_of_attribute = header.index(split_attribute)

    # Umwandlung von Zeilen in Spalten um jeweils die Einträge zu einem Attribut als Spalte/Liste zu haben
    inverted_data = [d for d in zip(*data)]

    # Bestimmung der Spalte des Attributs, nach dem aufgeteilt werden soll
    column_of_split_attribute = inverted_data[index_of_attribute]

    # Attributwerte des Split-Attributs ohne Duplikate
    values_split_attribute = unique_list(column_of_split_attribute)
    # Sortieren der Liste um immer ein deterministisches Baumlayout zu bekommen
    values_split_attribute.sort()

    # Liste für die aufgeteilten Datensätze
    splitted = []

    # Aufteilen von data nach den Attributwerten des Split-Attributs
    for attr_value in values_split_attribute:
        temp = []
        for d in data:
            if d[index_of_attribute] == attr_value:
                temp.append(d)
        splitted.append([attr_value, temp])

    # Löschen der Spalte split_attribute in allen Teildatensätzen
    for splitset in splitted:
        for set in splitset[1]:
            set.pop(index_of_attribute)

    header.pop(index_of_attribute)

    # Anfügen der reduzierten Headerzeile an jeden Teildatensatz
    for i in range(len(splitted)):
        splitted[i][1] = [header] + splitted[i][1]

    return splitted


def split_criterion_misclassification_error(dict_labels, number_of_elements):
    return (number_of_elements - max(dict_labels.values())) / number_of_elements


def split_criterion_misclassification_count(dict_labels, number_of_elements):
    return number_of_elements - max(dict_labels.values())


def split_criterion_gini_impurity(dict_labels, number_of_elements):
    gini_sum = 0
    for value in dict_labels.values():
        gini_sum += (value / number_of_elements) ** 2
    return 1-gini_sum


def split_criterion_entropy(dict_labels, number_of_elements):
    entropy = 0
    for value in dict_labels.values():
        entropy += (value / number_of_elements) * math.log2(value / number_of_elements)
    return -1 * entropy


def calculate_information_gains(split_criterion, header, data):
    information_gains = {}
    for i in range(len(header) - 1):
        information_gains[header[i]] = calculate_information_gain_for_attribute(index_of_attribute=i,
                                                                                split_criterion=split_criterion,
                                                                                data=data)
    return information_gains


def calculate_information_gain_for_attribute(index_of_attribute, split_criterion, data):
    # Informationsgehalt vor dem Aufteilen für den übergebenen Datensatz data unter Verwendung des übergebenen
    # Split-Kriteriums
    information_content_before_split = split_criterion(countOccourence([x[-1] for x in data]), len(data))

    information_content_after_split = 0
    # Attributwerte des zu berechnenden Attributs ohne Duplikate
    unique_values_attribute = unique_list([x[index_of_attribute] for x in data])

    # Berechnet den Informationsgehalt für jeden Attributwert des gewählten Attributs
    for u in unique_values_attribute:
        label_values_for_current_attribute_value = [x[-1] for x in data if x[index_of_attribute] == u]
        number_of_elements_current_attribut_value = len(label_values_for_current_attribute_value)
        # Falls nur die Fehlklassifikationen an sich gezählt werden, kürzt sich in der Formel die
        # Gewichtung und die Gesamtanzahl der Elemente; Man kann also mit 1 gewichten
        if split_criterion == split_criterion_misclassification_count:
            weighting_factor = 1
        else:
            weighting_factor = number_of_elements_current_attribut_value / len(data)

        content_split_criterion = split_criterion(countOccourence(label_values_for_current_attribute_value),
                                                  number_of_elements_current_attribut_value)

        information_content_after_split += (weighting_factor * content_split_criterion)


    information_gain = information_content_before_split - information_content_after_split

    # Behandlung von negativen Informationsgewinnen aufgrund von Rundungsfehler in der Darstellung als float
    if information_gain < 0:
        information_gain = 0

    return information_gain


def countOccourence(list_to_count):
    k = {}
    for i in list_to_count:
        if i in k:
            k[i] += 1
        else:
            k[i] = 1

    return k


def unique_list(list_with_duplicates):
    return list(set(list_with_duplicates))


def stop_criterion_is_dataset_pure(label_column):
    """
    Bestimmt, ob die gebene Liste rein ist.
    :param label_column: Label-Spalte des Datensatzes als Liste ohne Header-Element
    :return: True, wenn die Spalte rein ist, Sonst False
    """
    # return len(countOccourence(label_column).keys()) == 1
    return len(unique_list(label_column)) == 1


def stop_criterion_no_attributes_to_split_left(dataset):
    return len(dataset[0]) < 2


def stop_criterion_max_tree_depth_reached(current_depth, max_depth):
    return current_depth == max_depth


def stop_criterion_element_number_too_small(current_element_number, min_element_number):
    return current_element_number < min_element_number

def stop_criterion_purity_level_reached(min_purity_level, number_of_elements_in_max_class, number_of_elements_in_node):
    return min_purity_level <= (number_of_elements_in_max_class/number_of_elements_in_node)*100
