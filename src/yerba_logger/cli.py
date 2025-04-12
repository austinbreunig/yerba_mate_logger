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
             Add a yerba mate brand or profile value.
             
             Example: yerba add --type profile .. then follow the prompts
             """)
@click.option(
    "--type",
    type=click.Choice(["brand", "profile"], case_sensitive=False),
    prompt="What are you adding? (brand or profile)"
)
def add(type):
    type = type.lower()
    try:
        if type == "brand":
            name = click.prompt("Enter the brand name")
            value = click.prompt("Enter the brand location")
            BRANDS.add_brand(name, value)
            click.echo(f"✅ Added brand: {name} from {value}")
        else:
            name = questionary.select(
                "Select a profile type:",
                choices=["body", "flavor", "cycle", "effects"]
            ).ask()
            value = click.prompt(f"Enter the {name} profile value")
            PROFILES.add_profile(name=name, data=value)
            click.echo(f"✅ Added {name} profile: {value}")
            
    except (click.Abort, KeyboardInterrupt):
        click.echo("\n👋 Exiting.")
        raise SystemExit

@cli.command(help="""
                Remove a yerba mate brand or profile value.
             
                Example: yerba remove --brand .. then follow the prompts
             
                """)
@click.option(
    "--type",
    type=click.Choice(["brand", "profile"], case_sensitive=False),
    prompt="What are you removing? (brand or profile)"
)
def remove(type):
    type = type.lower()
    
    if type == "brand":
        name = click.prompt("Enter the brand name")
        BRANDS.remove_brand(name)
        click.echo(f"✅ Removed brand: {name}")
    else:
        name = questionary.select(
            "Select a profile type:",
            choices=["body", "flavor", "cycle", "effects"]
        ).ask()
        value = click.prompt(f"Enter the {name} profile value")
        PROFILES.remove_profile(name=name, data=value)
        click.echo(f"✅ Removed {name} profile: {value}")


@cli.command(help="""
             List all available mate brands.
             
             Example: yerba list "Brand Name"
             """)
@click.option("--brand", is_flag=True, help="List all yerba mate brands.")
@click.option("--body", is_flag=True, help="List all yerba mate body profiles.")
@click.option("--flavor", is_flag=True, help="List all yerba mate taste profiles.")
@click.option("--cycle", is_flag=True, help="List all yerba mate cycle profiles.")
@click.option("--effects", is_flag=True, help="List all yerba mate effects.")
def list(brand, body, flavor, cycle, effects):
    if brand:
        for name in BRANDS.list_brands():
            click.echo(f"- {name}")
    elif body:
        for name in PROFILES.get_profile("body"):
            click.echo(f"- {name}")
    elif flavor:
        for name in PROFILES.get_profile("flavor"):
            click.echo(f"- {name}")
    elif cycle:
        for name in PROFILES.get_profile("cycle"):
            click.echo(f"- {name}")
    elif effects:
        for name in PROFILES.get_profile("effects"):
            click.echo(f"- {name}")
    else:
        click.echo("Please specify a category to list.")

@cli.command(help="""
             Get the location of a specific yerba mate brand.
             
             Example: yerba get "Brand Name"
             """)
@click.argument("name")
def get(type, name):
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






