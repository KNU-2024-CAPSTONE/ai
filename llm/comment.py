from llm.llmKey import *

from langchain_upstage import ChatUpstage
from langchain_core.messages import HumanMessage, SystemMessage

chat = ChatUpstage(api_key=API_KEY, model="solar-pro")

request = "안녕? 오늘 대구 날씨에 대해 알려줘"

messages = [
    SystemMessage(
        content="오늘의 날씨에 대해 최고 기온, 최저 기온, 강수 확률을 알려주는 모델입니다. "
    ),
    HumanMessage(
        content=request
    )
]

response = chat.invoke(messages).content
print("질문 : " + request)
print("답변 : " + response)
