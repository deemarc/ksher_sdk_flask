from flask import Flask, request, jsonify
from ksher_pay_sdk import KsherPay
import os
import json

app = Flask(__name__)

mch_code = '35005'
product_name= 'marc-TestApi'

ksher_pay = KsherPay(appid='mch'+ mch_code , privatekey='./Mch'+mch_code+'_PrivateKey.pem', pubkey='./ksher_pubkey.pem')
host = 'https://5b27b3d4319a.ngrok.io'


@app.route('/')
def homepage():
    return "Hello"

@app.route('/api/gateway_pay/fail/')
def gateway_pay_fail():
    data = {
        'text': 'fail',
        'user': 'It\'s me Ada'
    }
    return jsonify(data)

@app.route('/api/gateway_pay/success/',methods=['POST','GET'])
def gateway_pay_success():
    content = request.json
    print('gateway_pay_success: ', content)
    data = {
        'text': 'success',
        'user': 'It\'s me Ada'
    }
    return jsonify(data)

@app.route('/api/order_query/',methods=['GET'])
def order_query():
    content = request.json
    response = ksher_pay.order_query(**{
        'mch_order_no':content["mch_order_no"],
        'ksher_order_no':content["ksher_order_no"],
        'channel_order_no':'alipay,linepay,airpay,wechat,bbl_promptpay,truemoney'
    })
    print(response)
    return response

@app.route('/api/gateway_order_query/',methods=['GET'])
def gateway_order_query():
    content = request.json
    #:param kwargs:
    #{"mch_order_no": "808"}
    response = ksher_pay.gateway_order_query(**{
        'mch_order_no': content["mch_order_no"]
    })
    print(response)
    return response

@app.route('/api/quick_pay/',methods=['POST'])
def quick_pay():
    content = request.json

    response = ksher_pay.quick_pay(**{
        'mch_order_no': content['mch_order_no'],
        'total_fee': content['total_fee'],
        'fee_type': content['fee_type'],
        'auth_code':content['auth_code'],
        'channel': content['channel']
    })
    print("response",response)
    return response

@app.route('/api/gateway_pay/',methods=['POST'])
def gateway_pay():
    content = request.json
    #:param kwargs:
    # {   "mch_order_no": "1101",
    #     "total_fee": "900",
    #     "fee_type": "THB",
    #     "channel_list": "alipay,linepay,airpay,wechat,bbl_promptpay,truemoney,ktbcard",
    #     "device": "H5"
    # }
    response = ksher_pay.gateway_pay(**{
        'mch_order_no': content['mch_order_no'],
        'total_fee': content['total_fee'],
        'fee_type': content['fee_type'],
        'channel_list': content['channel_list'],
        'mch_code': mch_code,
        'mch_redirect_url': host+'api/gateway_pay/success',
        'mch_redirect_url_fail': host+'api/gateway_pay/fail',
        'refer_url': host,
        'product_name': product_name,
        # 'device': content['device'],
        'lang':"th",
        'expire_time': 10
    })
    print("response",response)
    return response

@app.route('/api/native_pay/',methods=['GET', 'POST'])
def native_pay():
    content = request.json
    response = ksher_pay.native_pay(**{
        'mch_order_no': content['mch_order_no'],
        'total_fee': content['total_fee'],
        'fee_type': 'THB',
        'channel': content['channel'],
        'notify_url': host+'api/gateway_pay/success',
        'device_id':""
    })
    print(response)
    return response

@app.route('/api/order_refund/',methods=['GET', 'POST'])
def order_refund():
    content = request.json
    response = ksher_pay.order_refund(**{
        'total_fee': content['total_fee'],
        'fee_type': 'THB',
        'refund_fee': content['total_fee'],
        'mch_refund_no': content['mch_refund_no'],
        'ksher_order_no': content['ksher_order_no']
    })
    print(response)
    return response

@app.route('/api/refund_query/',methods=['GET', 'POST'])
def refund_query():
    response = ksher_pay.refund_query(**{
        'mch_refund_no':'',
        'ksher_refund_no':'',
        'channel_refund_no':'',
        'mch_order_no':'',
        'ksher_order_no':'',
        'channel_order_no':''
    })
    print(response)
    return response

@app.route('/api/app_pay/',methods=['GET', 'POST'])
def app_pay():
    content = request.json
    response = ksher_pay.app_pay(**{
        "channel": content['channel'],
        "fee_type": content['fee_type'],
        "mch_order_no": content['mch_order_no'],
        "notify_url": "https://ht.dspread.com/weixin/dev6/NativepayApp/pay_notify",
        "local_total_fee": content['local_total_fee'],
        "product": "goodName",
        "refer_url": "https://www.baidu.com/"
    })
    print(response)
    return response

@app.route('/api/order_close/',methods=['GET', 'POST'])
def order_close():
    content = request.json
    response = ksher_pay.order_close(**{
        'mch_order_no':content["mch_order_no"],
        'ksher_order_no':content["ksher_order_no"],
        'channel_order_no':content["channel_order_no"]
    })
    print(response)
    return response

if __name__== '__main__':
    app.run(port=5000)
