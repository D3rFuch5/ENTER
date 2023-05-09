import math
import random

color_list10 = ['#ff002970', '#ff700070', '#f5ff0070', '#5cff0070', '#00ff3d70', '#00ffd570', '#008fff70', '#0b00ff70',
                '#a500ff70', '#ff00bf70']

color_list100 = ['#ff002970', '#ff001b70', '#ff000d70', '#ff000070', '#ff0e0070', '#ff1c0070', '#ff2a0070', '#ff380070',
                 '#ff460070', '#ff540070', '#ff620070', '#ff700070', '#ff7e0070', '#ff8c0070', '#ff9a0070', '#ffa70070',
                 '#ffb50070', '#ffc30070', '#ffd10070', '#ffdf0070', '#ffed0070', '#fffb0070', '#f5ff0070', '#e7ff0070',
                 '#d9ff0070', '#cbff0070', '#bdff0070', '#afff0070', '#a2ff0070', '#94ff0070', '#86ff0070', '#78ff0070',
                 '#6aff0070', '#5cff0070', '#4eff0070', '#40ff0070', '#32ff0070', '#24ff0070', '#16ff0070', '#08ff0070',
                 '#00ff0670', '#00ff1370', '#00ff2170', '#00ff2f70', '#00ff3d70', '#00ff4b70', '#00ff5970', '#00ff6670',
                 '#00ff7470', '#00ff8270', '#00ff9070', '#00ff9e70', '#00ffac70', '#00ffba70', '#00ffc770', '#00ffd570',
                 '#00ffe370', '#00fff170', '#00ffff70', '#00f1ff70', '#00e3ff70', '#00d5ff70', '#00c7ff70', '#00b9ff70',
                 '#00abff70', '#009dff70', '#008fff70', '#0081ff70', '#0073ff70', '#0065ff70', '#0057ff70', '#0049ff70',
                 '#003bff70', '#002dff70', '#001fff70', '#0011ff70', '#0003ff70', '#0b00ff70', '#1900ff70', '#2700ff70',
                 '#3500ff70', '#4300ff70', '#5100ff70', '#5f00ff70', '#6d00ff70', '#7b00ff70', '#8900ff70', '#9700ff70',
                 '#a500ff70', '#b300ff70', '#c100ff70', '#cf00ff70', '#dd00ff70', '#eb00ff70', '#f900ff70', '#ff00f770',
                 '#ff00e970', '#ff00db70', '#ff00cd70', '#ff00bf70']


def get_color_List(number_of_colors):
    color_list_length = len(color_list100)
    # Auslesen der notwendigen Zahlen aus einer vorbereiteten Farbliste
    if number_of_colors <= color_list_length:
        step = math.floor(color_list_length / number_of_colors)
        node_colors = color_list100[:step * number_of_colors:step]
    # Falls in der Farbliste zu wenig Farben sind, werden zufällig weitere generiert
    else:
        node_colors = color_list100.copy()
        for i in range(number_of_colors - color_list_length):
            # Erstellen einer zufälligen Zahl im RGB-Zahlenbereich
            new_color_as_int = random.randrange(0, 2 ** 24)

            # Umwandlung in eine Hexadezimalzahl
            new_hex_color = hex(new_color_as_int)

            # Anfügen der zufälligen Zahl
            node_colors.append("#" + new_hex_color[2:] + "70")

    return node_colors
