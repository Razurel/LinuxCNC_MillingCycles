#!/usr/bin/env python3

import os
import sys
import math
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
    "circle.ngc"
)


# ============================================================
# FEHLER-POPUP
# ============================================================

def show_error(message):

    root = tk.Tk()

    root.withdraw()

    root.attributes("-topmost", True)

    messagebox.showerror(
        "Fehler bei Kreis-Fräsung",
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
            "Kreis in AXIS geladen."
        )

    except OSError:

        raise RuntimeError(
            "Die Vorschau wurde erzeugt, "
            "konnte aber nicht in AXIS geladen werden."
        )


# ============================================================
# Kreis erzeugen
# ============================================================

def create_circle():

    diameter = hal_value(
        "milling_cycles.circle_diameter",
        "Der Lochdurchmesser"
    )

    depth = hal_value(
        "milling_cycles.circle_depth",
        "Die Bohrtiefe"
    )

    tool_diameter = hal_value(
        "milling_cycles.circle_cutter_diameter",
        "Der Fräserdurchmesser"
    )

    pitch = hal_value(
        "milling_cycles.circle_pitch",
        "Die Spiralensteigung"
    )

    start_z = hal_value(
        "milling_cycles.circle_start_z",
        "Der Helix-Start"
    )

    retract = hal_value(
        "milling_cycles.circle_retract",
        "Der Rückzug zur Mitte"
    )

    feed_approach = hal_value(
        "milling_cycles.circle_feed_approach",
        "Der Zustell-Feed"
    )

    feed_mill = hal_value(
        "milling_cycles.circle_feed_mill",
        "Der Schnitt-Feed"
    )


    # ========================================================
    # Prüfungen
    # ========================================================

    if diameter <= 0:

        raise ValueError(
            "Der Lochdurchmesser muss "
            "größer als 0 sein."
        )


    if depth <= 0:

        raise ValueError(
            "Die Bohrtiefe muss "
            "größer als 0 sein."
        )


    if tool_diameter <= 0:

        raise ValueError(
            "Der Fräserdurchmesser muss "
            "größer als 0 sein."
        )


    if pitch <= 0:

        raise ValueError(
            "Die Spiralensteigung muss "
            "größer als 0 sein."
        )


    if start_z < 0:

        raise ValueError(
            "Der Helix-Start darf "
            "nicht negativ sein."
        )


    if retract < 0:

        raise ValueError(
            "Der Rückzug zur Mitte darf "
            "nicht negativ sein."
        )


    if feed_approach <= 0:

        raise ValueError(
            "Der Zustell-Feed muss "
            "größer als 0 sein."
        )


    if feed_mill <= 0:

        raise ValueError(
            "Der Schnitt-Feed muss "
            "größer als 0 sein."
        )


    if tool_diameter >= diameter:

        raise ValueError(
            "Der Fräserdurchmesser muss kleiner "
            "als der Lochdurchmesser sein.\n\n"
            f"Lochdurchmesser: {diameter:.3f} mm\n"
            f"Fräserdurchmesser: {tool_diameter:.3f} mm\n\n"
            "Dieser Zyklus ist zum Rundlochfräsen "
            "und nicht zum Bohren vorgesehen."
        )


    # ========================================================
    # Werkzeugmittelpunkt-Radius
    # ========================================================

    radius = (
        diameter - tool_diameter
    ) / 2.0


    if radius <= 0:

        raise ValueError(
            "Der berechnete Werkzeugmittelpunkt-"
            "Radius ist ungültig.\n\n"
            "Bitte prüfen Sie Lochdurchmesser "
            "und Fräserdurchmesser."
        )


    # ========================================================
    # Rückzug prüfen
    #
    # Der Rückzug erfolgt von der Werkzeugbahn
    # radial nach innen.
    #
    # Der Rückzug darf deshalb nicht größer sein
    # als der Abstand des Werkzeugmittelpunkts
    # zur Lochmitte.
    # ========================================================

    if retract > radius:

        raise ValueError(
            "Der Rückzug zur Mitte ist zu groß.\n\n"
            f"Werkzeugbahn-Radius: {radius:.3f} mm\n"
            f"Eingestellter Rückzug: {retract:.3f} mm\n\n"
            "Der Rückzug darf nicht größer als "
            "der Werkzeugbahn-Radius sein.\n"
            "Sonst fährt der Fräser über die Lochmitte "
            "hinaus und die Lochkontur wird beschädigt."
        )


    # ========================================================
    # Gesamte axiale Zustellstrecke
    # ========================================================

    total_z_distance = (
        start_z + depth
    )


    # ========================================================
    # Anzahl vollständiger Umdrehungen
    # ========================================================

    full_turns = int(
        math.floor(
            total_z_distance / pitch
        )
    )


    remaining_depth = (
        total_z_distance -
        full_turns * pitch
    )


    # ========================================================
    # G-Code erzeugen
    # ========================================================

    try:

        with open(
            NGC_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "( ========================================== )\n"
            )

            f.write(
                "( CIRCLE - Milling Cycles                   )\n"
            )

            f.write(
                "( ========================================== )\n"
            )

            f.write(
                f"( Lochdurchmesser   : {diameter:.3f} mm )\n"
            )

            f.write(
                f"( Bohrtiefe         : {depth:.3f} mm )\n"
            )

            f.write(
                f"( Fräserdurchmesser : {tool_diameter:.3f} mm )\n"
            )

            f.write(
                f"( Spiralensteigung  : {pitch:.3f} mm/U )\n"
            )

            f.write(
                f"( Helix-Start       : Z+{start_z:.3f} mm )\n"
            )

            f.write(
                f"( Endtiefe          : Z-{depth:.3f} mm )\n"
            )

            f.write(
                f"( Rückzug Mitte     : {retract:.3f} mm )\n"
            )

            f.write(
                f"( Werkzeugbahn-Radius: {radius:.3f} mm )\n"
            )

            f.write(
                "( ========================================== )\n"
            )

            f.write("\n")

            f.write("G21\n")
            f.write("G17\n")
            f.write("G90\n")
            f.write(f"F{feed_mill:.3f}\n")

            f.write("\n")


            # ====================================================
            # Startposition
            # ====================================================


            f.write(
                f"G0 X{radius:.6f} Y0.000000\n"
            )

            f.write(
                f"G0 Z{start_z:.3f}\n"
            )

            f.write("\n")


            # ====================================================
            # SPIRALE
            # ====================================================

            current_z = start_z


            # ----------------------------------------------------
            # Ganze Umdrehungen
            # ----------------------------------------------------

            for turn in range(
                full_turns
            ):

                next_z = (
                    current_z -
                    pitch
                )

                f.write(
                    f"G2 X{radius:.6f} "
                    f"Y0.000000 "
                    f"I{-radius:.6f} "
                    f"J0.000000 "
                    f"Z{next_z:.6f}\n"
                )

                current_z = next_z


            # ----------------------------------------------------
            # Restumdrehung
            # ----------------------------------------------------

            if remaining_depth > 0.0000001:

                remaining_turn = (
                    remaining_depth / pitch
                )

                remaining_angle = (
                    -2.0 *
                    math.pi *
                    remaining_turn
                )

                next_x = (
                    radius *
                    math.cos(
                        remaining_angle
                    )
                )

                next_y = (
                    radius *
                    math.sin(
                        remaining_angle
                    )
                )

                next_z = (
                    -depth
                )

                f.write(
                    f"G2 X{next_x:.6f} "
                    f"Y{next_y:.6f} "
                    f"I{-radius:.6f} "
                    f"J0.000000 "
                    f"Z{next_z:.6f}\n"
                )

                current_z = next_z


            # ====================================================
            # Endtiefe sicherstellen
            # ====================================================

            if abs(
                current_z + depth
            ) > 0.0000001:

                f.write(
                    f"F{feed_approach:.3f}\n"
                )

                f.write(
                    f"G1 Z{-depth:.6f}\n"
                )

                f.write(
                    f"F{feed_mill:.3f}\n"
                )

                current_z = -depth


            # ====================================================
            # SCHLICHTKREIS
            # ====================================================

            f.write("\n")

            f.write(
                "( Schlichtkreis auf Endtiefe )\n"
            )


            total_turns = (
                total_z_distance / pitch
            )

            final_angle = (
                -2.0 *
                math.pi *
                total_turns
            )

            final_x = (
                radius *
                math.cos(
                    final_angle
                )
            )

            final_y = (
                radius *
                math.sin(
                    final_angle
                )
            )


            opposite_x = (
                -final_x
            )

            opposite_y = (
                -final_y
            )


            # ----------------------------------------------------
            # Erster G2-Halbkreis
            # ----------------------------------------------------

            f.write(
                f"G2 X{opposite_x:.6f} "
                f"Y{opposite_y:.6f} "
                f"I{-final_x:.6f} "
                f"J{-final_y:.6f}\n"
            )


            # ----------------------------------------------------
            # Zweiter G2-Halbkreis
            # ----------------------------------------------------

            f.write(
                f"G2 X{final_x:.6f} "
                f"Y{final_y:.6f} "
                f"I{final_x:.6f} "
                f"J{final_y:.6f}\n"
            )


            # ====================================================
            # WEG VON DER LOCHWAND
            # ====================================================

            f.write("\n")

            f.write(
                "( Weg von der Lochwand )\n"
            )


            direction_x = math.cos(
                final_angle
            )

            direction_y = math.sin(
                final_angle
            )


            inside_x = (
                final_x -
                retract * direction_x
            )

            inside_y = (
                final_y -
                retract * direction_y
            )


            f.write(
                f"G1 X{inside_x:.6f} "
                f"Y{inside_y:.6f}\n"
            )


            # ====================================================
            # Z-Rückzug
            # ====================================================

            f.write("\n")

            f.write(
                "( Z zuerst auf Maschinenposition )\n"
            )

            f.write(
                "G53 G0 Z2.000\n"
            )


            # ====================================================
            # X/Y zurück
            # ====================================================

            f.write("\n")

            f.write(
                "( X/Y erst nach vollstaendigem Z-Rueckzug )\n"
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
            "Die Datei 'circle.ngc' konnte nicht "
            "geschrieben werden."
        )


    print(
        "Kreis erfolgreich erzeugt:"
    )

    print(
        NGC_FILE
    )

    print(
        f"Werkzeugbahn-Radius: {radius:.3f} mm"
    )

    print(
        f"Endtiefe: Z{-depth:.3f}"
    )

    print(
        "Schlichtkreis: G2 / voller Kreis"
    )


# ============================================================
# EINMALIGER PROGRAMMLAUF
# ============================================================

def main():

    print(
        "Kreis Python gestartet."
    )

    try:

        create_circle()

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
