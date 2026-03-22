from pathlib import Path
import click



@click.command()
@click.option("--output", default="output", help="Output directory (default ./output)")
@click.option("--config", default=None, type=click.Path(exists=True, path_type=Path), help="path to companies Yaml config (default: companies.yaml)")
def run(output:str, config: Path | None) -> None:
    output_dir = Path(output)
    #session = build_session()