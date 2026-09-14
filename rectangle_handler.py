#!/usr/bin/env python3

import os
import hal
import subprocess

import ui_save


class RectangleHandler:

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
            "rectangle_cutter_diameter",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "rectangle_width",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "rectangle_depth",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "rectangle_z_step",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "rectangle_milling_depth",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "rectangle_start_z",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "rectangle_start_top_left",
            hal.HAL_BIT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "rectangle_start_top_right",
            hal.HAL_BIT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "rectangle_start_bottom_left",
            hal.HAL_BIT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "rectangle_start_bottom_right",
            hal.HAL_BIT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "rectangle_start_center",
            hal.HAL_BIT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "rectangle_inside",
            hal.HAL_BIT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "rectangle_outside",
            hal.HAL_BIT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "rectangle_feed_approach",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "rectangle_feed_mill",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        # ====================================================
        # UI
        # ====================================================

        self.rectangle_cutter_diameter = builder.get_object(
            "rectangle_cutter_diameter"
        )

        self.rectangle_width = builder.get_object(
            "rectangle_width"
        )

        self.rectangle_depth = builder.get_object(
            "rectangle_depth"
        )

        self.rectangle_z_step = builder.get_object(
            "rectangle_z_step"
        )

        self.rectangle_milling_depth = builder.get_object(
            "rectangle_milling_depth"
        )

        self.rectangle_start_z = builder.get_object(
            "rectangle_start_z"
        )

        self.rectangle_preview = builder.get_object(
            "rectangle_preview"
        )

        self.rectangle_start_top_left = builder.get_object(
            "rectangle_start_left_top"
        )

        self.rectangle_start_top_right = builder.get_object(
            "rectangle_start_right_top"
        )

        self.rectangle_start_bottom_left = builder.get_object(
            "rectangle_start_left_bottom"
        )

        self.rectangle_start_bottom_right = builder.get_object(
            "rectangle_start_right_bottom"
        )

        self.rectangle_start_center = builder.get_object(
            "rectangle_start_middle"
        )

        self.rectangle_inside = builder.get_object(
            "rectangle_inside"
        )

        self.rectangle_outside = builder.get_object(
            "rectangle_outside"
        )

        self.rectangle_feed_approach = builder.get_object(
            "rectangle_feed_approach"
        )

        self.rectangle_feed_mill = builder.get_object(
            "rectangle_feed_mill"
        )

        # ====================================================
        # SPIN-KEYS
        # ====================================================

        self._spin_keys = [
            "rectangle_cutter_diameter",
            "rectangle_width",
            "rectangle_depth",
            "rectangle_z_step",
            "rectangle_milling_depth",
            "rectangle_start_z",
            "rectangle_feed_approach",
            "rectangle_feed_mill"
        ]

        # ====================================================
        # UPDATE
        # ====================================================

        self.rectangle_cutter_diameter.connect(
            "value-changed",
            self.update_rectangle_cutter_diameter
        )

        self.rectangle_width.connect(
            "value-changed",
            self.update_rectangle_width
        )

        self.rectangle_depth.connect(
            "value-changed",
            self.update_rectangle_depth
        )

        self.rectangle_z_step.connect(
            "value-changed",
            self.update_rectangle_z_step
        )

        self.rectangle_milling_depth.connect(
            "value-changed",
            self.update_rectangle_milling_depth
        )

        self.rectangle_start_z.connect(
            "value-changed",
            self.update_rectangle_start_z
        )

        self.rectangle_start_top_left.connect(
            "toggled",
            self.update_rectangle_start_top_left
        )

        self.rectangle_start_top_right.connect(
            "toggled",
            self.update_rectangle_start_top_right
        )

        self.rectangle_start_bottom_left.connect(
            "toggled",
            self.update_rectangle_start_bottom_left
        )

        self.rectangle_start_bottom_right.connect(
            "toggled",
            self.update_rectangle_start_bottom_right
        )

        self.rectangle_start_center.connect(
            "toggled",
            self.update_rectangle_start_center
        )

        self.rectangle_inside.connect(
            "toggled",
            self.update_rectangle_inside
        )

        self.rectangle_outside.connect(
            "toggled",
            self.update_rectangle_outside
        )

        self.rectangle_feed_approach.connect(
            "value-changed",
            self.update_rectangle_feed_approach
        )

        self.rectangle_feed_mill.connect(
            "value-changed",
            self.update_rectangle_feed_mill
        )

        # ====================================================
        # PREVIEW
        # ====================================================

        self.rectangle_preview.connect(
            "clicked",
            self.on_rectangle_preview_clicked
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

        self.halcomp["rectangle_cutter_diameter"] = self.round3(
            self.rectangle_cutter_diameter.get_value()
        )

        self.halcomp["rectangle_width"] = self.round3(
            self.rectangle_width.get_value()
        )

        self.halcomp["rectangle_depth"] = self.round3(
            self.rectangle_depth.get_value()
        )

        self.halcomp["rectangle_z_step"] = self.round3(
            self.rectangle_z_step.get_value()
        )

        self.halcomp["rectangle_milling_depth"] = self.round3(
            self.rectangle_milling_depth.get_value()
        )

        self.halcomp["rectangle_start_z"] = self.round3(
            self.rectangle_start_z.get_value()
        )

        self.halcomp["rectangle_start_top_left"] = (
            self.rectangle_start_top_left.get_active()
        )

        self.halcomp["rectangle_start_top_right"] = (
            self.rectangle_start_top_right.get_active()
        )

        self.halcomp["rectangle_start_bottom_left"] = (
            self.rectangle_start_bottom_left.get_active()
        )

        self.halcomp["rectangle_start_bottom_right"] = (
            self.rectangle_start_bottom_right.get_active()
        )

        self.halcomp["rectangle_start_center"] = (
            self.rectangle_start_center.get_active()
        )

        self.halcomp["rectangle_inside"] = (
            self.rectangle_inside.get_active()
        )

        self.halcomp["rectangle_outside"] = (
            self.rectangle_outside.get_active()
        )

        self.halcomp["rectangle_feed_approach"] = self.round3(
            self.rectangle_feed_approach.get_value()
        )

        self.halcomp["rectangle_feed_mill"] = self.round3(
            self.rectangle_feed_mill.get_value()
        )

    def update_rectangle_cutter_diameter(self, widget):

        self.halcomp["rectangle_cutter_diameter"] = self.round3(
            widget.get_value()
        )

    def update_rectangle_width(self, widget):

        self.halcomp["rectangle_width"] = self.round3(
            widget.get_value()
        )

    def update_rectangle_depth(self, widget):

        self.halcomp["rectangle_depth"] = self.round3(
            widget.get_value()
        )

    def update_rectangle_z_step(self, widget):

        self.halcomp["rectangle_z_step"] = self.round3(
            widget.get_value()
        )

    def update_rectangle_milling_depth(self, widget):

        self.halcomp["rectangle_milling_depth"] = self.round3(
            widget.get_value()
        )

    def update_rectangle_start_z(self, widget):

        self.halcomp["rectangle_start_z"] = self.round3(
            widget.get_value()
        )

    def update_rectangle_start_top_left(self, widget):

        self.halcomp["rectangle_start_top_left"] = (
            widget.get_active()
        )

    def update_rectangle_start_top_right(self, widget):

        self.halcomp["rectangle_start_top_right"] = (
            widget.get_active()
        )

    def update_rectangle_start_bottom_left(self, widget):

        self.halcomp["rectangle_start_bottom_left"] = (
            widget.get_active()
        )

    def update_rectangle_start_bottom_right(self, widget):

        self.halcomp["rectangle_start_bottom_right"] = (
            widget.get_active()
        )

    def update_rectangle_start_center(self, widget):

        self.halcomp["rectangle_start_center"] = (
            widget.get_active()
        )

    def update_rectangle_inside(self, widget):

        self.halcomp["rectangle_inside"] = (
            widget.get_active()
        )

    def update_rectangle_outside(self, widget):

        self.halcomp["rectangle_outside"] = (
            widget.get_active()
        )

    def update_rectangle_feed_approach(self, widget):

        self.halcomp["rectangle_feed_approach"] = self.round3(
            widget.get_value()
        )

    def update_rectangle_feed_mill(self, widget):

        self.halcomp["rectangle_feed_mill"] = self.round3(
            widget.get_value()
        )

    def on_rectangle_preview_clicked(self, widget):

        self.rectangle_cutter_diameter.update()
        self.rectangle_width.update()
        self.rectangle_depth.update()
        self.rectangle_z_step.update()
        self.rectangle_milling_depth.update()
        self.rectangle_start_z.update()
        self.rectangle_feed_approach.update()
        self.rectangle_feed_mill.update()

        self.update_all()

        self.save_values()

        rectangle_script = os.path.join(
            self.SCRIPT_DIR,
            "rectangle.py"
        )

        try:

            subprocess.Popen(
                [
                    "python3",
                    rectangle_script
                ]
            )

            print(
                "Rectangle Preview gestartet."
            )

        except OSError as error:

            print(
                "FEHLER beim Start von rectangle.py:"
            )

            print(
                error
            )