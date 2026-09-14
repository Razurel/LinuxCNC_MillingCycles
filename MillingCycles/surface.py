
#!/usr/bin/env python3

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox


# ============================================================
# Einstellungen
# ============================================================

SCRIPT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

NGC_FILE = os.path.join(
    SCRIPT_DIR,
    "oberflaeche.ngc"
)


# ============================================================
# FEHLER-POPUP
# ============================================================

def show_error(message):

    root = tk.Tk()

    root.withdraw()

    root.attributes("-topmost", True)

    messagebox.showerror(
        "Fehler bei Oberflächen-Fräsung",
        message,
        parent=root
    )

    root.destroy()


# ============================================================
# HAL FLOAT lesen
# ============================================================

def hal_value(pin_name, description):

    try:

        result = subprocess.run(
            [
                "halcmd",
                "getp",
                pin_name
            ],
            capture_output=True,
            text=True,
            check=True
        )

        return float(
            result.stdout.strip()
        )

    except (
        subprocess.CalledProcessError,
        ValueError,
        OSError
    ):

        raise ValueError(
            f"{description} konnte nicht aus "
            f"der Bedienoberfläche gelesen werden."
        )


# ============================================================
# HAL BIT lesen
# ============================================================

def hal_bit(pin_name):

    try:

        result = subprocess.run(
            [
                "halcmd",
                "getp",
                pin_name
            ],
            capture_output=True,
            text=True,
            check=True
        )

        value = result.stdout.strip().lower()

        return value in (
            "true",
            "1",
            "on"
        )

    except (
        subprocess.CalledProcessError,
        ValueError,
        OSError
    ):

        raise ValueError(
            "Der Startpunkt konnte nicht aus "
            "der Bedienoberfläche gelesen werden."
        )


# ============================================================
# Startpunkt lesen
# ============================================================

def get_startpunkt():

    pins = {
        "links_oben":
            "milling_cycles.surface_start_left_top",

        "rechts_oben":
            "milling_cycles.surface_start_right_top",

        "links_unten":
            "milling_cycles.surface_start_left_bottom",

        "rechts_unten":
            "milling_cycles.surface_start_right_bottom"
    }

    active = []

    for name, pin in pins.items():

        if hal_bit(pin):
            active.append(name)

    if len(active) != 1:

        raise ValueError(
            "Es muss genau ein Startpunkt "
            "ausgewählt sein."
        )

    return active[0]


# ============================================================
# AXIS Datei laden
# ============================================================

def load_in_axis():

    try:

        subprocess.Popen(
            [
                "axis-remote",
                NGC_FILE
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

        print(
            "Oberfläche in AXIS geladen."
        )

    except OSError:

        raise RuntimeError(
            "Die Vorschau wurde erzeugt, "
            "konnte aber nicht in AXIS geladen werden."
        )


# ============================================================
# Bahnpositionen erzeugen
# ============================================================

def build_pass_positions(lower, upper, step):

    if step <= 0:

        raise ValueError(
            "Der berechnete Bahnabstand muss "
            "größer als 0 sein."
        )

    positions = [lower]

    while positions[-1] < upper:

        next_position = positions[-1] + step

        if next_position >= upper:

            if positions[-1] != upper:
                positions.append(upper)

            break

        positions.append(next_position)

    return positions


# ============================================================
# Oberfläche erzeugen
# ============================================================

def create_oberflaeche():

    # --------------------------------------------------------
    # Werte aus PyVCP
    # --------------------------------------------------------

    fraeser_d = hal_value(
        "milling_cycles.surface_cutter_diameter",
        "Der Fräserdurchmesser"
    )

    z_zustellung = hal_value(
        "milling_cycles.surface_z_step",
        "Die Z-Zustellung"
    )

    breite = hal_value(
        "milling_cycles.surface_width",
        "Die Werkstück-Breite"
    )

    tiefe = hal_value(
        "milling_cycles.surface_depth",
        "Die Werkstück-Tiefe"
    )

    fraestiefe = hal_value(
        "milling_cycles.surface_milling_depth",
        "Die Frästiefe"
    )

    start_z = hal_value(
        "milling_cycles.surface_start_z",
        "Der Start Z"
    )

    ueberlappung = hal_value(
        "milling_cycles.surface_overlap",
        "Die Überlappung"
    )

    feed_approach = hal_value(
        "milling_cycles.surface_feed_approach",
        "Der Zustell-Feed"
    )

    feed_mill = hal_value(
        "milling_cycles.surface_feed_mill",
        "Der Schnitt-Feed"
    )

    startpunkt = get_startpunkt()


    # --------------------------------------------------------
    # Prüfungen
    # --------------------------------------------------------

    if fraeser_d <= 0:

        raise ValueError(
            "Der Fräserdurchmesser muss "
            "größer als 0 sein.\n\n"
            f"Fräserdurchmesser: {fraeser_d:.3f} mm"
        )


    if z_zustellung <= 0:

        raise ValueError(
            "Die Z-Zustellung muss "
            "größer als 0 sein.\n\n"
            f"Z-Zustellung: {z_zustellung:.3f} mm"
        )


    if breite <= 0:

        raise ValueError(
            "Die Werkstück-Breite muss "
            "größer als 0 sein.\n\n"
            f"Werkstück-Breite: {breite:.3f} mm"
        )


    if tiefe <= 0:

        raise ValueError(
            "Die Werkstück-Tiefe muss "
            "größer als 0 sein.\n\n"
            f"Werkstück-Tiefe: {tiefe:.3f} mm"
        )


    if fraestiefe <= 0:

        raise ValueError(
            "Die Frästiefe muss "
            "größer als 0 sein.\n\n"
            f"Frästiefe: {fraestiefe:.3f} mm"
        )


    if start_z < 0:

        raise ValueError(
            "Der Start Z darf "
            "nicht negativ sein.\n\n"
            f"Start Z: {start_z:.3f} mm"
        )


    if ueberlappung < 0 or ueberlappung >= 100:

        raise ValueError(
            "Die Überlappung muss "
            "zwischen 0 und 99 Prozent liegen.\n\n"
            f"Überlappung: {ueberlappung:.1f} %"
        )


    if feed_approach <= 0:

        raise ValueError(
            "Der Zustell-Feed muss "
            "größer als 0 sein.\n\n"
            f"Zustell-Feed: {feed_approach:.3f} mm/min"
        )


    if feed_mill <= 0:

        raise ValueError(
            "Der Schnitt-Feed muss "
            "größer als 0 sein.\n\n"
            f"Schnitt-Feed: {feed_mill:.3f} mm/min"
        )


    # ========================================================
    # Bahnabstand
    # ========================================================

    bahnabstand = (
        fraeser_d
        * (1.0 - ueberlappung / 100.0)
    )

    if bahnabstand <= 0:

        raise ValueError(
            "Der berechnete Bahnabstand ist ungültig.\n\n"
            f"Fräserdurchmesser: {fraeser_d:.3f} mm\n"
            f"Überlappung: {ueberlappung:.1f} %"
        )


    # ========================================================
    # Flächengrenzen
    # ========================================================

    x_min = 0.0
    x_max = breite

    y_min = 0.0
    y_max = tiefe


    # ========================================================
    # Y-Bahnen erzeugen
    # ========================================================

    y_positions = build_pass_positions(
        y_min,
        y_max,
        bahnabstand
    )


    # ========================================================
    # Startpunkt
    # ========================================================

    if startpunkt == "links_oben":

        y_positions.reverse()
        first_left_to_right = True

    elif startpunkt == "rechts_oben":

        y_positions.reverse()
        first_left_to_right = False

    elif startpunkt == "links_unten":

        first_left_to_right = True

    elif startpunkt == "rechts_unten":

        first_left_to_right = False

    else:

        raise ValueError(
            "Ungültiger Startpunkt."
        )


    # ========================================================
    # Erste Position
    # ========================================================

    first_y = y_positions[0]

    if first_left_to_right:

        first_x = x_min

    else:

        first_x = x_max


    # ========================================================
    # G-Code erzeugen
    # ========================================================

    try:

        with open(
            NGC_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            # ----------------------------------------------------
            # Kopf
            # ----------------------------------------------------

            f.write(
                "( ========================================== )\n"
            )

            f.write(
                "( OBERFLAECHE - Fraeszyklen               )\n"
            )

            f.write(
                "( ========================================== )\n"
            )

            f.write(
                f"( Fraeserdurchmesser: {fraeser_d:.3f} mm )\n"
            )

            f.write(
                f"( Breite            : {breite:.3f} mm )\n"
            )

            f.write(
                f"( Tiefe             : {tiefe:.3f} mm )\n"
            )

            f.write(
                f"( Fraestiefe        : {fraestiefe:.3f} mm )\n"
            )

            f.write(
                f"( Z-Zustellung      : {z_zustellung:.3f} mm )\n"
            )

            f.write(
                f"( Start Z           : {start_z:.3f} mm )\n"
            )

            f.write(
                f"( Ueberlappung      : {ueberlappung:.1f} % )\n"
            )

            f.write(
                f"( Bahnabstand       : {bahnabstand:.3f} mm )\n"
            )

            f.write(
                f"( Startpunkt        : {startpunkt} )\n"
            )

            f.write(
                "( Maeander: Hin und Her )\n"
            )

            f.write(
                "( Spindeldrehrichtung bleibt unveraendert )\n"
            )

            f.write(
                "( ========================================== )\n"
            )

            f.write("\n")


            # ----------------------------------------------------
            # Modalwerte
            # ----------------------------------------------------

            f.write("G21\n")
            f.write("G17\n")
            f.write("G90\n")
            f.write(f"F{feed_mill:.3f}\n")

            f.write("\n")


            # ----------------------------------------------------
            # Einmalige Startposition
            # ----------------------------------------------------

            f.write(
                "( Startposition )\n"
            )

            f.write(
                f"G0 X{first_x:.6f} "
                f"Y{first_y:.6f}\n"
            )

            f.write(
                f"G0 Z{start_z:.6f}\n"
            )

            f.write("\n")


            # ====================================================
            # Tiefenzustellungen
            # ====================================================

            current_depth = 0.0

            while current_depth < fraestiefe:

                next_depth = min(
                    current_depth + z_zustellung,
                    fraestiefe
                )

                current_z = -next_depth


                f.write(
                    f"( Zustellung Z{current_z:.3f} )\n"
                )


                # ------------------------------------------------
                # Ab zweiter Z-Ebene zuerst sicher hoch und zurück
                # ------------------------------------------------

                if current_depth > 0.0:

                    f.write(
                        f"G0 Z{start_z:.6f}\n"
                    )

                    f.write(
                        f"G0 X{first_x:.6f} "
                        f"Y{first_y:.6f}\n"
                    )


                # ------------------------------------------------
                # Auf neue Z-Tiefe
                # ------------------------------------------------

                f.write(
                    f"F{feed_approach:.3f}\n"
                )

                f.write(
                    f"G1 Z{current_z:.6f}\n"
                )

                f.write(
                    f"F{feed_mill:.3f}\n"
                )

                f.write("\n")


                # =================================================
                # Echter Mäander
                # =================================================

                direction_left_to_right = (
                    first_left_to_right
                )


                for index, y in enumerate(y_positions):

                    if direction_left_to_right:

                        end_x = x_max

                    else:

                        end_x = x_min


                    # ------------------------------------------------
                    # Längsbahn
                    # ------------------------------------------------

                    f.write(
                        f"G1 X{end_x:.6f} "
                        f"Y{y:.6f}\n"
                    )


                    # ------------------------------------------------
                    # Seitlicher Übergang
                    #
                    # G1 = zusammenhängender Schnittzug
                    # ------------------------------------------------

                    if index < len(y_positions) - 1:

                        next_y = y_positions[index + 1]

                        f.write(
                            f"G1 X{end_x:.6f} "
                            f"Y{next_y:.6f}\n"
                        )


                    direction_left_to_right = (
                        not direction_left_to_right
                    )


                f.write("\n")

                current_depth = next_depth


            # ====================================================
            # Z-Rückzug
            # ====================================================

            f.write(
                "( Z zuerst hoch )\n"
            )

            f.write(
                "G53 G0 Z2.000\n"
            )

            f.write("\n")


            # ====================================================
            # X/Y zurück
            # ====================================================

            f.write(
                "( X/Y erst nach Z-Rueckzug )\n"
            )

            f.write(
                "G53 G0 X0.000 Y0.000\n"
            )

            f.write("\n")

            f.write(
                "M2\n"
            )

    except OSError:

        raise RuntimeError(
            "Die Vorschau konnte nicht erzeugt werden.\n\n"
            "Die Datei 'oberflaeche.ngc' konnte nicht "
            "geschrieben werden."
        )


    # ========================================================
    # Ausgabe
    # ========================================================

    print(
        "Oberfläche erfolgreich erzeugt:"
    )

    print(
        NGC_FILE
    )

    print(
        "Fräser:",
        fraeser_d
    )

    print(
        "Breite:",
        breite
    )

    print(
        "Tiefe:",
        tiefe
    )

    print(
        "Frästiefe:",
        fraestiefe
    )

    print(
        "Z-Zustellung:",
        z_zustellung
    )

    print(
        "Start Z:",
        start_z
    )

    print(
        "Überlappung:",
        ueberlappung,
        "%"
    )

    print(
        "Bahnabstand:",
        bahnabstand
    )

    print(
        "Startpunkt:",
        startpunkt
    )

    print(
        "Mäander: hin und her"
    )

    print(
        "Spindeldrehrichtung: unverändert"
    )


# ============================================================
# Hauptprogramm
# ============================================================

def main():

    print(
        "Oberfläche Python gestartet."
    )

    try:

        create_oberflaeche()

        load_in_axis()

    except Exception as error:

        print(
            "FEHLER beim Erzeugen:",
            error
        )

        show_error(
            str(error)
        )

        sys.exit(1)


# ============================================================
# Programmstart
# ============================================================

if __name__ == "__main__":

    main()

