import validation, datetime, paramiko
from flask import * 
from routes.decorators import RouteDecorators
from urllib.parse import urlparse

from funcs.string import str_equals, is_str_empty, sanitize

from funcs.validator import Validation

Status = Blueprint("Status", __name__)

@Status.route("/status", methods=["GET"])
@RouteDecorators.log
@RouteDecorators.admin_key_required
def status():
    return {
        "code": 200,
    }

    
        
