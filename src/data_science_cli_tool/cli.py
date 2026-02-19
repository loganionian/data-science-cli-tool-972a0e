import click
from .core import DataCleaner

@click.command()
@click.option('--input', required=True, type=click.Path(exists=True), help='Input data file (CSV or JSON)')
@click.option('--output', required=True, type=click.Path(), help='Output data file (CSV or JSON)')
@click.option('--remove-null', is_flag=True, help='Remove null values from the dataset')
@click.option('--normalize', is_flag=True, help='Normalize features in the dataset')
@click.option('--remove-outliers', is_flag=True, help='Remove outliers from the dataset')
def clean_data(input: str, output: str, remove_null: bool, normalize: bool, remove_outliers: bool):
    cleaner = DataCleaner(input, output)
    cleaner.clean_data(remove_null, normalize, remove_outliers)
    click.echo(f"Data cleaned and saved to {output}")

if __name__ == '__main__':
    clean_data()