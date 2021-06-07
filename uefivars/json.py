#!/usr/bin/env python3
#
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT

import json
from .varstore import *

class JSONVar(UEFIVar):
    def __init__(self, jvar):
        var = {}
        name = jvar['name']
        data = bytes.fromhex(jvar['data'])
        guid = bytes.fromhex(jvar['guid'])
        attr = int(jvar['attr'])
        timestamp = None
        digest = None
        if jvar['timestamp']:
            timestamp = bytes.fromhex(jvar['timestamp'])
        if jvar['digest']:
            digest = bytes.fromhex(jvar['digest'])
        super().__init__(name, data, guid, attr, timestamp, digest)

    def __dict__(self):
        super().__dict__()

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return " ".join("{0:02x}".format(c) for c in o)
        try:
            return json.JSONEncoder.default(self, o)
        except:
            return o.__dict__()

class JSONUEFIVarStore(UEFIVarStore):
    def __init__(self, data):
        # Read the JSON file
        jsondec = json.JSONDecoder()
        json = jsondec.decode(f.read())

        # Copy all JSON elements to the store
        for jvar in json:
            self.vars.append(JSONVar(jvar).var)

    def __bytes__(self):
        return self.__str__().encode('utf-8')

    def __str__(self):
        jsonenc = JSONEncoder(indent=4, separators=(',', ': '))
        return jsonenc.encode(self.vars)
