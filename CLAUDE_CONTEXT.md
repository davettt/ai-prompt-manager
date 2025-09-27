# Claude Context - AI Prompt Manager

## Project Overview
AI Prompt Manager - Professional-grade prompt storage and retrieval system with intelligent metadata extraction and privacy-first architecture. Built using enhanced Python automation template patterns.

## Development Status
- **Foundation:** Complete
- **Current Phase:** Ready for Favorites system implementation
- **Next Milestone:** Enhanced search and usage analytics
- **Architecture:** Clean system eliminating problematic XML transformation workflows

## Project Structure
```
ai-prompt-manager/
├── main.py                    # Single entry point
├── prompt_manager.py          # Core functionality with enhanced CLI
├── metadata_extractor.py      # Claude API for intelligent analysis
├── utils/
│   ├── cli_helpers.py         # Enhanced terminal UI patterns
│   ├── file_helpers.py        # Professional file operations
│   └── __init__.py
├── prompts/
│   ├── public/                # Git tracked, sharable prompts
│   └── private/               # Git ignored, personal prompts
├── .env                       # API keys (git ignored)
├── .gitignore                 # Privacy-first exclusions
├── USER_START.md              # Quick setup guide
└── README.md                  # Professional documentation
```

## Key Files & Locations
- **Main script:** main.py (entry point)
- **Core logic:** prompt_manager.py (CLI interface and operations)
- **AI integration:** metadata_extractor.py (Claude API for metadata)
- **Utilities:** utils/ folder (CLI helpers, file operations)
- **Prompt library:** prompts/ (public/ and private/ separation)
- **Configuration:** .env file (API keys)

## API Integrations
- **Anthropic Claude API**: Used for intelligent metadata extraction and categorization
- **Rate limiting**: Efficient API usage patterns with graceful fallbacks
- **Authentication**: Bearer token via ANTHROPIC_API_KEY environment variable
- **Error handling**: Professional error messages and recovery when API unavailable

## Architecture Philosophy
- **Content Preservation**: Never modify user's carefully crafted prompts
- **Quality First**: Store only complete, optimized prompts  
- **AI for Organization**: Use Claude API for categorization, not content changes
- **Privacy Security**: Multiple layers preventing private content leaks
- **Professional Standards**: Support sophisticated prompts with technical specifications

## Privacy-First Architecture
- **Physical separation**: Private prompts in git-ignored directory
- **Multiple protection layers**: .gitignore, directory structure, explicit flags
- **Enhanced content-based privacy analysis**: Claude evaluates prompt content for confidential info AND personal characteristics
- **Personal characterization detection**: Prompts containing user personality traits → PRIVATE
- **Clear privacy criteria**: Private = personal/confidential; Public = general-purpose tools
- **User confirmation**: Final privacy decision always with user

## Enhanced Data Model
```json
{
  "id": "uuid",
  "title": "Elite Strategic Performance Advisor",
  "content": "Original prompt content (never modified)",
  "category": "Business Strategy", 
  "tags": ["coaching", "performance", "strategy"],
  "private": false,
  "description": "Systems-level performance acceleration",
  "technical_notes": {
    "recommended_llm": "Claude 3.5 Sonnet",
    "temperature": 0.4,
    "max_tokens": "4000-6000",
    "additional_notes": []
  },
  "ai_analysis": {
    "complexity_level": "advanced",
    "privacy_reasoning": "Professional methodology, safe to share",
    "suggested_category": "Business Strategy",
    "suggested_tags": ["coaching", "performance"]
  },
  "created": "2025-09-24T...",
  "usage_count": 0
}
```

## Template Patterns Implemented

### From python-automation-template:
- ✅ Enhanced CLI patterns with professional status reporting
- ✅ Multi-file intelligence and user guidance patterns  
- ✅ Proper error handling and graceful exits
- ✅ Table formatting for data display
- ✅ Validation patterns for user input
- ✅ Professional documentation standards
- ✅ USER_START.md for quick setup
- ✅ Comprehensive .gitignore protecting private content

### Security & Privacy:
- ✅ Environment variables for API credentials
- ✅ Clear separation of public/private data
- ✅ No hardcoded secrets anywhere
- ✅ Enhanced .gitignore with multiple protection layers

## Common Patterns Used
- **Enhanced CLI helpers**: Professional status indicators (✅❌⚠️ℹ️🔄)
- **File management utilities**: Safe filename generation, directory creation
- **Error handling**: Graceful keyboard interrupt and validation
- **Table displays**: Proper formatting for prompt listings
- **Privacy management**: Change privacy settings between public/private

## Development Notes
- **Clean architecture**: No legacy code from problematic XML workflows
- **Quality focus**: Accept only optimized, complete prompts
- **User agency**: All AI suggestions are confirmable/modifiable by user
- **Preservation first**: Original prompt content never touched
- **Fallback support**: Graceful degradation when API unavailable

## Future Enhancements
- **Favorites system**: Quick access to most-used prompts (next priority)
- **Usage analytics**: Track prompt effectiveness
- **Enhanced search**: Advanced filtering and discovery
- **Export capabilities**: Professional sharing formats
- **Bulk operations**: Import/export prompt collections

## Usage Instructions for New Conversations
"I'm working on the ai-prompt-manager project. Please read CLAUDE_CONTEXT.md to understand the intelligent metadata extraction approach, privacy-first design, enhanced CLI patterns, and template compliance before proceeding."

## Testing Priority
1. **Metadata extraction**: Test with Elite Strategic Performance Advisor prompt
2. **Privacy classification**: Verify AI privacy analysis accuracy
3. **Technical parsing**: Confirm LLM/temperature/token extraction
4. **Category intelligence**: Test AI-suggested categorization
5. **User workflow**: End-to-end prompt addition experience

---
*Status: Template-aligned foundation ready for Favorites system implementation*  
*Architecture: Professional prompt management with content preservation focus*
