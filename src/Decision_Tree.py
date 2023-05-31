import graphviz
import os

import src.Decision_Tree_Utils as Decision_Tree_Utils
import src.Color_Picker as Color_Picker


class DTree:
    split_criterion_MISCLASSIFICATION_COUNT = "Fehlklassifikationen zählen"
    split_criterion_MISCLASSIFICATION_ERROR = "Fehlklassifikationsrate"
    split_criterion_GINI_IMPURITY = "Gini-Impurity"
    split_criterion_ENTROPY = "Entropie"

    def __init__(self, dataset, max_tree_depth, min_element_number_for_node, min_purity_level,
                 selected_split_criterion, split_only_for_information_gain_greater_zero):
        self.tree_graphic = None
        self.root = None
        Node.node_number = 0
        label_column = [row[-1] for row in dataset[1:]]

        dict_occurrences_labels = Decision_Tree_Utils.countOccourence(label_column)
        number_of_elements_in_max_class = max(dict_occurrences_labels.values())

        # Datensatz bereits rein oder es gibt keine Attribute außer dem Label...
        # Der Baum besteht dann nur aus dem Wurzelknoten
        if Decision_Tree_Utils.stop_criterion_is_dataset_pure(label_column=label_column) \
                or Decision_Tree_Utils.stop_criterion_no_attributes_to_split_left(dataset=dataset) \
                or Decision_Tree_Utils.stop_criterion_max_tree_depth_reached(current_depth=0, max_depth=max_tree_depth) \
                or Decision_Tree_Utils.stop_criterion_element_number_too_small(current_element_number=len(dataset) - 1,
                                                                               min_element_number=min_element_number_for_node) \
                or Decision_Tree_Utils.stop_criterion_purity_level_reached(min_purity_level=min_purity_level,
                                                                           number_of_elements_in_max_class=number_of_elements_in_max_class,
                                                                           number_of_elements_in_node=len(dataset) - 1):
            label_of_max_class = max(dict_occurrences_labels, key=dict_occurrences_labels.get)
            self.root = LeaveNode(attribute=label_of_max_class, edge_label="", dataset=dataset,
                                  elements_in_max_class=number_of_elements_in_max_class)


        # Regulärer Fall, wenn der Datensatz weiter aufgesplittet wird
        else:
            if selected_split_criterion == self.split_criterion_MISCLASSIFICATION_ERROR:
                split_criterion_for_tree = Decision_Tree_Utils.split_criterion_misclassification_error
            elif selected_split_criterion == self.split_criterion_GINI_IMPURITY:
                split_criterion_for_tree = Decision_Tree_Utils.split_criterion_gini_impurity
            elif selected_split_criterion == self.split_criterion_ENTROPY:
                split_criterion_for_tree = Decision_Tree_Utils.split_criterion_entropy
            else:
                # Standard: Fehler zählen
                split_criterion_for_tree = Decision_Tree_Utils.split_criterion_misclassification_count

            best_attribute, information_gain_best_attribute, information_gains = \
                Decision_Tree_Utils.calculate_best_attribute(split_criterion=split_criterion_for_tree,
                                                             header=dataset[0],
                                                             data=dataset[1:])
            # Unterscheidung, dass bei nur bei einem echten Informationsgewinn weiter aufgeteilt wird
            # Falls der Informationsgewinn 0 ist, wird ein Blatt mit dem maximal vorkommenden Label erzeugt
            if split_only_for_information_gain_greater_zero == 1 and information_gain_best_attribute == 0:
                label_of_max_class = max(dict_occurrences_labels, key=dict_occurrences_labels.get)
                self.root = LeaveNode(attribute=label_of_max_class, edge_label="", dataset=dataset,
                                      elements_in_max_class=number_of_elements_in_max_class)
            # Falls die entsprechende Auswahl nicht aktiviert oder der Informationsgewinn größer 0 ist, wird weiter
            # aufgeteilt
            else:
                self.root = InnerNode(attribute=best_attribute, information_gains=information_gains, edge_label="",
                                      dataset=dataset, elements_in_max_class=number_of_elements_in_max_class)

                splitted_data = Decision_Tree_Utils.split_data_by_attribute(self.root.node_dataset, best_attribute)
                for d_elm in splitted_data:
                    self.root.node_children.append(self.root.build_tree(dataset=d_elm[1], edge_label=d_elm[0],
                                                                        split_criterion=split_criterion_for_tree,
                                                                        current_tree_depth=1,
                                                                        max_tree_depth=max_tree_depth,
                                                                        min_element_number_for_node=min_element_number_for_node,
                                                                        min_purity_level=min_purity_level,
                                                                        split_only_for_information_gain_greater_zero=split_only_for_information_gain_greater_zero))

    def print_tree_preorder(self):
        self.root.print_tree_preorder()

    def build_tree_graphic(self):
        if os.name == 'nt':
            dir = ".\Grafiken"
        # posix für Linux und MacOS
        else:
            dir = "./Grafiken"
        self.tree_graphic = graphviz.Graph(filename="calculated_tree", directory=dir,
                                           format='png')
        self.tree_graphic.graph_attr['dpi'] = "100"
        label_column = [row[-1] for row in self.root.node_dataset[1:]]
        labels = Decision_Tree_Utils.unique_list(label_column)
        # Sicherstellung einer deterministischen Farbzuordnung.
        # unique_list liefert nicht immer die gleiche Reihenfolge
        labels.sort()
        leaf_colors_dict = dict(zip(labels, Color_Picker.get_color_List(len(labels))))

        self.root.build_tree_graphic(graphic=self.tree_graphic, color_dictionary=leaf_colors_dict)
        self.tree_graphic.render(view=False)

    def search_by_node_number(self, node_number):
        if self.root is None:
            return None
        else:
            return self.root.search_by_node_number(node_number)

    def calculate_labels_test_data(self, testdataset):
        header = testdataset[0]
        testdata = testdataset[1:]
        calculated_labels_for_test_data = []

        for testset in testdata:
            calculated_labels_for_test_data.append(self.calculate_label(dict(zip(header, testset))))
        return calculated_labels_for_test_data

    def calculate_label(self, dataset_dict):
        """
        Berechnet das Label mit Hilfe des aktuellen Baums(self) für den Datensatz dataset_dict
        :param dataset_dict: Datensatz als Dictionary, welcher von Baum ausgewertet werden soll. Die keys sind die
         Merkmalsbezeichnungen, die values die zugehörigen Werte
        :return: Das vom Baum passende, gefundene Label. Falls kein passendes Label gefunden werden kann, wird None
         zurückgegeben
        """
        if self.root is None:
            return None
        else:
            return self.root.calculate_label(dataset_dict)


class Node:
    node_number = 0

    def __init__(self, dataset, attribute, edge_label, elements_in_max_class=0):
        self.node_number = Node.node_number
        Node.node_number += 1
        # Bestes Attribut
        self.node_attribute = attribute

        self.node_number_of_elements_in_max_class = elements_in_max_class

        # Label der Kante, die in diesen Knoten führt
        self.node_edge_label = edge_label
        self.node_dataset = dataset
        self.node_children = []

    def build_tree(self, dataset, split_criterion, current_tree_depth, max_tree_depth, min_purity_level,
                   min_element_number_for_node, edge_label, split_only_for_information_gain_greater_zero):
        label_column = [d[-1] for d in dataset[1:]]
        dict_occurrences_labels = Decision_Tree_Utils.countOccourence(label_column)
        number_of_elements_in_max_class = max(dict_occurrences_labels.values())

        if Decision_Tree_Utils.stop_criterion_is_dataset_pure(label_column=label_column) \
                or Decision_Tree_Utils.stop_criterion_no_attributes_to_split_left(dataset=dataset) \
                or Decision_Tree_Utils.stop_criterion_max_tree_depth_reached(current_depth=current_tree_depth,
                                                                             max_depth=max_tree_depth) \
                or Decision_Tree_Utils.stop_criterion_element_number_too_small(current_element_number=len(dataset) - 1,
                                                                               min_element_number=min_element_number_for_node) \
                or Decision_Tree_Utils.stop_criterion_purity_level_reached(min_purity_level=min_purity_level,
                                                                           number_of_elements_in_max_class=number_of_elements_in_max_class,
                                                                           number_of_elements_in_node=len(dataset) - 1):
            label_of_max_class = max(dict_occurrences_labels, key=dict_occurrences_labels.get)
            return LeaveNode(attribute=label_of_max_class, edge_label=edge_label, dataset=dataset,
                             elements_in_max_class=number_of_elements_in_max_class)
        else:
            best_attribute, information_gain_best_attribute, information_gains = \
                Decision_Tree_Utils.calculate_best_attribute(split_criterion=split_criterion, header=dataset[0],
                                                             data=dataset[1:])
            # Unterscheidung, dass bei nur bei einem echten Informationsgewinn weiter aufgeteilt wird
            # Falls der Informationsgewinn 0 ist, wird ein Blatt mit dem maximal vorkommenden Label erzeugt
            if split_only_for_information_gain_greater_zero == 1 and information_gain_best_attribute == 0:
                label_of_max_class = max(dict_occurrences_labels, key=dict_occurrences_labels.get)
                return LeaveNode(attribute=label_of_max_class, edge_label=edge_label, dataset=dataset,
                                 elements_in_max_class=number_of_elements_in_max_class)
            # Falls die entsprechende Auswahl nicht aktiviert oder der Informationsgewinn größer 0 ist, wird weiter
            # aufgeteilt
            else:
                temp = InnerNode(attribute=best_attribute, information_gains=information_gains, edge_label=edge_label,
                                 dataset=dataset, elements_in_max_class=number_of_elements_in_max_class)

                splitted_data = Decision_Tree_Utils.split_data_by_attribute(dataset=temp.node_dataset,
                                                                            split_attribute=temp.node_attribute)
                for d_elm in splitted_data:
                    temp.node_children.append(temp.build_tree(dataset=d_elm[1], edge_label=d_elm[0],
                                                              split_criterion=split_criterion,
                                                              current_tree_depth=current_tree_depth + 1,
                                                              max_tree_depth=max_tree_depth,
                                                              min_element_number_for_node=min_element_number_for_node,
                                                              min_purity_level=min_purity_level,
                                                              split_only_for_information_gain_greater_zero=split_only_for_information_gain_greater_zero))
                return temp


class InnerNode(Node):
    def __init__(self, dataset, attribute, edge_label, information_gains=None, elements_in_max_class=0):
        super().__init__(attribute=attribute, edge_label=edge_label, dataset=dataset,
                         elements_in_max_class=elements_in_max_class)
        self.node_children = []
        self.node_information_gains = information_gains

    def print_tree_preorder(self):
        print(self.node_attribute)
        for child in self.node_children:
            child.print_tree_preorder()

    def build_tree_graphic(self, graphic, color_dictionary):
        graphic.node(name=str(self.node_number), label='<<FONT POINT-SIZE="10"> Nr. ' + str(
            self.node_number) + ' </FONT><BR ALIGN="LEFT"/>' + '<FONT POINT-SIZE="16">' + str(
            self.node_attribute) + '</FONT>>', shape="box", style="rounded, filled", fillcolor="#f5b50570")
        for c in self.node_children:
            graphic.edge(str(self.node_number), str(c.node_number), label=" " + str(c.node_edge_label) + "    ")
            c.build_tree_graphic(graphic=graphic, color_dictionary=color_dictionary)

    def search_by_node_number(self, node_number):
        if self.node_number == node_number:
            return self
        else:
            for child in self.node_children:
                temp = child.search_by_node_number(node_number)
                if temp is not None:
                    return temp
            return None

    def calculate_label(self, dataset_dict):
        # Liefert None, falls das node_attribute nicht in den Attributen des Testdatensatzes vorkommt,
        # sprich kein Abstieg in den Baum gefunden werden kann
        value_of_dataset_for_node_attribute = dataset_dict.get(self.node_attribute)
        for child in self.node_children:
            if child.node_edge_label == value_of_dataset_for_node_attribute:
                return child.calculate_label(dataset_dict)
        # Falls kein child gefunden wird, wird None zurückgegeben
        return None


class LeaveNode(Node):
    def __init__(self, attribute, dataset, edge_label, elements_in_max_class=0):
        super().__init__(attribute=attribute, edge_label=edge_label, dataset=dataset,
                         elements_in_max_class=elements_in_max_class)

    def print_tree_preorder(self):
        print(self.node_attribute)

    def build_tree_graphic(self, graphic, color_dictionary):
        temp = self.node_number_of_elements_in_max_class / (len(self.node_dataset) - 1)
        ratio_correct = round(temp * 100, 1)
        built_color_string = color_dictionary[self.node_attribute] + ";" + str(
            temp) + ": #99999970" + ";" + str(1 - temp)
        graphic.node(name=str(self.node_number), label='<<FONT POINT-SIZE="10"> Nr. ' + str(
            self.node_number) + ' </FONT><BR ALIGN="LEFT"/>' + '<FONT POINT-SIZE="16">' + str(
            self.node_attribute) + '</FONT><BR/><FONT POINT-SIZE="12">' + str(
            ratio_correct) + ' %</FONT>>', shape="box", style="striped", fillcolor=built_color_string)

    def search_by_node_number(self, node_number):
        if self.node_number == node_number:
            return self
        else:
            return None

    def calculate_label(self, dataset_dict):
        return self.node_attribute
