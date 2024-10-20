from datetime import datetime

class Product:
    def __init__(self, productName, averageStarCount, review, postDate):
        self.productName = productName
        self.averageStarCount = averageStarCount
        self.review = review
        self.postDate = postDate
        self.score = 0

    # 평균 별점에 따른 가중치 계산
    def addStarPointScore(self):
        if self.averageStarCount < 1:
            self.score = self.score * 0.9
        elif self.averageStarCount < 2:
            self.score = self.score * 0.95
        elif self.averageStarCount < 3:
            self.score = self.score
        elif self.averageStarCount < 4:
            self.score = self.score * 1.05
        else:
            self.score = self.score * 1.1

    # 리뷰수에 따른 가중치 계산
    def addReviewCountScore(self):
        if self.review <= 100:
            self.score = self.score
        elif self.review <= 1000:
            self.score = self.score * 1.05
        else:
            self.score = self.score * 1.1

    # 제품 등록일에 따른 가중치 계산
    def addPostDateScore(self):
        today = datetime.now().date()
        daysDifference = (today - self.postDate).days

        if daysDifference < 7:
            self.score = self.score * 1.15
        elif daysDifference < 30:
            self.score = self.score * 1.1
        elif daysDifference < 100:
            self.score = self.score * 1.05