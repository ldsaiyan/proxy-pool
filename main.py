# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @FILE     : main.py
import click

from proxy_pool.process import ProxyPool
from setting import BANNER,VERSION

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=VERSION)
def cli():
    """ProxyPool cli工具"""
    click.echo(BANNER)

@cli.command(name="schedule")
def schedule():
    """ 调度程序 """
    #click.echo(BANNER)
    from proxy_pool.schedule import runSchedule
    runSchedule()
    #ProxyPool().run()

@cli.command(name="api")
def server():
    """ api服务 """
    #click.echo(BANNER)
    from proxy_pool.api.proxyApi import runFlask
    runFlask()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cli()


