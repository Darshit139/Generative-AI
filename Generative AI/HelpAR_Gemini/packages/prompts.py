summery = """
Context: You are an expert HTML scraper. You excel at deriving structured JSON data from
relative unstructured HTML. I'm going to give you unstructured HTML and I want you to produce the example output, possible.
The name of the brand is '{brand}'.

Request: I need you to parse the given file of HTML and extract a 'brand summary'. A 'brand summary' is
a corpus of text that describes the brand in general: what the brand is, how the brand operates, what
type of products the brand offers, and any other relevant information about the brand that a customer of
the brand might want to know.The 'brand summary' should also include information about the given product.
The product in question is '{product}'.

Constraints and parameters: You should always be able to derive a brand summary from the unstructured text
you're given. Please make the brand summary 5 sentences long - no longer, no shorter. If you cannot derive a
brand summary from the given HTML, you should just return an this string "HTML can not extrect". Do not include any other text or
output other than either the full 5-sentence brand summary, or the empty string (if you cannot derive a brand
summary). In addition to making the output length 5 sentences, please also make it at least 200 words.

Your input is:

```html
{html}
```
"""

final_summery = """
Context: You are an expert at describing ecommerce brands. You excel at deriving a concise summary about
what a particular brand is, what the brand does, and how the brand's products work. I'm going to give you
a combination of brand summaries, and I want you to summarize all of these summaries into a single summary.
Each of these summaries are 5 sentences long, and you should be able to derive a single 5-sentence summary that
encompasses all of the given summaries. The summaries are about the same brand, but they may contain different
information. The brand in question is '{brand}'.The product in question is '{product}'

Request: I need you to parse the given text and aggregate the brand summaries into a single 5-sentence summary.

Constraints and parameters: You should always be able to derive a brand summary from the given text. Please make
sure that your output is exactly 5 sentences long - no longer, no shorter. You should always be able to derive a
brand summary from the given text.

The context of brand summaries is:

```text
{context}
``
"""

classification = """
Context: You're an expert HTTP link classifier. You excel at categorizing links based on content that you believe
may be able to be found inside the webpage at this link. Here is a summary of the brand, and please use this context
when considering which categories to place each link into: '{brand_context}'.

Constraints and parameters are: Please only assign each link you're given to one of the categories provided below.
Do not include any other text or output other than the JSON array, and do not include the back ticks or the `json` keyword - only the raw array.

The link categories are:
 - product: A link that might potentially have product information in the page's HTML source code.
 - about: A link that might potentially have information about the brand or company (e.g., what the
    company does, how the company works, what the product does, or how the product works), in the page's HTML source code.
 - support: A link that might potentially have support with regard to contacting the brand or getting support
    information regarding the product, in the page's HTML source code.
 - other: A link that doesn't fit into any of the other categories.

The links in question are: '{links}'

Example output:

[
  {{
    "link": "https://mysite.com/",
    "category": "about"
  }},
  {{
    "link": "https://mysite.com/products/all",
    "category": "product"
  }},
  {{
    "link": "https://mysite.com/products/some-product-name",
    "category": "product"
  }},
  {{
    "link": "https://mysite.com/about",
    "category": "about"
  }},
  {{
    "link": "https://mysite.com/support",
    "category": "support"
  }},
  {{
    "link": "https://mysite.com/contact",
    "category": "support"
  }}
]
"""

faqs = """
Context: You are an expert HTML scraper. You excel at deriving structured JSON data from
relative unstructured HTML. I'm going to give you unstructured HTML and I want you to produce the example output, possible.
The name of the brand is '{brand}', and the product in question is '{product}'. Here is a summary
of the brand, and please use this context to create the quiz: '{brand_context}'.

Request: I want you to generate a set of FAQs using the given context. An FAQ is a list of questions
and answers that are commonly asked by customers about a product or brand. The FAQ should be a JSON
object with the following properties: 'question' and 'answer'. The 'question' property should be a
question that could be composed based on the context you're given. The 'answer' property should be the
answer to the question.


Constraints and parameters: Both the question and the answer for the FAQ should be a single sentence. There
might not be explicit questions and answers in the context you're given but your task is to derive
hypothetical questions and answers based on the context. The output should be a JSON array of objects,
where each object has the 'question' and 'answer' properties. If there are actual FAQs located on the page,
then please use all of those FAQs. However, if there are no clear FAQs on the page, please do your best using the
context to create at least 1 FAQ, and at most 5 FAQs. Again, if there are clear and obvious FAQs on the page, please
include all of these FAQs, not just 1-5. Do not include any other text or output other than
the JSON array, and do not include the back ticks or the `json` keyword - only the raw array.

Your context for creating the FAQ is:

```text
{context}
```

Example output:

[
  {{
    "question": "What is the return policy for the brand?",
    "answer": "We offer a 30-day return policy on all products."
  }},
  {{
    "question": "How long does shipping take?",
    "answer": "Shipping typically takes 3-5 business days."
  }},
  {{
    "question": "What is the brand's customer service number?",
    "answer": "You can reach our customer service team at 1-800-555-1234."
  }}

  // insert other FAQs as you find them
]
"""
product_extrector = """
Context: You are an expert HTML scraper. You excel at deriving structured JSON data from
relative unstructured HTML. I'm going to give you unstructured HTML and I want you to produce the example output, possible.
The name of the brand is '{brand}'. Here is a summary of the brand, and please use this
context to create the quiz: '{brand_context}'.

Request: I  need you to parse the given file of HTML and extract any all fully formed products
that might be contained in the page. The products should be returned in a JSON array, where
each object in the array has the following properties: 'name', 'image_url', 'images', 'price',
'source', 'description', 'link', 'metadata', and 'tags'. The 'name' property is the name of the
product. The 'image_url' property is the URL to the main image of the product. The 'images' property
is an array of URLs to additional images of the product. Note that the 'image' property is always
the first image in the 'images' array. The 'price' property is the price of the product. The 'source'
will always be 'ai'. The 'description' property is a description of the product. The 'link' property
is the URL to the product page. The 'metadata' property is an object containing any additional metadata
about the product. The 'tags' property is an array of strings that represent tags for the product. Please
attempt to find all fields for each product, but if a field is not found, you should return `null` for that
field. Note that the a product may or may not be able to be found on the page - if you derive a product and
the 'price' field is `null` or the 'name' field is `null`, you should not include that product in the output
because there is a high probability that it is not a valid product.

Constraints and parameters: It's important to remember that there may or may not be products contained in the
raw HTML you're given. If you finish parsing the HTML and all property values for an object are `null`, then
this is most likely not a real product. You must include a description for the product, and if you can't find one
directly mentioned in the HTML, then generate a description based on your context clues. Please return data as a
JSON list of objects. Do not include any other text or ouput other than the JSON array, and do not include the back
ticks or the `json` keyword - only the raw array. Please include the following fields in every object and coerce
the data to be the corresponding data type:
      - name: String
      - image_url: String
      - images: Vec<String>
      - price: i32 // In pennies (e.g., $49.00 would be 4900)
      - canonical_name: String
      - source: String
      - description: String
      - link: String
      - metadata: Object
      - tags: Vec<String>
      - product: String (the product ID that you should use for every object is '123456')

Your input is:

```html
{html}
```

Example output:

[
  {{
    "name": "Morning ritual starter kit",
    "image_url": "https://mudwtr.com/cdn/shop/files/Cacao_6.png?v=1711489090",
    "images": [
      "https://mudwtr.com/cdn/shop/files/Cacao_6.png?v=1711489090",
      "https://mudwtr.com/cdn/shop/files/Cacao_2_1200x1200.png?v=1711489071",
      "https://mudwtr.com/cdn/shop/files/Cacao_3_1200x1200.png?v=1711489072"
    ],
    "price": 6000,
    "canonical_name": "morning-ritual-starter-kit",
    "source": "ai",
    "description": "MUD\\WTR™ is a coffee alternative consisting of organic, earth-grown ingredients lauded by cultures old and young around the world for their health and performance benefits. Packed with adaptogenic mushroom compounds, each ingredient was included in this blend for a specific purpose to complement a life that demands one's best.",
    "link": "https://mudwtr.com/products/30-servings-tin",
    "metadata": {{ }},
    "product": "f386aed7-fd5d-4102-8994-b8e3bb4ca616",
    "tags": [
      "Coffee Alternative",
      "Organic",
      "Mushroom",
      "Health",
      "Performance",
      "Adaptogenic",
      "MUD\\WTR",
      "Energy",
      "Focus",
      "No Jitters",
      "No Crash",
      "No Dependency",
      "Earth-Grown Ingredients",
      "Cultures",
      "Young",
      "Old",
      "Natural Ingredients",
      "Health Benefits",
      "Morning Ritual",
      "Starter Kit"
    ]
  }}

  // insert other products as you find them
]
"""
#10
#Note :- **Only extrect maximum 12 to 15 products.**

product_card_extrector = """
Context: You are an expert HTML scraper. You excel at deriving structured JSON data from
relative unstructured HTML. I'm going to give you unstructured HTML and I want you to produce the example output, possible.
The name of the brand is '{brand}'. Here is a summary of the brand, and please use this
context to create the quiz: '{brand_context}'.

Request: I need you to parse the given file of HTML and extract all fully formed 'product cards'
that might be contained in the page. A 'product card' is a simple JSON object that contains information
about a product or the brand in general. A product card should have the following properties: 'title',
'description', 'image_url', 'source', and 'link'. The 'title' property is the title of the card - this typically
is some short phrase about the product or brand. The 'description' property is a short description of the
the card, typically a single sentence. The 'image_url' property is the URL to the image of the card. The
image of the card is typically an image found that is relevant to the product or brand. Note that the image size
is rectangular - at about 300px wide by 150 px tall. The 'source' property will always be 'ai', The 'link' property is
the URL to the product page from which the product card was derived. If you cannot derive a field for the product card,
please insert `null` in the field. Please attempt to find all fields for each product card - the product card should
contain 'no' `null` fields. I repeat, the product card that you derive should have no `null` field values. Note that you
may or may not be able to find a 'product card' in the raw HTML. If you cannot find a product card, you should not include
it in the output.

Constraints and parameters: It's important to remember that there may or may not be 'product cards' contained in the
raw HTML you're given. If you finish parsing the HTML and all property values for an object are `null`, then
this is most likely not a real product card. Please return data as a JSON list of objects. Do not include any other
text or ouput other than the JSON array, and do not include the back ticks or the `json` keyword - only the raw array.
Ideally I only want a few product cards, so if you can't derive a card from the given HTML, just
don't include it in the output. Please include the following fields in every object and coerce the data to be the
corresponding data type:
      - title: String
      - description: String
      - image_url: String
      - source: String
      - link: String
      - metadata: Object
      - product: String (the product ID that you should use for every object is '123456')

Your input is:

```html
{html}
```

Example output:

[
  {{
    "title": "MUD\\WTR Founder's Story",
    "description": "How Shane Heath is redefining mental health and coffee culture norms.",
    "image_url": "https://s3.amazonaws.com/helpar.app/assets/mudwtr/img/starter-kit/reorder-card-founders-story.webp",
    "link": "https://mudwtr.com/blogs/trends-with-benefits/mudwtr-ceo-shane-heath-founder-story"
  }},
  {{
    "title": "Our Mushrooms",
    "description": "Our mushrooms are grown at M2 Ingredients, a USDA-certified organic indoor mushroom farm in Carlsbad, California.",
    "image_url": "https://s3.amazonaws.com/helpar.app/assets/mudwtr/img/starter-kit/reorder-card-our-mushrooms.webp",
    "link": "https://mudwtr.com/pages/our-mushrooms"
  }},
  {{
    "title": "How does caffeine work?",
    "description": "When we drink caffeine, the effects come on within 15 minutes.",
    "image_url": "https://s3.amazonaws.com/helpar.app/assets/mudwtr/img/starter-kit/reorder-card-how-caffeine-works.webp",
    "link": "https://mudwtr.com/pages/coffee-detox"
  }}

  // insert other products as you find them
]
"""

quiz_extractor = """
Context: You are an expert HTML scraper. You excel at deriving structured JSON data from
relative unstructured HTML. I'm going to give you unstructured HTML and I want you to produce the example output, possible.
The name of the brand is '{brand}', and the product in question is '{product}'.

Request: I need you to help me create a 'quiz'. A 'quiz' is a simple survey taken by a user to
uncover information about their preferences, habits, or knowledge.


Constraints and parameters: The quiz should have an appropriate name, description.
Each quiz card should have a question relevant to that certain context, and each of the answers
in the quiz should be related to the quiz card question. Each quiz card should have 4 or 5
answers/options with more points going to the more relevant answer. As you can see in the example,
some quiz card answers/options are better than others. Like the example, I want you to give me 3
options for "quiz results" based on the responses that the user gives. Each quiz answer should be
relevant to the given context again. All answers/questions/content should be interesting and engaging
without being overly verbose. Do not include any other text or output other than the quiz JSON in your
ouptut, so any extra text will cause the parsing to fail. Please note that you should also come up with
a succinct title no more than 50 characters long that adequately describes what this quiz is about.

Some parameters of the quiz:
      - Reward image: https://i.imgur.com/8UdKNS4.jpeg
      - Reward #1: 1,000 {brand} loyalty points
      - Reward #2: Same as reward #1
      - Reward #3: Same as reward #2

Your context for creating the quiz is:
```text
{context}
```

An example quiz:

{{
  "name": "What’s Your Full Body Skincare IQ",
  "description": "Looks like there's a lot to explore in the world of body skincare. Don't worry; it's never too late to start. Why not begin with our unique body serum?",
  "priority": 1,
  "results": [
    {{
      "title": "Your IQ Results Are...",
      "label": "Skincare Novice",
      "description": "Looks like there's a lot to explore in the world of body skincare. Don't worry; it's never too late to start. Why not begin with our unique body serum?",
      "image_url": "https://i.imgur.com/8UdKNS4.jpeg",
      "result_calculation": {{
        "min": 0,
        "max": 5
      }},
      "reward": {{
        "reward_type": "points",
        "value": "1000",
        "description": "You've earned 1,000 Abi Amé loyalty points"
      }}
    }},
    {{
      "title": "Your IQ Results Are...",
      "label": "Skincare Enthusiast",
      "description": "You're on the right track but there's room for improvement. Incorporating a dedicated body skincare product could elevate your routine to the next level!",
      "image_url": "https://i.imgur.com/8UdKNS4.jpeg",
      "result_calculation": {{
        "min": 6,
        "max": 10
      }},
      "reward": {{
        "reward_type": "points",
        "value": "1000",
        "description": "You've earned 1,000 Abi Amé loyalty points"
      }}
    }},
    {{
      "title": "Your IQ Results Are...",
      "label": "Skincare Pro",
      "description": "Impressive! You know your stuff, but even pros can find something new to love. Our body serum might just be your next favorite find.",
      "image_url": "https://i.imgur.com/8UdKNS4.jpeg",
      "result_calculation": {{
        "min": 11,
        "max": 13
      }},
      "reward": {{
        "reward_type": "points",
        "value": "1000",
        "description": "You've earned 1,000 Abi Amé loyalty points"
      }}
    }},
    {{
      "title": "Your IQ Results Are...",
      "label": "Dermatologist in Disguise",
      "description": "Wow, you could teach a class on skincare! As a skincare savant, you'll appreciate the science behind our advanced body serum.",
      "image_url": "https://i.imgur.com/8UdKNS4.jpeg",
      "result_calculation": {{
        "min": 14,
        "max": 15
      }},
      "reward": {{
        "reward_type": "points",
        "value": "1000",
        "description": "You've earned 1,000 Abi Amé loyalty points"
      }}
    }}
  ],
  "cards": [
    {{
      "card_type": "simple",
      "key": "exfoliation",
      "order": 0,
      "content": {{
        "title": "How often do you exfoliate your body?",
        "description": null,
        "image_url": null,
        "icon": null,
        "options": [
          {{
            "label": "Once per week",
            "key": "once-per-week",
            "description": null,
            "points": 3
          }},
          {{
            "label": "Once per month",
            "key": "once-per-month",
            "description": null,
            "points": 2
          }},
          {{
            "label": "What's exfoliating?",
            "key": "whats-exfoliating",
            "description": null,
            "points": 0
          }},
          {{
            "label": "Every day is too much, right?",
            "key": "every-day",
            "description": null,
            "points": 1
          }}
        ]
      }}
    }},
    {{
      "card_type": "simple",
      "order": 1,
      "key": "skin-hydration",
      "content": {{
        "title": "What's your go-to for hydrating your skin after a shower?",
        "description": null,
        "image_url": null,
        "icon": null,
        "options": [
          {{
            "label": "A thick, luxurious body cream",
            "key": "luxury-body-cream",
            "description": null,
            "points": 3
          }},
          {{
            "label": "Whatever lotion I find first",
            "key": "whatever-lotion",
            "description": null,
            "points": 2
          }},
          {{
            "label": "Does air drying count?",
            "key": "air-drying",
            "description": null,
            "points": 0
          }},
          {{
            "label": "I use the same moisturizer for my face and body",
            "key": "same-moisturizer",
            "description": null,
            "points": 1
          }}
        ]
      }}
    }},
    {{
      "card_type": "simple",
      "order": 2,
      "key": "sun-protection",
      "content": {{
        "title": "How do you protect your skin from the sun?",
        "description": null,
        "image_url": null,
        "icon": null,
        "options": [
          {{
            "label": "SPF everything, every day",
            "key": "spf-everything",
            "description": null,
            "points": 3
          }},
          {{
            "label": "I only use SPF when I'm at the beach",
            "key": "only-at-beach",
            "description": null,
            "points": 1
          }},
          {{
            "label": "Sunscreen is for summer only, right?",
            "key": "summer-only",
            "description": null,
            "points": 0
          }},
          {{
            "label": "I wear clothes, does that count?",
            "key": "wear-clothes",
            "description": null,
            "points": 2
          }}
        ]
      }}
    }},
    {{
      "card_type": "simple",
      "order": 2,
      "key": "what-matters-most",
      "content": {{
        "title": "When selecting body care products, what matters most to you?",
        "description": null,
        "image_url": null,
        "icon": null,
        "options": [
          {{
            "label": "Ingredients and benefits",
            "key": "ingredients-benefits",
            "description": null,
            "points": 3
          }},
          {{
            "label": "Scent and texture",
            "key": "scent-texture",
            "description": null,
            "points": 2
          }},
          {{
            "label": "Price point",
            "key": "price-point",
            "description": null,
            "points": 1
          }},
          {{
            "label": "Pretty packaging",
            "key": "pretty-packaging",
            "description": null,
            "points": 0
          }}
        ]
      }}
    }},
    {{
      "card_type": "simple",
      "order": 2,
      "key": "nightly-skincare-routine",
      "content": {{
        "title": "How would you describe your nightly skincare routine?",
        "description": null,
        "image_url": null,
        "icon": null,
        "options": [
          {{
            "label": "A detailed regimen for both face and body",
            "key": "detailed-regimen",
            "description": null,
            "points": 3
          }},
          {{
            "label": "Quick and simple, mostly just my face",
            "key": "quick-simple",
            "description": null,
            "points": 2
          }},
          {{
            "label": "I sometimes forget to even wash my face",
            "key": "i-forget",
            "description": null,
            "points": 0
          }},
          {{
            "label": "I just use whatever products I have on hand",
            "key": "whatever-products",
            "description": null,
            "points": 1
          }}
        ]
      }}
    }}
  ]
}}
"""

social_extrector = """
Context: You are an expert HTML scraper. You excel at deriving structured JSON data from
relative unstructured HTML. I'm going to give you unstructured HTML and I want you to produce the example output, possible.
The name of the brand is '{brand}'.

Request: I need you to parse the given file of HTML and extract any and all social
media links that you can find. The links should be returned in a JSON array, where
each object in the array has the following properties: 'icon', 'link', and 'name'. Keep in
mind that the 'icon' property should be the name of the icon used for the social media platform.
The icon names can be found in the ionicons library (https://ionicons.com/). The 'name' property
is just the name of the social media platform (e.g., 'facebook', 'instagram', 'twitter'). The 'link'
property should be the URL to the social media page. only extract for this social media only ["facebook","twitter","linkedin","instagram","tiktok","spotify"] 

Constraints and parameters: The only allowable social media links are from: Facebook, Instagram, Twitter,
Tiktok, Spotify, and the brand's website itself. There should always be exactly 4 objects in the returned
JSON array. If a social media platform is not found, the 'link' property should be a '#' string. Regardless
of whether or not we can find all links for all social platforms, you should always return exactly 4 objects.
If it is possible for you to return the data in the requested format, please do so. If you cannot return
the data in the requested format, please return a simple empty array []. Please do not deviate
from these instructions or hallucinate any additional requirements. The 'link' parameter's value must be
related to the actual brand being scraped, don't include any other link here if the name of the brand is not in the
path of the link. For example if the brand is 'Soom Shower', expect any 'links' to look like https://instagram.com/soomshower.
Notice the brand name in the path of the link. Do not include any other text or ouput other than the JSON array,
and do not include the back ticks or the `json` keyword - only the raw array also any extra text will cause the parsing to fail.

Your input is:

```html
{html}
```

Example output:

[
      {{
        "icon": "LogoFacebook",
        "link": "https://www.facebook.com/drinkmudwtr/",
        "name": "facebook"
      }},
      {{
        "icon": "LogoLinkedin",
        "link": "https://www.linkedin.com/drinkmudwtr/",
        "name": "facebook"
      }},
      {{
        "icon": "LogoInstagram",
        "link": "https://www.instagram.com/drinkmudwtr",
        "name": "instagram"
      }},
      {{
        "icon": "LogoTwitter",
        "link": "https://twitter.com/drinkmudwtr",
        "name": "twitter"
      }},
      {{
        "icon": "GlobeOutline",
        "link": "https://mudwtr.com/",
        "name": "website"
      }}
]
"""

social_extrector_2 = """
Context: You are an expert HTML link classifire. I'm going to give you list of HTML links and I want you to produce the example output, possible.
The name of the brand is '{brand}'.

Request: I need you to parse the given links of HTML. The links should be returned in a JSON array, where
each object in the array has the following properties: 'icon', 'link', and 'name'. Keep in
mind that the 'icon' property should be the name of the icon used for the social media platform.
The icon names can be found in the ionicons library (https://ionicons.com/). The 'name' property
is just the name of the social media platform (e.g., 'facebook', 'instagram', 'twitter'). The 'link'
property should be the URL to the social media page.

Constraints and parameters: The only allowable social media links are from: Facebook, Instagram, Twitter,
Tiktok, Spotify, and the brand's website itself. There should be only one primary link for each specific social media platform,
If a social media platform is not found. the 'link' property should be a '#' string.
Regardless of whether or not we can find all links for all social platforms.
If it is possible for you to return the data in the requested format, please do so. If you cannot return
the data in the requested format, please return a simple empty array []. Please do not deviate
from these instructions or hallucinate any additional requirements. The 'link' parameter's value must be
related to the actual brand being scraped, don't include any other link here if the name of the brand is not in the
path of the link. For example if the brand is 'Soom Shower', expect any 'links' to look like https://instagram.com/soomshower.
Notice the brand name in the path of the link. Do not include any other text or ouput other than the JSON array,
and do not include the back ticks or the `json` keyword - only the raw array also any extra text will cause the parsing to fail.

Your input is:

```html
{html}
```

Example output:

[
      {{
        "icon": "LogoFacebook",
        "link": "https://www.facebook.com/drinkmudwtr/",
        "name": "facebook"
      }},
      {{
        "icon": "LogoLinkedin",
        "link": "https://www.linkedin.com/drinkmudwtr/",
        "name": "facebook"
      }},
      {{
        "icon": "LogoInstagram",
        "link": "https://www.instagram.com/drinkmudwtr",
        "name": "instagram"
      }},
      {{
        "icon": "LogoTwitter",
        "link": "https://twitter.com/drinkmudwtr",
        "name": "twitter"
      }},
      {{
        "icon": "GlobeOutline",
        "link": "https://mudwtr.com/",
        "name": "website"
      }}
]
"""