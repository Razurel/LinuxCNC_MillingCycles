#!/usr/bin/env python3

import os
import sys
import subprocess
import math
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
    "linie.ngc"
)


# ============================================================
# HAL FLOAT lesen
# ============================================================

def hal_value(pin_name, description=None):

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


# ============================================================
# Fehler-Popup
# ============================================================

def show_error(message):

    root = tk.Tk()
    root.withdraw()

    messagebox.showerror(
        "Linie – Eingabefehler",
        message,
        parent=root
    )

    root.destroy()


# ============================================================
# AXIS Datei laden
# ============================================================

def load_in_axis():

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
        "Linie in AXIS geladen."
    )


# ============================================================
# Linie erzeugen
# ============================================================

def create_linie():

    # --------------------------------------------------------
    # Werte aus GTK / HAL
    # --------------------------------------------------------

    fraeser_d = hal_value(
        "milling_cycles.line_cutter_diameter"
    )

    laenge = hal_value(
        "milling_cycles.line_length"
    )

    tiefe = hal_value(
        "milling_cycles.line_depth"
    )

    z_zustellung = hal_value(
        "milling_cycles.line_z_step"
    )

    start_z = hal_value(
        "milling_cycles.line_start_z"
    )

    winkel = hal_value(
        "milling_cycles.line_angle"
    )

    feed_approach = hal_value(
        "milling_cycles.line_feed_approach",
        "Der Zustell-Feed"
    )

    feed_mill = hal_value(
        "milling_cycles.line_feed_mill",
        "Der Schnitt-Feed"
    )


    # ========================================================
    # Prüfungen
    # ========================================================

    if fraeser_d <= 0:

        raise ValueError(
            "Fräserdurchmesser muss größer als 0 sein."
        )

    if laenge <= 0:

        raise ValueError(
            "Schnittlänge muss größer als 0 sein."
        )

    if tiefe <= 0:

        raise ValueError(
            "Frästiefe muss größer als 0 sein."
        )

    if z_zustellung <= 0:

        raise ValueError(
            "Z-Zustellung muss größer als 0 sein."
        )

    if start_z < 0:

        raise ValueError(
            "Start Z darf nicht negativ sein."
        )

    if feed_approach <= 0:

        raise ValueError(
            "Zustell-Feed muss größer als 0 sein."
        )

    if feed_mill <= 0:

        raise ValueError(
            "Schnitt-Feed muss größer als 0 sein."
        )

    if winkel < 0 or winkel > 360:

        raise ValueError(
            "Winkel muss zwischen 0° und 360° liegen."
        )


    # ========================================================
    # Winkel berechnen
    #
    # 0°   = nach hinten   (+Y)
    # 90°  = nach rechts   (+X)
    # 180° = nach vorne    (-Y)
    # 270° = nach links    (-X)
    # 360° = nach hinten   (+Y)
    # ========================================================

    winkel_rad = math.radians(winkel)

    dx = math.sin(winkel_rad) * laenge
    dy = math.cos(winkel_rad) * laenge


    # ========================================================
    # Startpunkt
    # ========================================================

    start_x = 0.0
    start_y = 0.0


    # ========================================================
    # Endpunkt
    # ========================================================

    end_x = start_x + dx
    end_y = start_y + dy


    # ========================================================
    # G-Code erzeugen
    # ========================================================

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
            "( LINIE - Fraeszyklen                     )\n"
        )

        f.write(
            "( ========================================== )\n"
        )

        f.write(
            f"( Fraeserdurchmesser: {fraeser_d:.3f} mm )\n"
        )

        f.write(
            f"( Schnittlaenge     : {laenge:.3f} mm )\n"
        )

        f.write(
            f"( Fraestiefe        : {tiefe:.3f} mm )\n"
        )

        f.write(
            f"( Z-Zustellung      : {z_zustellung:.3f} mm )\n"
        )

        f.write(
            f"( Start Z           : {start_z:.3f} mm )\n"
        )

        f.write(
            f"( Winkel            : {winkel:.1f} Grad )\n"
        )

        f.write(
            "( 0 Grad = hinten / 90 Grad = rechts )\n"
        )

        f.write(
            "( 180 Grad = vorne / 270 Grad = links )\n"
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
        # Startposition
        # ----------------------------------------------------

        f.write(
            "( Startposition )\n"
        )

        f.write(
            f"G0 X{start_x:.6f} "
            f"Y{start_y:.6f}\n"
        )

        f.write(
            f"G0 Z{start_z:.6f}\n"
        )

        f.write("\n")


        # ====================================================
        # Tiefenzustellungen
        # ====================================================

        current_depth = 0.0

        while current_depth < tiefe:

            next_depth = min(
                current_depth + z_zustellung,
                tiefe
            )

            current_z = -next_depth


            f.write(
                f"( Zustellung Z{current_z:.3f} )\n"
            )

            f.write(
                f"F{feed_approach:.3f}\n"
            )


            # ------------------------------------------------
            # Bei jeder neuen Ebene zuerst sicher hoch
            # und zum Startpunkt zurück
            # ------------------------------------------------

            if current_depth > 0.0:

                f.write(
                    f"G0 Z{start_z:.6f}\n"
                )

                f.write(
                    f"G0 X{start_x:.6f} "
                    f"Y{start_y:.6f}\n"
                )


            # ------------------------------------------------
            # Auf neue Z-Tiefe
            # ------------------------------------------------

            f.write(
                f"G1 Z{current_z:.6f}\n"
            )

            f.write(
                f"F{feed_mill:.3f}\n"
            )

            f.write("\n")


            # ------------------------------------------------
            # Schnitt
            # ------------------------------------------------

            f.write(
                f"G1 X{end_x:.6f} "
                f"Y{end_y:.6f}\n"
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


    # ========================================================
    # Ausgabe
    # ========================================================

    print(
        "Linie erfolgreich erzeugt:"
    )

    print(
        NGC_FILE
    )

    print(
        "Fräser:",
        fraeser_d
    )

    print(
        "Schnittlänge:",
        laenge
    )

    print(
        "Frästiefe:",
        tiefe
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
        "Winkel:",
        winkel
    )

    print(
        "Endpunkt X:",
        end_x
    )

    print(
        "Endpunkt Y:",
        end_y
    )


# ============================================================
# Hauptprogramm
# ============================================================

def main():

    print(
        "Linie Python gestartet."
    )

    try:

        create_linie()

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
