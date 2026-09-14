#!/usr/bin/env python3

import os


def load_values(path):

    values = {}

    if not os.path.exists(path):

        return values

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            stripped = line.strip()

            if not stripped:

                continue

            if stripped.startswith("#"):

                continue

            if "=" not in stripped:

                continue

            key, value = stripped.split(
                "=",
                1
            )

            values[key.strip()] = value.strip()

    return values


def save_values(path, values):

    written = set()

    lines = []

    if os.path.exists(path):

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            lines = f.readlines()

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        for line in lines:

            stripped = line.strip()

            if (
                stripped
                and "=" in stripped
                and not stripped.startswith("#")
            ):

                key = stripped.split(
                    "=",
                    1
                )[0].strip()

                if key in values:

                    f.write(
                        f"{key}={values[key]}\n"
                    )

                    written.add(key)

                    continue

            f.write(line)

        for key, value in values.items():

            if key not in written:

                if lines and not lines[-1].endswith("\n"):

                    f.write("\n")

                f.write(
                    f"{key}={value}\n"
                )