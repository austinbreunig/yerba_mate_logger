import click
import questionary
from yerba_logger.registry import BrandRegistry, ProfileRegistry

BRANDS = BrandRegistry()
PROFILES = ProfileRegistry()

@click.group(help="""
             Welcome to the Yerba Mate Logger!

                This is a command line interface (CLI) for managing your mate consumption.
             
                For understanding available brands:
             
                You can add new brands, list all available brands, and get the location of a specific brand.
             
                For Logging your yerba mate consumption:
             
                You can log your smell, taste, and effects of yerba mate. Each property can be rated from 1 to 5.
                You can also view your logs and get a summary of your yerba mate consumption.
                
                Graphs and statistics on consumption are also available.
             
                SALUDOS! 🍵"""
            )
def cli():
    pass

@cli.command(help="""
             Add a new yerba mate brand.
             
             Example: yerba add "Brand Name" "Location"
             """)
@click.argument("name")
@click.argument("location")
def add(name, location):
    BRANDS.add_brand(name, location)
    click.echo(f"✅ Added {name} from {location}.")

@cli.command(help="""
             List all available mate brands.
             
             Example: yerba list "Brand Name"
             """)
def list():
    for name in BRANDS.list_brands():
        click.echo(f"- {name}")

@cli.command(help="""
             Get the location of a specific yerba mate brand.
             
             Example: yerba get "Brand Name"
             """)
@click.argument("name")
def get(name):
    """Get location of a specific brand."""
    loc = BRANDS.get_location(name)
    if loc:
        click.echo(f"{name} is from {loc}.")
    else:
        click.echo(f"❌ Brand '{name}' not found.")

@cli.command(help="""
             Log yerba mate consumption.
             
             Follow the prompts to log your yerba mate consumption!
             """)
def log():
    brands = BRANDS.list_brands()
    flavors = PROFILES.get_profile("flavor")
    effects = PROFILES.get_profile("effects")
    bodies = PROFILES.get_profile("body")
    cycles = PROFILES.get_profile("cycle")

    brand = questionary.select(
    "Choose a yerba mate:",
    choices=brands
    ).ask()

    date = questionary.text("Enter the date (YYYY-MM-DD):").ask()
    body = questionary.select(
        "Rate the body (1-5):",
        choices=["1", "2", "3", "4", "5"]
    ).ask()
    body_profile = questionary.checkbox(
        "Select the body profile:",
        choices=bodies
    ).ask()
    taste = questionary.select(
        "Rate the taste (1-5):",
        choices=["1", "2", "3", "4", "5"]
    ).ask()
    taste_profile = questionary.checkbox(
        "Select the taste profile:",
        choices=flavors 
    ).ask()
    cycle = questionary.select(
        "Rate the cycle (1-5):",
        choices=["1", "2", "3", "4", "5"]
    ).ask()
    cycle_profile = questionary.checkbox(
        "Select the cycle profile:",
        choices=cycles
    ).ask()
    effect = questionary.select(
        "Rate the effects (1-5):",
        choices=["1", "2", "3", "4", "5"]
    ).ask()
    effect_category = questionary.checkbox(
        "Select the effects:",
        choices=effects
    ).ask()

    print(f'You selected the following:')
    print(f'Brand: {brand}')
    print(f'Date: {date}')
    print(f'Body: {body}')
    print(f'Body Profile: {body_profile}')
    print(f'Taste: {taste}')
    print(f'Taste Profile: {taste_profile}')
    print(f'Cycle: {cycle}')
    print(f'Cycle Profile: {cycle_profile}')
    print(f'Effects: {effect}')
    print(f'Effect Category: {effect_category}')






