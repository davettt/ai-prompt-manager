# AI Prompt Manager

A streamlined, intelligent prompt storage and retrieval system that focuses on preserving your carefully crafted prompts while providing smart organization and metadata extraction.

## Philosophy

This system takes a fundamentally different approach:
- **Quality First**: Add only your complete, optimized prompts
- **Preservation**: Never modify your prompt content 
- **Intelligence**: Let Claude analyze and categorize your prompts
- **Privacy**: Secure separation of public and private content
- **Simplicity**: Clean, focused functionality without complexity

## Quick Start

1. **Setup**:
   ```bash
   cd ai-prompt-manager
   pip install -r requirements.txt
   cp .env.example .env  # Add your ANTHROPIC_API_KEY
   ```

2. **Add a prompt**:
   ```bash
   python main.py
   # Select [1] Add new prompt
   # Paste your complete prompt
   # Review AI-suggested metadata
   # Save to public or private library
   ```

3. **Browse your library**:
   ```bash
   python main.py
   # Select [2] List all prompts
   ```

## Key Features

### Intelligent Metadata Extraction
- **Auto-detects title** from your prompt structure (# Title format)
- **Extracts technical specs** (LLM recommendations, temperature, tokens)
- **AI categorization** using Claude API for smart organization
- **Privacy analysis** with reasoning for public/private recommendations
- **Content preservation** - your prompts are never modified

### Professional CLI Interface
- **Enhanced table displays** for prompt browsing
- **Interactive detailed views** with copy-to-clipboard functionality
- **Professional status indicators** (✅❌⚠️ℹ️🔄)
- **Graceful error handling** and keyboard interrupt support
- **Rich prompt summaries** with technical specifications

### Privacy-First Architecture
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

### Rich Metadata Storage
Each prompt includes:
- **Core info**: title, category, tags, description
- **Technical notes**: recommended LLM, temperature, token limits
- **AI analysis**: complexity level, use case, privacy reasoning
- **Usage tracking**: creation date, usage count

## Data Structure

```json
{
  "id": "uuid",
  "title": "Elite Strategic Performance Advisor",
  "content": "# Elite Strategic Performance Advisor\\n\\n**Recommended LLM**: Claude...",
  "category": "business_strategy",
  "tags": ["coaching", "performance", "strategy"],
  "private": false,
  "description": "Systems-level performance acceleration through evidence-based guidance",
  "technical_notes": {
    "recommended_llm": "Claude 3.5 Sonnet",
    "temperature": 0.4,
    "max_tokens": "4000-6000"
  },
  "ai_analysis": {
    "complexity_level": "advanced",
    "privacy_reasoning": "Professional methodology, safe to share publicly"
  }
}
```

## Commands

- `python main.py` - Main interface
- `python metadata_extractor.py` - Test metadata extraction

## Privacy & Security

- **Private prompts** are completely excluded from git via `.gitignore`
- **API keys** stored securely in `.env` file (never committed)
- **Content preservation** - no AI modification of your prompt content
- **Intelligent privacy analysis** - Claude suggests public/private based on content

## Migration from Previous Versions

This system is designed for professional-grade prompts with a focus on content preservation. Previous versions focused on XML transformation and improvement workflows that proved problematic for complex prompts.

Key improvements:
- ❌ No more XML forcing or content modification
- ❌ No more "improvement" workflows that lose content
- ✅ Intelligent metadata extraction without content changes
- ✅ Support for any prompt format (markdown, XML, plain text)
- ✅ Professional technical specifications storage
- ✅ AI-powered categorization and privacy analysis

## Development

The system is built with simplicity and reliability in mind:
- **Clean separation**: Each module has a single responsibility
- **Error handling**: Graceful fallbacks when API is unavailable
- **Privacy protection**: Multiple layers preventing private content leaks
- **Extensible**: Easy to add new features without complexity

Ready to store and organize your professional prompt library!
