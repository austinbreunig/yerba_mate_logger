import click
from brands import BrandRegistry

registry = BrandRegistry()

@click.group()
def cli():
    """Mate CLI to manage yerba mate brands."""
    pass

@cli.command()
@click.argument("name")
@click.argument("location")
def add(name, location):
    """Add a new yerba mate brand."""
    registry.add_brand(name, location)
    click.echo(f"✅ Added {name} from {location}.")

@cli.command()
def list():
    """List all yerba mate brands."""
    for name, location in registry.list_brands():
        click.echo(f"- {name} ({location})")

@cli.command()
@click.argument("name")
def get(name):
    """Get location of a specific brand."""
    loc = registry.get_location(name)
    if loc:
        click.echo(f"{name} is from {loc}.")
    else:
        click.echo(f"❌ Brand '{name}' not found.")
