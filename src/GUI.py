import platform
import tkinter as tk
import tkinter.ttk as ttk

import os

default_FONT_SMALL = "Calibri 11"
default_FONT_SMALL_ITALIC = "Calibri 11 italic"

default_FONT = "Calibri 12"
default_FONT_BOLD = "Calibri 12 bold"
default_FONT_ITALIC = "Calibri 12 italic"


class GUI_Main_Window:
    split_criterion_MISCLASSIFICATION_COUNT = "Fehlklassifikationen zählen"
    split_criterion_MISCLASSIFICATION_ERROR = "Fehlklassifikationsrate"
    split_criterion_GINI_IMPURITY = "Gini-Impurity"
    split_criterion_ENTROPY = "Entropie"

    path_WINDOWS_icon_image = ".\Grafiken\Icon_simple_dtree.png"
    path_MAC_icon_image = "./Grafiken/Icon_simple_dtree.png"

    path_WINDOWS_startup_image = ".\Grafiken\default_tree_image.png"
    path_MAC_startup_image = "./Grafiken/default_tree_image.png"

    path_WINDOWS_logo_image = ".\Grafiken\logo_fuchs_wolf.png"
    path_MAC_logo_image = "./Grafiken/logo_fuchs_wolf.png"

    def __init__(self, main_object):
        self.main_object = main_object
        self.main_window = tk.Tk()
        self.main_window.title("ENTER_ENTscheidungsbaum-ERsteller - Beta 1.3")
        # Setze Fenstergröße auf minimal sinnvolle Größe
        self.main_window.geometry("1000x650")
        self.main_window.wm_minsize(920, 500)

        app_style = ttk.Style()

        if os.name == 'nt':
            path = self.path_WINDOWS_icon_image
            self.current_logo_path = self.path_WINDOWS_logo_image
            self.current_startup_image_path = self.path_WINDOWS_startup_image
            app_style.theme_use("vista")
        # posix für Linux und MacOS
        else:
            path = self.path_MAC_icon_image
            self.current_logo_path = self.path_MAC_logo_image
            self.current_startup_image_path = self.path_MAC_startup_image
            app_style.theme_use("clam")
        self.main_window.iconphoto(True,
                                   tk.PhotoImage(file=path))

        app_style.configure('.', font=default_FONT)

        app_style.configure("BoldLabel.TLabel", font=default_FONT_BOLD)

        app_style.configure("TNotebook.Tab", foreground="blue", font=default_FONT_ITALIC, padding=[2, 2])

        app_style.configure('Treeview.Heading', font=default_FONT_BOLD)

        self.main_window.option_add('*TCombobox*Listbox.font', default_FONT_SMALL)

        # Dynamische Größenanpassung an das Fenster.
        # Alles in column 0 des main_window wird an die Breite des Fensters angepasst
        self.main_window.columnconfigure(0, weight=1)
        self.main_window.rowconfigure(2, weight=1)

        # Vorbereitung für das Fenster zur Anzeige der im Knoten verwendeten Daten
        self.node_details_window = None

        # Widgets für die Auswahl der Trainingsdaten
        self.entered_filepath_training_data = None
        self.frm_choose_training_data = None
        self.btn_choose_training_data = None
        self.lbl_display_selected_filepath_training_data = None
        self.lbl_logo = None
        self.img_logo = None

        self.init_gui_data_selection()

        # Widgets für die Kontrolloberfläche
        self.selected_split_criterion = None
        self.use_hyperparameter_tree_depth = None
        self.use_hyperparameter_purity_level = None
        self.use_hyperparameter_min_elements_in_set = None
        self.entered_tree_depth = None
        self.entered_purity_level = None
        self.entered_min_elements_in_set = None
        self.show_window_node_details = None

        self.frm_controls = None
        self.frm_choose_split_criterion = None
        self.lbl_text_other_settings = None
        self.com_box_split_criterion_selection = None
        self.lbl_text_split_criteria = None
        self.use_only_split_for_real_information_gain = None
        self.ck_btn_split_for_information_gain_zero = None

        self.frm_choose_hyperparameter = None
        self.ck_btn_hyperparameter_tree_depth = None
        self.etr_max_tree_depth = None
        self.ck_btn_hyperparameter_purity_level = None
        self.etr_purity_level = None
        self.ck_btn_hyperparameter_min_elements_in_set = None
        self.etr_min_elements_in_set = None

        self.frm_choose_settings = None
        self.ck_btn_show_display_split_dataset = None

        self.frm_data_sampling = None
        self.ck_btn_use_data_sampling = None
        self.etr_training_data_ratio = None
        self.ck_btn_shuffle_on_tree_creation = None
        self.use_data_sampling = None
        self.entered_training_data_ratio = None
        self.use_shuffle_on_tree_creation = None

        self.frm_train_test_control = None
        self.btn_train_tree = None
        self.btn_initiate_testing = None

        self.init_gui_controls()

        # Widgets für die Anzeige der Trainingsdaten
        self.frm_display_training_data_container = None
        self.frm_display_training_data = None
        self.treeview_training_data = None
        self.scrollbar_vertical_display_training_data = None
        self.scrollbar_horizontal_display_training_data = None

        # Widgets für die Anzeige des Baums
        self.frm_display_tree_container = None
        self.img_dtree = None
        self.y_coordinate_P_image_for_centering = None
        self.x_coordinate_P_image_for_centering = None
        self.canvas_display_tree = None
        self.canvas_image_tree_id = None
        self.scrollbar_vertical_display_tree = None
        self.scrollbar_horizontal_display_tree = None

        # Widgets für die Anzeige der Testdaten
        self.frm_display_test_phase_container = None
        self.entered_filepath_test_data = None
        self.frm_choose_test_data = None
        self.btn_choose_test_data = None
        self.lbl_display_selected_filepath_test_data = None

        self.frm_display_test_data = None
        self.treeview_test_data = None
        self.scrollbar_horizontal_display_test_data = None
        self.scrollbar_vertical_display_test_data = None

        self.frm_run_testing = None
        self.btn_run_testing = None

        self.frm_display_test_data_results = None
        self.treeview_test_data_results = None

        # Widgets für die Anzeige der Konfusionsmatrix, Gütemaß
        self.frm_display_confusion_matrix_container = None
        self.frm_display_quality_criterion = None
        self.text_field_quality_criterion = None
        self.frm_display_confusion_matrix = None
        self.canvas_confusion_matrix_scrollbars = None
        self.tk_label_list = None
        self.tk_description_label_list = None
        self.frm_confusion_matrix = None
        self.scrollbar_vertical_confusion_matrix = None
        self.scrollbar_horizontal_confusion_matrix = None
        self.canvas_confusion_matrix_id = None

        self.main_notebook = None
        self.init_gui_notebook()

        self.init_gui_footer_credits()

    def init_gui_data_selection(self):
        self.entered_filepath_training_data = tk.StringVar(master=self.main_window)

        self.frm_choose_training_data = tk.LabelFrame(master=self.main_window,
                                                      text="W\u00E4hlen Sie die Trainingsdaten aus:",
                                                      font=default_FONT_BOLD, borderwidth=0)
        self.frm_choose_training_data.grid(column=0, row=0, sticky="ew", padx=(2, 2))

        self.btn_choose_training_data = ttk.Button(master=self.frm_choose_training_data, text="\u00D6ffnen", width=21,
                                                   command=lambda: self.main_object.call_open_file_training_data(
                                                       self.lbl_display_selected_filepath_training_data))
        self.btn_choose_training_data.grid(column=0, row=0, sticky="ew", padx=(2, 0))
        self.lbl_display_selected_filepath_training_data = ttk.Label(master=self.frm_choose_training_data, width=1)

        self.lbl_display_selected_filepath_training_data.grid(column=1, row=0, padx=(5, 0), sticky="ew")
        self.frm_choose_training_data.columnconfigure(1, weight=1)

        self.img_logo = tk.PhotoImage(file=self.current_logo_path)

        self.lbl_logo = ttk.Label(master=self.frm_choose_training_data, image=self.img_logo)
        self.lbl_logo.image = self.img_logo
        self.lbl_logo.grid(column=2, row=0, sticky="e")

    def init_gui_controls(self):
        self.selected_split_criterion = tk.StringVar(master=self.main_window)

        self.use_only_split_for_real_information_gain = tk.IntVar()

        self.use_hyperparameter_tree_depth = tk.IntVar()
        self.use_hyperparameter_purity_level = tk.IntVar()
        self.use_hyperparameter_min_elements_in_set = tk.IntVar()

        self.entered_tree_depth = tk.StringVar(master=self.main_window, value=str(self.main_object.default_TREE_DEPTH))
        self.entered_purity_level = tk.StringVar(master=self.main_window,
                                                 value=str(self.main_object.default_PURITY_LEVEL))
        self.entered_min_elements_in_set = tk.StringVar(master=self.main_window,
                                                        value=str(self.main_object.default_MIN_ELEMENT_NUMBER))

        self.show_window_node_details = tk.IntVar()

        self.use_data_sampling = tk.IntVar()
        self.entered_training_data_ratio = tk.StringVar(master=self.main_window,
                                                        value=str(self.main_object.default_TRAINING_DATA_RATIO))
        self.use_shuffle_on_tree_creation = tk.IntVar()

        self.frm_controls = ttk.Frame(master=self.main_window)
        self.frm_controls.grid(column=0, row=1, sticky="ew", padx=(1, 0))

        # Anpassung damit sich die drei Teilframes in frm_control mit der Fenstergröße anpassen
        self.frm_controls.columnconfigure(0, weight=1)
        self.frm_controls.columnconfigure(1, weight=10)
        self.frm_controls.columnconfigure(2, weight=10)
        self.frm_controls.columnconfigure(3, weight=1)

        # Oberfläche der Auswahl des Splitkriteriums
        self.frm_choose_split_criterion = tk.LabelFrame(master=self.frm_controls, text="Informationsgewinn",
                                                        font=default_FONT_BOLD)
        self.frm_choose_split_criterion.grid(column=0, row=0, sticky="nsew", padx=(1, 0))

        self.lbl_text_split_criteria = ttk.Label(master=self.frm_choose_split_criterion, text="Split-Kriterium:",
                                                 style="BoldLabel.TLabel")
        self.lbl_text_split_criteria.grid(column=0, row=0, sticky="nw")

        self.com_box_split_criterion_selection = ttk.Combobox(master=self.frm_choose_split_criterion, state="readonly",
                                                              width=25, font=default_FONT_SMALL,
                                                              textvariable=self.selected_split_criterion,
                                                              values=[self.split_criterion_MISCLASSIFICATION_COUNT,
                                                                      self.split_criterion_MISCLASSIFICATION_ERROR,
                                                                      self.split_criterion_GINI_IMPURITY,
                                                                      self.split_criterion_ENTROPY])
        self.com_box_split_criterion_selection.current(0)
        self.com_box_split_criterion_selection.grid(column=0, row=1, sticky="nw", padx=(2, 2))

        self.lbl_text_other_settings = ttk.Label(master=self.frm_choose_split_criterion, text="Weitere Einstellungen:",
                                                 style="BoldLabel.TLabel")
        self.lbl_text_other_settings.grid(column=0, row=2, sticky="sw", pady=(7, 0))

        self.ck_btn_split_for_information_gain_zero = ttk.Checkbutton(master=self.frm_choose_split_criterion,
                                                                      text="Nur bei Informations- \ngewinn > 0 aufteilen",
                                                                      takefocus=0,
                                                                      variable=self.use_only_split_for_real_information_gain,
                                                                      onvalue=1,
                                                                      offvalue=0)
        self.ck_btn_split_for_information_gain_zero.grid(column=0, row=3, sticky="sw")

        # Oberfläche der Hyperparameterauswahl
        self.frm_choose_hyperparameter = tk.LabelFrame(master=self.frm_controls,
                                                       text="Hyperparameter",
                                                       font=default_FONT_BOLD)
        self.frm_choose_hyperparameter.grid(column=1, row=0, sticky="nsew", padx=(1, 0))
        self.frm_choose_hyperparameter.columnconfigure(0, weight=1)
        self.frm_choose_hyperparameter.columnconfigure(1, weight=100)

        self.ck_btn_hyperparameter_tree_depth = ttk.Checkbutton(master=self.frm_choose_hyperparameter,
                                                                text="Maximale Baumtiefe: ", takefocus=0,
                                                                variable=self.use_hyperparameter_tree_depth, onvalue=1,
                                                                offvalue=0)
        self.use_hyperparameter_tree_depth.set(0)
        self.ck_btn_hyperparameter_tree_depth.grid(column=0, row=0, sticky="nw")

        self.etr_max_tree_depth = ttk.Entry(master=self.frm_choose_hyperparameter, width=10,
                                            textvariable=self.entered_tree_depth)
        self.etr_max_tree_depth.grid(column=1, row=0, sticky="w", padx=(0, 5))

        self.ck_btn_hyperparameter_purity_level = ttk.Checkbutton(master=self.frm_choose_hyperparameter,
                                                                  text="Minimale Reinheit in \u0025 "
                                                                       "\nf\u00fcr Klassifikation: ",
                                                                  takefocus=0,
                                                                  variable=self.use_hyperparameter_purity_level,
                                                                  onvalue=1,
                                                                  offvalue=0)
        self.use_hyperparameter_purity_level.set(0)
        self.ck_btn_hyperparameter_purity_level.grid(column=0, row=1, sticky="nw")

        self.etr_purity_level = ttk.Entry(master=self.frm_choose_hyperparameter, width=10,
                                          textvariable=self.entered_purity_level)
        self.etr_purity_level.grid(column=1, row=1, sticky="w", padx=(0, 5))

        self.ck_btn_hyperparameter_min_elements_in_set = ttk.Checkbutton(master=self.frm_choose_hyperparameter,
                                                                         text="Minimale Elementanzahl \nin Knoten: ",
                                                                         takefocus=0,
                                                                         variable=self.use_hyperparameter_min_elements_in_set,
                                                                         onvalue=1,
                                                                         offvalue=0)
        self.use_hyperparameter_min_elements_in_set.set(0)
        self.ck_btn_hyperparameter_min_elements_in_set.grid(column=0, row=2, sticky="nw")

        self.etr_min_elements_in_set = ttk.Entry(master=self.frm_choose_hyperparameter, width=10,
                                                 textvariable=self.entered_min_elements_in_set)
        self.etr_min_elements_in_set.grid(column=1, row=2, sticky="w", padx=(0, 5))

        # Oberfläche DataSampler
        self.frm_data_sampling = tk.LabelFrame(master=self.frm_controls,
                                               text="Autom. Datenaufteilung",
                                               font=default_FONT_BOLD)
        self.frm_data_sampling.grid(column=2, row=0, sticky="nsew", padx=(1, 1))
        self.frm_data_sampling.columnconfigure(0, weight=1)
        self.frm_data_sampling.columnconfigure(1, weight=100)

        self.ck_btn_use_data_sampling = ttk.Checkbutton(master=self.frm_data_sampling,
                                                        text="Anteil der Trainingsdaten in %: ", takefocus=0,
                                                        variable=self.use_data_sampling,
                                                        onvalue=1,
                                                        offvalue=0,
                                                        command=self.main_object.call_data_sampling_use)
        self.use_data_sampling.set(0)
        self.ck_btn_use_data_sampling.grid(column=0, row=0, sticky="nw")

        self.etr_training_data_ratio = ttk.Entry(master=self.frm_data_sampling, width=10,
                                                 textvariable=self.entered_training_data_ratio)
        self.etr_training_data_ratio.grid(column=1, row=0, sticky="nw", padx=(0, 5))

        self.ck_btn_shuffle_on_tree_creation = ttk.Checkbutton(master=self.frm_data_sampling,
                                                               text="Daten neu mischen bei Baumerstellung", takefocus=0,
                                                               variable=self.use_shuffle_on_tree_creation,
                                                               onvalue=1,
                                                               offvalue=0,
                                                               command=self.main_object.call_data_sampling_shuffle_on_tree_creation)
        self.use_shuffle_on_tree_creation.set(0)
        self.ck_btn_shuffle_on_tree_creation.grid(column=0, row=1, sticky="nw", columnspan=2)

        # Oberfläche der Trainings- und Testbuttons
        self.frm_train_test_control = tk.LabelFrame(master=self.frm_controls,
                                                    text="Training und Testen",
                                                    font=default_FONT_BOLD)
        self.frm_train_test_control.grid(column=3, row=0, sticky="nsew", padx=(1, 1))

        self.btn_train_tree = ttk.Button(master=self.frm_train_test_control, text="Entscheidungsbaum erstellen",
                                         width=25,
                                         command=self.main_object.call_train_tree)
        self.btn_train_tree.grid(column=0, row=0, sticky='ew')

        self.ck_btn_show_display_split_dataset = ttk.Checkbutton(master=self.frm_train_test_control,
                                                                 text="Knotendetails anzeigen",
                                                                 variable=self.show_window_node_details, onvalue=1,
                                                                 offvalue=0,
                                                                 command=self.main_object.call_show_window_node_details)
        self.show_window_node_details.set(0)
        self.ck_btn_show_display_split_dataset.grid(column=0, row=1, sticky="nw")

        self.btn_initiate_testing = ttk.Button(master=self.frm_train_test_control, text="Testmodus aktivieren",
                                               command=self.main_object.call_activate_test_phase)
        self.btn_initiate_testing.grid(column=0, row=2, sticky="sew", pady=(0, 2))
        self.frm_train_test_control.columnconfigure(0, weight=1)
        self.frm_train_test_control.rowconfigure(2, weight=1)

    def init_gui_notebook(self):
        # Erstellen des Notebooks
        self.main_notebook = ttk.Notebook(master=self.main_window)
        self.main_notebook.grid(column=0, row=2, sticky="nsew", pady=(5, 0))

        # Erstellen der Frames, welche im Notebook angezeigt werden/auswählbar sein sollen
        self.init_frame_display_training_data()
        self.init_frame_display_tree()
        self.init_frame_display_test_phase()
        self.init_frame_display_confusion_matrix()

        # Hinzufügen der Frames zum Notebook
        # Tab 0
        self.main_notebook.add(child=self.frm_display_training_data_container, text="Ansicht Trainingsdaten  ",
                               sticky="nsew")
        # Tab 1
        self.main_notebook.add(child=self.frm_display_tree_container, text=" Ansicht Entscheidungsbaum  ",
                               sticky="nsew")
        # Tab 2
        self.main_notebook.add(child=self.frm_display_test_phase_container, text=" Ansicht Testphase  ", sticky="nsew")
        # Tab 3
        self.main_notebook.add(child=self.frm_display_confusion_matrix_container,
                               text=" Ansicht Konfusionsmatrix und G\u00FCtema\u00DF ",
                               sticky="nsew")

        # Dieser beiden Tabs werden erst bei Bedarf eingeblendet
        self.main_notebook.hide(2)
        self.main_notebook.hide(3)

    def init_frame_display_training_data(self):
        self.frm_display_training_data_container = tk.Frame(master=self.main_notebook, borderwidth=0)
        self.frm_display_training_data_container.pack(fill="both", expand=True)

        self.frm_display_training_data = tk.LabelFrame(master=self.frm_display_training_data_container,
                                                       text="Geladene Trainingsdaten(0 Elemente):",
                                                       font=default_FONT_BOLD, borderwidth=0)

        self.frm_display_training_data.grid(column=0, row=0, sticky="nsew", pady=(5, 0))
        self.frm_display_training_data_container.columnconfigure(0, weight=1)
        self.frm_display_training_data_container.rowconfigure(0, weight=1)

        # TreeView zum Anzeigen der Daten
        self.treeview_training_data = ttk.Treeview(master=self.frm_display_training_data, selectmode='none')

        self.treeview_training_data.grid(column=0, row=0, sticky="nsew")
        self.frm_display_training_data.columnconfigure(0, weight=1)
        self.frm_display_training_data.rowconfigure(0, weight=1)

        self.scrollbar_vertical_display_training_data = ttk.Scrollbar(master=self.frm_display_training_data,
                                                                      orient="vertical")
        self.scrollbar_vertical_display_training_data.config(command=self.treeview_training_data.yview)

        self.scrollbar_vertical_display_training_data.grid(column=1, row=0, sticky="ns")

        self.treeview_training_data.configure(yscrollcommand=self.scrollbar_vertical_display_training_data.set)

        self.scrollbar_horizontal_display_training_data = ttk.Scrollbar(master=self.frm_display_training_data,
                                                                        orient="horizontal")
        self.scrollbar_horizontal_display_training_data.config(command=self.treeview_training_data.xview)

        self.scrollbar_horizontal_display_training_data.grid(column=0, row=1, sticky="ew")

        self.treeview_training_data.configure(xscrollcommand=self.scrollbar_horizontal_display_training_data.set)

    def init_frame_display_tree(self):
        self.frm_display_tree_container = tk.Frame(master=self.main_notebook, borderwidth=0, bg="white")
        self.frm_display_tree_container.pack(fill="both", expand=True)

        # Standardbild laden
        self.img_dtree = tk.PhotoImage(file=self.current_startup_image_path)

        # Erstellen des scrollbaren Canvas, welches für die Anzeige des Bildes verwendet wird
        self.canvas_display_tree = tk.Canvas(master=self.frm_display_tree_container, background="white", borderwidth=0,
                                             highlightthickness=0)

        self.canvas_display_tree.grid(column=0, row=0, sticky="nsew")
        self.frm_display_tree_container.columnconfigure(0, weight=1)
        self.frm_display_tree_container.rowconfigure(0, weight=1)

        # Anlegen und Platzieren der Scrollbars
        self.scrollbar_vertical_display_tree = ttk.Scrollbar(self.frm_display_tree_container, orient="vertical")
        self.scrollbar_vertical_display_tree.config(command=self.canvas_display_tree.yview)
        self.canvas_display_tree.config(yscrollcommand=self.scrollbar_vertical_display_tree.set)
        self.scrollbar_vertical_display_tree.grid(column=1, row=0, sticky="ns")

        self.scrollbar_horizontal_display_tree = ttk.Scrollbar(self.frm_display_tree_container, orient="horizontal")
        self.scrollbar_horizontal_display_tree.config(command=self.canvas_display_tree.xview)
        self.canvas_display_tree.config(xscrollcommand=self.scrollbar_horizontal_display_tree.set)
        self.scrollbar_horizontal_display_tree.grid(column=0, row=1, sticky="ew")

        # Aktualisierung der Anzeige
        self.frm_display_tree_container.update_idletasks()

        # Zeichnen des Bilds auf dem Canvas
        self.canvas_image_tree_id = self.canvas_display_tree.create_image(0, 0, image=self.img_dtree, anchor="nw")

        dimensions = self.canvas_display_tree.bbox("all")
        dim_canvas_image_x = dimensions[2] - dimensions[0]
        dim_canvas_image_y = dimensions[3] - dimensions[1]

        # Scrollbereich aktualisieren
        self.canvas_display_tree.config(scrollregion=(0, 0, dim_canvas_image_x, dim_canvas_image_y))

        # Bei Änderung der Größe des frm_display_tree (oder eines beinhaltenden Widgets) wird diese Methode aufgerufen.
        # Hier die globalen Variablen, bzw. Methodenaufrufe(height() und width()) verwenden, da diese Bindung
        # auch später noch funktionieren soll
        self.canvas_display_tree.bind(
            "<Configure>",
            lambda e: self.hold_image_centered(e, image_dim_x=self.img_dtree.width(),
                                               image_dim_y=self.img_dtree.height()))

    def init_frame_display_test_phase(self):
        self.frm_display_test_phase_container = tk.Frame(master=self.main_notebook, borderwidth=0)
        self.frm_display_test_phase_container.pack(fill="both", expand=True)
        # Betrifft die Dateiauswahl, die Treeview zur Anzeige der Testdaten und die Scrollbar
        self.frm_display_test_phase_container.columnconfigure(0, weight=1)
        # Betrifft den Frame mit dem Button zur Trainingsphase und den Frame zur Anzeige der Klassifiaktionsergebnisse
        # self.frm_display_test_phase_container.columnconfigure(1, weight=1)
        # Betrifft die Treeview zur Anzeige der Testdaten und den Frame zur Anzeige der Klassifiaktionsergebnisse
        self.frm_display_test_phase_container.rowconfigure(1, weight=1)

        self.entered_filepath_test_data = tk.StringVar(master=self.frm_display_test_phase_container)

        # Frame, welchen für die Auswahl des Testdatenfiles
        self.frm_choose_test_data = tk.LabelFrame(master=self.frm_display_test_phase_container,
                                                  text="W\u00E4hlen Sie die Testdaten aus:",
                                                  font=default_FONT_BOLD, borderwidth=0)
        self.frm_choose_test_data.grid(column=0, row=0, sticky="ew", padx=(2, 2), pady=(5, 0))
        # Columnconfigure für das Label der Dateipfadanzeige
        self.frm_choose_test_data.columnconfigure(1, weight=1)

        self.btn_choose_test_data = ttk.Button(master=self.frm_choose_test_data, text="\u00D6ffnen", width=21,
                                               command=lambda: self.main_object.call_open_file_test_data(
                                                   self.lbl_display_selected_filepath_test_data))
        self.btn_choose_test_data.grid(column=0, row=0, sticky="nw")
        self.lbl_display_selected_filepath_test_data = ttk.Label(master=self.frm_choose_test_data, width=1)
        self.lbl_display_selected_filepath_test_data.grid(column=1, row=0, sticky="ew")

        # Frame, welcher den Kontrollbutton zur Ausführung des Testens enthält
        self.frm_run_testing = tk.LabelFrame(master=self.frm_display_test_phase_container, text="Testen des Modells",
                                             font=default_FONT_BOLD, borderwidth=0)
        self.frm_run_testing.grid(column=1, row=0, sticky="ew", pady=(5, 0))
        # Damit der Button zur Ausführung des Trainings immer so breit wie die Spalte ist (Spalte selbst fix, da kein
        # columnconfigure 1 im container Frame)
        self.frm_run_testing.columnconfigure(0, weight=1)
        self.btn_run_testing = ttk.Button(master=self.frm_run_testing, text="Ausf\u00fchren",
                                          command=self.main_object.call_perform_testing)
        self.btn_run_testing.grid(column=0, row=0, sticky="ew")

        # Frame zur Anzeige der Testdaten
        self.frm_display_test_data = tk.LabelFrame(master=self.frm_display_test_phase_container,
                                                   text="Testdaten(0 Elemente): ",
                                                   font=default_FONT_BOLD, borderwidth=0)
        self.frm_display_test_data.grid(column=0, row=1, sticky="nsew", padx=(2, 0), pady=(15, 0))
        # Damit sich die Treeview zur Anzeige der Testdaten immer maximal ausdehnt
        self.frm_display_test_data.columnconfigure(0, weight=1)
        self.frm_display_test_data.rowconfigure(0, weight=1)

        # TreeView zum Anzeigen der Testdaten
        self.treeview_test_data = ttk.Treeview(master=self.frm_display_test_data, selectmode='none')
        self.treeview_test_data.grid(column=0, row=0, sticky="nsew", padx=(2, 2))

        self.scrollbar_horizontal_display_test_data = ttk.Scrollbar(master=self.frm_display_test_phase_container,
                                                                    orient="horizontal")
        self.scrollbar_horizontal_display_test_data.config(command=self.treeview_test_data.xview)
        self.scrollbar_horizontal_display_test_data.grid(column=0, row=2, sticky="ew")
        self.treeview_test_data.configure(xscrollcommand=self.scrollbar_horizontal_display_test_data.set)

        # Frame zur Anzeige der vom Modell berechneten Labels für die Testdaten
        # Anpassung der Anzeige des Testdatenbereichs mit Fenstergröße vertikal über rowconfigure bereits oben
        # columnconfigure nicht nötig, da eine feste Breite behalten werden soll
        self.frm_display_test_data_results = tk.LabelFrame(master=self.frm_display_test_phase_container,
                                                           text="Berechnete Labels: ",
                                                           font=default_FONT_BOLD, borderwidth=0)
        self.frm_display_test_data_results.grid(column=1, row=1, sticky="nsew", pady=(15, 0))
        # Betrifft die Treeview zum Anzeige der Klassifikationsergebnisse
        self.frm_display_test_data_results.columnconfigure(0, weight=1)
        # Betrifft die Treeview zum Anzeige der Klassifikationsergebnisse und die zugehörige Scrollbar
        self.frm_display_test_data_results.rowconfigure(0, weight=1)

        # TreeView zum Anzeigen der Testergebnisse
        # Keine Column/Row-Configure, da sich dieses Treeview nicht mit dem Fenster resizen soll
        self.treeview_test_data_results = ttk.Treeview(master=self.frm_display_test_data_results, selectmode='none')

        # Header zu Treeview hinzufügen
        # Header festlegen
        self.treeview_test_data_results["columns"] = ['col_calc_label']
        # Headerwerte anzeigen
        self.treeview_test_data_results['show'] = 'headings'

        # Layout der Headerzeile festlegen und Werte in die Headerzeile speichern
        self.treeview_test_data_results.column(column="col_calc_label", minwidth=200, anchor='c', stretch=True)
        self.treeview_test_data_results.heading(column="col_calc_label", text="Berechnetes Label")

        self.treeview_test_data_results.grid(column=0, row=0, sticky="nsew", padx=(2, 2))

        self.scrollbar_vertical_display_test_data = ttk.Scrollbar(master=self.frm_display_test_data_results,
                                                                  orient="vertical")
        self.scrollbar_vertical_display_test_data.config(command=self.mulitple_y_view)
        self.scrollbar_vertical_display_test_data.grid(column=1, row=0, sticky="ns")
        self.treeview_test_data.configure(yscrollcommand=self.scrollbar_vertical_display_test_data.set)
        self.treeview_test_data_results.configure(yscrollcommand=self.scrollbar_vertical_display_test_data.set)

        # Windows oder Mac
        if platform.system() == ('Windows' or 'Darwin'):
            self.treeview_test_data.bind("<MouseWheel>", self.parallel_mouse_scrolling_treeviews_test_phase)
            self.treeview_test_data_results.bind("<MouseWheel>", self.parallel_mouse_scrolling_treeviews_test_phase)
        else:
            self.treeview_test_data.bind("<Button-4>", self.parallel_mouse_scrolling_treeviews_test_phase)
            self.treeview_test_data.bind("<Button-5>", self.parallel_mouse_scrolling_treeviews_test_phase)

            self.treeview_test_data_results.bind("<Button-4>", self.parallel_mouse_scrolling_treeviews_test_phase)
            self.treeview_test_data_results.bind("<Button-5>", self.parallel_mouse_scrolling_treeviews_test_phase)

    def parallel_mouse_scrolling_treeviews_test_phase(self, event):
        # Für Mac
        if platform.system() == 'Darwin':
            num = 1
        else:
            num = 120
        self.treeview_test_data.yview_scroll(-1 * int(event.delta / num), "units")
        self.treeview_test_data_results.yview_scroll(-1 * int(event.delta / num), "units")
        # Damit default-Bindungen nicht feuern und somit doppelt gescrollt wird
        return "break"

    def init_frame_display_confusion_matrix(self):
        self.frm_display_confusion_matrix_container = tk.Frame(master=self.main_notebook, borderwidth=0, bg="white")
        self.frm_display_confusion_matrix_container.pack(fill="both", expand=True)

        # Frame zur Anzeige der Gütemaße
        self.frm_display_quality_criterion = tk.LabelFrame(master=self.frm_display_confusion_matrix_container,
                                                           text="G\u00FCtema\u00DF: ",
                                                           font=default_FONT_BOLD, bg="white")
        self.frm_display_quality_criterion.grid(column=0, row=0, sticky="nsew", padx=(2, 0), pady=(5, 0))
        self.frm_display_confusion_matrix_container.columnconfigure(0, weight=1)

        # Erstellen des Text-Widgets zur Anzeige des Gütemaß-Texts
        self.text_field_quality_criterion = tk.Text(master=self.frm_display_quality_criterion, height=7,
                                                    state=tk.DISABLED, borderwidth=0)
        self.text_field_quality_criterion.grid(column=0, row=0, sticky="nsew")
        self.frm_display_quality_criterion.columnconfigure(0, weight=1)

        # Frame zur Anzeige der Konfusionsmatrix
        self.frm_display_confusion_matrix = tk.LabelFrame(master=self.frm_display_confusion_matrix_container,
                                                          text="Konfusionsmatrix: ",
                                                          font=default_FONT_BOLD, bg="white")
        self.frm_display_confusion_matrix.grid(column=0, row=1, sticky="nsew", padx=(2, 0), pady=(15, 0))
        self.frm_display_confusion_matrix_container.rowconfigure(1, weight=1)

        self.canvas_confusion_matrix_scrollbars = tk.Canvas(master=self.frm_display_confusion_matrix,
                                                            background="white", borderwidth=0,
                                                            highlightthickness=0)

        self.tk_label_list = None
        self.tk_description_label_list = []
        self.frm_confusion_matrix = tk.Frame(master=self.canvas_confusion_matrix_scrollbars, bg="white")

        # Horizontale Benennung
        self.tk_description_label_list.append(tk.Label(master=self.frm_confusion_matrix, text="Berechnet",
                                                       anchor=tk.CENTER, font=default_FONT_ITALIC, height=2,
                                                       borderwidth=1,
                                                       relief=tk.SOLID))
        # Senkrechte Benennung
        self.tk_description_label_list.append(
            tk.Label(master=self.frm_confusion_matrix, text="Erwartet", anchor=tk.CENTER,
                     justify=tk.CENTER, wraplength=1, font=default_FONT_ITALIC, width=6,
                     borderwidth=1, relief=tk.SOLID))

        self.canvas_confusion_matrix_scrollbars.grid(column=0, row=0, sticky="nsew", pady=(5, 0))
        self.frm_display_confusion_matrix.columnconfigure(0, weight=1)
        self.frm_display_confusion_matrix.rowconfigure(0, weight=1)

        # Anlegen und Platzieren der Scollbars
        self.scrollbar_vertical_confusion_matrix = ttk.Scrollbar(self.frm_display_confusion_matrix, orient="vertical")
        self.scrollbar_vertical_confusion_matrix.config(command=self.canvas_confusion_matrix_scrollbars.yview)
        self.canvas_confusion_matrix_scrollbars.config(yscrollcommand=self.scrollbar_vertical_confusion_matrix.set)

        self.scrollbar_horizontal_confusion_matrix = ttk.Scrollbar(self.frm_display_confusion_matrix,
                                                                   orient="horizontal")
        self.scrollbar_horizontal_confusion_matrix.config(command=self.canvas_confusion_matrix_scrollbars.xview)
        self.canvas_confusion_matrix_scrollbars.config(xscrollcommand=self.scrollbar_horizontal_confusion_matrix.set)

        # Hinzufügen des Frames, der die Konfusionsmatrix enthält zum Canvas
        self.canvas_confusion_matrix_id = self.canvas_confusion_matrix_scrollbars.create_window(0, 0, anchor=tk.NW,
                                                                                                window=self.frm_confusion_matrix)

    def hold_centered_confusion_matrix(self, event, maxtrix_x_dim, maxtrix_y_dim):
        # Herausfiltern der Größenänderung des Frames, der das Canvas beinhaltet
        if event.widget == self.canvas_confusion_matrix_scrollbars:
            x_new = max(0, round((self.canvas_confusion_matrix_scrollbars.winfo_width() - maxtrix_x_dim) / 2))

            self.canvas_confusion_matrix_scrollbars.moveto(self.canvas_confusion_matrix_id, x_new, 0)

            if self.canvas_confusion_matrix_scrollbars.winfo_width() > maxtrix_x_dim:
                self.scrollbar_horizontal_confusion_matrix.grid_forget()
            else:
                self.scrollbar_horizontal_confusion_matrix.grid(column=0, row=1, sticky="ew")

            if self.canvas_confusion_matrix_scrollbars.winfo_height() > maxtrix_y_dim:
                self.scrollbar_vertical_confusion_matrix.grid_forget()
            else:
                self.scrollbar_vertical_confusion_matrix.grid(column=1, row=0, sticky="ns")

    def update_display_confusion_matrix(self):
        self.canvas_confusion_matrix_scrollbars.update_idletasks()
        dimensions = self.canvas_confusion_matrix_scrollbars.bbox("all")
        dim_matrix_x = dimensions[2] - dimensions[0]
        dim_matrix_y = dimensions[3] - dimensions[1]

        # Scrollbereich aktualisieren
        self.canvas_confusion_matrix_scrollbars.config(scrollregion=(0, 0, dim_matrix_x, dim_matrix_y))

        # Bindung der Größenänderung mit den neuen Matrixdimensionen aktualisieren
        self.canvas_confusion_matrix_scrollbars.bind(
            "<Configure>",
            lambda e: self.hold_centered_confusion_matrix(e, maxtrix_x_dim=dim_matrix_x, maxtrix_y_dim=dim_matrix_y))

        # Berechnung der neuen Zentrierung
        x_new = max(0,
                    round((self.canvas_confusion_matrix_scrollbars.winfo_width() - dim_matrix_x) / 2))

        self.canvas_confusion_matrix_scrollbars.moveto(self.canvas_confusion_matrix_id, x_new, 0)

        # Bei Notwendigkeit einblenden der Scrollbars
        if self.canvas_confusion_matrix_scrollbars.winfo_width() > dim_matrix_x:
            self.scrollbar_horizontal_confusion_matrix.grid_forget()
        else:
            self.scrollbar_horizontal_confusion_matrix.grid(column=0, row=1, sticky="ew")

        if self.canvas_confusion_matrix_scrollbars.winfo_height() > dim_matrix_y:
            self.scrollbar_vertical_confusion_matrix.grid_forget()
        else:
            self.scrollbar_vertical_confusion_matrix.grid(column=1, row=0, sticky="ns")

    # Kleiner Hack um die beiden Treeviews simultan scrollen zu können
    def mulitple_y_view(self, *args):
        self.treeview_test_data_results.yview(*args)
        self.treeview_test_data.yview(*args)

    def hold_image_centered_old(self, event, x_old, frame_width, img_width, y_old, frame_height, img_height,
                                scrollbar_dim):
        # Herausfiltern der Größenänderung des Frames, der das Canvas beinhaltet
        if event.widget == self.frm_display_tree_container:
            if (self.frm_display_tree_container.winfo_width != frame_width
                    or self.canvas_display_tree.winfo_height != frame_height):
                # Bestimmung der neuen x Koordinate für die Zentrierung
                x_new = max(0, round((self.frm_display_tree_container.winfo_width() - img_width) / 2))
                y_new = max(0, round((self.frm_display_tree_container.winfo_height() - img_height) / 2))

                # Verschieben des Bilds
                self.canvas_display_tree.move(self.canvas_image_tree_id, (x_new - x_old), (y_new - y_old))

                # Aktualisieren der x Koordinate für die Zentrierung
                self.x_coordinate_P_image_for_centering = x_new
                self.y_coordinate_P_image_for_centering = y_new

                x_max = max(self.img_dtree.width(),
                            self.frm_display_tree_container.winfo_width() - scrollbar_dim)
                y_max = max(self.img_dtree.height(),
                            self.frm_display_tree_container.winfo_height() - scrollbar_dim)
                self.canvas_display_tree.config(scrollregion=(0, 0, x_max, y_max))

    def hold_image_centered(self, event, image_dim_x, image_dim_y):
        # Herausfiltern der Größenänderung des Frames, der das Canvas beinhaltet
        if event.widget == self.canvas_display_tree:
            # Bestimmung der neuen x Koordinate für die Zentrierung
            x_new = max(0, round((self.canvas_display_tree.winfo_width() - image_dim_x) / 2))
            y_new = max(0, round((self.canvas_display_tree.winfo_height() - image_dim_y) / 2))

            # Verschieben des Bilds
            self.canvas_display_tree.moveto(self.canvas_image_tree_id, x_new, y_new)

            if self.canvas_display_tree.winfo_width() > image_dim_x:
                self.scrollbar_horizontal_display_tree.grid_forget()
            else:
                self.scrollbar_horizontal_display_tree.grid(column=0, row=1, sticky="ew")

            if self.canvas_display_tree.winfo_height() > image_dim_y:
                self.scrollbar_vertical_display_tree.grid_forget()
            else:
                self.scrollbar_vertical_display_tree.grid(column=1, row=0, sticky="ns")

    def enter_new_picture(self, img):
        self.img_dtree = img
        image_dim_x = img.width()
        image_dim_y = img.height()
        # Bestimmung der neuen x Koordinate für die Zentrierung
        x_new = max(0, round((self.canvas_display_tree.winfo_width() - image_dim_x) / 2))
        y_new = max(0, round((self.canvas_display_tree.winfo_height() - image_dim_y) / 2))

        # Löschen des alten Bilds
        self.canvas_display_tree.delete(self.canvas_image_tree_id)

        # Zeichnen des Bilds auf dem Canvas
        self.canvas_image_tree_id = self.canvas_display_tree.create_image(x_new, y_new, image=img, anchor="nw")

        dimensions = self.canvas_display_tree.bbox("all")
        dim_canvas_image_x = dimensions[2] - dimensions[0]
        dim_canvas_image_y = dimensions[3] - dimensions[1]

        # Aktualisieren des Scrollbereichs
        self.canvas_display_tree.config(scrollregion=(0, 0, dim_canvas_image_x, dim_canvas_image_y))
        self.canvas_display_tree.moveto(self.canvas_image_tree_id, x_new, y_new)

        # Bei Notwendigkeit einblenden der Scrollbars
        if self.canvas_display_tree.winfo_width() > image_dim_x:
            self.scrollbar_horizontal_display_tree.grid_forget()
        else:
            self.scrollbar_horizontal_display_tree.grid(column=0, row=1, sticky="ew")
        if self.canvas_display_tree.winfo_height() > image_dim_y:
            self.scrollbar_vertical_display_tree.grid_forget()
        else:
            self.scrollbar_vertical_display_tree.grid(column=1, row=0, sticky="ns")

    def init_gui_footer_credits(self):
        # Anlegen der Credit-Zeile
        frm_credits = ttk.Frame(master=self.main_window)
        frm_credits.grid(column=0, row=3, sticky="sew")
        frm_credits.columnconfigure(0, weight=1)
        lbl_didaktik = tk.Label(master=frm_credits, anchor=tk.W, justify=tk.LEFT,
                                text=" Didaktik der Informatik - Universit\u00E4t Passau",
                                font=default_FONT_SMALL_ITALIC)
        lbl_didaktik.grid(column=0, row=0, sticky="w")
        lbl_university = tk.Label(master=frm_credits, anchor=tk.E, justify=tk.RIGHT,
                                  text="Tobias Fuchs, Wolfgang Pfeffer  ", font=default_FONT_SMALL_ITALIC)
        lbl_university.grid(column=1, row=0, sticky="e")

    def disable_inputs_training_phase(self, disable_inputs):
        if disable_inputs:
            usage_status = tk.DISABLED
            self.com_box_split_criterion_selection['state'] = usage_status
        else:
            usage_status = tk.NORMAL
            self.com_box_split_criterion_selection['state'] = "readonly"

        self.btn_choose_training_data['state'] = usage_status
        self.ck_btn_hyperparameter_tree_depth['state'] = usage_status
        self.ck_btn_hyperparameter_purity_level['state'] = usage_status
        self.ck_btn_hyperparameter_min_elements_in_set['state'] = usage_status
        self.etr_max_tree_depth['state'] = usage_status
        self.etr_purity_level['state'] = usage_status
        self.etr_min_elements_in_set['state'] = usage_status
        self.ck_btn_use_data_sampling['state'] = usage_status
        self.ck_btn_shuffle_on_tree_creation['state'] = usage_status
        self.ck_btn_split_for_information_gain_zero['state'] = usage_status

        # Falls das Data Sampling aktiv war/ist, wurde eine korrekte Aufteilungsrate eingelesen und die Eingabe soll
        # weiterhin gesperrt bleiben, da nur bei Aktivierung des Data Sampling geprüft wird
        if self.use_data_sampling.get() == 1:
            self.etr_training_data_ratio['state'] = tk.DISABLED
        else:
            self.etr_training_data_ratio['state'] = usage_status

        self.btn_train_tree['state'] = usage_status

    def adapt_gui_for_data_sampler(self, enable_data_sampling):
        if enable_data_sampling:
            self.frm_choose_training_data['text'] = "W\u00E4hlen Sie die Daten aus:"
        else:
            self.frm_choose_training_data['text'] = "W\u00E4hlen Sie die Trainingsdaten aus:"


# Helper-Methoden
def display_treeview_from_beginning(treeview):
    treeview_elements = treeview.get_children()
    if treeview_elements != ():
        treeview.see(treeview_elements[0])


def build_confusion_matrix(containing_frame, number_of_labels, matrix_entries, tk_description_label_list,
                           tk_label_list):
    # Ausdehnung der Beschriftungen Erwartet(tk_description_label_list[1]) und Berechnet(tk_description_label_list[0])
    # anpassen
    tk_description_label_list[0].grid_forget()
    tk_description_label_list[1].grid_forget()
    tk_description_label_list[0].grid(column=1, row=0, columnspan=number_of_labels + 1, sticky="nsew")
    tk_description_label_list[1].grid(column=0, row=1, rowspan=number_of_labels + 1, sticky="nsew")

    # Innerer Teil der Konfusionsmatrix
    if tk_label_list is not None:
        # Loslösen der Labels
        for elm in tk_label_list:
            elm.grid_forget()

        # Nur notwendige Anzahl an Label erstellen bzw. welche löschen
        diff = len(matrix_entries) - len(tk_label_list)
        for i in range(diff):
            if diff > 0:
                temp = tk.Label(master=containing_frame, text="          ", borderwidth=1, relief=tk.SOLID)
                tk_label_list.append(temp)
            else:
                tk_label_list.pop().destroy()

    else:
        tk_label_list = []
        for i in range(len(matrix_entries)):
            tk_label_list.append(tk.Label(master=containing_frame, text="          ", borderwidth=1, relief=tk.SOLID))

    # Anordnen der Labels
    counter = 0
    for j in range(1, number_of_labels + 2):
        for i in range(1, number_of_labels + 2):
            text_color = "black"
            if i == j:
                text_color = "blue"

            text_font = default_FONT
            if i == 1 or j == 1:
                text_font = default_FONT_BOLD
            temp = tk_label_list[counter]
            temp.configure(font=text_font, foreground=text_color)
            temp.grid(column=i, row=j, sticky="nsew")
            counter += 1

    # Füllen der Konfusionsmatrix
    label_max_length = 0
    for i in range(1, number_of_labels + 1):
        label_max_length = max(label_max_length, len(matrix_entries[i]))

    # Erweitern der Zeilenheadereintrgäge auf selbe Breite
    for i in range(1, number_of_labels + 1):
        temp = len(matrix_entries[i])
        if temp < label_max_length:
            diff = round((label_max_length - temp) / 2)
            matrix_entries[i] = " " * diff + matrix_entries[i] + " " * diff

    for elm, val in zip(tk_label_list, matrix_entries):
        elm.configure(text=" " + str(val) + " ")


def fill_text_widget_quality_criterion_precision(text_widget, number_classified_correctly, number_all, precision,
                                                 not_classifiable):
    # Textfeld bearbeitbar machen
    text_widget.configure(state=tk.NORMAL)

    # Leeren des Textfelds
    text_widget.delete("1.0", tk.END)

    # Füllen des Text-Widgets
    text_widget.insert(tk.INSERT, "Gütemaß Genauigkeit:\n", 'bold')
    text_widget.insert(tk.END, "Genauigkeit = ")
    text_widget.insert(tk.END, "Anzahl korrekt klassifizierter Datenobjekte", 'blue')
    text_widget.insert(tk.END, " / Anzahl aller Datenobjekte\n")
    text_widget.insert(tk.END, "Genauigkeit", 'white')
    text_widget.insert(tk.END, " = ")
    text_widget.insert(tk.END, str(number_classified_correctly), 'blue')
    text_widget.insert(tk.END, " / " + str(number_all) + "\n")
    text_widget.insert(tk.END, "Genauigkeit", 'white')
    text_widget.insert(tk.END, " = ")
    text_widget.insert(tk.END, str(precision))
    text_widget.insert(tk.END, " = ")
    text_widget.insert(tk.END, str(precision * 100))
    text_widget.insert(tk.END, "%\n")
    if not_classifiable != 0:
        text_widget.insert(tk.END, "Hinweis:  ", 'bold')
        text_widget.insert(tk.END, str(not_classifiable), "red_bold")
        # Behandlung Plural und Singular
        if not_classifiable == 1:
            text_widget.insert(tk.END, " Testdatenobjekt konnte nicht zugeordnet werden.\n")
        else:
            text_widget.insert(tk.END, " Testdatenobjekte konnten nicht zugeordnet werden.\n")
        text_widget.insert(tk.END, "Hinweis:  ", 'white_bold')
        text_widget.insert(tk.END,
                           "Mögl. Gründe: Nicht zum Training passende Testdaten,"
                           " nicht trainierte Label/Merkmalswerte,...")

    # Konfiguration der Tags
    text_widget.tag_configure('bold', font=default_FONT_BOLD)
    text_widget.tag_configure('red_bold', foreground="red", font=default_FONT_BOLD)
    text_widget.tag_configure('white_bold', foreground="white", font=default_FONT_BOLD)
    text_widget.tag_configure('blue', foreground="blue")
    text_widget.tag_configure('white', foreground="white")

    # Textfeld Read-Only machen
    text_widget.configure(state=tk.DISABLED)


def clear_treeview(treeview):
    # Löschen der Header-Zeile
    treeview["columns"] = ()

    # Leeren des Treeview
    for child in treeview.get_children():
        treeview.delete(child)


def fill_treeview_with_data(treeview, dataset):
    # Anzahl der Columns über die Elemente im Header festlegen
    treeview["columns"] = dataset[0]

    # Headerwerte anzeigen
    treeview['show'] = 'headings'

    # Berechnung der Spaltenbreite in Abhängigkeit von der Fensterbreite
    num_of_columns = len(dataset[0])
    # Sorgt für der leeren Treeview auf Treeviewbreite
    if num_of_columns == 0:
        num_of_columns = 1

    col_width = treeview.winfo_width() // num_of_columns

    # Layout der Headerzeile festlegen und Werte in die Headerzeile speichern
    for d in dataset[0]:
        treeview.column(column=d, minwidth=200, width=col_width, anchor='c', stretch=True)
        treeview.heading(column=d, text=str(d))

    even_flag = "even"

    # Befüllen der Treeview-Tabelle mit den Werten
    for d in dataset[1:]:
        treeview.insert(parent="", index='end', text="L1", values=d, tags=even_flag)
        if even_flag == "even":
            even_flag = "odd"
        else:
            even_flag = "even"

    treeview.tag_configure("even", background='#C6E2FF')
    treeview.tag_configure("odd", background='#FFFFFF')


def clear_treeview_without_header(treeview):
    # Leeren des Treeview
    for child in treeview.get_children():
        treeview.delete(child)


def fill_treeview_with_calculated_labels(treeview, label_column, calculated_labels):
    # Header festlegen
    treeview["columns"] = ['col_calc_label']
    # Headerwerte anzeigen
    treeview['show'] = 'headings'

    # Layout der Headerzeile festlegen und Werte in die Headerzeile speichern
    treeview.column(column="col_calc_label", minwidth=200, anchor='c', stretch=True)
    treeview.heading(column="col_calc_label", text="Berechnetes Label")

    # Befüllen der Treeview-Tabelle mit den Werten
    even_flag = "odd"
    for calc_label, actual_label in zip(calculated_labels, label_column):
        if even_flag == "even":
            even_flag = "odd"
        else:
            even_flag = "even"

        if calc_label == actual_label:
            predicted_correctly = "correct"
        else:
            predicted_correctly = "incorrect"
        treeview.insert(parent="", index='end', text="L1", values=str(calc_label), tags=predicted_correctly + even_flag)

    treeview.tag_configure("incorrecteven", background='#C6E2FF', foreground='red', font=default_FONT_BOLD)
    treeview.tag_configure("incorrectodd", background='#FFFFFF', foreground='red', font=default_FONT_BOLD)

    treeview.tag_configure("correcteven", background='#C6E2FF')
    treeview.tag_configure("correctodd", background='#FFFFFF')


class GUI_Node_Details_Window:

    def __init__(self, main_gui, main_object):
        # Toplevel Fenster
        self.window = tk.Toplevel(master=main_gui.main_window)
        self.window.title("Knotendetails anzeigen")
        self.main_object = main_object

        self.window.geometry("825x420")
        self.window.wm_minsize(460, 275)

        # Dynamische Größenanpassung an das Fenster.
        # Alles in column 0 des main_window wird an die Breite des Fensters angepasst
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(2, weight=1)

        # Redefinition des Befehls beim Schließen des Fensters
        self.window.protocol('WM_DELETE_WINDOW', lambda: self.close_node_details_window(main_gui=main_gui))

        # Widgets für die Kontrollzeile der
        self.frm_controls = None
        self.frm_enter_node_number = None
        self.lbl_enter_node_number = None
        self.entered_node_number = None
        self.etr_node_number = None
        self.btn_show_details_of_node = None

        # Widgets für die Anzeige der Informationsgewinne
        self.frm_display_information_gains = None
        self.frm_display_best_attribute = None
        self.lbl_best_attribute_label = None
        self.lbl_best_attribute_value = None
        self.lbl_information_gains_label = None
        self.treeview_information_gains = None
        self.scrollbar_horizontal_display_information_gains = None

        # Widgets für die Anzeige der Daten des Knotens
        self.frm_display_data = None
        self.treeview_data = None
        self.scrollbar_vertical_display_data = None
        self.scrollbar_horizontal_display_data = None

        self.init_gui_node_details_controls()
        self.init_gui_node_details_display_information_gains()
        self.init_gui_node_details_display_data()

    def init_gui_node_details_controls(self):
        self.entered_node_number = tk.StringVar(master=self.window)

        self.frm_controls = tk.Frame(master=self.window)

        self.frm_controls.grid(column=0, row=0, sticky="nsew")

        self.frm_enter_node_number = tk.LabelFrame(master=self.frm_controls,
                                                   text="Knotennummer eingeben",
                                                   font=default_FONT_BOLD, borderwidth=0)
        self.frm_enter_node_number.grid(column=0, row=0, padx=(5, 0))

        self.lbl_enter_node_number = ttk.Label(master=self.frm_enter_node_number,
                                               text="Knotennummer: ",
                                               font=default_FONT_BOLD)
        self.lbl_enter_node_number.grid(column=0, row=0, sticky="w")

        self.etr_node_number = ttk.Entry(master=self.frm_enter_node_number,
                                         textvariable=self.entered_node_number)
        self.etr_node_number.grid(column=1, row=0, sticky="nw", padx=(0, 10))

        self.btn_show_details_of_node = ttk.Button(master=self.frm_controls, text="Details anzeigen", width=21,
                                                   command=self.main_object.call_display_node_details)
        self.btn_show_details_of_node.grid(column=1, row=0, padx=(10, 10), pady=(10, 0))

    def init_gui_node_details_display_information_gains(self):
        self.frm_display_information_gains = tk.LabelFrame(master=self.window,
                                                           text="Bestes Attribut und Informationsgewinne:",
                                                           font=default_FONT_BOLD, borderwidth=0)
        self.frm_display_information_gains.columnconfigure(0, weight=1)
        self.frm_display_information_gains.rowconfigure(1, weight=1)

        self.frm_display_information_gains.grid(column=0, row=1, padx=(5, 5), sticky="ew", pady=(15, 0))

        self.frm_display_best_attribute = tk.Frame(master=self.frm_display_information_gains)
        self.frm_display_best_attribute.grid(column=0, row=0, sticky="nsew")
        self.lbl_best_attribute_label = ttk.Label(master=self.frm_display_best_attribute, text="Bestes Attribut: ",
                                                  font=default_FONT_ITALIC)
        self.lbl_best_attribute_label.pack(side=tk.LEFT)
        self.lbl_best_attribute_value = ttk.Label(master=self.frm_display_best_attribute, text="  ",
                                                  font=default_FONT)
        self.lbl_best_attribute_value.pack(side=tk.LEFT)
        self.lbl_information_gains_label = ttk.Label(master=self.frm_display_information_gains,
                                                     text="Informationsgewinne der einzelnen Attribute:",
                                                     font=default_FONT_ITALIC)
        self.lbl_information_gains_label.grid(column=0, row=1, pady=(5, 0), sticky="w")

        # TreeView zum Anzeigen der Daten
        self.treeview_information_gains = ttk.Treeview(master=self.frm_display_information_gains, selectmode='none',
                                                       height=1)
        self.treeview_information_gains.grid(column=0, row=1, sticky="ew")

        # Scrollbar für die Anzeige der Informationsgewinne
        self.scrollbar_horizontal_display_information_gains = ttk.Scrollbar(master=self.frm_display_information_gains,
                                                                            orient="horizontal")
        self.scrollbar_horizontal_display_information_gains.config(command=self.treeview_information_gains.xview)
        self.scrollbar_horizontal_display_information_gains.grid(column=0, row=2, sticky="ew")

        self.treeview_information_gains.configure(
            xscrollcommand=self.scrollbar_horizontal_display_information_gains.set)

    def init_gui_node_details_display_data(self):
        self.frm_display_data = tk.LabelFrame(master=self.window, text="Daten des Knotens(0 Elemente):",
                                              font=default_FONT_BOLD, borderwidth=0)

        self.frm_display_data.grid(column=0, row=2, sticky="nsew", pady=(5, 0), padx=(5, 0))
        self.frm_display_data.columnconfigure(0, weight=1)
        self.frm_display_data.rowconfigure(0, weight=1)

        # TreeView zum Anzeigen der Daten
        self.treeview_data = ttk.Treeview(master=self.frm_display_data, selectmode='none')

        self.treeview_data.grid(column=0, row=0, sticky="nsew")

        self.scrollbar_vertical_display_data = ttk.Scrollbar(master=self.frm_display_data,
                                                             orient="vertical")
        self.scrollbar_vertical_display_data.config(command=self.treeview_data.yview)

        self.scrollbar_vertical_display_data.grid(column=1, row=0, sticky="ns")

        self.treeview_data.configure(yscrollcommand=self.scrollbar_vertical_display_data.set)

        self.scrollbar_horizontal_display_data = ttk.Scrollbar(master=self.frm_display_data,
                                                               orient="horizontal")
        self.scrollbar_horizontal_display_data.config(command=self.treeview_data.xview)

        self.scrollbar_horizontal_display_data.grid(column=0, row=1, sticky="ew")

        self.treeview_data.configure(xscrollcommand=self.scrollbar_horizontal_display_data.set)

    def fill_information_gains_and_best_attribute(self, current_node):
        self.lbl_best_attribute_value['text'] = current_node.node_attribute

        attributes = [" "] + list(current_node.node_information_gains.keys())
        info_gains = ["Informationsgewinn"] + ['{:f}'.format(ig) for ig in
                                               list(current_node.node_information_gains.values())]

        # Anzahl der Columns über die Elemente im Header festlegen
        self.treeview_information_gains["columns"] = attributes

        # Headerwerte anzeigen
        self.treeview_information_gains['show'] = 'headings'

        col_width = self.treeview_information_gains.winfo_width() // len(attributes)

        # Layout der Headerzeile festlegen und Werte in die Headerzeile speichern
        for d in attributes:
            self.treeview_information_gains.column(column=d, minwidth=200, width=col_width, anchor='c',
                                                   stretch=True)
            self.treeview_information_gains.heading(column=d, text=str(d))

        # Befüllen der Treeview-Tabelle mit den Werten
        self.treeview_information_gains.insert(parent="", index='end', text="L1", values=info_gains)

    def show_node_details_window(self):
        self.window.deiconify()

    def close_node_details_window(self, main_gui):
        """
        Schließt das Fenster zur Anzeige der Knotendetails und setzt es auf den Initialzustand zurück
        :param main_gui: Referenz auf das Hauptfenster; wird benötigt, damit auch die Checkbox "Knotendetails anzeigen"
                         "unset" wird
        """
        # Häkchen in Checkbox entfernen
        main_gui.show_window_node_details.set(0)

        # Daten zurücksetzen
        self.entered_node_number.set("")
        self.lbl_best_attribute_value['text'] = " "

        # Leeren des Treeview treeview_information_gains
        clear_treeview(treeview=self.treeview_information_gains)

        # Leeren des Treeview treeview_data
        clear_treeview(treeview=self.treeview_data)

        # Hinzufügen der Anzeige der Informationsgewinne, falls vor Schließen des Fensters ein Blatt angezeigt wurde
        # und diese Anzeige somit entfernt wurde
        self.frm_display_information_gains.grid(column=0, row=1, padx=(5, 5), sticky="ew", pady=(15, 0))

        # Zurücksetzen der Anzeige der Elementanzahl der Knotendatensatzes
        self.frm_display_data['text'] = "Daten des Knotens(0 Elemente):"

        # Ausblenden des Fensters
        self.window.withdraw()
