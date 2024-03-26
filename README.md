# README for Trending GitHub Repositories Analysis Project

## Overview

This project is designed to analyze trending GitHub repositories, providing insights into the most popular repositories over the past week. It comprises two main Python scripts: one for preprocessing and fetching repository data, and another for analyzing the data to gain insights into programming language distribution, average stars, forks, and the similarities between repository summaries.

## File Descriptions

- `preprocessing.py`: This script fetches trending repositories from GitHub, retrieves their README files, and generates summaries for each repository. It saves the repository data, including the generated summaries, to a CSV file for further analysis.

- `analysis.py`: This script loads the repository data from the CSV file and performs analysis to determine the distribution of programming languages among the trending repositories, the average number of stars, and forks. It also generates insights into the similarities between the repositories based on their summaries.

## Setup and Requirements

### Prerequisites

- Python 3.x
- Requests library
- BeautifulSoup library
- Pandas library
- Numpy library
- OpenAI library

### Installation

1. Clone the repository to your local machine.
2. Ensure Python 3.x is installed on your system.
3. Install the required Python libraries by running `pip install -r requirements.txt` from your terminal or command prompt.

### Environmental Variables

Before running the scripts, you need to set up the following environment variable:

- `GITHUB_TOKEN`: Your personal GitHub access token for fetching README files from private repositories.
- `OPENAI_API`: Your OpenAI API key for using GPT-3.5 for generating summaries and analyzing similarities between repositories.

You can set these environment variables in your operating system or directly in your Python scripts (not recommended for production environments due to security concerns).

## Usage

### Preprocessing

Run the `preprocessing.py` script to fetch and preprocess the trending GitHub repositories. This script outputs a CSV file named `trending_repositories.csv`, containing repository details and their summaries.

```
python preprocessing.py
```

### Analysis

After running the preprocessing script, you can perform the analysis by running the `analyze_trending_repos.py` script. This script reads the `trending_repositories.csv` file, performs statistical analysis, and prints the insights.

```
python analyze_trending_repos.py
```

## License

This project is open-sourced under the MIT License. See the LICENSE file for more details.