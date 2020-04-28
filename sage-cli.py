#!/usr/bin/env python3


import sys
import click
import json
import logging
import sage_storage




@click.group()
@click.option('--token', envvar='SAGE_USER_TOKEN', help='SAGE use token (or use environment variable SAGE_USER_TOKEN)')
@click.option('--host', envvar='SAGE_HOST', help='SAGE host (or use environment variable SAGE_HOST)')
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug, host, token):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)
    #print("got token: {}".format(token))
    if debug:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        ctx.obj['DEBUG'] = True
    
    ctx.obj['TOKEN'] = token
    ctx.obj['HOST'] = host
    


@cli.group(help='SAGE storage')
@click.pass_context
def storage(ctx):
    #click.echo('Debug is %s' % (ctx.obj['DEBUG'] and 'on' or 'off'))
    #print(ctx)
    pass


@storage.group(help='bucket')
@click.pass_context
def bucket(ctx):
    pass
    #click.echo('Debug is %s' % (ctx.obj['DEBUG'] and 'on' or 'off'))
    #print(ctx)



@bucket.command(help='create bucket', name='create')
@click.pass_context
@click.option('--name', help='name of bucket')
@click.option('--datatype', required=True, help='datatype of bucket')
def bucketCreate(ctx, name, datatype):

    debug = False
    if "DEBUG" in ctx.obj:
        debug = ctx.obj['DEBUG']
   
    try:
        bucket = sage_storage.createBucket(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], datatype=datatype, name=name, debug=debug)
    except Exception as e:
        sys.exit(e)

    
    print(json.dumps(bucket, indent=2))
   

# edge code repository
@cli.command(help='SAGE edge code repository (not implemented)')
@click.pass_context
def ecr(ctx):
    #click.echo('Debug is %s' % (ctx.obj['DEBUG'] and 'on' or 'off'))
    print(ctx)


if __name__ == '__main__':
    cli(obj={})



