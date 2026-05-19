# News Aggregator

News Aggregator is a news GUI Python app that fetches articles from NewsAPI and New York Times API.

## Project Structure

The project follows a clean separation of concerns pattern:

```
news-aggregator/
├── src/
│   ├── __init__.py          # Package marker
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration & API keys
│   ├── api.py               # News fetching & scraping logic
│   └── ui.py                # Tkinter GUI components
│
├── tests/
│   ├── test_api.py          # API module tests
│   ├── test_config.py       # Config module tests
│   └── test_ui.py           # UI module tests
│
├── requirements.txt         # Python dependencies
├── run.py                  # Application entry point
└── README.md               # This file
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Rename `example.env` to `.env` in the root directory and add your API keys:
```
NEWS_API_KEY=<your_newsapi_key>
NYT_API_KEY=<your_nyt_api_key>
```

## Running the Application

```bash
python -m src.main
```

Or from the src directory:
```bash
python main.py
```

## Running Tests

Run all tests:
```bash
python -m unittest discover -s tests
```

Run specific test file:
```bash
python -m unittest tests.test_api
```

Run with verbose output:
```bash
python -m unittest discover -s tests -v
```

Run with coverage report:
```bash
pip install coverage
coverage run -m unittest discover -s tests
coverage report -m --include=src/
```

## Module Breakdown

### `config.py`
- Loads environment variables from `.env`
- Defines API keys, categories, and settings
- Provides configuration constants for other modules
- **Responsibility**: Configuration management

### `api.py`
- `NewsScraper` class: Fetches articles from NewsAPI and NYT API
- Handles web scraping with BeautifulSoup
- Manages HTTP requests and error handling
- **Responsibility**: External API communication & data fetching

### `ui.py`
- `NewsApp` class: Tkinter GUI components
- Handles user interactions (search, display)
- Manages article display and popup windows
- **Responsibility**: User interface & presentation

### `main.py`
- Entry point for the application
- Orchestrates initialisation of all components
- Validates API keys before startup
- **Responsibility**: Application orchestration

## Testing Strategy

Tests are organized by module using Python's standard `unittest` framework:

- **test_api.py**: Tests for news fetching and scraping logic
  - Mocks HTTP requests to test without real API calls
  - Tests error handling and edge cases
  
- **test_config.py**: Tests for configuration module
  - Validates configuration constants
  - Tests settings and mappings
  
- **test_ui.py**: Tests for GUI components
  - Tests widget initialisation
  - Tests user interaction handling

All external dependencies (API calls, network requests) are mocked using `unittest.mock` to ensure tests run offline and complete quickly.

## Contributing

## History

Version 0.2 (2026-05-17) - Refactored to separation of concerns architecture
Version 0.1 (2026-04-23) - Initial project setup

## Credits

**University of Technology Sydney - PYTHON_IN_PROGRESS**

- Leon Hsu - 26324145

- Ishani Bondade - 26147280

- Chaemin Jin - 26492722

- Niki Miyake - 14742605

## License

The MIT License (MIT)

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.