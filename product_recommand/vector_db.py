import json
from score_weight import *

#langchain 및 vectorDB 관련 import
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from pathlib import Path

# productList는 Product 클래스(productName, averageStarCount, review, postDate) 순서로 데이터 받음
# shoppingMallName을 통해 각 쇼핑몰 별 vectorDB 구별
# update = True일 시 productList로 vectorDB 업데이트
def loadVectorDB(productList, shoppingMallName, update=False):
    folder_path = Path("faiss_db/"+shoppingMallName)
    file_path = folder_path / f"{shoppingMallName}.index"

    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)

    hf = HuggingFaceEmbeddings(model_name='jhgan/ko-sroberta-multitask')

    # productList에서 productName만 추출하여 임베딩
    productNames = [product.productName for product in productList]
    productDictionary = [product.__dict__ for product in productList]

    # 벡터 db가 현재 존재하지 않거나, 요청할 때 제품 목록을 업데이트 해야하는 경우에만 새로운 벡터 db 생성
    if not file_path.exists() or update:  
        # productName을 임베딩하여 인덱스를 생성
        vectorstore = FAISS.from_texts(texts=productNames, embedding=hf, metadatas=productDictionary)
        
        # 인덱스 저장
        vectorstore.save_local(folder_path=str(folder_path), index_name=shoppingMallName)
    else:
        vectorstore = FAISS.load_local(folder_path=folder_path, 
                                    index_name=shoppingMallName, 
                                    embeddings=hf, 
                                    )

    return vectorstore

# k는 반환할 유사한 제품의 개수, isReview, isStarCount, isPostDate는 각각 리뷰 수, 별점, 등록일을 점수에 반영할 지의 여부를 결정, 기본값은 True
def findSimilarProduct(product, vectorstore, k=4, isReview = True, isStarCount = True, isPostDate = True):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2*k})

    results = retriever.invoke(product)
    
    # 첫 번째는 자신을 가지므로 제외
    results.pop(0)
    
    # 원본 제품 데이터 찾기
    similarProducts = []
    
    for result in results:
        data = result.metadata
        newProduct = Product(data["productName"], data["averageStarCount"], data["review"], data["postDate"])
        if isReview:
            newProduct.addReviewCountScore()
        if isStarCount:
            newProduct.addStarPointScore()
        if isPostDate:
            newProduct.addPostDateScore()
            
        similarProducts.append(newProduct)

    similarProducts.sort(key=lambda p:(-p.score))
    
    return similarProducts[0:k]

def main():
    print("Hello World.")
  



if __name__ == "__main__":
	main()