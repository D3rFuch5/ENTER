import copy
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from itertools import product
import tkinter as tk
import os

import src.CSV_Reader as CSV_Reader
import src.Decision_Tree as Decision_Tree
import src.Decision_Tree_Utils as Decision_Tree_Utils
import src.GUI as GUI
import src.Exceptions as Exceptions
import src.Data_Sampler as Data_Sampler


class Main:
    # Generelle Anmerkung: data nur Daten, dataset = Header und Daten

    default_TREE_DEPTH = 5
    default_PURITY_LEVEL = 95
    default_MIN_ELEMENT_NUMBER = 1
    default_TRAINING_DATA_RATIO = 75
    default_NODE_NUMBER = 0

    tab_TRAINING_DATA = 0
    tab_DISPLAY_TREE = 1
    tab_TEST_PHASE = 2
    tab_CONFUSION_MATRIX = 3

    path_WINDOWS_default_image = ".\Grafiken\default_tree_image.png"
    path_MAC_default_image = "./Grafiken/default_tree_image.png"

    path_WINDOWS_calculated_tree_image = ".\Grafiken\calculated_tree.png"
    path_MAC_calculated_tree_image = "./Grafiken/calculated_tree.png"

    def __init__(self):
        self.my_Tree = None
        self.my_gui = GUI.GUI_Main_Window(self)
        # Anzeige der Baumansicht als Initialansicht
        self.my_gui.main_notebook.select(self.tab_DISPLAY_TREE)

        if os.name == 'nt':
            self.current_calculated_tree_image_path = self.path_WINDOWS_calculated_tree_image
            self.current_default_image_path = self.path_WINDOWS_default_image
        # posix für Linux und MacOS
        else:
            self.current_calculated_tree_image_path = self.path_MAC_calculated_tree_image
            self.current_default_image_path = self.path_MAC_default_image

        self.selected_filepath_data = ""
        self.header_used_training_data = []
        self.data_used_training_data = [[]]

        self.selected_filepath_test_data = ""
        self.header_used_test_data = []
        self.data_used_test_data = [[]]

        self.read_in_header = []
        self.read_in_dataset = [[]]

        # Statusvariable zum Speichern, ob die Testphase gerade aktiv
        self.test_phase_activated = False

        # Statusvariable zum Anzeigen des Hinweises zur autom. Datenaufteilung
        self.notification_data_sampler_displayed = False

    def call_open_file_training_data(self, lbl):
        # Dataset Window zurücksetzen und ausblenden
        if self.my_gui.node_details_window is not None:
            self.my_gui.node_details_window.close_node_details_window(main_gui=self.my_gui)

        # Einlesen des ausgewählten Dateipfads
        self.selected_filepath_data = askopenfilename(
            filetypes=[("CSV Files", "*.csv")])
        GUI.clear_treeview(treeview=self.my_gui.treeview_training_data)
        # Anzeige der Trainingsdatenansicht
        self.my_gui.main_notebook.select(self.tab_TRAINING_DATA)
        # Zurücksetzen der Baumanzeige
        self.my_Tree = None
        self.my_gui.enter_new_picture(img=tk.PhotoImage(file=self.current_default_image_path))
        try:
            self.read_in_header, self.read_in_dataset = CSV_Reader.read_in_csv(
                self.selected_filepath_data)
            lbl["text"] = f"{os.path.basename(self.selected_filepath_data)}"
            # Data Sampler ist aktiv
            if self.my_gui.use_data_sampling.get() == 1:
                self.header_used_training_data = self.read_in_header
                self.header_used_test_data = self.read_in_header
                self.data_used_training_data, self.data_used_test_data = self.data_sampling_split_data_by_entered_ratio(
                    data=copy.deepcopy(self.read_in_dataset))
            # Data Sampler nicht aktiv
            else:
                self.header_used_training_data = self.read_in_header
                self.data_used_training_data = self.read_in_dataset
            GUI.fill_treeview_with_data(treeview=self.my_gui.treeview_training_data,
                                        data=[self.header_used_training_data] + self.data_used_training_data)
        except Exceptions.EmptyFileException:
            err_msg = "Die eingelesene Datei war leer!"
            self.selected_filepath_data = ""
            self.header_used_training_data = []
            self.data_used_training_data = [[]]
            self.header_used_test_data = []
            self.data_used_test_data = [[]]
            self.my_gui.lbl_display_selected_filepath_training_data['text'] = ""
            messagebox.showerror(parent=self.my_gui.main_window, title="Fehler", message=err_msg)
        except Exception:
            err_msg = "Es ist ein Fehler aufgetreten!"
            if self.selected_filepath_data == "":
                err_msg = "Es wurde keine Datei ausgewählt!"
            self.selected_filepath_data = ""
            self.header_used_training_data = []
            self.data_used_training_data = [[]]
            self.header_used_test_data = []
            self.data_used_test_data = [[]]
            self.my_gui.lbl_display_selected_filepath_training_data['text'] = ""
            messagebox.showerror(parent=self.my_gui.main_window, title="Fehler", message=err_msg)

    def call_open_file_test_data(self, lbl):
        GUI.clear_treeview(treeview=self.my_gui.treeview_test_data)
        GUI.clear_treeview_without_header(treeview=self.my_gui.treeview_test_data_results)
        self.my_gui.main_notebook.hide(self.tab_CONFUSION_MATRIX)
        try:
            # Einlesen des ausgewählten Dateipfads
            self.selected_filepath_test_data = askopenfilename(
                filetypes=[("CSV Files", "*.csv")])
            self.header_used_test_data, self.data_used_test_data = CSV_Reader.read_in_csv(
                self.selected_filepath_test_data)
            lbl["text"] = f"{os.path.basename(self.selected_filepath_test_data)}"
            GUI.fill_treeview_with_data(treeview=self.my_gui.treeview_test_data,
                                        data=[self.header_used_test_data] + self.data_used_test_data)
        except Exceptions.EmptyFileException:
            err_msg = "Die eingelesene Datei war leer!"
            self.selected_filepath_test_data = ""
            self.header_used_test_data = []
            self.data_used_test_data = [[]]
            self.my_gui.lbl_display_selected_filepath_test_data['text'] = ""
            messagebox.showerror(parent=self.my_gui.main_window, title="Fehler", message=err_msg)
        except Exception:
            err_msg = "Es ist ein Fehler aufgetreten!"
            if self.selected_filepath_test_data == "":
                err_msg = "Es wurde keine Datei ausgewählt!"
            self.selected_filepath_test_data = ""
            self.header_used_test_data = []
            self.data_used_test_data = [[]]
            self.my_gui.lbl_display_selected_filepath_test_data['text'] = ""
            messagebox.showerror(parent=self.my_gui.main_window, title="Fehler", message=err_msg)

    def call_activate_testing_phase(self):
        if self.my_Tree is not None:
            self.test_phase_activated = not self.test_phase_activated
            self.my_gui.disable_inputs_training_phase(disable_inputs=self.test_phase_activated)
            # Testmodus soll aktiviert werden
            if self.test_phase_activated:
                self.my_gui.btn_initiate_testing["text"] = "Testmodus deaktivieren"
                # Anzeigen der bereits vorliegenden Testdaten durch den Data Sampler
                if self.my_gui.use_data_sampling.get() == 1:
                    GUI.fill_treeview_with_data(treeview=self.my_gui.treeview_test_data,
                                                data=[self.header_used_test_data] + self.data_used_test_data)
                    self.my_gui.btn_choose_test_data['state'] = tk.DISABLED
                    self.my_gui.lbl_display_selected_filepath_test_data[
                        'text'] = "  Automatisch aus den geladenen Daten entnommen."
                self.my_gui.main_notebook.add(child=self.my_gui.frm_display_test_phase_container)
                self.my_gui.main_notebook.select(self.tab_TEST_PHASE)
            # Testmodus soll deaktiviert werden
            else:
                # Zurücksetzen des Testmodus
                # Konfusionsmatrix und Gütemaß nicht, da dieser Tab erst bei erfolgreichem Training eingeblendet wird
                # und dann sowieso mit den aktuellen Daten gefüllt ist
                self.my_gui.btn_initiate_testing["text"] = "Testmodus aktivieren"

                GUI.clear_treeview(treeview=self.my_gui.treeview_test_data)
                GUI.clear_treeview_without_header(treeview=self.my_gui.treeview_test_data_results)

                self.my_gui.btn_choose_test_data['state'] = tk.NORMAL
                self.my_gui.lbl_display_selected_filepath_test_data['text'] = " "

                # Falls keine automatische Datenaufteilung aktiv ist, werden ggf. geladene Testdaten bei Deaktivierung
                # des Testmodus gelöscht
                if self.my_gui.use_data_sampling.get() != 1:
                    self.header_used_test_data = []
                    self.data_used_test_data = [[]]

                # Ausblenden der Tabs des Testmodus
                self.my_gui.main_notebook.hide(self.tab_TEST_PHASE)
                self.my_gui.main_notebook.hide(self.tab_CONFUSION_MATRIX)

        else:
            self.my_gui.show_window_node_details.set(0)
            messagebox.showerror(parent=self.my_gui.main_window, title="Fehler",
                                 message="Es ist aktuell kein Baum trainiert!")

    def call_perform_testing(self):
        if self.data_used_test_data != [[]]:
            GUI.clear_treeview_without_header(treeview=self.my_gui.treeview_test_data_results)
            # Zum ersten Element springen
            GUI.display_treeview_from_beginning(treeview=self.my_gui.treeview_test_data)

            label_column_test_data = [row[-1] for row in self.data_used_test_data]
            calculated_labels = self.my_Tree.calculate_labels_test_data(
                [self.header_used_test_data] + self.data_used_test_data)

            GUI.fill_treeview_with_calculated_labels(treeview=self.my_gui.treeview_test_data_results,
                                                     calculated_labels=calculated_labels,
                                                     label_column=label_column_test_data)

            unique_labels = Decision_Tree_Utils.unique_list([row[-1] for row in self.data_used_training_data])
            unique_labels.sort()
            confusion_matrix_entries, not_classifiable = calculate_confusion_matrix(trained_unique_labels=unique_labels,
                                                                                    actual_labels=label_column_test_data,
                                                                                    calculated_labels=calculated_labels)

            correct_class_elm, all_elm, precision = calculate_quality_measure_accuracy(confusion_matrix_entries,
                                                                                       not_classifiable)

            GUI.fill_text_widget_quality_criterion_precision(text_widget=self.my_gui.text_field_quality_criterion,
                                                             number_classified_correctly=correct_class_elm,
                                                             number_all=all_elm,
                                                             precision=precision,
                                                             not_classifiable=not_classifiable)
            # Erstellen der Liste der Eintragungen in die Konfusionsmatrix
            entries_confusion_matrix = [" "]
            for elm in unique_labels:
                entries_confusion_matrix.append(elm)
            for actual_label in unique_labels:
                entries_confusion_matrix.append(actual_label)
                for calculated_label in unique_labels:
                    entries_confusion_matrix.append(str(confusion_matrix_entries.get((actual_label, calculated_label))))

            # Konfusionsmatrix erstellen in dem übergebenen Frame erstellen
            GUI.build_confusion_matrix(containing_frame=self.my_gui.frm_confusion_matrix,
                                       number_of_labels=len(unique_labels),
                                       matrix_entries=entries_confusion_matrix,
                                       tk_label_list=self.my_gui.tk_label_list,
                                       tk_description_label_list=self.my_gui.tk_description_label_list)
            # Oberfläche mit aktueller Konfusionsmatrix aktualisieren und die Scrollbars, usw aktualisieren
            self.my_gui.update_display_confusion_matrix()
            # Einblenden des Tabs zur Anzeige der Konfusionsmatrix
            self.my_gui.main_notebook.add(child=self.my_gui.frm_display_confusion_matrix_container)
        else:
            messagebox.showerror(parent=self.my_gui.main_window, title="Fehler",
                                 message="Es sind keine Testdaten geladen!")

    def call_train_tree(self):
        # Sperren des Buttons während der Berechnung, falls diese länger dauert
        self.my_gui.btn_train_tree['state'] = tk.DISABLED
        self.my_gui.btn_train_tree.update()

        # Dataset Window zurücksetzen und ausblenden
        if self.my_gui.node_details_window is not None:
            self.my_gui.node_details_window.close_node_details_window(main_gui=self.my_gui)

        # Falls keine Daten geladen sind...
        if self.header_used_training_data == [] or self.data_used_training_data == [[]]:
            messagebox.showerror(parent=self.my_gui.main_window, title="Fehler", message="Es sind keine Daten geladen!")
        # Trainingsdaten liegen vor
        else:
            # Einlesen der Eingaben für die Hyperparameter. Bei fehlerhafter Eingabe eines Parameters ist err_msg != ""
            err_msg, entered_tree_depth, entered_purity_level, entered_min_element_number = self.check_inputs_train_tree()

            # Neu würfeln der automatischen Datenaufteilung
            # Nur wenn die Option des neu würfelns aktiv ist, wird bei Baumerstellung neu gewürfelt und es muss die
            # Eingabe der Trainingsdatenrate neu geprüft werden
            if self.my_gui.use_shuffle_on_tree_creation.get() == 1:
                error, entered_ratio = self.check_input_data_sampler_training_data_ratio()
                # Einlesen der neuen Trainingsdatenrate für die Datenaufteilung hat korrekt funktioniert
                if error == "":
                    # Die Header werden direkt bei Öffnen einer Datei oder Aktivierung des Datasamplers gesetzt.
                    # Es müssen also nur die Daten gesetzt werden.
                    self.data_used_training_data, self.data_used_test_data = Data_Sampler.split_data_according_to_ratio(
                        data=copy.deepcopy(self.read_in_dataset), ratio=entered_ratio, do_shuffle=True)
                    # Aktualisierung der Anzeige mit den aktuellen Daten
                    GUI.clear_treeview(treeview=self.my_gui.treeview_training_data)
                    GUI.fill_treeview_with_data(treeview=self.my_gui.treeview_training_data,
                                                data=[self.header_used_training_data] + self.data_used_training_data)
                # Falls keine korrekte Rate eingelesen werden konnte, bleiben die alten Trainingsdaten erhalten
                # und die Fehlermeldung wird ergänzt.
                else:
                    err_msg += error

            # Kein Fehler beim Einlesen der Hyperparameter.
            # Nicht ausgewählte Hyperparameter werden auf Wert gesetzt, der keinen Einfluss hat
            if err_msg == "":
                # Rückgabe -1, falls die Baumtiefe nicht ausgewählt.
                # Dann wird die maximale Baumtiefe auf die Anzahl der Attribute +1 gesetzt, was sicher
                # größer als die maximal mögliche Baumtiefe ist
                if entered_tree_depth == -1:
                    entered_tree_depth = len(self.header_used_training_data)

                # Rückgabe -1, falls die minimale Elementanzahl nicht ausgewählt.
                # Dann wird die minimale Elementanzahl auf 1 gesetzt.
                if entered_min_element_number == -1:
                    entered_min_element_number = 1

                # Rückgabe -1, falls das minimale Reinheitslevel nicht ausgewählt.
                # Dann wird das minimale Reinheitslevel auf 100 gesetzt.
                if entered_purity_level == -1:
                    entered_purity_level = 100
                try:
                    # Erstellen des Entscheidungsbaums
                    self.my_Tree = Decision_Tree.DTree(
                        dataset=[self.header_used_training_data] + self.data_used_training_data,
                        selected_split_criterion=self.my_gui.selected_split_criterion.get(),
                        max_tree_depth=entered_tree_depth,
                        min_element_number_for_node=entered_min_element_number,
                        min_purity_level=entered_purity_level)
                    # Erstellen der Grafik, welche den Entscheidungsbaum darstellt
                    self.my_Tree.build_tree_graphic()
                    # Anzeigen der Entscheidungsbaumgrafik in der Oberfläche
                    self.my_gui.enter_new_picture(
                        img=tk.PhotoImage(file=self.current_calculated_tree_image_path))
                except Exception:
                    self.my_Tree = None
                    self.my_gui.enter_new_picture(img=tk.PhotoImage(file=self.current_default_image_path))
                    # Entsperren des Buttons nach der Berechnung
                    self.my_gui.btn_train_tree['state'] = tk.NORMAL
                    messagebox.showerror(parent=self.my_gui.main_window, title="Fehler",
                                         message="Es ist ein Fehler aufgetreten!")
            else:
                self.my_Tree = None
                self.my_gui.enter_new_picture(img=tk.PhotoImage(file=self.current_default_image_path))
                messagebox.showerror(parent=self.my_gui.main_window, title="Fehler", message=err_msg)
        # Entsperren des Buttons nach der Berechnung
        self.my_gui.btn_train_tree['state'] = tk.NORMAL

        # Anzeige der Trainingsdatenansicht
        self.my_gui.main_notebook.select(self.tab_DISPLAY_TREE)

    def call_show_window_node_details(self):
        if self.my_Tree is not None:
            if self.my_gui.show_window_node_details.get() == 1:
                if self.my_gui.node_details_window is None:
                    self.my_gui.node_details_window = GUI.GUI_Node_Details_Window(self.my_gui, self)
                else:
                    self.my_gui.node_details_window.show_node_details_window()
            elif self.my_gui.node_details_window is not None:
                self.my_gui.node_details_window.close_node_details_window(main_gui=self.my_gui)
        else:
            self.my_gui.show_window_node_details.set(0)
            messagebox.showerror(parent=self.my_gui.main_window, title="Fehler",
                                 message="Es ist aktuell kein Baum trainiert!")

    def call_display_node_details(self):
        number_node_to_display = self.default_NODE_NUMBER
        GUI.clear_treeview(treeview=self.my_gui.node_details_window.treeview_data)
        GUI.clear_treeview(treeview=self.my_gui.node_details_window.treeview_information_gains)
        err_msg = ""
        try:
            number_node_to_display = int(self.my_gui.node_details_window.entered_node_number.get())
            if number_node_to_display < 0:
                raise Exceptions.NegativeNumberException
        except ValueError:
            err_msg += "Die eingegebene Knotennummer ist keine ganze Zahl!\n"
            self.my_gui.node_details_window.entered_node_number.set(self.default_NODE_NUMBER)
        except Exceptions.NegativeNumberException:
            err_msg += "Die eingegebene Knotennummer darf keine negative Zahl sein!\n"
            self.my_gui.node_details_window.entered_node_number.set(self.default_NODE_NUMBER)

        if err_msg == "":
            node_to_display = self.my_Tree.search_by_node_number(number_node_to_display)
            if node_to_display is not None:
                GUI.fill_treeview_with_data(treeview=self.my_gui.node_details_window.treeview_data,
                                            data=node_to_display.node_dataset)
                self.my_gui.node_details_window.display_information_gains(current_node=node_to_display,
                                                                          type_InnerNode=Decision_Tree.InnerNode)
            else:
                messagebox.showerror(parent=self.my_gui.node_details_window.window, title="Fehler",
                                     message="Die eingegebene Knotennummer gehört zu keinem Knoten im aktuellen Baum!")
        else:
            messagebox.showerror(parent=self.my_gui.node_details_window.window, title="Fehler", message=err_msg)

    def call_data_sampling_use(self):
        # Aufruf, wenn der Data Sampler deaktiviert wird
        if self.my_gui.use_data_sampling.get() == 0:
            # GUI-Anpassung
            self.my_gui.use_shuffle_on_tree_creation.set(0)
            self.my_gui.frm_choose_training_data['text'] = "W\u00E4hlen Sie die Trainingsdaten aus:"

            # Setzen der Trainingsdaten auf alle eingelesenen Daten und Löschen des Baums
            # Anzeige des Dummy-Baums
            self.header_used_training_data = self.read_in_header
            self.data_used_training_data = self.read_in_dataset
            self.header_used_test_data = []
            self.data_used_test_data = [[]]
        else:
            self.my_gui.frm_choose_training_data['text'] = "W\u00E4hlen Sie die Daten aus:"
            # Setzen der Header-Zeilen von Trainings- und Testdaten
            self.header_used_training_data = self.read_in_header
            self.header_used_test_data = self.read_in_header
            # Aufteilung der eingelesenen Daten in Trainings- und Testdaten mit dem Data Sampler
            self.data_used_training_data, self.data_used_test_data = self.data_sampling_split_data_by_entered_ratio(
                data=copy.deepcopy(self.read_in_dataset))
            if not self.notification_data_sampler_displayed:
                self.notification_data_sampler_displayed = True
                messagebox.showinfo(parent=self.my_gui.main_window, title="Hinweis",
                                    message="Ein neuer Prozentsatz für die Datenaufteilung wird erst bei erneuter "
                                            "Aktivierung dieser Option aktiv")

        # Aktualisierung der Anzeige mit den aktuellen Daten
        GUI.clear_treeview(treeview=self.my_gui.treeview_training_data)
        GUI.fill_treeview_with_data(treeview=self.my_gui.treeview_training_data,
                                    data=[self.header_used_training_data] + self.data_used_training_data)
        # Zurücksetzen der Baumanzeige
        self.my_Tree = None
        self.my_gui.enter_new_picture(img=tk.PhotoImage(file=self.current_default_image_path))

    def call_data_sampling_shuffle_on_tree_creation(self):
        if self.my_gui.use_data_sampling.get() != 1:
            self.my_gui.use_shuffle_on_tree_creation.set(0)
            messagebox.showerror(parent=self.my_gui.main_window, title="Fehler",
                                 message="Die automatische Aufteilung in Trainings- und Testdaten ist nicht aktiv!")

    def check_input_data_sampler_training_data_ratio(self):
        """
        Liefert die eingegebene Trainingsdatenrate und einen Fehlerstring.
        Falls die Datenaufteilung aktiv ist, wird die Eingabe überprüft.
        Wird diese korrekt eingelesen, wird ein leerer Fehlerstring und die Eingabe geliefert.
        Wird die Eingabe nicht korrekt eingelesen, wird als ein nicht-leerer Fehlerstring und -1 als Eingabe geliefert
        Ist die Eingabe deaktiviert, wird ein leerer Fehlerstring und -1 als Eingabe geliefert
        :return: Fehlerstring und eingelesene Eingabe
        """
        err_msg = ""
        entered_training_data_ratio = -1
        if self.my_gui.use_data_sampling.get() == 1:
            try:
                entered_training_data_ratio = int(self.my_gui.entered_training_data_ratio.get())
                if entered_training_data_ratio < 0 or entered_training_data_ratio > 100:
                    raise Exceptions.OutOfRangeException
            except ValueError:
                err_msg += "Der eingegebene Prozentsatz der Trainingsdaten ist keine ganze Zahl!\n"
                self.my_gui.entered_training_data_ratio.set(self.default_TRAINING_DATA_RATIO)
                entered_training_data_ratio = -1
            except Exceptions.OutOfRangeException:
                err_msg += "Der eingegebene Prozentsatz der Trainingsdaten liegt nicht im Bereich zwischen 0 und 100!\n"
                self.my_gui.entered_training_data_ratio.set(self.default_TRAINING_DATA_RATIO)
                entered_training_data_ratio = -1
        return err_msg, entered_training_data_ratio

    def check_inputs_train_tree(self):
        err_msg = ""
        entered_depth = -1
        entered_purity = -1
        entered_min_number_of_elements = -1
        if self.my_gui.use_hyperparameter_tree_depth.get() == 1:
            try:
                entered_depth = int(self.my_gui.entered_tree_depth.get())
                if entered_depth < 0:
                    raise Exceptions.NegativeNumberException
            except ValueError:
                err_msg += "Die eingegebene Baumtiefe ist keine ganze Zahl!\n"
                self.my_gui.entered_tree_depth.set(self.default_TREE_DEPTH)
                entered_depth = -1
            except Exceptions.NegativeNumberException:
                err_msg += "Die eingegebene Baumtiefe darf keine negative Zahl sein!\n"
                self.my_gui.entered_tree_depth.set(self.default_TREE_DEPTH)
                entered_depth = -1

        if self.my_gui.use_hyperparameter_purity_level.get() == 1:
            try:
                entered_purity = int(self.my_gui.entered_purity_level.get())
                if entered_purity < 0 or entered_purity > 100:
                    raise Exceptions.OutOfRangeException
            except ValueError:
                err_msg += "Das eingegebene Reinheitslevel ist keine ganze Zahl!\n"
                self.my_gui.entered_purity_level.set(self.default_PURITY_LEVEL)
                entered_purity = -1
            except Exceptions.OutOfRangeException:
                err_msg += "Das eingegebene Reinheitslevel liegt nicht im Bereich zwischen 0 und 100!\n"
                self.my_gui.entered_purity_level.set(self.default_PURITY_LEVEL)
                entered_purity = -1

        if self.my_gui.use_hyperparameter_min_elements_in_set.get() == 1:
            try:
                entered_min_number_of_elements = int(self.my_gui.entered_min_elements_in_set.get())
                if entered_min_number_of_elements < 1:
                    raise Exceptions.NegativeNumberException
            except ValueError:
                err_msg += "Die eingegebene minimale Elementanzahl ist keine ganze Zahl!"
                self.my_gui.entered_min_elements_in_set.set(self.default_MIN_ELEMENT_NUMBER)
                entered_min_number_of_elements = -1
            except Exceptions.NegativeNumberException:
                err_msg += "Die eingegebene minimale Elementanzahl muss eine positive Zahl sein!"
                self.my_gui.entered_min_elements_in_set.set(self.default_MIN_ELEMENT_NUMBER)
                entered_min_number_of_elements = -1

        return err_msg, entered_depth, entered_purity, entered_min_number_of_elements

    def data_sampling_split_data_by_entered_ratio(self, data):
        err_msg, entered_ratio = self.check_input_data_sampler_training_data_ratio()

        if err_msg == "":
            training_data, test_data = Data_Sampler.split_data_according_to_ratio(data=data, ratio=entered_ratio)
        else:
            training_data = []
            test_data = []
            messagebox.showerror(parent=self.my_gui.main_window, title="Fehler", message=err_msg)
        return training_data, test_data

    def start(self):
        self.my_gui.main_window.mainloop()

    def print_tree_preorder(self):
        self.my_Tree.print_tree_preorder()


# Helper Methoden
def calculate_confusion_matrix(trained_unique_labels, actual_labels, calculated_labels):
    not_classifiable = 0
    cartesian_product_labels = list(product(trained_unique_labels, trained_unique_labels))
    confusion_entries = dict.fromkeys(cartesian_product_labels, 0)
    for test_set in zip(actual_labels, calculated_labels):
        try:
            confusion_entries[test_set] += 1
        except KeyError:
            not_classifiable += 1
    return confusion_entries, not_classifiable


def calculate_quality_measure_accuracy(confusion_entries, not_classifiable):
    number_of_all_test_sets = sum(confusion_entries.values()) + not_classifiable
    number_of_correctly_classified_sets = sum([confusion_entries[x] for x in confusion_entries if x[0] == x[1]])
    return number_of_correctly_classified_sets, number_of_all_test_sets, (
            number_of_correctly_classified_sets / number_of_all_test_sets)
