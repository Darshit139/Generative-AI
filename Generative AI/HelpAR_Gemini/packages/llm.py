import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from dotenv import load_dotenv
from .prompts import *

load_dotenv()

class LLM:
    def __init__(self):
        self.chat_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.8, max_output_tokens=8192)
    
    def summarize(self, html, brand,product):
        try:
            prompt = PromptTemplate(template=summery, input_variables=["html","brand","product"])
            chain = prompt | self.chat_llm | StrOutputParser()
            result = chain.invoke({'html': html,"brand":brand,"product":product})
            return result
        except Exception as e:
            logging.error(f'Error in LLM: {e}')

    def final_summarize(self, context,brand,product):
        try:
            prompt = PromptTemplate(template=final_summery, input_variables=["context","brand","product"])
            chain = prompt | self.chat_llm | StrOutputParser()
            result = chain.invoke({'context': context,"brand":brand,"product":product})
            return result
        except Exception as e:
            logging.error(f'Error in LLM: {e}')
    
    def classify_links(self, links,brand_context):
        try:
            prompt = PromptTemplate(template=classification, input_variables=["links","brand_context"])
            chain = prompt | self.chat_llm | StrOutputParser()
            result = chain.invoke({'links':links,'brand_context':brand_context})
            return result
        except Exception as e:
            logging.error(f'Error in LLM: {e}')

    def faqs(self, html,brand_context,brand,product):
        try:
            prompt = PromptTemplate(template=faqs, input_variables=["brand_context","html","brand","product"])
            chain = prompt | self.chat_llm | StrOutputParser()
            result = chain.invoke({'brand_context':brand_context,'context':html,"brand":brand,"product":product})
            return result
        except Exception as e:
            logging.error(f'Error in LLM: {e}')

    def product_extrector(self, html,brand_context,brand):
        try:
            prompt = PromptTemplate(template=product_extrector, input_variables=["brand_context","html","brand"])
            chain = prompt | self.chat_llm | StrOutputParser()
            result = chain.invoke({'brand_context':brand_context,'html':html,"brand":brand})
            return result
        except Exception as e:
            logging.error(f'Error in LLM: {e}')

    def product_card_extrector(self, html,brand_context,brand):
        try:
            prompt = PromptTemplate(template=product_card_extrector, input_variables=["brand_context","html","brand"])
            chain = prompt | self.chat_llm | StrOutputParser()
            result = chain.invoke({'brand_context':brand_context,'html':html,"brand":brand})
            return result
        except Exception as e:
            logging.error(f'Error in LLM: {e}')

    def quiz_extrector(self,brand_context,brand,product):
        try:
            prompt = PromptTemplate(template=quiz_extractor, input_variables=["context","brand","product"])
            chain = prompt | self.chat_llm | StrOutputParser()
            result = chain.invoke({'context':brand_context,"brand":brand,"product":product})
            return result
        except Exception as e:
            logging.error(f'Error in LLM: {e}')
    
    def social_extrector(self,brand,links):
        try:
            prompt = PromptTemplate(template=social_extrector_2, input_variables=["brand","html"])
            chain = prompt | self.chat_llm | StrOutputParser()
            result = chain.invoke({"brand":brand,"html":links})
            return result
        except Exception as e:
            logging.error(f'Error in LLM: {e}')
    
    
    