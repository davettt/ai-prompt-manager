# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- (Future changes go here)

### Changed
- (Future changes go here)

### Fixed
- (Future changes go here)

## [1.3.0] - 2025-10-09

### Added
- **Rich Markdown Rendering**: Beautiful formatted display when viewing full prompts
  - Headers, bold, lists, and code blocks render properly
  - Raw markdown preserved for clipboard and Claude Project exports
  - Graceful fallback if Rich not installed
- **Delete Command**: Remove prompts directly from browser with `[number]d`
  - Confirmation dialog with warning panel
  - File removed from disk safely
- **Edit Command**: Modify prompt metadata with `[number]e`
  - Edit title, category, tags, privacy, and description
  - Clear display of current values
  - Privacy changes automatically move files between public/private
- **Readline Support**: Arrow keys now work properly when entering prompts
  - Navigate and edit text naturally during input
  - Standard text editor behavior

### Changed
- Consistent Rich formatting for headers and panels
- Edit input uses standard input() for better UX (no backspace issues)
- Browse commands section includes new delete and edit options

### Fixed
- Backspace no longer deletes prompt labels during edit
- Input fields work naturally with arrow keys and standard keyboard shortcuts

## [1.2.0] - 2025-10-09

### Added
- Development tools: Black (formatter), Ruff (linter), mypy (type checker)
- Security scanning with bandit
- Pre-commit hooks for automatic code quality checks
- Additional pre-commit hooks for enhanced safety:
  - detect-private-key (prevents committing SSH/GPG keys)
  - check-case-conflict (cross-platform filename safety)
  - check-toml (validates pyproject.toml syntax)
  - check-ast (validates Python syntax)
  - mixed-line-ending (ensures consistent line endings)
- Tool configuration in pyproject.toml
- Development dependencies in requirements-dev.txt
- Complete .claude/ structure with project guide and workflow documentation

### Changed
- Code formatted with Black for consistency
- Linting issues fixed with Ruff
- Updated development workflow in .claude/workflow/code_standards.md
- Added timeout to API requests for better security

## [1.1.0] - 2025-10-09

### Added
- **Favorites System**: Star your most-used prompts for quick access
  - Toggle favorites with `⭐` indicator in browser
  - Quick commands: `[number]fav` and `[number]unfav`
  - Filter favorites with `⭐` or "favorites" search
  - Persistent favorite status across sessions
- **Claude Project Export**: Format and copy prompts for Claude Projects
  - New command: `[number]p` to copy formatted for Claude Project
  - Includes setup instructions and proper formatting
  - Simplifies Claude Project custom instructions workflow
- **Enhanced Search with OR Logic**: Smart multi-term search with relevance scoring
  - Search matches ANY term (not requiring all terms)
  - Relevance scoring prioritizes: title > category > tags > discovery text
  - Smart refinement suggestions when too many results
  - Better discovery with scored results
- **Improved Browse UX**: Interactive inline expansion
  - Press number to toggle detailed info
  - Clear screen display for cleaner interface
  - Quick actions visible in expanded view
  - Smooth navigation without page breaks

### Changed
- Search now uses OR logic instead of AND (matches any term, not all terms)
- Browser displays relevance-scored results (most relevant first)
- Enhanced privacy workflow with clearer warnings when changing settings
- Better discovery metadata display in expanded prompts

### Fixed
- Discovery information now displays correctly in inline expansion
- Technical notes (LLM, temperature, tokens) shown in expanded view

## [1.0.0] - 2025-09-27

### Added
- Initial release with core prompt management functionality
- Intelligent metadata extraction using Claude AI
- Privacy-first architecture with public/private separation
- Professional CLI interface with interactive menus
- Rich metadata storage (title, category, tags, technical notes)
- AI-powered privacy analysis and categorization
- Content preservation (never modifies user prompts)
- Search and browse functionality
- Safe operations with preview before saving

### Features
- Add new prompts with AI analysis
- Browse all prompts with category organization
- Search prompts by title, category, content, or tags
- Copy prompts to clipboard
- Change privacy settings (public ↔ private)
- Delete prompts with confirmation
- View full prompt content and metadata

### Privacy & Security
- Physical separation of public/private prompts
- Git-ignored private directory
- Multiple protection layers in .gitignore
- AI content-based privacy analysis
- User confirmation for all privacy changes

---

## Version Format

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version (X.0.0): Incompatible API changes or breaking changes
- **MINOR** version (0.X.0): New functionality in a backward compatible manner
- **PATCH** version (0.0.X): Backward compatible bug fixes

### Breaking Changes
Changes that require users to modify their workflow or data structure are marked as **BREAKING** in the changelog.

---

[1.3.0]: https://github.com/[username]/ai-prompt-manager/releases/tag/v1.3.0
[1.2.0]: https://github.com/[username]/ai-prompt-manager/releases/tag/v1.2.0
[1.1.0]: https://github.com/[username]/ai-prompt-manager/releases/tag/v1.1.0
[1.0.0]: https://github.com/[username]/ai-prompt-manager/releases/tag/v1.0.0
