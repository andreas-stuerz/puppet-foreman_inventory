#!/usr/bin/env python

"""
This script returns host that matches the search query as bolt inventory targets
Requires: hammer-cli-foreman
See: https://github.com/theforeman/hammer-cli-foreman
"""
import json
import os
import sys
import subprocess
import shlex

params = json.load(sys.stdin)
query = params['query']
page = params.get('page', 1)
per_page = params.get('per_page', 1000)
server_url = params.get('server_url', '')
username = params.get('username', '')
password = params.get('password', '')

hammer_cli_bin = os.path.expanduser(params.get('hammer_cli_bin', '~/.gem/ruby/2.5.0/bin/hammer'))

targets = []
exitcode = 0

if server_url:
    server_url = ("-s %s" % server_url)

if username:
    username = ("-u %s" % username)

if password:
    password = ("-p %s" % password)

def make_error(msg, code, type = "error"):
    error = {
        "_error": {
            "kind": type,
            "msg": msg,
            "details": { "exitcode": code },
        }
    }
    return error

command = "%s %s %s %s --no-headers --output csv host list --search '%s' --per-page %d --page %d --fields name" \
          % (hammer_cli_bin, server_url, username, password, query, per_page, page)
args = shlex.split(command)

p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output,error = p.communicate()
if output:
    for target in output.split("\n"):
        if target:
            targets.append(target)
    json.dump({'value': targets}, sys.stdout)
    exit(0)
if error:
    exitcode = p.returncode
    result = make_error(error.strip(), p.returncode, 'hammer cli subcommand')

print(json.dumps(result))
exit(exitcode)

