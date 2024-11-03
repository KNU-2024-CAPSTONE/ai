import random
import string
from datetime import datetime

class Product:
    def __init__(self, category, name, price):
        self.category = category
        self.name = name
        self.price = price

# (email, gender, age, product(category, name, price), quantity, starCount, totalPrice, purchaseTime, isRefund)
class PurchaseLog():
    def __init__(self, email, gender, age, product, quantity, starCount, totalPrice, purchaseTime, isRefund):
        self.email = email
        self.gender = gender
        self.age = age
        self.product = product
        self.quantity = quantity
        self.starCount = starCount
        self.totalPrice = totalPrice
        self.purchaseTime = purchaseTime
        self.isRefund = isRefund

def parseJsonToPurchaseLogClass(data):
    purchaseLogs = []
    for item in data:
        productInfo = item["product"]
        product = Product(
            category=productInfo["category"],
            name=productInfo["name"],
            price=productInfo["price"]
        )

        purchaseLog = PurchaseLog(
            email=item["email"],
            gender=item["gender"],
            age=item["age"],
            product=product,
            quantity=item["quantity"],
            starCount=item["starCount"],
            totalPrice=item["totalPrice"],
            purchaseTime=datetime.strptime(item["purchaseTime"], '%Y-%m-%dT%H:%M:%S'),
            isRefund=item["isRefund"]
        )
        purchaseLogs.append(purchaseLog)

    return purchaseLogs

class Coupon():
    def __init__(self, category, code, discount):
        self.category = category
        self.code = code
        self.discount = discount

    def to_dict(self):
        return {
            "category": self.category,
            "code": self.code,
            "discount": self.discount
        }

def generateCoupon(length=12):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

# 쿠폰의 발급 유무를 판단, 발급 시 (category, code, disCountPercent)를 리턴하고, 아닐 경우 None을 리턴한다.
def distinctCoupon(purchaseJson, lastPurchase = 6, purchaseWithCategory = 3, refundPercent = 50, number = 5):
    purchaseLogList = parseJsonToPurchaseLogClass(purchaseJson)

    # 최근 1개월동안 환불 여부 확인을 위한 변수
    month1 = 0
    refundCount = 0
    # 최근 3개월동안 카테고리별 구매 횟수를 확인하기 위한 dictionary
    month3 = dict()
    # 최근 6개월동안 이용 내역을 확인하기 위한 변수
    isExit = False
    
    #purchaseLogList 값을 하나씩 탐색하며 조건 확인
    for purchaseLog in purchaseLogList:
        daysDifference = (datetime.now() - purchaseLog.purchaseTime).days

        if daysDifference < 30:
            month1 = month1 + 1
            if purchaseLog.isRefund: refundCount = refundCount + 1
        if daysDifference < purchaseWithCategory * 30:
            if not purchaseLog.isRefund:
                key = purchaseLog.product.category
                if key in month3:
                    month3[key] = month3[key] + 1
                else:
                    month3[key] = 1
        if daysDifference < lastPurchase * 30:
            isExit = True
    
    # 6개월 동안(default) 구매기록이 없을 경우 15%(default) 쿠폰 발급
    if not isExit:
        return Coupon(None, generateCoupon(), 15).to_dict()
    # 1개월 동안 5번 이상 구매, 절반 이상(default)이 환불일 경우 10% 쿠폰 발급
    if month1 != 0 and (refundCount // month1) * 100 >  refundPercent and month1 > 5:
        return Coupon(None, generateCoupon(), 10).to_dict()
    
    # dictionary를 순차 탐색하며 3개월 동안(default) 5회 이상(default) 구매한 카테고리의 10% 쿠폰 발급
    for key, value in month3.items():
        if value >= number:
            return Coupon(key, generateCoupon(), 10).to_dict()
    
    return None