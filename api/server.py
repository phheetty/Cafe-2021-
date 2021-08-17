#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import *



@app.route("/api/test",methods=["GET"])
def auth_gen():
    try:
        result = {'status':"OK",'message':"Running"}
        # data = request.json
        # if 'taxid' in data:
        #     encode_taxid = generate_authorize(data['taxid'])
        #     if encode_taxid['status'] == 'OK':
        #         data = json.dumps(data)
        #         encode_data = auth_encode(data)
        #         result = {'status':"OK",'access_token': encode_taxid['message'],'data': encode_data}
        #         return jsonify(result),200
        #     else:
        #         return jsonify(encode_taxid),401
        # else:
        #     result = {'status':"ER",'message': 'data incorrect'}
        #     return jsonify(result),401
        return jsonify(result),200
    except Exception as e:
        result = {
            "status":"ER",
            "errorMessage":str(e),
            "errorCode":"ER999"
        }
        return jsonify(result),500
