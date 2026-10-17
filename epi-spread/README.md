# Epi-Spread

A grid-based epidemic simulation game. Model disease spread, manage resources, and try to contain the outbreak before it's too late.

## Project Structure

```
epi-spread/
├── src/              # Source code
│   ├── core/         # Engine & grid simulation
│   ├── config/       # Game settings & configuration
│   └── ui/           # User interface (web)
├── tests/            # Unit tests
├── config/           # Configuration files
├── assets/           # Game assets (images, sounds, etc.)
└── docs/             # Documentation
```

## Getting Started

### Prerequisites
- Python 3.9 or higher
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd epi-spread
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate    # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game

```bash
python -m src.ui.web_app
```

### Running Tests

```bash
pytest
```

## License

MIT License