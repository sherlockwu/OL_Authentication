#!/usr/bin/env python
import os, sys, random, string

import rethinkdb as r

from common import *

NGINX_EXAMPLE = 'docker run -d -p 80:80 -v %s:/usr/share/nginx/html:ro nginx'

def db_init(dest_ip):
    # connect
    conn = r.connect(dest_ip, 28015)
    state = ''
    try:
        r.db_drop('authentication').run(conn)
        state = 'deleted, then created'
    except:
        state = 'created'

    r.db_create('authentication').run(conn)
    r.db('authentication').table_create('user', primary_key = 'fbid').run(conn)

    # new database (if created, delete)

def main():
    app_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
    static_dir = os.path.join(SCRIPT_DIR, 'static')
    root_dir = os.path.join(SCRIPT_DIR, '..', '..')
    cluster_dir = os.path.join(root_dir, 'util', 'cluster')
    builder_dir = os.path.join(root_dir, 'lambda-generator')
    if not os.path.exists(cluster_dir):
        return 'cluster not running'

    # build image
    print '='*40
    print 'Building image'
    builder = os.path.join(builder_dir, 'builder.py')
    run(builder + ' -n %s -l %s -c %s' %
        (app_name,
         os.path.join(SCRIPT_DIR, 'authentication.py'),
         os.path.join(SCRIPT_DIR, 'lambda-config.json')))

    # push image
    print '='*40
    print 'Pushing image'
    registry = rdjs(os.path.join(cluster_dir, 'registry.json'))
    img = 'localhost:%s/%s' % (registry['host_port'], app_name)
    run('docker tag -f %s %s' % (app_name, img))
    run('docker push ' + img)

    # setup config
    worker0 = rdjs(os.path.join(cluster_dir, 'worker-0.json'))
    balancer = rdjs(os.path.join(cluster_dir, 'loadbalancer-1.json'))
    config_file = os.path.join(static_dir, 'config.json')
    url = ("http://%s:%s/runLambda/%s" %
           (balancer['host_ip'], balancer['host_port'], app_name))
    wrjs(config_file, {'url': url})

    # init database
        # print
    print '='*40
    print 'Initing Database'
        # db_init
    db_init(worker0['ip']) # TODO which IP?

if __name__ == '__main__':
    rv = main()
    if rv != None:
        print 'ERROR: ' + rv
        sys.exit(1)
    sys.exit(0)
