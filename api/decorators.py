from functools import wraps
from flask import request, g, abort
from .entry_params import EntryParams
import uuid
from flask import request, abort
import os

def require_token(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        expected_token = os.getenv('API_TOKEN')
        received_token = request.headers.get('Authorization')

        if not received_token or received_token != f"Bearer {expected_token}":
            abort(401, description="Unauthorized. Invalid or missing token.")

        return func(*args, **kwargs)
    return wrapper

def validate_fields(request_data, required_fields):
    if missing_fields := required_fields - request_data.keys():
        abort(400, f'Missing required parameters: {", ".join(missing_fields)}')

def validate_entry_params(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        g.request_id = str(uuid.uuid4())[:8]
        required_fields = {'origem', 'destino', 'data', 'passageiros'}
        request_data = request.json
        request_params = set(request_data.keys())
        validate_fields(request_data, required_fields)
        entry_params_dict = {key: request_data[key] for key in request_params & set(EntryParams.__dataclass_fields__)}
        entry_params = EntryParams(**entry_params_dict)
        g.entry_params = entry_params.__dict__

        return func(entry_params, *args, **kwargs)
    return wrapper