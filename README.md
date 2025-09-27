# AI Prompt Manager

*Professional-grade prompt storage and retrieval system with intelligent metadata extraction and privacy-first architecture*

## Features

✅ **Intelligent Metadata Extraction**: Auto-detects titles, categories, and technical specs using Claude AI  
✅ **Privacy-First Architecture**: Secure separation of public and private prompts  
✅ **Content Preservation**: Never modifies your carefully crafted prompts  
✅ **Smart Organization**: Automatic categorization and workflow optimization  
✅ **Professional CLI Interface**: Enhanced table displays and interactive views  
✅ **Safe Operations**: Preview metadata before saving prompts  

## Quick Start

### Prerequisites
- Python 3.7+
- Anthropic API access (claude.ai)
- Git (for version control)

### Installation
```bash
git clone [YOUR_REPO_URL]
cd ai-prompt-manager
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
python main.py
```

## How It Works

1. **Add Complete Prompts**: Paste your optimized prompts into the system
2. **AI Analysis**: Claude extracts metadata, suggests categories, analyzes privacy
3. **Smart Organization**: Automatic categorization with public/private separation
4. **Easy Retrieval**: Search, browse, and copy prompts with professional interface

## Example Workflow

**You:** Paste a complex coaching prompt into the system

**Claude AI:** Analyzes content and suggests:
- Title: "Elite Strategic Performance Advisor"
- Category: "Business Strategy" 
- Privacy: "Private" (contains personal coaching elements)
- Technical notes: "Claude 3.5 Sonnet, Temperature 0.4"

**System:** Saves to appropriate folder with rich metadata for easy retrieval

## Using with Claude

**Start any Claude conversation with:**
```
I have an AI Prompt Manager system. Please read the documentation files in this folder:

/path/to/ai-prompt-manager

The system stores and organizes prompts with intelligent metadata extraction.
```

## Core Commands

```bash
# Main interface
python main.py

# Test metadata extraction
python metadata_extractor.py

# Direct prompt management
python prompt_manager.py
```

## Project Structure

```
ai-prompt-manager/
├── README.md                    # This file
├── USER_START.md               # Quick setup guide
├── main.py                     # Entry point
├── prompt_manager.py           # Core functionality
├── metadata_extractor.py       # Claude AI integration
├── utils/                      # Shared utilities
│   ├── cli_helpers.py         # Enhanced CLI patterns
│   └── file_helpers.py        # File operations
├── prompts/                   # Prompt library
│   ├── public/               # Git tracked, shareable
│   └── private/              # Git ignored, personal
├── .env.example             # Environment template
└── CLAUDE_CONTEXT.md        # Technical documentation
```

## Privacy & Security Architecture

```
prompts/
├── public/          # Git tracked, shared prompts
│   ├── business/
│   ├── technical/
│   └── creative/
└── private/         # Git ignored, personal prompts
    ├── personal/
    └── confidential/
```

### Privacy Protection
- 🔒 **Private prompts** completely excluded from git via `.gitignore`
- 🏠 **Personal data** stays on your machine only
- 🤖 **AI privacy analysis** suggests public/private based on content
- ✅ **Content preservation** - no AI modification of your prompt content
- 🚫 **No cloud storage** of sensitive prompt information

## Rich Metadata Storage

Each prompt includes:
```json
{
  "id": "uuid",
  "title": "Elite Strategic Performance Advisor",
  "content": "Original prompt content (never modified)",
  "category": "business_strategy",
  "tags": ["coaching", "performance", "strategy"],
  "private": false,
  "description": "Systems-level performance acceleration",
  "technical_notes": {
    "recommended_llm": "Claude 3.5 Sonnet",
    "temperature": 0.4,
    "max_tokens": "4000-6000"
  },
  "ai_analysis": {
    "complexity_level": "advanced",
    "privacy_reasoning": "Professional methodology, safe to share"
  }
}
```

## Usage & Forking

This project is open source under MIT license. You're welcome to:
- **Fork the repository** and customize for your needs
- **Report bugs** via GitHub issues
- **Suggest improvements** in discussions

*Note: This is a personal productivity system. While the code is open source, I keep contributions minimal to maintain system stability.*

## Roadmap

- [x] Core prompt storage and metadata extraction
- [x] Privacy-first architecture with public/private separation
- [x] Professional CLI interface with search functionality
- [ ] Favorites system for quick access to most-used prompts
- [ ] Enhanced search with advanced filtering
- [ ] Usage analytics and prompt effectiveness tracking
- [ ] Export/import capabilities for sharing prompt collections

## Important Disclaimers

⚠️  **Use at your own risk:** This software is provided "as is" without warranty. Users are responsible for:
- Securing API tokens and personal data
- Testing with non-critical prompts first
- Understanding the privacy implications of public vs private prompts
- Regular backups of important prompt data

**No warranty provided.** The author is not responsible for any data loss, API quota exhaustion, or unintended prompt modifications.

## Support

- 📖 Read USER_START.md for quick setup
- 📋 Check CLAUDE_CONTEXT.md for technical details
- 🐛 Report issues on GitHub
- 💡 Suggest features in discussions

---

*Supercharge your AI productivity with intelligent prompt management!*
