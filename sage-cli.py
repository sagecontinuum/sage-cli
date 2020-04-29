#!/usr/bin/env python3


import sys
import click
import json
import logging
import sage_storage

# storage:
# bucket
#        create
#        show
#        list
# bucket-permission
#        add
#        delete
# files --bucket_id
#        list
#        upload
#        download



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


@storage.group(help='bucket operations (create, list, ...)')
@click.pass_context
def bucket(ctx):
    pass
   
@storage.group(help='bucket permissions (private, public, sharing, ...)')
@click.pass_context
def permissions(ctx):
    pass

@storage.group(help='file operations (upload, download, list, ...)')
@click.pass_context
def files(ctx):
    pass


@bucket.command(help='create a new bucket', name='create')
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


@bucket.command(help='show bucket', name='show')
@click.pass_context
@click.argument('id')
def bucketShow(ctx, id):

    debug = False
    if "DEBUG" in ctx.obj:
        debug = ctx.obj['DEBUG']
   
    try:
        bucket = sage_storage.showBucket(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], bucketID=id, debug=debug)
    except Exception as e:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(e)

    
    print(json.dumps(bucket, indent=2))


@bucket.command(help='list buckets', name='list')
@click.pass_context
def bucketList(ctx):

    debug = False
    if "DEBUG" in ctx.obj:
        debug = ctx.obj['DEBUG']
   
    try:
        bucket = sage_storage.listBuckets(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], debug=debug)
    except Exception as e:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(e)

    
    print(json.dumps(bucket, indent=2))



@permissions.command(help='get bucket permissions', name='show')
@click.pass_context
@click.argument('id')
def bucketGetPermissions(ctx, id):

    debug = False
    if "DEBUG" in ctx.obj:
        debug = ctx.obj['DEBUG']
   
    try:
        p = sage_storage.getPermissions(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], bucketID=id, debug=debug)
    except Exception as e:
        sys.exit(e)

    
    print(json.dumps(p, indent=2))



#{"granteeType": "USER", "grantee": "otheruser", "permission": "READ"}'
@permissions.command(short_help='add bucket permissions', name='add')
@click.pass_context
@click.argument('bucket_id')
@click.argument('granteetype')  # USER or GROUP
@click.argument('grantee')      # user or group to get permission
@click.argument('permission')   # possible permisson: READ, WRITE, READ_ACL, WRITE_ACL
def bucketAddPermissions(ctx, bucket_id, granteetype, grantee, permission):
    # example: <BUCKET_ID> USER  otheruser READ 
   
    try:
        p = sage_storage.addPermissions(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], bucketID=bucket_id, granteeType=granteetype, grantee=grantee, permission=permission)
    except Exception as e:
        sys.exit(e)

    
    print(json.dumps(p, indent=2))


@permissions.command(short_help='make bucket public', name='public')
@click.pass_context
@click.argument('bucket_id')
def bucketMakePublic(ctx, bucket_id):
  
    try:
        p = sage_storage.makePublic(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], bucketID=bucket_id)
    except Exception as e:
        sys.exit(e)

    
    print(json.dumps(p, indent=2))


# edge code repository
@cli.command(help='SAGE edge code repository (not implemented)')
@click.pass_context
def ecr(ctx):
    #click.echo('Debug is %s' % (ctx.obj['DEBUG'] and 'on' or 'off'))
    print(ctx)


if __name__ == '__main__':
    cli(obj={})



