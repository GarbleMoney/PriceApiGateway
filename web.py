# coding = utf-8
from sanic import Sanic
from sanic_cors import CORS
from sanic.response import json
from utils import fetch_token_price


app = Sanic("PriceApiGateway")
CORS(app)

@app.route("/api/v1/token/price", methods=['GET', 'OPTIONS'])
def get_token_price(request):
    token = request.args.get('token')
    ret_dict = {'status': 'error', 'description': None}
    if token:
        return json(fetch_token_price(token))
    else:
        ret_dict['description'] = 'token not provided'
        return json(ret_dict)

if __name__ == '__main__':
    app.run(debug=False, port=8000, host='0.0.0.0', workers=5)
