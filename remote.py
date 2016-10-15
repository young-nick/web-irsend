#!/usr/bin/env python

import argparse

from lirc.lirc import Lirc
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, jsonify

BASE_URL = ''

app = Flask(__name__)

# Initialise the Lirc config parser
lircParse = Lirc('/etc/lirc/lircd.conf')

app.config['devices'] = lircParse.devices()

@app.route("/")
@app.route("/<device>")
def index(device=None):
    # Get the devices from the config file
    devices = []
    for dev in app.config['devices'].keys():
        d = {
            'id': dev,
            'name': dev,
        }
        devices.append(d)
    
    return render_template('remote.html', devices=devices)


@app.route("/device/<device_id>")
def device(device_id=None):
    print "called %s" % device_id
    d = {'id':device_id,
         'keydefs': app.config['devices'][device_id]
         }
    if 'format' in request.args:
        print request.args['format']
        return jsonify(d)
    else:
        return render_template('control.html', d=d)


@app.route("/device/<device_id>/clicked/<op>")
def clicked(device_id=None, op=None):
    # Send message to Lirc to control the IR
    lircParse.send_once(device_id, op)
    
    return ""



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ipaddr',
                        default="0.0.0.0",
                        help="IP address to listen on, default %(default)s")
    parser.add_argument('-p', '--port',
                        default=5000,
                        type=int,
                        help="Port to listen on, default %(default)s")
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help="Debug mode, default %(default)s")
    args = parser.parse_args()

    app.run(args.ipaddr, args.port, debug=args.debug)


