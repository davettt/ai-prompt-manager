# AI Prompt Manager

> **Not currently maintained.** I'm not using or developing this app at the moment. I may pick it up again in future, so the code stays here. Until then, issues and pull requests may go unanswered.

*Store, organize, and retrieve your AI prompts with intelligent metadata extraction and privacy-first architecture.*

**Current Version:** v1.0.0 | [Changelog](CHANGELOG.md)

---

## What It Does

- 💾 **Store prompts safely** - Never lose your carefully crafted prompts again
- 🤖 **AI metadata extraction** - Claude automatically categorizes and tags your prompts
- 🔒 **Privacy-first** - Separate public (shareable) and private (personal) prompts
- ⭐ **Favorites system** - Star your most-used prompts for quick access
- 🔍 **Smart search** - Find prompts by keyword, category, or tags
- 📋 **Claude Project export** - One-click formatting for Claude Projects

---

## Quick Start

**Want to try it right now?**

```bash
# 1. Clone and install
git clone <repo-url>
cd ai-prompt-manager
pip install -r requirements.txt

# 2. Set up API key
cp .env.example .env
# Add: ANTHROPIC_API_KEY=your-key-here

# 3. Run
python main.py
```

**That's it!** See [Installation](#installation) for detailed setup.

---

## Installation

### Prerequisites

Before installing, make sure you have:
- **Python 3.7 or newer** ([Check version](https://www.python.org/downloads/): `python3 --version`)
- **pip** (usually comes with Python)
- **Anthropic API key** ([Get one here](https://console.anthropic.com/) - paid service)

### Step 1: Clone the Repository

```bash
git clone <repo-url>
cd ai-prompt-manager
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**What this installs:** Python packages for Claude AI integration, CLI interface, etc.

### Step 3: Configure API Key

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Anthropic API key:
# ANTHROPIC_API_KEY=sk-ant-...
```

Get an API key from [Anthropic's Console](https://console.anthropic.com/).

### Step 4: First Run

```bash
python main.py
```

**Expected result:** You'll see a menu to add, search, or browse prompts.

### Troubleshooting Installation

**Python not found?**
- Install from [python.org](https://www.python.org/downloads/)
- Try `python3` instead of `python`

**"No module named 'anthropic'" or similar?**
- Install dependencies: `pip install -r requirements.txt`
- Make sure you're in the ai-prompt-manager directory

**API key not working?**
- Check `.env` file format: `ANTHROPIC_API_KEY=sk-ant-...` (no quotes, no spaces)
- Get a new token from [console.anthropic.com](https://console.anthropic.com/)

---

## How to Use

### Main Menu

```bash
python main.py
```

You'll see options to:
- **Add new prompt** - Paste a prompt, AI extracts metadata
- **Browse prompts** - See your entire library with inline filtering
- **Search prompts** - Opens browser with search filter applied
- **Exit**

### Example Workflow

**1. Add a prompt:**
```bash
python main.py
# Choose: Add new prompt
# Paste your prompt
```

**AI analyzes and suggests:**
- Title: "Elite Strategic Performance Advisor"
- Category: "Business Strategy"
- Privacy: "Private" (contains personal info)
- Tags: coaching, performance, strategy

**2. Star it as favorite:**
```bash
# In search/browse view
# Type: [number]fav
```

**3. Export to Claude Project:**
```bash
# Type: [number]p
# Copies formatted prompt to clipboard
```

---

## Common Tasks

### Adding Your First Prompt

```bash
python main.py
# Choose: Add new prompt
# Paste your prompt text
# AI suggests title, category, privacy level
# Review and confirm
```

### Browsing and Filtering Prompts

```bash
python main.py
# Choose: Browse prompts
```

**In the browser, you can:**
- Press `[number]` to expand/collapse details
- Type text to filter (smart OR logic, relevance scored)
- Type `favorites` or `⭐` to see only starred prompts
- Type `private` to see only private prompts
- Type `public` to see only public prompts
- Type `x` to clear current filter

### Searching for Prompts

```bash
python main.py
# Choose: Search prompts
# Enter keywords
# Browser opens with filter applied
```

**Search opens the browser with your search already filtered!**

### Viewing and Managing Favorites

```bash
# In browse view:
# Type: favorites  (or ⭐)
# Shows only starred prompts
```

**To star/unstar:**
```bash
# [number]fav    - Star a prompt
# [number]unfav  - Unstar a prompt
```

**Favorites are marked with ⭐ in all lists**

### Exporting to Claude Projects

```bash
# In browse view:
# Type: [number]p
# Formatted prompt copied to clipboard
# Paste into Claude Project custom instructions
```

### Editing Prompt Metadata

```bash
# In browse view:
# Type: [number]e
# Edit title, category, tags, privacy, description
```

---

## Requirements

- Python 3.7 or newer
- Anthropic API key (paid service for AI analysis)

---

## Data Storage & Privacy

- 🏠 **Your prompts stay local** in `prompts/` folder
  - `prompts/public/` - Git tracked, shareable prompts
  - `prompts/private/` - Git ignored, personal prompts only
- 🔒 **API keys** stored in `.env` file (never committed to git)
- 🤖 **AI analysis** only for metadata extraction (title, category, tags)
- 🚫 **No cloud storage** of your prompts
- ✅ **Open source** - review all code yourself

**Your private files:**
- `prompts/private/` - Your personal prompts
- `.env` - Your API key
- Both are automatically excluded from git

---

## Usage & Forking

This project is open source under MIT license. You're welcome to:
- **Fork the repository** and customize for your own needs
- **Report bugs** via GitHub issues
- **Suggest improvements** in discussions

*Note: This is a personal productivity system. While the code is open source, I keep contributions minimal to maintain system stability for personal use.*

### For Developers (Forking/Customization)

If you've forked this project and want to modify it, see:
- **[.claude/README.md](.claude/README.md)** - Claude Code integration guide
- **[CLAUDE_CONTEXT.md](CLAUDE_CONTEXT.md)** - Technical documentation

**Quick fork setup:**
```bash
git clone <your-fork-url>
cd ai-prompt-manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Install dev tools
pip install -r requirements-dev.txt
pre-commit install
```

---

## Support

- 📖 **Questions?** Check the [Common Tasks](#common-tasks) section above
- 📚 **Quick setup?** See [USER_START.md](USER_START.md)
- 🐛 **Found a bug?** Open an issue on GitHub
- 💡 **Have an idea?** Start a discussion

---

## Advanced

### Rich Metadata Storage

Each prompt includes comprehensive metadata:
```json
{
  "id": "uuid",
  "title": "Elite Strategic Performance Advisor",
  "content": "Original prompt (never modified by AI)",
  "category": "business_strategy",
  "tags": ["coaching", "performance", "strategy"],
  "private": false,
  "favorite": true,
  "description": "Systems-level performance acceleration",
  "technical_notes": {
    "recommended_llm": "Claude 3.5 Sonnet",
    "temperature": 0.4
  }
}
```

### Privacy Architecture

```
prompts/
├── public/          # Git tracked - safe to share
│   ├── business/
│   ├── technical/
│   └── creative/
└── private/         # Git ignored - your personal prompts
    ├── personal/
    └── confidential/
```

### Search Features

- **OR logic**: Matches ANY keyword (not all required)
- **Relevance scoring**: Best matches appear first
- **Inline expansion**: Press [number] to toggle details
- **Filter by favorites**: Type "favorites" to see only starred

### CLI Commands

**In the browser:**
- `[number]` - Toggle inline expansion (show/hide details)
- `[number]f` - Show full prompt content
- `[number]c` - Copy prompt to clipboard
- `[number]p` - Export to Claude Project format
- `[number]fav` - Star as favorite
- `[number]unfav` - Remove from favorites
- `[number]e` - Edit metadata (title, category, tags, privacy, description)
- `[number]d` - Delete prompt
- `favorites` or `⭐` - Filter to favorites only
- `private` - Filter to private prompts only
- `public` - Filter to public prompts only
- `x` - Clear current filter
- `q` - Exit browser

### Project Structure

```
ai-prompt-manager/
├── main.py                     # Start here
├── prompt_manager.py           # Core functionality
├── metadata_extractor.py       # AI analysis
├── utils/                      # Helper functions
├── prompts/
│   ├── public/                # Shareable prompts
│   └── private/               # Personal prompts
└── .env                       # Your API key
```

### Roadmap

**✅ Current (v1.0.0):**
- Core prompt storage and metadata extraction
- Privacy-first architecture
- Favorites system
- Search and browse
- Claude Project export

**🚀 Next:**
- Usage analytics
- Bulk import/export
- Prompt versioning
- Advanced filtering

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

**Version:** v1.0.0 | **Last updated:** 2025-10-12

**Ready to organize your prompts?** Run `python main.py` 🚀
