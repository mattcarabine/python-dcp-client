## Python DCP Client
A modified DCP client written in python designed to reproduce
[MB-19093](https://issues.couchbase.com/browse/MB-19093).

If you want to use this to test then you should run pillowfight (or similar
load generation tool) against the cluster you are testing.

Then run the client as follows:

```
python example.py [host] [bucket] [user] [password]
```

e.g

```
python example.py 10.240.0.9 bucket1 Administrator password
```

The client will then automatically identify which vbuckets are the replica
vbuckets for the given node and constantly open replica streams against them,
likely to trigger the bug.

This is far quicker than waiting for the reproduction the usual way, it usually
triggers within a matter of minutes.

If you have any questions or problems please contact
matt.carabine@couchbase.com