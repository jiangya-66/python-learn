# Python Learning Project

This is a Python learning project containing multiple Python programming exercises and a complete information extractor application.

## Project Structure

```
.
├── README.md                    # Project documentation
├── config.json                  # Configuration file
├── py-day1.py                   # Async programming: coroutines and concurrent IO operations
├── py-day2.py                   # Async programming: concurrent request limiter
├── py-day3.py                   # Pydantic data validation exercises
├── py-day4.py                   # Pydantic configuration management
├── py-day5.py                   # Information extractor demonstration
└── info_extractor/              # Information extractor subproject
    ├── __init__.py              # Package initialization
    ├── info_extractor.py        # Main implementation of information extractor
    ├── example_usage.py         # Usage examples
    ├── test_extractor.py        # Test files
    ├── requirements.txt         # Dependencies list
    └── README.md                # Detailed documentation for information extractor
```

## File Descriptions

### 1. Async Programming Exercises

**py-day1.py** - Async Programming Basics
- Implement coroutine functions using `asyncio`
- Simulate different IO operations (network requests, file reading, database queries)
- Use `asyncio.gather()` for concurrent task execution

**py-day2.py** - Concurrent Request Limiter
- Implement concurrency control using `asyncio.Semaphore`
- Simulate 100 API requests with maximum 5 concurrent executions
- Demonstrate resource management in async programming

### 2. Pydantic Data Validation Exercises

**py-day3.py** - Pydantic Advanced Features
- Basic model definition and data validation
- Nested models and custom validators
- Data conversion and serialization
- Generic support and recursive models
- FastAPI integration examples

**py-day4.py** - Pydantic Configuration Management
- Load configuration from JSON files
- Use `ConfigDict` for model configuration
- Field validation and alias generators
- Environment variable support

### 3. Information Extractor Application

**py-day5.py** - Information Extractor Demonstration
- Integrate information extractor functionality
- Provide multiple example review analyses
- Show complete API usage workflow

**info_extractor/** - Complete Information Extractor Project
- Use Pydantic to define strict output models
- Integrate DeepSeek LLM for intelligent analysis
- Support sentiment analysis, keyword extraction, and scoring
- Complete error handling and validation

## Quick Start

### Environment Requirements
- Python 3.8+
- pip package manager

### Install Dependencies

```bash
# Install information extractor dependencies
cd info_extractor
pip install -r requirements.txt

# Or install globally
pip install pydantic openai aiohttp aiofiles
```

### Run Examples

```bash
# Run async programming examples
python py-day1.py
python py-day2.py

# Run Pydantic examples
python py-day3.py
python py-day4.py

# Run information extractor demo (requires DeepSeek API key)
python py-day5.py
```

## Information Extractor Usage

### 1. Get API Key
1. Visit [DeepSeek Platform](https://platform.deepseek.com/api_keys)
2. Register and get an API key
3. Set environment variable:

```bash
# Windows
set DEEPSEEK_API_KEY=your-api-key

# Linux/Mac
export DEEPSEEK_API_KEY='your-api-key'
```

### 2. Basic Usage

```python
from info_extractor import InfoExtractor

# Initialize (automatically reads environment variable)
extractor = InfoExtractor()

# Analyze review
review_text = "This phone has great camera quality and excellent battery life!"
result = extractor.extract(review_text)

# Access results
print(f"Sentiment: {result.sentiment}")      # positive/neutral/negative
print(f"Keywords: {result.keywords}")        # ['camera quality', 'battery life', ...]
print(f"Score: {result.score}/5")            # 1-5

# Get JSON string
json_output = result.model_dump_json(indent=2)
print(json_output)
```

### 3. Output Example

```json
{
  "sentiment": "positive",
  "keywords": [
    "camera quality",
    "battery life",
    "performance",
    "value for money"
  ],
  "score": 5
}
```

## Learning Objectives

Through this project, you can learn:

1. **Async Programming**: Concepts like coroutines, tasks, semaphores
2. **Data Validation**: Strict data validation using Pydantic
3. **API Integration**: How to integrate third-party API services
4. **Project Structure**: Proper Python project organization
5. **Error Handling**: Comprehensive exception handling and user feedback

## Technology Stack

- **Python 3.8+**: Main programming language
- **asyncio**: Async programming framework
- **Pydantic**: Data validation and settings management
- **DeepSeek API**: Large language model service
- **aiohttp/aiofiles**: Async HTTP and file operations

## Notes

1. **API Limits**: DeepSeek API has call frequency and quota limits
2. **Cost**: Using API incurs costs, monitor usage
3. **Network**: Stable network connection required
4. **Error Handling**: Add retry mechanisms for production environments

## License

MIT License

## Support

For issues or suggestions, check comments in each file or submit an Issue.

## Changelog

- **2024**: Project created with Python learning exercises
- **2025**: Added information extractor functionality
- **Continuous Updates**: Add new features based on learning progress

---

**Tip**: This project is suitable for intermediate Python learners, covering practical skills like async programming, data validation, and API integration. Recommended to learn in file number order.