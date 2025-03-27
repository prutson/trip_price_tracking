from flask import Flask, make_response
import sys
from lib.parser import Parser
from api.decorators import validate_entry_params, require_token
from lib.shared import *

sys.dont_write_bytecode = True
app = Flask(__name__)

@app.route('/api/v1/guanabara', methods=['GET'])
@require_token
@validate_entry_params
def api_fetch_price(entry_params):
    log_message('Buscando informações...')
    response = Parser(entry_params).get_price()
    log_message(response)
    return make_response({'result': response}, 200)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')