# MCP LangChain Application

This is the main application directory for the MCP LangChain integration.

## 📁 Directory Structure

- `app.py` - Main application code
- `browser_mcp.json` - Search configuration
- `requirements.txt` - Python dependencies
- `.env.example` - Example environment variables
- `run_with_node.sh` - Helper script for Node.js integration
- `test_gemini.py` - Test script for Gemini API

## 🚀 Getting Started

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

## ⚙️ Configuration

Edit `browser_mcp.json` to adjust search settings:
- `delay`: Time between requests (ms)
- `retries`: Number of retry attempts
- `timeout`: Request timeout (ms)

## 📝 Notes
- Ensure you have Node.js installed for DuckDuckGo search functionality
- The application uses environment variables for sensitive configuration
- Check the root README.md for more detailed documentation
