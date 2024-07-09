from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import json

chat = ChatGroq(
    temperature=0,
    model="llama3-70b-8192",
)

human = """
This is my github data:
```json
{github_data}
```
"""
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])



chain = prompt | chat
print(chain.invoke({"github_data": github_data}).content)