# AI Prompt Manager - Claude Context

## Project Overview
AI Prompt Manager - Professional-grade prompt storage and retrieval system focused on intelligent organization without content modification. Built using proven automation template patterns.

## Current Development Status
- **Phase:** Core Implementation Complete
- **Status:** Ready for feature enhancement (Favorites system next)
- **Approach:** Clean architecture eliminating problematic XML transformation workflows

## Architecture Philosophy
- **Content Preservation**: Never modify user's carefully crafted prompts
- **Quality First**: Store only complete, optimized prompts  
- **AI for Organization**: Use Claude API for categorization, not content changes
- **Privacy Security**: Multiple layers preventing private content leaks
- **Professional Standards**: Support sophisticated prompts with technical specifications

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
└── README.md                  # Professional documentation
```

## Key Features Implementation

### Intelligent Metadata Extraction
- **Enhanced title detection**: Parses multiple formats (markdown, JSON, role patterns)
- **Automatic title generation**: Uses Claude API when title not found
- **Technical specs parsing**: Extracts LLM recommendations, temperature, token limits
- **JSON structure support**: Handles structured prompts with purpose/role fields
- **AI categorization**: Uses Claude API to suggest categories and tags
- **Privacy analysis**: AI reasoning for public/private recommendations
- **Content preservation**: Zero modification of original prompt content
- **Intelligent defaults**: Suggests technical parameters based on prompt type

### Enhanced Data Model
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

### Privacy-First Architecture
- **Physical separation**: Private prompts in git-ignored directory
- **Multiple protection layers**: .gitignore, directory structure, explicit flags
- **Enhanced content-based privacy analysis**: Claude evaluates prompt content for both confidential info AND personal characteristics
- **Personal characterization detection**: Prompts containing user personality traits, individual challenges, or specific user contexts → PRIVATE
- **Clear privacy criteria**: Private = contains personal/confidential info OR reveals user characteristics; Public = general-purpose tools
- **User confirmation**: Final privacy decision always with user
- **Examples**: Generic coaching frameworks = PUBLIC; Coaching with embedded user traits = PRIVATE

### Professional CLI Interface
- **Enhanced menu patterns**: From automation template
- **Rich status indicators**: ✅❌⚠️ℹ️🔄 with consistent messaging
- **Table displays**: Proper formatting for prompt listings
- **Interactive detailed views**: Copy-to-clipboard, full content display
- **Privacy management**: Change privacy settings between public/private
- **Search functionality**: Full-text search across all metadata fields
- **Error handling**: Graceful keyboard interrupt and validation
- **Progress feedback**: Clear status updates during operations

## Template Patterns Implemented

### From python-automation-template:
- ✅ Enhanced CLI patterns with professional status reporting
- ✅ Multi-file intelligence and user guidance patterns  
- ✅ Proper error handling and graceful exits
- ✅ Table formatting for data display
- ✅ Validation patterns for user input

### Security & Privacy:
- ✅ Environment variables for API credentials
- ✅ Comprehensive .gitignore protecting private content
- ✅ Clear separation of public/private data
- ✅ No hardcoded secrets anywhere

## API Integration Details
- **Claude API**: Used only for metadata analysis, never content modification
- **Fallback support**: Graceful degradation when API unavailable
- **Rate limiting awareness**: Efficient API usage patterns
- **Error handling**: Professional error messages and recovery

## Development Workflow
- **Clean architecture**: No legacy code from problematic previous XML workflows
- **Quality focus**: Accept only optimized, complete prompts
- **User agency**: All AI suggestions are confirmable/modifiable by user
- **Preservation first**: Original prompt content never touched

## Future Enhancements
- **Favorites system**: Quick access to most-used prompts (next priority)
- **Usage analytics**: Track prompt effectiveness
- **Enhanced search**: Advanced filtering and discovery
- **Export capabilities**: Professional sharing formats
- **Bulk operations**: Import/export prompt collections

## Usage Instructions for New Conversations
"I'm working on ai-prompt-manager. Please read CLAUDE_CONTEXT.md to understand the architecture, intelligent metadata extraction approach, privacy-first design, and enhanced CLI patterns before proceeding."

## Testing Priority
1. **Metadata extraction**: Test with Elite Strategic Performance Advisor prompt
2. **Privacy classification**: Verify AI privacy analysis accuracy
3. **Technical parsing**: Confirm LLM/temperature/token extraction
4. **Category intelligence**: Test AI-suggested categorization
5. **User workflow**: End-to-end prompt addition experience

---
*Architecture: Clean system eliminating problematic XML transformation workflows*  
*Status: Ready for Favorites system implementation*
