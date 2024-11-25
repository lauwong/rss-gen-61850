import openai
import requests
from dotenv import load_dotenv
import os

load_dotenv()
# Set your OpenAI API key
openai.api_key = os.getenv("SECRET_KEY")
# print(openai.api_key)

def fetch_website_html(url):
    """Fetch HTML content from a URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch website. Status code: {response.status_code}")

def generate_rss_feed(html_content, website_url):
    """Use ChatGPT to generate an RSS feed from HTML content."""
    prompt = f"""
Given the following HTML content and website URL, generate an RSS feed XML file. Include a title, description, link to the website, and create at least three dummy <item> entries with title, description, link, and publication date.

Website URL: {website_url}

HTML content:
{html_content[:2000]}  # Truncate for token limits; only the start is included.

Generate the RSS feed:
    """

    response = openai.completions.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5
    )
    return response.choices[0].text.strip()

def save_rss_feed_to_file(rss_feed, filename="rss_feed.xml"):
    """Save the generated RSS feed to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(rss_feed)
    print(f"RSS feed saved to {filename}")

if __name__ == "__main__":
    try:
        # Replace this with the URL of the website you want to scrape
        website_url = "https://example.com"
        
        # Fetch HTML content from the website
        html_content = fetch_website_html(website_url)
        
        # Generate the RSS feed using ChatGPT
        rss_feed = generate_rss_feed(html_content, website_url)
        
        # Save the RSS feed to a file
        save_rss_feed_to_file(rss_feed)
    except Exception as e:
        print(f"Error: {e}")
