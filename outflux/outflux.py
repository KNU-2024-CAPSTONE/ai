import random
import string
from datetime import datetime

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

def generateCoupon(length=12):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

# 쿠폰의 발급 유무를 판단, 발급 시 (category, code, disCountPercent)를 리턴하고, 아닐 경우 None을 리턴한다.
def distinctCoupon(purchaseLogList):
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
        if daysDifference < 90:
            if not purchaseLog.isRefund:
                key = purchaseLog.product.category
                if key in month3:
                    month3[key] = month3[key] + 1
                else:
                    month3[key] = 1
        if daysDifference < 180:
            isExit = True
    
    # 6개월 동안 구매기록이 없을 경우 15%(default) 쿠폰 발급
    if isExit:
        return None, generateCoupon(), 15
    # 1개월 동안 5번 이상 구매, 절반 이상이 환불일 경우 10%(default) 쿠폰 발급
    if refundCount > month1 // 2 and month1 > 5:
        return None, generateCoupon(), 10
    
    # dictionary를 순차 탐색하며 3개월 동안 5회 이상 구매한 카테고리의 10%(default) 쿠폰 발급
    for key, value in month3.items():
        if value >= 5:
            return key, generateCoupon(), 10
    
    return None