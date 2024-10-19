import json
import score_weight

#langchain 및 vectorDB 관련 import
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from pathlib import Path

def tupleToDictionary(product):
   dictionary = {
      "productName":product[0],
      "averageStarcount":product[1],
      "review":product[2],
      "postDate":product[3]
      }
   
   return dictionary

def dictionaryToTuple(product, score):
   return (product.get("productName"), product.get("averageStarcount"), product.get("review"), product.get("postDate"), score)

# productList는 (productName, averageStarCount, review, postDate) 순서로 데이터 받음(튜플 형태)
# shoppingMallName을 통해 각 쇼핑몰별 vectorDB 구별
# update = True일 시 productList로 vectorDB 업데이트
def loadVectorDB(productList, shoppingMallName, update=False):
    folder_path = Path("faiss_db/"+shoppingMallName)
    file_path = folder_path / f"{shoppingMallName}.index"

    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)

    hf = HuggingFaceEmbeddings(model_name='jhgan/ko-sroberta-multitask')

    # productList에서 productName만 추출하여 임베딩
    productNames = [product[0] for product in productList]
    productDictionary = [tupleToDictionary(product) for product in productList]

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


def findSimilarProduct(product, vectorstore, k=4):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2*k, "return_score": True})

    results = retriever.invoke(product)
    
    # 첫 번째는 자신을 가지므로 제외
    results.pop(0)
    
    # 원본 제품 데이터 찾기
    similarProducts = []
    
    for result in results:
        data = dictionaryToTuple(result.metadata, result.score)
        similarProducts.append(data)

    return similarProducts

def main():
    print("Hello World.")
  



if __name__ == "__main__":
	main()