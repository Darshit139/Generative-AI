import json
import logging
import os
import asyncio
import configparser
from packages.scrape import Scrape

# Setup logging configuration
log_file_path = 'webhook.log'
config = configparser.ConfigParser()
config.read('C:\\Users\\darshitp\\Desktop\\HelpAR_Gemini\\companies.ini')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', handlers=[
    logging.FileHandler(log_file_path, encoding='utf-8'),
    logging.StreamHandler()
])

async def main():
    scrape = Scrape()
    
    for section in config.sections():
        if "company" in section:

            urls_to_scrape = config[section]['domain'].strip("[]").replace("'", "").split(',')
            name = config[section]['name']
            product = config[section]['product']

            if not os.path.exists(name):
                os.makedirs(name)

            exclude_domains = ['facebook.com', 'youtube.com', 'twitter.com', 'linkedin.com']

            logging.info("Starting main process.")

            # Check if scraped_links.json already exists
            if not os.path.exists(f'{name}/scraped_links.json'):
                scraped_links = await scrape.scrape_main_link(urls_to_scrape, exclude_domains, name)
                logging.info(f"Links saved")
            else:
                with open(f'{name}/scraped_links.json', 'r') as file:
                    scraped_links = json.load(file)

            if not os.path.exists(f'{name}/final_summary.txt'):
                summary = await scrape.scrape_summary_data(scraped_links, urls_to_scrape, name, product)
                logging.info(f"Summary saved to file")
            else:
                with open(f'{name}/final_summary.txt', 'r') as file:
                    summary = file.read()

            if not os.path.exists(f'{name}/classified_links.json'):
                classified_links = await scrape.classify_links(scraped_links, summary, name)
                logging.info(f"Links are classified and saved to file")
            else:
                with open(f'{name}/classified_links.json', 'r') as file:
                    classified_links = json.load(file)

            if not os.path.exists(f'{name}/faqs.json'):
                faqs = await scrape.generate_faqs(classified_links, summary, name, product)
                logging.info(f"FAQs saved to file")
            else:
                with open(f'{name}/faqs.json', 'r') as file:
                    faqs = json.load(file)

            if not os.path.exists(f'{name}/all_products.json'):
                all_products = await scrape.extract_products(classified_links, summary, name)
                products = await scrape.unique_products(all_products, name)
                logging.info(f"Unique products saved to files")
            else:
                if not os.path.exists(f'{name}/unique_products.json'):
                    with open(f'{name}/all_products.json', 'r') as file:
                        all_products = json.load(file)

                    products = await scrape.unique_products(all_products, name)
                    logging.info(f"Unique products saved to files")
                else:
                    with open(f'{name}/unique_products.json', 'r') as file:
                        products = json.load(file)

            if not os.path.exists(f'{name}/all_products_card.json'):
                all_products_card = await scrape.extract_product_cards(classified_links, summary, name)
                products_card = await scrape.unique_product_cards(all_products_card, name)
                logging.info(f"Unique products card saved to files")
            else:
                if not os.path.exists(f'{name}/unique_products_card.json'):
                    with open(f'{name}/all_products_card.json', 'r') as file:
                        all_products_card = json.load(file)

                    products_card = await scrape.unique_product_cards(all_products_card, name)
                    logging.info(f"Unique products card saved to files")
                else:
                    with open(f'{name}/unique_products_card.json', 'r') as file:
                        products_card = json.load(file)

            if not os.path.exists(f'{name}/quiz.json'):
                quiz = await scrape.extrect_quiz(summary, name, product)
            else:
                with open(f'{name}/quiz.json', 'r') as file:
                    quiz = json.load(file)

            if not os.path.exists(f'{name}/social_links.json'):
                links = [item['link'] for item in classified_links]
                social = await scrape.extrect_social(links, name,urls_to_scrape)
            else:
                with open(f'{name}/social_links.json', 'r') as file:
                    social = json.load(file)

            logging.info("Main process completed.")

if __name__ == "__main__":
    asyncio.run(main())
