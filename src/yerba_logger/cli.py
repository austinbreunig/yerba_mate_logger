import os
import pandas as pd
import click
import questionary
from yerba_logger.registry import BrandRegistry, ProfileRegistry, WeightRegistry, get_user_file
from yerba_logger.mate import Mate
from yerba_logger.utils import (
    ask_date,
    ask_body_profile,
    ask_flavor_profile,
    ask_effect_profile,
)

BRANDS = BrandRegistry()
PROFILES = ProfileRegistry()
WEIGHTS = WeightRegistry()

@click.group(help="""
             Welcome to the Yerba Mate Logger!

                This is a command line interface (CLI) for managing your mate consumption.
             
                For understanding available brands:
             
                You can add new brands, list all available brands, and get the location of a specific brand.
             
                For Logging your yerba mate consumption:
             
                You can log your smell, flavor, and effects of yerba mate. Each property can be rated from 1 to 5.
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
             
                Example: yerba remove --> then follow the prompts
             
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
@click.option("--flavor", is_flag=True, help="List all yerba mate flavor profiles.")
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
             Set the yerba log weights. These weights are used to calculate the overall score of yerba mate.
             
             Example: yerba set_weights --smell 0.2 --flavor 0.3 --energy 0.5

             Ctrl+C to exit at any time.
             """)
@click.option("--cycle", type=float, default=0.05, help="Weight for cycle. Value between 0 and 1. Default is 5%.")
@click.option("--body", type=float, default=0.05, help="Weight for body. Value between 0 and 1. Default is 5%.")
@click.option("--flavor", type=float, default=0.4, help="Weight for flavor. Value between 0 and 1. Default is 40%.")
@click.option("--effects", type=float, default=0.5, help="Weight for effects. Value between 0 and 1. Default is 50%.")
def set_weights(cycle, body, flavor, effects):
    """Set the yerba log weights."""
    if cycle + body + flavor + effects != 1:
        click.echo("❌ The sum of all weights must be equal to 1.")
        return

    weights = {'cycle':cycle, 'body':body, 'flavor':flavor, 'effects':effects}
    for name, value in weights.items():
        WEIGHTS.add_weight(name=name, data=value)

    click.echo(f"✅ Weights set:")
    click.echo(f"- Cycle: {cycle}")
    click.echo(f"- Body: {body}")
    click.echo(f"- Flavor: {flavor}")
    click.echo(f"- Effects: {effects}")


@cli.command(help="""
             Log yerba mate consumption.
             
             Follow the prompts to log your yerba mate consumption!

             Ctrl+C to exit at any time.
             """)
@click.option("--show", is_flag=True, help="Show the yerba log.")
@click.option("--summary", is_flag=True, help="Show the yerba log summary.")
def log(show, summary):
    user_path = get_user_file('yerba_log.csv')
    if show:
        click.echo(user_path)
        if os.path.exists(user_path):
            df = pd.read_csv(user_path)
            click.echo(df.head(5))
        else:
            click.echo("❌ No yerba log found.")
        return
    
    if summary:
        if os.path.exists(user_path):
            df = pd.read_csv(user_path)
            click.echo(df.describe())
        else:
            click.echo("❌ No yerba log found.")
        return
    
    brands = BRANDS.list_brands()
    flavors = PROFILES.get_profile("flavor")
    effects = PROFILES.get_profile("effects")
    bodies = PROFILES.get_profile("body")
    cycles = PROFILES.get_profile("cycle")

    brand = questionary.select(
    "Choose a yerba mate:",
    choices=brands
    ).ask()

    date = ask_date() # asking for date

    gourd_count = int(questionary.text("Enter the number of gourds:").ask()) or 1

    body = int(questionary.select(
        "Rate the body (1-5):",
        choices=["1", "2", "3", "4", "5"]
    ).ask())
    body_profile = ask_body_profile(bodies) # asking for body profile

    flavor = int(questionary.select(
        "Rate the flavor (1-5):",
        choices=["1", "2", "3", "4", "5"]
    ).ask())
    flavor_profile = ask_flavor_profile(flavors) # asking for flavor profile

    cycle = int(questionary.select(
        "Rate the cycle (1-5):",
        choices=["1", "2", "3", "4", "5"]
    ).ask())
    cycle_profile = questionary.select(
        "Select a cycle profile:",
        choices=cycles
    ).ask() # asking for cycle profile

    effect = int(questionary.select(
        "Rate the effects (1-5):",
        choices=["1", "2", "3", "4", "5"]
    ).ask())
    effect_category = ask_effect_profile(effects)

    strength = int(questionary.select(
        "Rate the strength: (1(Light) - 5(Very Strong))",
        choices=["1", "2", "3", "4", "5"]
    ).ask())

    mate = Mate(
        date=date,
        name=brand,
        location=BRANDS.get_location(brand),
        gourd_count=gourd_count,
        body_rank=body,
        body_profile=body_profile,
        flavor_rank=flavor,
        flavor_profile=flavor_profile,
        cycle_rank=cycle,
        cycle_profile=cycle_profile,
        effects_rank=effect,
        effects_profile=effect_category,
        strength_rank=strength,
    )
    log_df = mate.process()
    click.echo(f"Log Entry: {log_df}")

    if os.path.exists(user_path):
        main_df = pd.read_csv(user_path)
        main_df = pd.concat([main_df, log_df], ignore_index=True).sort_values(by='date', ascending=False)

        main_df.to_csv(user_path, index=False)
    else:
        log_df.to_csv(user_path, index=False)
    click.echo(f"✅ Log entry saved to {user_path}.")






