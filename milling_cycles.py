#!/usr/bin/env python3

import sys

import gi
import hal
import os

sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__))
)

gi.require_version("Gtk", "3.0")

import ui_save

from circle_handler import CircleHandler
from rectangle_handler import RectangleHandler
from line_handler import LineHandler
from surface_handler import SurfaceHandler


# ============================================================
# MILLING CYCLES – GladeVCP
#
# Zentrale Verwaltung der einzelnen Fräszyklen.
#
# Die eigentliche Logik befindet sich in:
#
#   circle_handler.py
#   rectangle_handler.py
#   line_handler.py
#   surface_handler.py
#
# Die SpinBox-Werte werden beim Start aus der
# UI_Save.txt geladen und beim Vorschau-Klick gespeichert.
# ============================================================


class MillingCycles:

    SCRIPT_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    UI_SAVE_PATH = os.path.join(
        SCRIPT_DIR,
        "UI_Save.txt"
    )

    def __init__(self, halcomp, builder, useropts):

        self.halcomp = halcomp
        self.builder = builder
        self.useropts = useropts

        # ====================================================
        # CIRCLE
        # ====================================================

        self.circle = CircleHandler(
            halcomp,
            builder
        )

        # ====================================================
        # RECTANGLE
        # ====================================================

        self.rectangle = RectangleHandler(
            halcomp,
            builder
        )

        # ====================================================
        # LINE
        # ====================================================

        self.line = LineHandler(
            halcomp,
            builder
        )

        # ====================================================
        # SURFACE
        # ====================================================

        self.surface = SurfaceHandler(
            halcomp,
            builder
        )

        # ====================================================
        # GESPEICHERTE WERTE LADEN
        # ====================================================

        self.load_values()

    def load_values(self):

        values = ui_save.load_values(
            self.UI_SAVE_PATH
        )

        if not values:

            return

        self.circle.set_values(values)
        self.rectangle.set_values(values)
        self.line.set_values(values)
        self.surface.set_values(values)


# ============================================================
# GLADEVCP HANDLER
# ============================================================


def get_handlers(halcomp, builder, useropts):

    return [
        MillingCycles(
            halcomp,
            builder,
            useropts
        )
    ]