
import json
import threading
import time

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
    host = '10.240.0.3'
    client.connect(host, 8091, 'bucket1', 'Administrator', 'password',
                   handler)
    for i in range(880, 1024):
        result = client.add_stream(i, host, 0, 0, 10, 0, 0, 0)
        if result['status'] != 0:
            print 'Stream request to vb %d failed due to error %d' %\
                (i, result['status'])

    while handler.has_active_streams():
        time.sleep(.25)

    client.close()

if __name__ == "__main__":
    main()

