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
    "rectangle.ngc"
)


# ============================================================
# Fehler-Popup
# ============================================================

def show_error(message):

    root = tk.Tk()

    root.withdraw()

    root.attributes(
        "-topmost",
        True
    )

    messagebox.showerror(
        "Fehler bei Rechteck-Fräsung",
        message,
        parent=root
    )

    root.destroy()


# ============================================================
# HAL FLOAT lesen
# ============================================================

def hal_value(pin_name, description=None):

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

    except Exception:

        raise ValueError(
            "Die Einstellung konnte nicht aus "
            "der Bedienoberfläche gelesen werden."
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

    except Exception:

        raise ValueError(
            "Die Einstellung konnte nicht aus "
            "der Bedienoberfläche gelesen werden."
        )


# ============================================================
# Startpunkt lesen
# ============================================================

def get_startpunkt():

    pins = {
        "links_oben":
            "milling_cycles.rectangle_start_top_left",

        "rechts_oben":
            "milling_cycles.rectangle_start_top_right",

        "links_unten":
            "milling_cycles.rectangle_start_bottom_left",

        "rechts_unten":
            "milling_cycles.rectangle_start_bottom_right",

        "mitte":
            "milling_cycles.rectangle_start_center"
    }

    active = []

    for name, pin in pins.items():

        if hal_bit(pin):
            active.append(name)

    if len(active) != 1:

        raise ValueError(
            "Es muss genau ein Startpunkt ausgewählt sein."
        )

    return active[0]


# ============================================================
# Fräsart lesen
# ============================================================

def get_fraesart():

    try:

        innen = hal_bit(
            "milling_cycles.rectangle_inside"
        )

        aussen = hal_bit(
            "milling_cycles.rectangle_outside"
        )

    except ValueError:

        raise ValueError(
            "Die Fräsart konnte nicht aus "
            "der Bedienoberfläche gelesen werden."
        )

    if innen and not aussen:

        return "innen"

    if aussen and not innen:

        return "aussen"

    raise ValueError(
        "Es muss genau eine Fräsart ausgewählt sein:\n\n"
        "Innenkontur oder Aussenkontur."
    )


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
        "Rechteck in AXIS geladen."
    )


# ============================================================
# Rechteck erzeugen
# ============================================================

def create_rectangle():

    # --------------------------------------------------------
    # Werte aus GUI / HAL
    # --------------------------------------------------------

    cutter_diameter = hal_value(
        "milling_cycles.rectangle_cutter_diameter"
    )

    width = hal_value(
        "milling_cycles.rectangle_width"
    )

    depth = hal_value(
        "milling_cycles.rectangle_depth"
    )

    z_step = hal_value(
        "milling_cycles.rectangle_z_step"
    )

    milling_depth = hal_value(
        "milling_cycles.rectangle_milling_depth"
    )

    start_z = hal_value(
        "milling_cycles.rectangle_start_z"
    )

    feed_approach = hal_value(
        "milling_cycles.rectangle_feed_approach",
        "Der Zustell-Feed"
    )

    feed_mill = hal_value(
        "milling_cycles.rectangle_feed_mill",
        "Der Schnitt-Feed"
    )

    start_point = get_startpunkt()

    milling_type = get_fraesart()


    # --------------------------------------------------------
    # Prüfungen
    # --------------------------------------------------------

    if cutter_diameter <= 0:

        raise ValueError(
            "Der Fräserdurchmesser muss größer als "
            "0 mm sein."
        )


    if width <= 0:

        raise ValueError(
            "Die Rechteck-Breite muss größer als "
            "0 mm sein."
        )


    if depth <= 0:

        raise ValueError(
            "Die Rechteck-Tiefe muss größer als "
            "0 mm sein."
        )


    if z_step <= 0:

        raise ValueError(
            "Die Z-Zustellung muss größer als "
            "0 mm sein."
        )


    if milling_depth <= 0:

        raise ValueError(
            "Die Frästiefe muss größer als "
            "0 mm sein."
        )


    if start_z < 0:

        raise ValueError(
            "Start Z über Werkstück darf nicht "
            "negativ sein."
        )


    if feed_approach <= 0:

        raise ValueError(
            "Der Zustell-Feed muss größer als "
            "0 sein."
        )


    if feed_mill <= 0:

        raise ValueError(
            "Der Schnitt-Feed muss größer als "
            "0 sein."
        )


    radius = cutter_diameter / 2.0


    # --------------------------------------------------------
    # Innenfräsen prüfen
    # --------------------------------------------------------

    if milling_type == "innen":

        if width < cutter_diameter:

            raise ValueError(
                "Innenkontur kann nicht gefräst werden.\n\n"
                "Die Rechteck-Breite muss größer als "
                "der Fräserdurchmesser sein.\n\n"
                f"Rechteck-Breite: {width:.1f} mm\n"
                f"Fräserdurchmesser: {cutter_diameter:.1f} mm"
            )


        if depth < cutter_diameter:

            raise ValueError(
                "Innenkontur kann nicht gefräst werden.\n\n"
                "Die Rechteck-Tiefe muss größer als "
                "der Fräserdurchmesser sein.\n\n"
                f"Rechteck-Tiefe: {depth:.1f} mm\n"
                f"Fräserdurchmesser: {cutter_diameter:.1f} mm"
            )


    # ========================================================
    # Werkstück-Koordinaten
    # ========================================================

    if start_point == "links_oben":

        x_min = 0.0
        x_max = width

        y_min = -depth
        y_max = 0.0


    elif start_point == "rechts_oben":

        x_min = -width
        x_max = 0.0

        y_min = -depth
        y_max = 0.0


    elif start_point == "links_unten":

        x_min = 0.0
        x_max = width

        y_min = 0.0
        y_max = depth


    elif start_point == "rechts_unten":

        x_min = -width
        x_max = 0.0

        y_min = 0.0
        y_max = depth


    elif start_point == "mitte":

        x_min = -width / 2.0
        x_max = width / 2.0

        y_min = -depth / 2.0
        y_max = depth / 2.0


    else:

        raise ValueError(
            "Der ausgewählte Startpunkt ist ungültig."
        )


    # ========================================================
    # Werkzeugmittelpunktbahn
    # ========================================================

    if milling_type == "innen":

        tool_x_min = x_min + radius
        tool_x_max = x_max - radius

        tool_y_min = y_min + radius
        tool_y_max = y_max - radius

    else:

        tool_x_min = x_min - radius
        tool_x_max = x_max + radius

        tool_y_min = y_min - radius
        tool_y_max = y_max + radius


    # ========================================================
    # Konturpunkte
    #
    # Innen = CCW
    # Aussen = CW
    #
    # Der Startpunkt bestimmt nur den Beginn.
    # ========================================================

    if milling_type == "innen":

        # ----------------------------------------------------
        # INNEN = CCW
        # ----------------------------------------------------

        if start_point == "links_oben":

            start_x = tool_x_min
            start_y = tool_y_max

            path = [
                (tool_x_min, tool_y_max),
                (tool_x_min, tool_y_min),
                (tool_x_max, tool_y_min),
                (tool_x_max, tool_y_max),
                (tool_x_min, tool_y_max)
            ]


        elif start_point == "rechts_oben":

            start_x = tool_x_max
            start_y = tool_y_max

            path = [
                (tool_x_max, tool_y_max),
                (tool_x_min, tool_y_max),
                (tool_x_min, tool_y_min),
                (tool_x_max, tool_y_min),
                (tool_x_max, tool_y_max)
            ]


        elif start_point == "links_unten":

            start_x = tool_x_min
            start_y = tool_y_min

            path = [
                (tool_x_min, tool_y_min),
                (tool_x_max, tool_y_min),
                (tool_x_max, tool_y_max),
                (tool_x_min, tool_y_max),
                (tool_x_min, tool_y_min)
            ]


        elif start_point == "rechts_unten":

            start_x = tool_x_max
            start_y = tool_y_min

            path = [
                (tool_x_max, tool_y_min),
                (tool_x_max, tool_y_max),
                (tool_x_min, tool_y_max),
                (tool_x_min, tool_y_min),
                (tool_x_max, tool_y_min)
            ]


        else:

            start_x = tool_x_min
            start_y = tool_y_min

            path = [
                (tool_x_min, tool_y_min),
                (tool_x_max, tool_y_min),
                (tool_x_max, tool_y_max),
                (tool_x_min, tool_y_max),
                (tool_x_min, tool_y_min)
            ]


    else:

        # ----------------------------------------------------
        # AUSSEN = CW
        # ----------------------------------------------------

        if start_point == "links_oben":

            start_x = tool_x_min
            start_y = tool_y_max

            path = [
                (tool_x_min, tool_y_max),
                (tool_x_max, tool_y_max),
                (tool_x_max, tool_y_min),
                (tool_x_min, tool_y_min),
                (tool_x_min, tool_y_max)
            ]


        elif start_point == "rechts_oben":

            start_x = tool_x_max
            start_y = tool_y_max

            path = [
                (tool_x_max, tool_y_max),
                (tool_x_max, tool_y_min),
                (tool_x_min, tool_y_min),
                (tool_x_min, tool_y_max),
                (tool_x_max, tool_y_max)
            ]


        elif start_point == "links_unten":

            start_x = tool_x_min
            start_y = tool_y_min

            path = [
                (tool_x_min, tool_y_min),
                (tool_x_min, tool_y_max),
                (tool_x_max, tool_y_max),
                (tool_x_max, tool_y_min),
                (tool_x_min, tool_y_min)
            ]


        elif start_point == "rechts_unten":

            start_x = tool_x_max
            start_y = tool_y_min

            path = [
                (tool_x_max, tool_y_min),
                (tool_x_min, tool_y_min),
                (tool_x_min, tool_y_max),
                (tool_x_max, tool_y_max),
                (tool_x_max, tool_y_min)
            ]


        else:

            start_x = tool_x_max
            start_y = tool_y_min

            path = [
                (tool_x_max, tool_y_min),
                (tool_x_min, tool_y_min),
                (tool_x_min, tool_y_max),
                (tool_x_max, tool_y_max),
                (tool_x_max, tool_y_min)
            ]


    # ========================================================
    # G-Code erzeugen
    # ========================================================

    with open(
        NGC_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "( ========================================== )\n"
        )

        f.write(
            "( RECTANGLE - Milling Cycles                )\n"
        )

        f.write(
            "( ========================================== )\n"
        )

        f.write(
            f"( Cutter diameter : {cutter_diameter:.3f} mm )\n"
        )

        f.write(
            f"( Width           : {width:.3f} mm )\n"
        )

        f.write(
            f"( Depth           : {depth:.3f} mm )\n"
        )

        f.write(
            f"( Z step          : {z_step:.3f} mm )\n"
        )

        f.write(
            f"( Milling depth   : {milling_depth:.3f} mm )\n"
        )

        f.write(
            f"( Start Z         : {start_z:.3f} mm )\n"
        )

        f.write(
            f"( Start point     : {start_point} )\n"
        )

        f.write(
            f"( Milling type    : {milling_type} )\n"
        )

        if milling_type == "innen":

            f.write(
                "( Milling direction: Climb / CCW )\n"
            )

        else:

            f.write(
                "( Milling direction: Climb / CW )\n"
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
        # Zustellungen
        # ====================================================

        current_depth = 0.0

        while current_depth < milling_depth:

            next_depth = min(
                current_depth + z_step,
                milling_depth
            )

            current_z = -next_depth


            f.write(
                f"( Zustellung Z{current_z:.3f} )\n"
            )

            f.write(
                f"F{feed_approach:.3f}\n"
            )

            f.write(
                f"G1 Z{current_z:.6f}\n"
            )

            f.write(
                f"F{feed_mill:.3f}\n"
            )


            # ------------------------------------------------
            # Kontur fahren
            # ------------------------------------------------

            for point_x, point_y in path:

                f.write(
                    f"G1 X{point_x:.6f} "
                    f"Y{point_y:.6f}\n"
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
    # Meldung
    # ========================================================

    print(
        "Rechteck erfolgreich erzeugt:"
    )

    print(
        NGC_FILE
    )

    print(
        "Startpunkt:",
        start_point
    )

    print(
        "Fräsart:",
        milling_type
    )

    if milling_type == "innen":

        print(
            "Fräsrichtung: Gleichlauf / CCW"
        )

    else:

        print(
            "Fräsrichtung: Gleichlauf / CW"
        )


# ============================================================
# EINMALIGER PROGRAMMLAUF
# ============================================================

def main():

    print(
        "Rectangle Python gestartet."
    )

    try:

        create_rectangle()

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

