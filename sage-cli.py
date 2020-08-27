#!/usr/bin/env python3


import sys
import click
import json
import logging
import sage_storage
import linecache
import sys
import os

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


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"):\n{}'.format(filename, lineno, line.strip(), exc_obj))




@click.group()
@click.option('--token', envvar='SAGE_USER_TOKEN', help='SAGE use token (or use environment variable SAGE_USER_TOKEN)')
#@click.option('--host', envvar='SAGE_HOST', help='SAGE host (or use environment variable SAGE_HOST)')
@click.option('--sage_store_url', envvar='SAGE_STORE_URL', help='SAGE host (or use environment variable SAGE_STORE_URL)')

@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug, sage_store_url, token):
    
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)
    #print("got token: {}".format(token))
    if debug:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        ctx.obj['DEBUG'] = True
    
    if not sage_store_url:
        print("Please specifiy --sage_store_url or SAGE_STORE_URL")
        sys.exit(1)
    
    sage_store_url = sage_store_url.rstrip('/')
    
    ctx.obj['TOKEN'] = token
    ctx.obj['SAGE_STORE_URL'] = sage_store_url
    
    

@cli.command(help='show config')
@click.pass_context
def config(ctx):
   
    print("SAGE_STORE_URL: "+os.environ.get("SAGE_STORE_URL", "N/A"))

    print("SAGE_USER_TOKEN: "+os.environ.get("SAGE_USER_TOKEN", "N/A"))

    pass


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
        bucket = sage_storage.createBucket(host=ctx.obj['SAGE_STORE_URL'], token=ctx.obj['TOKEN'], datatype=datatype, name=name)
    except Exception as e:
        PrintException()
        sys.exit(1)

    
    
    print(json.dumps(bucket, indent=2))
    if 'error' in bucket:
        sys.exit(1)

@bucket.command(help='show bucket', name='show')
@click.pass_context
@click.argument('id')
def bucketShow(ctx, id):


   
    try:
        bucket = sage_storage.showBucket(host=ctx.obj['SAGE_STORE_URL'], token=ctx.obj['TOKEN'], bucketID=id)
    except Exception as e:
        PrintException()
        sys.exit(1)

    
    print(json.dumps(bucket, indent=2))
    if 'error' in bucket:
        sys.exit(1)


@bucket.command(help='delete bucket', name='delete')
@click.pass_context
@click.argument('id')
def bucketDelete(ctx, id):


   
    try:
        bucket = sage_storage.deleteBucket(host=ctx.obj['SAGE_STORE_URL'], token=ctx.obj['TOKEN'], bucketID=id)
    except Exception as e:
        PrintException()
        sys.exit(1)

    
    print(json.dumps(bucket, indent=2))
    if 'error' in bucket:
        sys.exit(1)


@bucket.command(help='list buckets', name='list')
@click.pass_context
def bucketList(ctx):


   
    try:
        bucket = sage_storage.listBuckets(host=ctx.obj['SAGE_STORE_URL'], token=ctx.obj['TOKEN'])
    except Exception as e:
        PrintException()
        sys.exit(1)

    
    print(json.dumps(bucket, indent=2))
    if 'error' in bucket:
        sys.exit(1)


@permissions.command(help='get bucket permissions', name='show')
@click.pass_context
@click.argument('id')
def permissionsGet(ctx, id):


   
    try:
        p = sage_storage.getPermissions(host=ctx.obj['SAGE_STORE_URL'], token=ctx.obj['TOKEN'], bucketID=id)
    except Exception as e:
        PrintException()
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
        p = sage_storage.addPermissions(host=ctx.obj['SAGE_STORE_URL'], token=ctx.obj['TOKEN'], bucketID=bucket_id, granteeType=granteetype, grantee=grantee, permission=permission)
    except Exception as e:
        PrintException()
        sys.exit(1)

    
    print(json.dumps(p, indent=2))
    if 'error' in p:
        sys.exit(1)


@permissions.command(short_help='make bucket public', name='public')
@click.pass_context
@click.argument('bucket_id')
def bucketMakePublic(ctx, bucket_id):
  
    try:
        p = sage_storage.makePublic(host=ctx.obj['SAGE_STORE_URL'], token=ctx.obj['TOKEN'], bucketID=bucket_id)
    except Exception as e:
        PrintException()
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
        p = sage_storage.deletePermissions(host=ctx.obj['SAGE_STORE_URL'], token=ctx.obj['TOKEN'], bucketID=bucket_id, granteeType=granteetype, grantee=grantee, permission=permission)
    except Exception as e:
        PrintException()
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
        result = sage_storage.upload(host=ctx.obj['SAGE_STORE_URL'], token=ctx.obj['TOKEN'], bucketID=bucket_id, sources=files, key=key)
    except Exception as e:
        PrintException()
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
        sage_storage.downloadFile(host=ctx.obj['SAGE_STORE_URL'], token=ctx.obj['TOKEN'], bucketID=bucket_id, key=key,  target=target)
    except Exception as e:
        PrintException()
        sys.exit(1)

    
    #print(json.dumps(result, indent=2))
    #if 'error' in result:
    #    sys.exit(1)




@files.command(help='get listing', name='list')
@click.pass_context
@click.argument('bucket_id')
@click.option('--prefix', help='choose subdirectory')
@click.option('--recursive/--no-recursive', default=False, )
@click.option('--limit', required=False, type=int)
@click.option('--all/--no-all', default=False, help='lists all files without pagination')
@click.option('--format', default='table', help='table (default), json')
@click.option('--ctoken', required=False, type=str , help='continuationToken')
def filesList(ctx, bucket_id, prefix, recursive, limit, all, format, ctoken):
    

    if prefix:
        if prefix[-1] != "/":
            prefix = prefix + "/"

        prefix_str = prefix
    else:
        prefix_str = ""
    
    page = 0
    #ctoken = ""
    while True:
        page += 1
        try:
            
            result = sage_storage.listFiles(host=ctx.obj['SAGE_STORE_URL'], token=ctx.obj['TOKEN'], bucketID=bucket_id, prefix=prefix, recursive=recursive, cToken=ctoken, limit=limit)
        except Exception:
            PrintException()
            sys.exit(1)

        #TODO CommonPrefixes

        #print(result)
        if 'error' in result:
            if format=='json':
                print(json.dumps(result, indent=2))
            else:
                print(json.dumps(result['error'], indent=2))
            sys.exit(1)
        
        
        isTruncated = 'IsTruncated' in result  and result['IsTruncated']

        if format=='json':
            print(json.dumps(result, indent=2))

            if not all:         
                break

            print("---")

        if format=='table':
            if not recursive:
                if "CommonPrefixes" in result and result["CommonPrefixes"] != None and len(result["CommonPrefixes"]) != 0:
                    for key in result["CommonPrefixes"]:
                        if "Prefix" in key:
                            print(key["Prefix"])
                        else:
                            print("Field \"Prefix\" missing")
                            sys.exit(1)

            if "Contents" in result and result["Contents"] != None:
                for item in result["Contents"]:
                    if "Key" in item:
                        print("{}{} {} {}".format(prefix_str, item.get("Key"), item.get("Size"), item.get("LastModified")))
                    else:
                        print("error: Item has no key {}".format( item))
                        sys.exit(1)


            if not all:
                if isTruncated:
                    print("# results have been truncated")
                    print( "# NextContinuationToken={}".format(result['NextContinuationToken']) ) 
                break

                #for key in result["Contents"][:-1]:
                #    print(json.dumps(key)+",")
                

                #print(json.dumps(result["Contents"][-1]))



        #result["Contents"]=None    
        #print(result)
        #sys.exit(0)
        #print("page: {} ({})".format(page, ctoken))

        

        if not ( isTruncated):
            break

        if not 'NextContinuationToken' in result:
            print("error: NextContinuationToken is missing")
            sys.exit(1)

        if result['NextContinuationToken'] == ctoken:
            print("error: NextContinuationToken is the same as the previous token  {} vs {}".format( ctoken, result['NextContinuationToken']))
            sys.exit(1)

        ctoken=result['NextContinuationToken']
        

    
    #print(json.dumps(result, indent=2))
    if 'error' in result:
        sys.exit(1)

@files.command(help='delete file', name='delete')
@click.pass_context
@click.argument('bucket_id')
@click.argument('key')
#@click.option('--prefix', help='choose subdirectory')
#@click.option('--recursive', default=False)
def fileDelete(ctx, bucket_id, key):

   
    try:
        result = sage_storage.deleteFile(host=ctx.obj['SAGE_STORE_URL'], token=ctx.obj['TOKEN'], bucketID=bucket_id, key=key)
    except Exception as e:
        PrintException()
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



