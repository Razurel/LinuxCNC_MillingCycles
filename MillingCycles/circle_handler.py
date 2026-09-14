#!/usr/bin/env python3

import os
import hal
import subprocess

import ui_save


class CircleHandler:

    SCRIPT_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    UI_SAVE_PATH = os.path.join(
        SCRIPT_DIR,
        "UI_Save.txt"
    )

    def __init__(self, halcomp, builder):

        self.halcomp = halcomp

        # ====================================================
        # HAL-PINS
        # ====================================================

        halcomp.newpin(
            "circle_diameter",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "circle_depth",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "circle_cutter_diameter",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "circle_pitch",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "circle_start_z",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "circle_retract",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "circle_feed_approach",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "circle_feed_mill",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        # ====================================================
        # UI
        # ====================================================

        self.circle_diameter = builder.get_object(
            "circle_diameter"
        )

        self.circle_depth = builder.get_object(
            "circle_depth"
        )

        self.circle_cutter_diameter = builder.get_object(
            "circle_cutter_diameter"
        )

        self.circle_pitch = builder.get_object(
            "circle_pitch"
        )

        self.circle_start_z = builder.get_object(
            "circle_start_z"
        )

        self.circle_retract = builder.get_object(
            "circle_retract"
        )

        self.circle_feed_approach = builder.get_object(
            "circle_feed_approach"
        )

        self.circle_feed_mill = builder.get_object(
            "circle_feed_mill"
        )

        self.circle_preview = builder.get_object(
            "circle_preview"
        )

        # ====================================================
        # SPIN-KEYS
        # ====================================================

        self._spin_keys = [
            "circle_diameter",
            "circle_depth",
            "circle_cutter_diameter",
            "circle_pitch",
            "circle_start_z",
            "circle_retract",
            "circle_feed_approach",
            "circle_feed_mill"
        ]

        # ====================================================
        # UPDATE
        # ====================================================

        self.circle_diameter.connect(
            "value-changed",
            self.update_circle_diameter
        )

        self.circle_depth.connect(
            "value-changed",
            self.update_circle_depth
        )

        self.circle_cutter_diameter.connect(
            "value-changed",
            self.update_circle_cutter_diameter
        )

        self.circle_pitch.connect(
            "value-changed",
            self.update_circle_pitch
        )

        self.circle_start_z.connect(
            "value-changed",
            self.update_circle_start_z
        )

        self.circle_retract.connect(
            "value-changed",
            self.update_circle_retract
        )

        self.circle_feed_approach.connect(
            "value-changed",
            self.update_circle_feed_approach
        )

        self.circle_feed_mill.connect(
            "value-changed",
            self.update_circle_feed_mill
        )

        # ====================================================
        # PREVIEW
        # ====================================================

        self.circle_preview.connect(
            "clicked",
            self.on_circle_preview_clicked
        )

    def round3(self, value):

        return round(
            float(value),
            3
        )

    def get_values(self):

        values = {}

        for key in self._spin_keys:

            widget = getattr(
                self,
                key,
                None
            )

            if widget is not None:

                values[key] = self.round3(
                    widget.get_value()
                )

        return values

    def set_values(self, values):

        for key, value in values.items():

            widget = getattr(
                self,
                key,
                None
            )

            if (
                widget is not None
                and hasattr(widget, "set_value")
            ):

                try:

                    widget.set_value(
                        float(value)
                    )

                except (TypeError, ValueError):
                    pass

    def save_values(self):

        ui_save.save_values(
            self.UI_SAVE_PATH,
            self.get_values()
        )

    def update_all(self):

        self.halcomp["circle_diameter"] = self.round3(
            self.circle_diameter.get_value()
        )

        self.halcomp["circle_depth"] = self.round3(
            self.circle_depth.get_value()
        )

        self.halcomp["circle_cutter_diameter"] = self.round3(
            self.circle_cutter_diameter.get_value()
        )

        self.halcomp["circle_pitch"] = self.round3(
            self.circle_pitch.get_value()
        )

        self.halcomp["circle_start_z"] = self.round3(
            self.circle_start_z.get_value()
        )

        self.halcomp["circle_retract"] = self.round3(
            self.circle_retract.get_value()
        )

        self.halcomp["circle_feed_approach"] = self.round3(
            self.circle_feed_approach.get_value()
        )

        self.halcomp["circle_feed_mill"] = self.round3(
            self.circle_feed_mill.get_value()
        )

    def update_circle_diameter(self, widget):

        self.halcomp["circle_diameter"] = self.round3(
            widget.get_value()
        )

    def update_circle_depth(self, widget):

        self.halcomp["circle_depth"] = self.round3(
            widget.get_value()
        )

    def update_circle_cutter_diameter(self, widget):

        self.halcomp["circle_cutter_diameter"] = self.round3(
            widget.get_value()
        )

    def update_circle_pitch(self, widget):

        self.halcomp["circle_pitch"] = self.round3(
            widget.get_value()
        )

    def update_circle_start_z(self, widget):

        self.halcomp["circle_start_z"] = self.round3(
            widget.get_value()
        )

    def update_circle_retract(self, widget):

        self.halcomp["circle_retract"] = self.round3(
            widget.get_value()
        )

    def update_circle_feed_approach(self, widget):

        self.halcomp["circle_feed_approach"] = self.round3(
            widget.get_value()
        )

    def update_circle_feed_mill(self, widget):

        self.halcomp["circle_feed_mill"] = self.round3(
            widget.get_value()
        )

    def on_circle_preview_clicked(self, widget):

        self.circle_diameter.update()
        self.circle_depth.update()
        self.circle_cutter_diameter.update()
        self.circle_pitch.update()
        self.circle_start_z.update()
        self.circle_retract.update()
        self.circle_feed_approach.update()
        self.circle_feed_mill.update()

        self.update_all()

        self.save_values()

        circle_script = os.path.join(
            self.SCRIPT_DIR,
            "circle.py"
        )

        try:

            subprocess.Popen(
                [
                    "python3",
                    circle_script
                ]
            )

            print(
                "Circle Preview gestartet."
            )

        except OSError as error:

            print(
                "FEHLER beim Start von circle.py:"
            )

            print(
                error
            )