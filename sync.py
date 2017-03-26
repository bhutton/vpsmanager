#!/usr/local/bin/python

file = "./excludes.txt"
rsync_cmd = "/usr/local/bin/rsync"
rsync_args = "-rvp"
rsync_exc = "--exclude-from" + file