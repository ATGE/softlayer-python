"""Get details for a hardware device."""
# :license: MIT, see LICENSE for more details.

import click

import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI import formatting
from SoftLayer.CLI import helpers
from SoftLayer.CLI.virt.bandwidth import create_bandwidth_table
from SoftLayer import utils


@click.command()
@click.argument('identifier')
@click.option('--start_date', '-s', type=click.STRING, required=True,
              help="Start Date YYYY-MM-DD, YYYY-MM-DDTHH:mm:ss,")
@click.option('--end_date', '-e', type=click.STRING, required=True,
              help="End Date YYYY-MM-DD, YYYY-MM-DDTHH:mm:ss")
@click.option('--summary_period', '-p', type=click.INT, default=3600, show_default=True,
              help="300, 600, 1800, 3600, 43200 or 86400 seconds")
@click.option('--quite_summary', '-q', is_flag=True, default=False, show_default=True,
              help="Only show the summary table")
@environment.pass_env
def cli(env, identifier, start_date, end_date, summary_period, quite_summary):
    """Bandwidth data over date range. Bandwidth is listed in GB

    Using just a date might get you times off by 1 hour, use T00:01 to get just the specific days data
    Timezones can also be included with the YYYY-MM-DDTHH:mm:ss.00000-HH:mm format.

    Example::

        slcli hw bandwidth 1234 -s 2019-05-01T00:01 -e 2019-05-02T00:00:01.00000-12:00
    """
    hardware = SoftLayer.HardwareManager(env.client)
    hardware_id = helpers.resolve_id(hardware.resolve_ids, identifier, 'hardware')
    data = hardware.get_bandwidth_data(hardware_id, start_date, end_date, None, summary_period)

    title = "Bandwidth Report: %s - %s" % (start_date, end_date)
    table, sum_table = create_bandwidth_table(data, summary_period, title)

    env.fout(sum_table)
    if not quite_summary:
        env.fout(table)


def mb_to_gb(mbytes):
    """Converts a MegaByte int to GigaByte. mbytes/2^10"""
    return round(mbytes / 2 ** 10, 4)
