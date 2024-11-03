from outflux.outflux import *
from product_recommand.vector_db import *

from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

@app.route('/api/ai/outflux', methods=['POST'])
def outfluxAPI():
    #Header 추출
    headers = request.headers
    lastPurchase = 6 if headers.get('lastPurchase') is None else headers.get('lastPurchase')
    purchaseWithCategory = 3 if headers.get('purchaseWithCategory') is None else headers.get('purchaseWithCategory')
    refundPercent = 50 if headers.get('refundPercent') is None else headers.get('refundPercent')
    number = 5 if headers.get('number') is None else headers.get('number')

    #Body 추출
    purchaseJson = request.get_json()
    result = distinctCoupon(purchaseJson=purchaseJson, lastPurchase=lastPurchase, purchaseWithCategory=purchaseWithCategory, number=number)
    response = make_response(jsonify(result))
    response.status_code = 200

    return response

@app.route('/api/ai/product-recommand', methods=['POST'])
def productRecommandAPI():
    # Body 추출
    bodyJson = request.get_json()

    if bodyJson and "productList" in bodyJson: productJson = bodyJson.get("productList")
    else: productJson = None
        
    shoppingMallName = bodyJson.get('shoppingMallName')
    product = bodyJson.get('product')

    if bodyJson and "isReview" in bodyJson: isReview = bodyJson.get('isReview')
    else: isReview = True

    if bodyJson and "isStarCount" in bodyJson: isStarCount = bodyJson.get('isStarCount')
    else: isStarCount = True
    
    if bodyJson and "isPostDate" in bodyJson: isPostDate = bodyJson.get('isPostDate')
    else: isPostDate = True

    if bodyJson and "k" in bodyJson: k = bodyJson.get('k')
    else: k = 4

    result = productRecommand(productJson, shoppingMallName, product, k, isReview, isStarCount, isPostDate)
    response = make_response(jsonify([prod.to_dict() for prod in result]))
    response.status_code = 200

    return response

if __name__ == '__main__':
    app.run(debug=True)