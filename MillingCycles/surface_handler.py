#!/usr/bin/env python3

import os
import hal
import subprocess

import ui_save


class SurfaceHandler:

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
            "surface_cutter_diameter",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "surface_z_step",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "surface_width",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "surface_depth",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "surface_milling_depth",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "surface_start_z",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "surface_overlap",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "surface_start_left_top",
            hal.HAL_BIT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "surface_start_right_top",
            hal.HAL_BIT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "surface_start_left_bottom",
            hal.HAL_BIT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "surface_start_right_bottom",
            hal.HAL_BIT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "surface_feed_approach",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        halcomp.newpin(
            "surface_feed_mill",
            hal.HAL_FLOAT,
            hal.HAL_OUT
        )

        # ====================================================
        # UI
        # ====================================================

        self.surface_cutter_diameter = builder.get_object(
            "surface_cutter_diameter"
        )

        self.surface_z_step = builder.get_object(
            "surface_z_step"
        )

        self.surface_width = builder.get_object(
            "surface_width"
        )

        self.surface_depth = builder.get_object(
            "surface_depth"
        )

        self.surface_milling_depth = builder.get_object(
            "surface_milling_depth"
        )

        self.surface_start_z = builder.get_object(
            "surface_start_z"
        )

        self.surface_overlap = builder.get_object(
            "surface_overlap"
        )

        self.surface_start_left_top = builder.get_object(
            "surface_start_left_top"
        )

        self.surface_start_right_top = builder.get_object(
            "surface_start_right_top"
        )

        self.surface_start_left_bottom = builder.get_object(
            "surface_start_left_bottom"
        )

        self.surface_start_right_bottom = builder.get_object(
            "surface_start_right_bottom"
        )

        self.surface_feed_approach = builder.get_object(
            "surface_feed_approach"
        )

        self.surface_feed_mill = builder.get_object(
            "surface_feed_mill"
        )

        self.surface_preview = builder.get_object(
            "surface_preview"
        )

        # ====================================================
        # SPIN-KEYS
        # ====================================================

        self._spin_keys = [
            "surface_cutter_diameter",
            "surface_z_step",
            "surface_width",
            "surface_depth",
            "surface_milling_depth",
            "surface_start_z",
            "surface_overlap",
            "surface_feed_approach",
            "surface_feed_mill"
        ]

        # ====================================================
        # UPDATE
        # ====================================================

        self.surface_cutter_diameter.connect(
            "value-changed",
            self.update_surface_cutter_diameter
        )

        self.surface_z_step.connect(
            "value-changed",
            self.update_surface_z_step
        )

        self.surface_width.connect(
            "value-changed",
            self.update_surface_width
        )

        self.surface_depth.connect(
            "value-changed",
            self.update_surface_depth
        )

        self.surface_milling_depth.connect(
            "value-changed",
            self.update_surface_milling_depth
        )

        self.surface_start_z.connect(
            "value-changed",
            self.update_surface_start_z
        )

        self.surface_overlap.connect(
            "value-changed",
            self.update_surface_overlap
        )

        self.surface_start_left_top.connect(
            "toggled",
            self.update_surface_start_left_top
        )

        self.surface_start_right_top.connect(
            "toggled",
            self.update_surface_start_right_top
        )

        self.surface_start_left_bottom.connect(
            "toggled",
            self.update_surface_start_left_bottom
        )

        self.surface_start_right_bottom.connect(
            "toggled",
            self.update_surface_start_right_bottom
        )

        self.surface_feed_approach.connect(
            "value-changed",
            self.update_surface_feed_approach
        )

        self.surface_feed_mill.connect(
            "value-changed",
            self.update_surface_feed_mill
        )

        # ====================================================
        # PREVIEW
        # ====================================================

        self.surface_preview.connect(
            "clicked",
            self.on_surface_preview_clicked
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

        self.halcomp["surface_cutter_diameter"] = self.round3(
            self.surface_cutter_diameter.get_value()
        )

        self.halcomp["surface_z_step"] = self.round3(
            self.surface_z_step.get_value()
        )

        self.halcomp["surface_width"] = self.round3(
            self.surface_width.get_value()
        )

        self.halcomp["surface_depth"] = self.round3(
            self.surface_depth.get_value()
        )

        self.halcomp["surface_milling_depth"] = self.round3(
            self.surface_milling_depth.get_value()
        )

        self.halcomp["surface_start_z"] = self.round3(
            self.surface_start_z.get_value()
        )

        self.halcomp["surface_overlap"] = self.round3(
            self.surface_overlap.get_value()
        )

        self.halcomp["surface_start_left_top"] = (
            self.surface_start_left_top.get_active()
        )

        self.halcomp["surface_start_right_top"] = (
            self.surface_start_right_top.get_active()
        )

        self.halcomp["surface_start_left_bottom"] = (
            self.surface_start_left_bottom.get_active()
        )

        self.halcomp["surface_start_right_bottom"] = (
            self.surface_start_right_bottom.get_active()
        )

        self.halcomp["surface_feed_approach"] = self.round3(
            self.surface_feed_approach.get_value()
        )

        self.halcomp["surface_feed_mill"] = self.round3(
            self.surface_feed_mill.get_value()
        )

    def update_surface_cutter_diameter(self, widget):

        self.halcomp["surface_cutter_diameter"] = self.round3(
            widget.get_value()
        )

    def update_surface_z_step(self, widget):

        self.halcomp["surface_z_step"] = self.round3(
            widget.get_value()
        )

    def update_surface_width(self, widget):

        self.halcomp["surface_width"] = self.round3(
            widget.get_value()
        )

    def update_surface_depth(self, widget):

        self.halcomp["surface_depth"] = self.round3(
            widget.get_value()
        )

    def update_surface_milling_depth(self, widget):

        self.halcomp["surface_milling_depth"] = self.round3(
            widget.get_value()
        )

    def update_surface_start_z(self, widget):

        self.halcomp["surface_start_z"] = self.round3(
            widget.get_value()
        )

    def update_surface_overlap(self, widget):

        self.halcomp["surface_overlap"] = self.round3(
            widget.get_value()
        )

    def update_surface_start_left_top(self, widget):

        self.halcomp["surface_start_left_top"] = (
            widget.get_active()
        )

    def update_surface_start_right_top(self, widget):

        self.halcomp["surface_start_right_top"] = (
            widget.get_active()
        )

    def update_surface_start_left_bottom(self, widget):

        self.halcomp["surface_start_left_bottom"] = (
            widget.get_active()
        )

    def update_surface_start_right_bottom(self, widget):

        self.halcomp["surface_start_right_bottom"] = (
            widget.get_active()
        )

    def update_surface_feed_approach(self, widget):

        self.halcomp["surface_feed_approach"] = self.round3(
            widget.get_value()
        )

    def update_surface_feed_mill(self, widget):

        self.halcomp["surface_feed_mill"] = self.round3(
            widget.get_value()
        )

    def on_surface_preview_clicked(self, widget):

        self.surface_cutter_diameter.update()
        self.surface_z_step.update()
        self.surface_width.update()
        self.surface_depth.update()
        self.surface_milling_depth.update()
        self.surface_start_z.update()
        self.surface_overlap.update()
        self.surface_feed_approach.update()
        self.surface_feed_mill.update()

        self.update_all()

        self.save_values()

        surface_script = os.path.join(
            self.SCRIPT_DIR,
            "surface.py"
        )

        try:

            subprocess.Popen(
                [
                    "python3",
                    surface_script
                ]
            )

            print(
                "Surface Preview gestartet."
            )

        except OSError as error:

            print(
                "FEHLER beim Start von surface.py:"
            )

            print(
                error
            )