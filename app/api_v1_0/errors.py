###########################################
# File: errors.py
# Desc: definition of some errors
# Apr 2018
###########################################

from app.exceptions import ValidationError
from . import api

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
