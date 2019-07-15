"""Manage LBaaS members."""
import click

import SoftLayer
from SoftLayer.CLI import environment, formatting, helpers
from SoftLayer.exceptions import SoftLayerAPIError
from SoftLayer import utils
from pprint import pprint as pp 

@click.command()
@click.argument('identifier')
@click.option('--member', '-m', required=True, help="Member UUID")
@environment.pass_env
def remove(env, identifier,   member):
    """Remove a LBaaS member.

    Member UUID can be found from `slcli lb detail`.
    """

    mgr = SoftLayer.LoadBalancerManager(env.client)

    uuid, lbid = mgr.get_lbaas_uuid_id(identifier)
    # Get a member ID to remove

    try:
        result = mgr.delete_lb_member(uuid, member)
        click.secho("Member {} removed".format(member), fg='green')
    except SoftLayerAPIError as e:
        click.secho("ERROR: {}".format(e.faultString), fg='red')


@click.command()
@click.argument('identifier')
@click.option('--private/--public', default=True, required=True, help="Private or public IP of the new member.")
@click.option('--member', '-m', required=True, help="Member IP address.")
@click.option('--weight', '-w', default=50, type=int, help="Weight of this member.")
@environment.pass_env
def add(env, identifier,  private, member, weight):
    """Add a new LBaaS members."""

    mgr = SoftLayer.LoadBalancerManager(env.client)
    uuid, lbid = mgr.get_lbaas_uuid_id(identifier)
    # Get a server ID to add
    to_add = {"weight": weight}
    if private:
        to_add['privateIpAddress'] = member
    else:
        to_add['publicIpAddress'] = member

    try:
        result = mgr.add_lb_member(uuid, to_add)
        click.secho("Member {} added".format(member), fg='green')
    except SoftLayerAPIError as e:
        if 'publicIpAddress must be a string' in e.faultString:
            click.secho("This LB requires a Public IP address for its members and none was supplied", fg='red')
        elif 'privateIpAddress must be a string' in e.faultString:
            click.secho("This LB requires a Private IP address for its members and none was supplied", fg='red')
        click.secho("ERROR: {}".format(e.faultString), fg='red')



