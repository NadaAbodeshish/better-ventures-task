import pandas as pd
import numpy as np
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API'))

def analyze_repositories_df(repositories_df):
    if 'Programming Language' in repositories_df.columns:
        language_distribution = repositories_df['Programming Language'].value_counts().to_dict()
    else:
        language_distribution = {}

    average_stars = repositories_df['Stars'].mean() if 'Stars' in repositories_df.columns else 0
    average_forks = repositories_df['Forks'].mean() if 'Forks' in repositories_df.columns else 0

    return language_distribution, average_stars, average_forks


def generate_similarity_between_repos(text, client):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Tell me the similarities between all these summaries and say why they are trending, they are separated by this substring \"***\" : {text}"}
        ]
    )
    return response.choices[0].message.content


repositories = pd.read_csv('trending_repositories.csv')
print("Analyzing repositories...")
language_distribution, average_stars, average_forks = analyze_repositories_df(repositories)

print("\nRepository Analysis:")
print(f"Language Distribution: {language_distribution}")
print(f"Average Stars: {average_stars}")
print(f"Average Forks: {average_forks}")

print('Analyzing Similarities between Repositories: ......')
summaries = repositories['summary'].to_numpy()
summaries_joined = "***".join(summaries)
res = generate_similarity_between_repos(summaries_joined, client)
print('Similarities between trending repositories: ', res)