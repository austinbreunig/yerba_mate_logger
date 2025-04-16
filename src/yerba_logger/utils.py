import questionary
import pandas as pd


def ask_body_profile(bodies):
    while True:
        body_profile = questionary.checkbox(
            "Select the body profile (must select at least one):",
            choices=bodies
        ).ask()

        if body_profile:  # Valid if list is non-empty
            return body_profile
        else:
            print("⚠️  Please select at least one option before continuing.\n")

def ask_flavor_profile(flavors):
    while True:
        flavor_profile = questionary.checkbox(
            "Select the flavor profile (must select at least one):",
            choices=flavors
        ).ask()

        if flavor_profile:  # Valid if list is non-empty
            return flavor_profile
        else:
            print("⚠️  Please select at least one option before continuing.\n")

def ask_cycle_profile(cycles):
    while True:
        cycle_profile = questionary.checkbox(
            "Select the cycle profile (must select at least one):",
            choices=cycles
        ).ask()

        if cycle_profile:  # Valid if list is non-empty
            return cycle_profile
        else:
            print("⚠️  Please select at least one option before continuing.\n")

def ask_effect_profile(effects):
    while True:
        effect_profile = questionary.checkbox(
            "Select the effects (must select at least one):",
            choices=effects
        ).ask()

        if effect_profile:  # Valid if list is non-empty
            return effect_profile
        else:
            print("⚠️  Please select at least one option before continuing.\n")

def ask_date():
    while True:
        date = questionary.text("Enter the date (YYYY-MM-DD):").ask()
        try:
            # Attempt to parse the date string
            parsed_date = pd.to_datetime(date, format="%Y-%m-%d")
            return parsed_date.strftime("%Y-%m-%d")  # Return in desired format
        except ValueError:
            print("⚠️  Invalid date format. Please enter the date in YYYY-MM-DD format.\n")

