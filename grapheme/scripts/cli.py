# Skeleton of a CLI

import click

import grapheme


@click.command('grapheme')
@click.argument('count', type=int, metavar='N')
def cli(count):
    """Echo a value `N` number of times"""
    for i in range(count):
        click.echo(grapheme.has_legs)
