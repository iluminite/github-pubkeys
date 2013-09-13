#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright (c) 2013, illumin-us-r3v0lution 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''
Post SSH Public Key to Github API, use Token for authentication

retrieve a token from the github web UI

'''

import os
import sys
import json
import logging
import argparse

import requests


logger = logging.getLogger(__name__)

API_URL = 'https://api.github.com/'


def process_args():
    '''
    process command line arguments passed to the script
    returns parsed args (as a dictionary) from argparse

    '''
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--create',
                        action='store_true',
                        default=False,
                        help='full path to SSH public key')

    parser.add_argument('-f', '--file',
                        action='store',
                        default=None,
                        help='full path to SSH public key')

    parser.add_argument('-l', '--list',
                        action='store_true',
                        default=False,
                        help='list all user public keys in Github')

    parser.add_argument('-d', '--delete',
                        action='store',
                        default=False,
                        help='ID of the SSH key to delete from Github')

    parser.add_argument(      '--debug',
                        action='store_true',
                        default=False,
                        help='flag to enable/disable debug logging')

    parser.add_argument(      '--test',
                        action='store_true',
                        default=False,
                        help='enable test mode')

    parser.add_argument(      '--title',
                        action='store',
                        default='key for OMS deployment',
                        help='enable test mode')

    parser.add_argument('-t', '--token',
                        action='store',
                        default=None,
                        help='Token (from web UI) to use with Github authorization')

    parser.add_argument('-u', '--user',
                        action='store',
                        default=None,
                        help='Github username for authorization')

    return parser.parse_args()


def _test_api_access(auth):
    '''
    GET user info, just to test API access with user/token

    '''
    return requests.get(API_URL+'user',
                        auth)


def _get_public_key(f):
    '''
    provided ``file``, an SSH public keyfile, return the key as a string

    '''
    with open(f, 'r') as keyfile:
        key = keyfile.readline()
    return key


def _create_key(new_key=None,
                auth=None):
    '''
    provided a public key dictionary ``new_key``, and an authentication tuple
    ``auth`` to create the key for the github user.

    '''
    logger.debug(('POST data: %s' % json.dumps(new_key,
                                               indent=4)))
    return requests.post(API_URL+'user/keys',
                         json.dumps(new_key),
                         auth=auth)


def _list_keys(auth=None):
    '''
    look up the SSH public keys currently in github, authorizing with ``user``
    and ``token``.

    '''
    return requests.get(API_URL+'user/keys',
                        auth=auth)
    

def _delete_key(kid=None,
                auth=None):
    '''
    provided the ID of an SSH Key in the Github API, ``kid``, and ``auth`` as a
    requests authentication object/tubple, use the Github API to delete the key.

    '''
    return requests.delete((API_URL+'user/keys/%s' % kid),
                           auth=auth)


def main():
    '''
    use Github's API to create an SSH Key for a Github user

    '''
    args = process_args()
    response = None

    # set log level and setup logging
    log_level = logging.INFO
    if args.debug:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level,
                        stream=sys.stderr,
                        format="%(asctime)s [%(process)d] %(message)s")

    logger.debug(('Script args: %s' % args))

    if args.test:
        logger.debug(('Testing Github API access for %s' % args.user))
        response = _test_api_access(auth=(args.user, args.token))
    # if we've received a file to read, use the API to create a key
    elif args.create:
        keyfile = args.file
        if not keyfile:
            print('--file (-f) must specify a file to read from')
            sys.exit(1)

        logger.debug(('Opening public key file %s' % keyfile))
        public_key = _get_public_key(keyfile)
        # error out if no key received
        if not public_key:
            print(('unable to read key from file %s' % keyfile))
            sys.exit(1)
        post_data = {
            "title": args.title,
            "key": public_key.rstrip('\n')
        }
        response = _create_key(new_key=post_data,
                               auth=(args.user, args.token))

    # else, if we are supposed to list the current keys..
    elif args.list:
        response = _list_keys(auth=(args.user, args.token))

    # else, if we have a key to delete, do that instead
    elif args.delete:
        response = _delete_key(kid=args.delete,
                               auth=(args.user, args.token))
        print response.text

    # dump response to user
    if response:
        logger.info(('API Response: %s' % json.dumps(response.json(),
                                                     indent=4)))
    else:
        print('No response to print, did you specify an action to take?')


if __name__ == '__main__':
    main()
