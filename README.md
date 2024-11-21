# ai
종합설계프로젝트1 ai 레포지토리
5000번 포트를 사용한다.

POST /api/ai/outflux

Request Body
- purchaseLog : 구매 기록(필수)
- lastPurchase : 마지막 월단위 구매 일자(선택)
- lastRefund : 마지막 월단위 환불 일자(선택)
- refundPercent : 환불 비율(선택)
- purchaseWithCategory : 카테고리별 월단위 구매 일자(선택)
- purchaseNumber : 환불 횟수(선택)


Response Body

쿠폰 발급 된 경우
- category : 적용가능한 카테고리, null일 경우 전체 카테고리
- code : 쿠폰 코드, 12자리 숫자 및 영어 대문자 혼합
- discount : 할인 비율, 0 ~ 100 사이의 정수

쿠폰 발급되지 않은 경우(해당 안될 경우)
- null

예시)
Request Body
'''
{
    "purchaseLog":[{
        "email": "user3@example.com",
        "gender": "male",
        "age": 32,
        "product": {
            "category": "차량 서비스",
            "name": "실리 스 유리발수 코팅(S40) 전면유리",
            "price": 80000
        },
        "quantity": 4,
        "starCount": 5,
        "totalPrice": 320000,
        "purchaseTime": "2024-01-27T13:44:46",
        "isRefund": true
    },
    {
        "email": "user3@example.com",
        "gender": "male",
        "age": 32,
        "product": {
            "category": "차량 트레이",
            "name": "멀티 트레이, 아이오닉 5 (NE/NE PE)",
            "price": 85000
        },
        "quantity": 5,
        "starCount": 1,
        "totalPrice": 425000,
        "purchaseTime": "2024-01-29T16:36:04",
        "isRefund": true
    },
    {
        "email": "user3@example.com",
        "gender": "male",
        "age": 32,
        "product": {
            "category": "디저트 세트",
            "name": "부드러운 디저트 세트 아이스 카페 아메리카노 T 2잔＋부드러운 생크림 카스텔라",
            "price": 12000
        },
        "quantity": 2,
        "starCount": 4,
        "totalPrice": 24000,
        "purchaseTime": "2024-01-15T11:20:30",
        "isRefund": true
    },
    {
        "email": "user3@example.com",
        "gender": "male",
        "age": 32,
        "product": {
            "category": "차량 서비스",
            "name": "포터 차바닥 시공 서비스 초장축 더블캡",
            "price": 450000
        },
        "quantity": 3,
        "starCount": 1,
        "totalPrice": 1350000,
        "purchaseTime": "2024-01-26T20:31:07",
        "isRefund": true
    },
    {
        "email": "user3@example.com",
        "gender": "male",
        "age": 32,
        "product": {
            "category": "차량 액세서리",
            "name": "TPE 트렁크매트",
            "price": 65000
        },
        "quantity": 1,
        "starCount": 4,
        "totalPrice": 65000,
        "purchaseTime": "2024-01-03T18:49:08",
        "isRefund": true
    },
    {
        "email": "user3@example.com",
        "gender": "male",
        "age": 32,
        "product": {
            "category": "아이스크림",
            "name": "하프갤론 아이스크림",
            "price": 18000
        }, ...
    ],
    "lastPurchase":6,
    "purchaseWithCategory":3,
    "refundPercent":50,
    "lastRefund":3,
    "purchaseNumber":5
}
'''

Response Body
'''
{
    "category": "차량 매트",
    "code": "6LR2C17XOQT5",
    "discount": 10
}
'''
  
POST /api/ai/product-recommand

Request Body
- productList : 제품 목록(선택)
- shoppingMallName : 쇼핑몰 이름(필수)
- product : 구매한 제품(필수)
- isReview : 점수에 리뷰 포함할 지 여부(선택)
- isStarCount : 점수에 평균 별점 포함할 지 여부(선택)
- isPostDate : 점수에 상품 등록일 포함할 지(선택)
- k : 반환할 유사한 상품 개수(선택)

Response Body
- productList : 유사한 상품 목록

예시)
Request Body
'''
{
    "productList":[
        {"productName": "DYSON 슈퍼소닉 HD15 블루코퍼(케이스 내장)", "averageStarCount": 3, "review": 222, "postDate": "2024-11-06"}
        ,
        {"productName": "BLDC 차량용 핸디형 무선 청소기 플러스", "averageStarCount": 5, "review": 462, "postDate": "2024-11-06"}
        ,
        {"productName": "DYSON 무선청소기 V8 실버/레드", "averageStarCount": 0, "review": 952, "postDate": "2024-11-06"}
        ,...
    ],
    "product":"허니콤보",
    "shoppingMallName":"hyundai",
    "isReview":true,
    "isStarCount":true,
    "isPostDate":true,
    "k":4
}
'''

Response Body
'''
[
    {
        "averageStarCount": 5,
        "postDate": "2024-11-06",
        "productName": "뿌링클 콤보＋치즈볼＋콜라1.25L",
        "review": 7,
        "score": 125
    },
    {
        "averageStarCount": 3,
        "postDate": "2024-11-06",
        "productName": "반반콤보＋콜라1.25L",
        "review": 773,
        "score": 120
    },
    {
        "averageStarCount": 2,
        "postDate": "2024-11-06",
        "productName": "허니오리지날＋레드오리지날＋콜라1.25L",
        "review": 940,
        "score": 115
    },
    {
        "averageStarCount": 2,
        "postDate": "2024-11-06",
        "productName": "교촌콤보＋콜라1.25L",
        "review": 166,
        "score": 115
    }
]
'''
