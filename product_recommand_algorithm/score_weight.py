from datetime import datetime

# 평균 별점에 따른 가중치 계산, product_list는 (productName, averageStarCount, review, postDate, score) 순서로 데이터 받음(튜플 형태)
def addStarPointScore(product_list):
    for product in product_list:
        averageStarCount = product[1]
        score = product[4]
        if averageStarCount < 1:
            product[4] = score * 0.9
        elif averageStarCount < 2:
            product[4] = score * 0.95
        elif averageStarCount < 3:
            product[4] = score
        elif averageStarCount < 4:
            product[4] = score * 1.05
        else:
            product[4] = score * 1.1

# 리뷰수에 따른 가중치 계산, product_list는 (productName, averageStarCount, review, postDate, score) 순서로 데이터 받음(튜플 형태)
def addReviewCountScore(product_list):
    for product in product_list:
        review = product[2]
        score = product[4]
        if review <= 100:
            product[4] = score
        elif review <= 1000:
            product[4] = score * 1.05
        else:
            product[4] = score * 1.1

# 제품 등록일에 따른 가중치 계산, product_list는 (productName, averageStarCount, review, postDate, score) 순서로 데이터 받음(튜플 형태)
def addPostDateScore(product_list):
    for product in product_list:
        postDate = product[3]
        score = product[4]
        today = datetime.now().date()

        daysDifference = (today - postDate).days
        if daysDifference < 7:
            product[4] = score * 1.15
        elif daysDifference < 30:
            product[4] = score * 1.1
        elif daysDifference < 180:
            product[4] = score * 1.05