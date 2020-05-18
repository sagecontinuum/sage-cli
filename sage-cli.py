#!/usr/bin/env python3


import sys
import click
import json
import logging
import sage_storage

# storage:
# bucket
#       create
#       delete
#       show
#       list
#       (rename)
# permissions
#       add
#       delete
#       public
#       (private)
#       show
# files
#       list
#       upload
#       download
#       delete
#       (rename) # more difficult as S3 requires to copy an object


# (metadata)
#        add
#        search


# (ecr:) # edge code repository
# (app)
#       (create)
#       (delete)
#       (show)
#       (update) # update partial app definition 


# (ecs:) # edge code scheduler
# (job)
#       (create)
#       (delete)
#       (show)
#       (config) # send new config ?


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


   
    try:
        bucket = sage_storage.createBucket(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], datatype=datatype, name=name)
    except Exception as e:
        print("Unexpected error: {}, {}".format( sys.exc_info()[0], e ))
        sys.exit(1)

    
    print(json.dumps(bucket, indent=2))
    if 'error' in bucket:
        sys.exit(1)

@bucket.command(help='show bucket', name='show')
@click.pass_context
@click.argument('id')
def bucketShow(ctx, id):


   
    try:
        bucket = sage_storage.showBucket(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], bucketID=id)
    except Exception as e:
        print("Unexpected error: {}, {}".format( sys.exc_info()[0], e ))
        sys.exit(1)

    
    print(json.dumps(bucket, indent=2))
    if 'error' in bucket:
        sys.exit(1)


@bucket.command(help='delete bucket', name='delete')
@click.pass_context
@click.argument('id')
def bucketDelete(ctx, id):


   
    try:
        bucket = sage_storage.deleteBucket(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], bucketID=id)
    except Exception as e:
        print("Unexpected error: {}, {}".format( sys.exc_info()[0], e ))
        sys.exit(1)

    
    print(json.dumps(bucket, indent=2))
    if 'error' in bucket:
        sys.exit(1)


@bucket.command(help='list buckets', name='list')
@click.pass_context
def bucketList(ctx):


   
    try:
        bucket = sage_storage.listBuckets(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'])
    except Exception as e:
        print("Unexpected error: {}, {}".format( sys.exc_info()[0], e ))
        sys.exit(1)

    
    print(json.dumps(bucket, indent=2))
    if 'error' in bucket:
        sys.exit(1)


@permissions.command(help='get bucket permissions', name='show')
@click.pass_context
@click.argument('id')
def permissionsGet(ctx, id):


   
    try:
        p = sage_storage.getPermissions(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], bucketID=id)
    except Exception as e:
        print("Unexpected error: {}, {}".format( sys.exc_info()[0], e ))
        sys.exit(1)

    
    print(json.dumps(p, indent=2))
    if 'error' in p:
        sys.exit(1)
    


#{"granteeType": "USER", "grantee": "otheruser", "permission": "READ"}'
@permissions.command(short_help='add bucket permissions', name='add')
@click.pass_context
@click.argument('bucket_id')
@click.argument('granteetype')  # USER or GROUP
@click.argument('grantee')      # user or group to get permission
@click.argument('permission')   # possible permisson: READ, WRITE, READ_ACL, WRITE_ACL
def permissionsAdd(ctx, bucket_id, granteetype, grantee, permission):
    # example: <BUCKET_ID> USER  otheruser READ 
   
    try:
        p = sage_storage.addPermissions(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], bucketID=bucket_id, granteeType=granteetype, grantee=grantee, permission=permission)
    except Exception as e:
        print("Unexpected error: {}, {}".format( sys.exc_info()[0], e ))
        sys.exit(1)

    
    print(json.dumps(p, indent=2))
    if 'error' in p:
        sys.exit(1)


@permissions.command(short_help='make bucket public', name='public')
@click.pass_context
@click.argument('bucket_id')
def bucketMakePublic(ctx, bucket_id):
  
    try:
        p = sage_storage.makePublic(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], bucketID=bucket_id)
    except Exception as e:
        print("Unexpected error: {}, {}".format( sys.exc_info()[0], e ))
        sys.exit(1)

    
    print(json.dumps(p, indent=2))
    if 'error' in p:
        sys.exit(1)



@permissions.command(short_help='delete a permission', name='delete')
@click.pass_context
@click.argument('bucket_id')
@click.argument('granteetype')
@click.argument('grantee')
@click.option('--permission', help='remove only specific permission from grantee')
def permissionDelete(ctx, bucket_id, granteetype, grantee, permission):
  
    try:
        p = sage_storage.deletePermissions(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], bucketID=bucket_id, granteeType=granteetype, grantee=grantee, permission=permission)
    except Exception as e:
        print("Unexpected error: {}, {}".format( sys.exc_info()[0], e ))
        sys.exit(1)

    
    print(json.dumps(p, indent=2))
    if 'error' in p:
        sys.exit(1)



@files.command(help='upload file', name='upload')
@click.pass_context
@click.argument('bucket_id')
@click.argument('files', type=click.Path(exists=True), nargs=-1)
@click.option('--key', help='remote path and filename')
def fileUpload(ctx, bucket_id, files, key):


   
    try:
        result = sage_storage.upload(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], bucketID=bucket_id, sources=files, key=key)
    except Exception as e:
        print("Unexpected error: {}, {}".format( sys.exc_info()[0], e ))
        
        sys.exit(1)

    
    print(json.dumps(result, indent=2))
    if isinstance(result,dict):
        if 'error' in result:
            sys.exit(1)




@files.command(help='download file', name='download')
@click.pass_context
@click.argument('bucket_id')
@click.argument('key')
@click.option('--target', help='target filename or directory')
#@click.option('--key', help='remote path and filename')
def fileUpload(ctx, bucket_id, key, target):

   
    try:
        sage_storage.downloadFile(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], bucketID=bucket_id, key=key,  target=target)
    except Exception as e:
        print("Unexpected error: {}, {}".format( sys.exc_info()[0], e ))
        sys.exit(1)

    
    #print(json.dumps(result, indent=2))
    #if 'error' in result:
    #    sys.exit(1)




@files.command(help='get listing', name='list')
@click.pass_context
@click.argument('bucket_id')
@click.option('--prefix', help='choose subdirectory')
@click.option('--recursive', default=False)
def filesList(ctx, bucket_id, prefix, recursive):

   
    try:
        result = sage_storage.listFiles(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], bucketID=bucket_id, prefix=prefix, recursive=recursive)
    except Exception as e:
        print("Unexpected error: {}, {}".format( sys.exc_info()[0], e ))
        sys.exit(1)

    
    print(json.dumps(result, indent=2))
    if 'error' in result:
        sys.exit(1)

@files.command(help='delete file', name='delete')
@click.pass_context
@click.argument('bucket_id')
@click.argument('key')
#@click.option('--prefix', help='choose subdirectory')
#@click.option('--recursive', default=False)
def filesList(ctx, bucket_id, key):

   
    try:
        result = sage_storage.deleteFile(host=ctx.obj['HOST'], token=ctx.obj['TOKEN'], bucketID=bucket_id, key=key)
    except Exception as e:
        print("Unexpected error: {}, {}".format( sys.exc_info()[0], e ))
        sys.exit(1)

    
    print(json.dumps(result, indent=2))
    if 'error' in result:
        sys.exit(1)


# edge code repository
@cli.command(help='SAGE edge code repository (not implemented)')
@click.pass_context
def ecr(ctx):
    #click.echo('Debug is %s' % (ctx.obj['DEBUG'] and 'on' or 'off'))
    print(ctx)


if __name__ == '__main__':
    cli(obj={})



