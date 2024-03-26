import requests
from openai import OpenAI
from bs4 import BeautifulSoup
import base64
import pandas as pd
import os

def fetch_trending_repositories():
    url = 'https://github.com/trending?since=weekly'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    repositories = []

    articles = soup.find_all('article', class_='Box-row')

    for article in articles:
        repo_name = article.find('h2').get_text(strip=True)
        description = article.find('p', class_='col-9').get_text(strip=True) if article.find('p', class_='col-9') else "No description"
        programming_language_element = article.find('span', itemprop='programmingLanguage')
        programming_language = programming_language_element.get_text(strip=True) if programming_language_element else "Not specified"
        
        stars = article.find('a', href=lambda x: x and 'stargazers' in x).get_text(strip=True).replace(',', '') if article.find('a', href=lambda x: x and 'stargazers' in x) else "0"
        forks = article.find('a', href=lambda x: x and 'forks' in x).get_text(strip=True).replace(',', '') if article.find('a', href=lambda x: x and 'forks' in x) else "0"
        
        stars_thisweek_container = article.find('span', class_='d-inline-block float-sm-right')
        stars_thisweek = stars_thisweek_container.get_text(strip=True).split(' ')[0].replace(',', '') if stars_thisweek_container else "0"
        
        repository_details = {
            "Repository Name": repo_name,
            "Description": description,
            "Programming Language": programming_language,
            "Stars": int(stars),
            "Forks": int(forks),
            "Stars This Week": int(stars_thisweek)
        }

        repositories.append(repository_details)

    return repositories


def fetch_readme_for_repositories(repositories):
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    for repo in repositories:
        full_name = repo['Repository Name']
        owner, repo_name = full_name.split('/')
        url = f"https://api.github.com/repos/{owner.strip()}/{repo_name.strip()}/readme"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            readme_data = response.json()
            readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
            repo['README'] = readme_content
        else:
            repo['README'] = "README not found or could not be accessed."
            
    return repositories

def generate_summary(text, client):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize this for a general audience: {text}"}
        ]
    )
    return response.choices[0].message.content


def main():
    print("Fetching trending repositories...")
    repositories = fetch_readme_for_repositories(fetch_trending_repositories())
    if not repositories:
        print("No trending repositories found.")
        return

    client = OpenAI(api_key=os.getenv('OPENAI_API'))

    for repo in repositories:
        print(f"\nGenerating summary for {repo['Repository Name']}...")
        description = repo['README']
        summary = generate_summary(description, client)
        repo['summary'] = summary
        print(f"Summary: {summary}")

    return repositories

repos = main()
df = pd.DataFrame(repos)
df = df.drop(columns=['README'])
df.to_csv('trending_repositories.csv', index=False)
