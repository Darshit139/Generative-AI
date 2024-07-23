import aiohttp
import asyncio
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
import requests
import random
from packages.html_processor import HTMLProcessor
from packages.llm import LLM

class Scrape:

    def __init__(self):
        self.html_processor = HTMLProcessor()
        self.llm = LLM()

    def is_scrapable_link(self, link):
        return True

    def is_absolute(self, url):
        return bool(urlparse(url).netloc)

    def is_excluded(self, url, exclude_links):
        domain = urlparse(url).netloc
        return any(exclude in domain for exclude in exclude_links)
    
    def random_sample_links(self, links, count):
        return random.sample(links, count)

    async def scrape_main_link(self, url, exclude_links, brand_name):
        work = list(url)
        links = set()
        link_filename = f'{brand_name}/scraped_links.json'

        logging.info("Crawler starting.")

        async with aiohttp.ClientSession() as session:
            while work:
                link = work.pop()
                if self.is_scrapable_link(link):
                    html_content = await self.html_processor.fetch(session, link)
                    if html_content:
                        soup = BeautifulSoup(html_content, 'html.parser')
                        href_elements = soup.find_all('a', href=True)
                        for elem in href_elements:
                            href = elem['href']
                            if href and self.is_absolute(href) and not self.is_excluded(href, exclude_links):
                                if href != link:
                                    links.add(href)
        
        logging.info("Crawler finished.")

        with open(link_filename, 'w') as file:
            json.dump(list(links), file, indent=4)

        return list(links)

    async def scrape_summary_data(self, scraped_links, product_domain, brand_name, product_name):
        all_summary = ""
        summery_filename = f'{brand_name}/final_summary.txt'

        selected_links = self.random_sample_links(scraped_links, 7)
        selected_links.append(product_domain[0])
        print(selected_links)

        async with aiohttp.ClientSession() as session:
            for link in selected_links:
                logging.info(f"Processing link: {link}")
                html_content = await self.html_processor.fetch(session, link)
                if html_content:
                    cleaned_html = self.html_processor.clean_html(html_content)
                    if cleaned_html:
                        result =  self.llm.summarize(cleaned_html, brand_name, product_name)
                        if result:
                            all_summary += result + "\n-------\n"
                            print(f"Summary for {link}:")
                            print("=" * 50)

        final_summary = self.llm.final_summarize(all_summary, brand_name, product_name)
        print("\n\n----------------------Final Summary--------------------\n\n")
        print(final_summary)

        with open(summery_filename, 'w') as text_file:
            text_file.write(final_summary)

        print("Final summary saved to final_summary.txt")

        return final_summary
        
    async def classify_links(self, scraped_links, summary, brand_name):
        classify_filename = f"{brand_name}/classified_links.json"

        urls_string = "\n".join(scraped_links)
        classified_links = self.llm.classify_links(urls_string, summary)

        classified_links = json.loads(classified_links)
        with open(classify_filename, 'w') as f:
            json.dump(classified_links, f, indent=2)

        print("Classified links saved to classified_links.json")

        return classified_links
    
    async def generate_faqs(self, classified_links, summary, brand_name, product_name):
        faqs_list = []
        faqs_filename = f'{brand_name}/faqs.json'

        async with aiohttp.ClientSession() as session:
            for classified_link in classified_links:
                category = classified_link.get('category')
                if category in ['about', 'support']:
                    link = classified_link.get('link')
                    try:
                        html_content = await self.html_processor.fetch(session, link)
                        if html_content:
                            cleaned_html = self.html_processor.clean_html(html_content)
                            if cleaned_html:
                                faq = self.llm.faqs(cleaned_html, summary, brand_name, product_name)
                                print(faq)
                                if faq:
                                    faq = faq.replace('json', '')
                                    faq = faq.replace('```', '')
                                    faq = faq.replace('\\', '')
                                    faqs_list.extend(json.loads(faq))
                                    print(f"Link: {link}, Category: {category}")
                                    logging.info(f"Generated FAQs: {faqs_list}")

                    except aiohttp.ClientError as e:
                        logging.error(f"Error fetching HTML content for link {link}: {e}")
        
        with open(faqs_filename, 'w') as file:
            json.dump((faqs_list), file, indent=4)

        return faqs_list
    
    async def extract_products(self, classified_links, summary, brand_name):
        products_list = []
        products_filename = f'{brand_name}/all_products.json'

        async with aiohttp.ClientSession() as session:
            for classified_link in classified_links:
                category = classified_link.get('category')
                if category in ['product']:
                    link = classified_link.get('link')
                    print(f"Link: {link}, Category: {category}")
                    try:
                        html_content = await self.html_processor.fetch(session, link)
                        if html_content:
                            cleaned_html = self.html_processor.clean_html(html_content)
                            if cleaned_html:
                                try:
                                    product = self.llm.product_extrector(cleaned_html, summary, brand_name)
                                    if product:
                                        product = product.replace('json', '')
                                        product = product.replace('```', '')
                                        product = product.replace('\\', '')
                                        with open('product.txt', 'w') as text_file:
                                            text_file.write(product)
                                        logging.info(f"Link: {link}, Category: {category}")
                                        logging.info(f"Products: {product}")
                                        products_list.extend(json.loads(product))
                                except Exception as e:
                                    print("Error in product extraction:", e)
                                    logging.info("Error in product extraction:", e)

                    except aiohttp.ClientError as e:
                        logging.error(f"Error fetching HTML content for link {link}: {e}")
        
        logging.info(f"Extracted Products: {products_list}")

        with open(products_filename, 'w') as file:
            json.dump((products_list), file, indent=4)

        return products_list

    async def unique_products(self, data, brand_name):
        def calculate_length(entry):
            entry_copy = entry.copy()
            if 'description' in entry_copy:
                del entry_copy['description']
            return len(json.dumps(entry_copy))

        max_length_entries = {}
        for entry in data:
            name = entry['name']
            entry_length = calculate_length(entry)
            if name not in max_length_entries or entry_length > max_length_entries[name]['length']:
                max_length_entries[name] = {
                    'length': entry_length,
                    'entry': entry
                }

        result = [value['entry'] for value in max_length_entries.values()]

        output_file_path = f'{brand_name}/unique_products.json'
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(result, file, indent=4)
        
        logging.info(f"Processed {len(data)} entries and saved {len(result)} entries with maximum length to {output_file_path}.")

        return result

    async def extract_product_cards(self, classified_links, summary, brand_name):
        products_card_list = []
        products_filename = f'{brand_name}/all_products_card.json'

        async with aiohttp.ClientSession() as session:
            for classified_link in classified_links:
                category = classified_link.get('category')
                if category in ['product']:
                    link = classified_link.get('link')
                    try:
                        html_content = await self.html_processor.fetch(session, link)
                        if html_content:
                            cleaned_html = self.html_processor.clean_html(html_content)
                            if cleaned_html:
                                try:
                                    product_card = self.llm.product_card_extrector(cleaned_html, summary, brand_name)
                                    if product_card:
                                        product_card = product_card.replace('json', '')
                                        product_card = product_card.replace('```', '')
                                        product_card = product_card.replace('\\', '')
                                        logging.info(f"Link: {link}, Category: {category}")
                                        logging.info(f"Products Card: {product_card}")
                                        products_card_list.extend(json.loads(product_card))
                                except Exception as e:
                                    print("Error in product card extraction:", e)
                                    logging.info("Error in product card extraction:", e)
                    
                    except aiohttp.ClientError as e:
                        logging.error(f"Error fetching HTML content for link {link}: {e}")

        logging.info(f"Extracted Products Card: {products_card_list}")

        with open(products_filename, 'w') as file:
            json.dump((products_card_list), file, indent=4)

        return products_card_list

    async def unique_product_cards(self, data, brand_name):
        def calculate_length(entry):
            entry_copy = entry.copy()
            return len(json.dumps(entry_copy))

        max_length_entries = {}
        for entry in data:
            title = entry.get('title', '')
            entry_length = calculate_length(entry)
            if title not in max_length_entries or entry_length > max_length_entries[title]['length']:
                max_length_entries[title] = {
                    'length': entry_length,
                    'entry': entry
                }

        result = [value['entry'] for value in max_length_entries.values()]

        output_file_path = f'{brand_name}/unique_products_card.json'
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(result, file, indent=4)

        logging.info(f"Processed {len(data)} entries and saved {len(result)} unique entries with maximum length to {output_file_path}.")

        return result

    async def extrect_quiz(self, summary, brand_name, product_name):
        products_filename = f'{brand_name}/quiz.json'

        try:
            quiz = self.llm.quiz_extrector(summary, brand_name, product_name)

            if quiz:
                quiz = quiz.replace('json', '')
                quiz = quiz.replace('```', '')
                quiz = quiz.replace('\\', '')

                quiz = json.loads(quiz)

                with open(products_filename, 'w') as file:
                    json.dump(quiz, file, indent=4)
                
                logging.info(f"Quiz extracted and saved to {products_filename}")

        except Exception as e:
            logging.error(f"Error in quiz extraction: {e}")
            print("Error in quiz extraction:", e)

        return quiz
    
    # async def extrect_social(self, classified_links, brand_name):
    #     link_filename = f'{brand_name}/social_links.json'

    #     social_names = [
    #         "facebook",
    #         "twitter",
    #         "linkedin",
    #         "instagram",
    #         "tiktok",
    #         "spotify",
    #     ]

    #     social_links = []
    #     async with aiohttp.ClientSession() as session:
    #         for link in classified_links:
    #             logging.info(f"Processing link: {link}")
    #             try:
    #                 html_content = await self.html_processor.fetch(session, link)
    #                 if html_content:
    #                     cleaned_html = self.html_processor.clean_html(html_content)
    #                     if cleaned_html:
    #                         social = self.llm.social_extrector(brand_name, cleaned_html)
                            
    #                         if social:
    #                             social = social.replace('json', '').replace('```', '').replace('\\', '')
                                
    #                             try:
    #                                 extracted_links = json.loads(social)
    #                                 social_links.extend(extracted_links)
    #                             except json.JSONDecodeError as e:
    #                                 logging.error(f"JSON decode error for link {link}: {e}")
    #                                 print("JSON decode error:", e)

    #             except Exception as e:
    #                 logging.error(f"Error in social extraction for link {link}: {e}")
    #                 print("Error in social extraction:", e)

    #     # Filter out entries where link is '#'
    #     filtered_data = [entry for entry in social_links if entry['link'] != '#']

    #     # Remove duplicates based on 'link'
    #     unique_data = []
    #     seen_links = set()
    #     for entry in filtered_data:
    #         if entry['link'] not in seen_links:
    #             unique_data.append(entry)
    #             seen_links.add(entry['link'])

    #     # Write unique data to file
    #     with open(link_filename, 'w') as file:
    #         json.dump(unique_data, file, indent=4)

    #     logging.info(f"Social links extracted and saved to {link_filename}")
    #     return unique_data
    
    async def extrect_social(self, classified_links, brand_name,url):
        link_filename = f'{brand_name}/social_links.json'

        social_names = [
            "facebook",
            "twitter",
            "linkedin",
            "instagram",
            "tiktok",
            "spotify",
        ]

        # Initialize an empty set to store unique social media links
        socials = set()

        async with aiohttp.ClientSession() as session:
            for link in classified_links:
                try:
                    # Fetch HTML content using the provided fetch function
                    html_content = await self.html_processor.fetch(session, link)
                    if html_content:
                        # Parse the HTML content using BeautifulSoup
                        soup = BeautifulSoup(html_content, 'html.parser')

                        # Find all <a> tags
                        atags = soup.find_all('a')
                        for a in atags:
                            href = a.get('href')
                            if href and any(name in href for name in social_names):
                                print(f"Found potential social media link: {href}")
                                socials.add(href)
                except Exception as e:
                    logging.error(f"Error in social extraction for link {link}: {e}")
                    print("Error in social extraction:", e)

        logging.info("ALL Social Links got.")

        socials.add(url[0])
        social_links = "\n".join(socials)
        print(social_links)

        try:
            logging.info("LLM is calling for classification")

            extracted_links = self.llm.social_extrector(brand_name, social_links)

            if extracted_links:
                extracted_links = extracted_links.replace('json', '')
                extracted_links = extracted_links.replace('```', '')
                extracted_links = extracted_links.replace('\\', '')

                extracted_links = json.loads(extracted_links)

                with open(link_filename, 'w') as file:
                    json.dump(extracted_links, file, indent=4)

        except Exception as e:
            print("Error in social extraction:", e)
            logging.error(f"Error in social extraction: {e}")

