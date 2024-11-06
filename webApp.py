from outflux.outflux import *
from product_recommand.vector_db import *

from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

@app.route('/api/ai/outflux', methods=['POST'])
def outfluxAPI():
    #Body 추출
    body = request.get_json()

    if body and "lastPurchase" in body: lastPurchase = body.get('lastPurchase')
    else: lastPurchase = 6

    if body and "purchaseWithCategory" in body: purchaseWithCategory = body.get('purchaseWithCategory')
    else: purchaseWithCategory = 3

    if body and "refundPercent" in body: refundPercent = body.get('refundPercent')
    else: refundPercent = 50

    if body and "number" in body: number = body.get('number')
    else: number = 5

    purchaseJson = body.get('purchaseLog')

    result = distinctCoupon(purchaseJson=purchaseJson, lastPurchase=lastPurchase, purchaseWithCategory=purchaseWithCategory, number=number, refundPercent=refundPercent)
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
    app.run()