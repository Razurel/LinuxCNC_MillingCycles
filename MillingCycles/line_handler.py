#!/usr/bin/env python3

import os
import hal
import subprocess

import ui_save


class LineHandler:

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
            "line_cutter_diameter",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "line_length",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "line_depth",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "line_z_step",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "line_start_z",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "line_angle",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "line_feed_approach",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "line_feed_mill",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        # ====================================================
        # UI
        # ====================================================

        self.line_cutter_diameter = builder.get_object(
            "line_cutter_diameter"
        )

        self.line_length = builder.get_object(
            "line_length"
        )

        self.line_depth = builder.get_object(
            "line_depth"
        )

        self.line_z_step = builder.get_object(
            "line_z_step"
        )

        self.line_start_z = builder.get_object(
            "line_start_z"
        )

        self.line_angle = builder.get_object(
            "line_angle"
        )

        self.line_feed_approach = builder.get_object(
            "line_feed_approach"
        )

        self.line_feed_mill = builder.get_object(
            "line_feed_mill"
        )

        self.line_preview = builder.get_object(
            "line_preview"
        )

        # ====================================================
        # SPIN-KEYS
        # ====================================================

        self._spin_keys = [
            "line_cutter_diameter",
            "line_length",
            "line_depth",
            "line_z_step",
            "line_start_z",
            "line_angle",
            "line_feed_approach",
            "line_feed_mill"
        ]

        # ====================================================
        # UPDATE
        # ====================================================

        self.line_cutter_diameter.connect(
            "value-changed",
            self.update_line_cutter_diameter
        )

        self.line_length.connect(
            "value-changed",
            self.update_line_length
        )

        self.line_depth.connect(
            "value-changed",
            self.update_line_depth
        )

        self.line_z_step.connect(
            "value-changed",
            self.update_line_z_step
        )

        self.line_start_z.connect(
            "value-changed",
            self.update_line_start_z
        )

        self.line_angle.connect(
            "value-changed",
            self.update_line_angle
        )

        self.line_feed_approach.connect(
            "value-changed",
            self.update_line_feed_approach
        )

        self.line_feed_mill.connect(
            "value-changed",
            self.update_line_feed_mill
        )

        # ====================================================
        # PREVIEW
        # ====================================================

        self.line_preview.connect(
            "clicked",
            self.on_line_preview_clicked
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

        self.halcomp["line_cutter_diameter"] = self.round3(
            self.line_cutter_diameter.get_value()
        )

        self.halcomp["line_length"] = self.round3(
            self.line_length.get_value()
        )

        self.halcomp["line_depth"] = self.round3(
            self.line_depth.get_value()
        )

        self.halcomp["line_z_step"] = self.round3(
            self.line_z_step.get_value()
        )

        self.halcomp["line_start_z"] = self.round3(
            self.line_start_z.get_value()
        )

        self.halcomp["line_angle"] = self.round3(
            self.line_angle.get_value()
        )

        self.halcomp["line_feed_approach"] = self.round3(
            self.line_feed_approach.get_value()
        )

        self.halcomp["line_feed_mill"] = self.round3(
            self.line_feed_mill.get_value()
        )

    def update_line_cutter_diameter(self, widget):

        self.halcomp["line_cutter_diameter"] = self.round3(
            widget.get_value()
        )

    def update_line_length(self, widget):

        self.halcomp["line_length"] = self.round3(
            widget.get_value()
        )

    def update_line_depth(self, widget):

        self.halcomp["line_depth"] = self.round3(
            widget.get_value()
        )

    def update_line_z_step(self, widget):

        self.halcomp["line_z_step"] = self.round3(
            widget.get_value()
        )

    def update_line_start_z(self, widget):

        self.halcomp["line_start_z"] = self.round3(
            widget.get_value()
        )

    def update_line_angle(self, widget):

        self.halcomp["line_angle"] = self.round3(
            widget.get_value()
        )

    def update_line_feed_approach(self, widget):

        self.halcomp["line_feed_approach"] = self.round3(
            widget.get_value()
        )

    def update_line_feed_mill(self, widget):

        self.halcomp["line_feed_mill"] = self.round3(
            widget.get_value()
        )

    def on_line_preview_clicked(self, widget):

        self.line_cutter_diameter.update()
        self.line_length.update()
        self.line_depth.update()
        self.line_z_step.update()
        self.line_start_z.update()
        self.line_angle.update()
        self.line_feed_approach.update()
        self.line_feed_mill.update()

        self.update_all()

        self.save_values()

        line_script = os.path.join(
            self.SCRIPT_DIR,
            "line.py"
        )

        try:

            subprocess.Popen(
                [
                    "python3",
                    line_script
                ]
            )

            print(
                "Line Preview gestartet."
            )

        except OSError as error:

            print(
                "FEHLER beim Start von line.py:"
            )

            print(
                error
            )