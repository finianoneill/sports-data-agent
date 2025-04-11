# Sports Data Agent

This repository contains a workflow that leverages OpenAI models and Langchain to create an agent to download and structure data about particular sports that could subsequently be leveraged by a ML classification based pipeline to predict the outcome of sports events.

## Features

- **NBA Statistics Scraper**: Uses web searches to gather and structure current NBA game data and player statistics
- **Multi-Category Data Collection**: Gathers comprehensive statistics including points, rebounds, assists, steals, blocks, and shooting percentages
- **Structured Data Output**: Processes unstructured web data into clean JSON format for analysis
- **Interactive Data Exploration**: Command-line interface for browsing collected statistics by category
- **Automated Reports**: Generates CSV files for specific statistics categories
- **Error Handling**: Robust parsing with detailed error reporting for debugging

## Technologies Used

- **LangChain**: This project utilizes LangChain, a framework for building applications with large language models. It provides tools and utilities for creating agents, tools, and chains to interact with LLMs.

- **OpenAI**: OpenAI's GPT-4o model is used for natural language processing and data extraction, enabling the conversion of unstructured web search results into structured, usable data formats.

- **DuckDuckGo Search**: For retrieving current web information about NBA statistics without requiring API keys.

- **pandas**: For data manipulation, analysis, and export to CSV format.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/sports-data-agent.git
cd sports-data-agent
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up the necessary environment variables by creating a `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

To run the Sports Data Agent:

```bash
python sports_data_agent.py
```

Once the script is running, you can interact with it using the following commands:
- `view points`: Display the current NBA points leaders
- `view rebounds`: Display the current NBA rebounds leaders
- `view [stat_type]`: View leaders for any collected statistic category
- `refresh`: Fetch updated statistics from the web
- `exit`: Terminate the program

All data is automatically saved to the `nba_stats` directory in both JSON and CSV formats.

## Project Structure

```
sports-data-agent/
├── sports_data_agent.py  # Main script for the NBA statistics agent
├── requirements.txt      # Required Python packages
├── .env                  # Environment variables (not tracked by git)
├── LICENSE               # MIT License
└── nba_stats/            # Generated directory for output data
    ├── nba_stats_YYYY-MM-DD.json  # Daily statistics in JSON format
    └── points_leaders_YYYY-MM-DD.csv  # Daily points leaders in CSV format
```

## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.