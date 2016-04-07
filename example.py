import argparse
import json
import threading
import time
import sys
import urllib2

from dcp import DcpClient, ResponseHandler


class MyHandler(ResponseHandler):

    def __init__(self):
        ResponseHandler.__init__(self)
        self.lock = threading.Lock()
        self.count = 0

    def mutation(self, response):
        self.lock.acquire()
        #print "Mutation: ", response
        self.count +=1
        self.lock.release()

    def deletion(self, response):
        self.lock.acquire()
        #print "Deletion: ", response
        self.count += 1
        self.lock.release()

    def marker(self, response):
        self.lock.acquire()
        #print "Marker: ", response
        self.lock.release()

    def stream_end(self, response):
        self.lock.acquire()
        #print "Stream End: ", response
        self.lock.release()

    def get_num_items(self):
        return self.count


def main():
    handler = MyHandler()
    client = DcpClient()
    args = parse_arguments(sys.argv[1:])
    endpoint = 'http://{}:8091/pools/default/buckets/{}'.format(args.host,
                                                                args.bucket)
    vb_map = json.loads(urllib2.urlopen(endpoint).read())['vBucketServerMap']
    replicas = get_replica_vbuckets(vb_map, args.host)
    client.connect(args.host, 8091, args.bucket, args.username, args.password,
                   handler)
    while True:
        for i in replicas:
            result = client.add_stream(i, args.host, 0, 0, 1, 0, 0, 0)
            while result['status'] == 2:
                time.sleep(0.5)
                result = client.add_stream(i, args.host, 0, 0, 1, 0, 0, 0)
            if result['status'] != 0:
                print 'Stream request to vb %d failed due to error %d' % \
                      (i, result['status'])

    client.close()


def get_replica_vbuckets(vb_map, host):
    host += ':11210'
    node_index = vb_map['serverList'].index(host)
    replicas = [i for i in xrange(1024) if vb_map['vBucketMap'][i][1] == node_index]
    return replicas

def parse_arguments(program_args):
    parser = argparse.ArgumentParser(description='DCP client to reproduce MB-19093')
    parser.add_argument('host', default='localhost',
                        help='hostname of the couchbase node to test')
    parser.add_argument('bucket', default='default',
                        help='name of the bucket to test')
    parser.add_argument('username', default='Administrator',
                        help='couchbase username')
    parser.add_argument('password', default='password',
                        help='couchbase password')
    return parser.parse_args(program_args)


if __name__ == "__main__":
    main()

