import math
from rich.console import Console
from rich.table import Table

def format_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return '0B'
    
    size_name = ('B', 'KB', 'MB', 'GB', 'TB')
    i = int(math.floor(math.log(size_bytes, 1024)))
    pow = math.pow(1024, i)
    size = round(size_bytes / pow, 2)

    return f'{size} {size_name[i]}'

def print_objects_table(objects):
    console = Console()
    table = Table(title='S3 Objects Info')

    table.add_column('Key', style='cyan', no_wrap=True)
    table.add_column('Size', style='green')
    table.add_column('Last Modified', style='magenta')

    for obj in objects:
        table.add_row(obj['Key'], format_size(obj['Size']), str(obj['LastModified']))
    
    console.print(table)

def print_success(message: str):
    console = Console()

    console.print(f'[green]{message}[/green]')

def print_error(message: str):
    console = Console()

    console.print(f'[red]{message}[/red]')

def print_url(url: str):
    console = Console()

    console.print(f'[blue]Presigned URL:[/blue] [yellow][underline]{url}[/underline][/yellow]')