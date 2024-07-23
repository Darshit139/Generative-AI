import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from dotenv import load_dotenv
from .prompts import *
import aiohttp, asyncio

load_dotenv()

class HTMLProcessor:
    def __init__(self):
        self.TAG_REMOVAL_LIST = ['style', 'script', 'video', 'audio', 'link', 'meta']

    async def fetch(self, session, url):
        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                return await response.text()
        except aiohttp.ClientError as e:
            logging.error(f"Error fetching {url}: {e}")
            return None
        except asyncio.TimeoutError:
            logging.error(f"Timeout error fetching {url}")
            return None

    # def fetch_html_content(self, url):
    #     try:
    #         response = requests.get(url)
    #         response.raise_for_status()
    #         return response.content
    #     except requests.exceptions.RequestException as e:
    #         logging.error(f"Error fetching {url}: {e}")
    #         return None

    def clean_html(self, html_content):
        if not html_content:
            return None
        
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove specified tags
        for tag in self.TAG_REMOVAL_LIST:
            for elem in soup.find_all(tag):
                elem.decompose()

        # Remove inline style attributes
        for elem in soup.find_all(True):
            if elem.has_attr('style'):
                del elem['style']

        return soup.prettify()
    
    
