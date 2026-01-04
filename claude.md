# Bakesite Project Context

## Overview

Bakesite is a refreshingly simple static site generator built with Python. The philosophy is "Make the easy things simple, and the hard things possible." It was created as a reaction to over-engineered solutions like Jekyll, Pelican, and Hugo, with the goal of being simple to understand, alter, and contribute to.

In addition, it is Andrew's personal side project to hack around on. So if you are asked to plan code changes, but not write them, please keep that in mind!

**Core Purpose**: Convert Markdown files to HTML with minimal configuration and complexity.

**Target Users**: Developers who want a simple, fast workflow for publishing content (e.g., from Obsidian notes to blog posts).

## Project Structure

```
bakesite/
├── src/
│   ├── bakesite/
│   │   ├── __init__.py        # CLI entry point (Click-based)
│   │   ├── compile.py         # Core baking logic
│   │   ├── parameters.py      # Configuration loading
│   │   ├── server.py          # Local development server
│   │   ├── boilerplate.py     # Project initialization
│   │   ├── logging.py         # Logging utilities
│   │   ├── boilerplate/       # Template files for `bakesite init`
│   │   │   ├── bakesite.yaml
│   │   │   └── content/
│   │   └── layouts/
│   │       └── basic/         # HTML layout templates
│   └── tests/                 # Test suite
├── pyproject.toml             # Project metadata and dependencies
└── README.md                  # User-facing documentation
```

## Key Components

### CLI (`__init__.py`)
- Built with Click framework
- Three main commands:
  - `bakesite init` - Initialize a new site
  - `bakesite bake` - Generate static HTML from markdown
  - `bakesite serve` - Start local dev server (optional `--bake` flag)

### Core Logic (`compile.py`)
- Handles the main markdown-to-HTML conversion
- Processes front matter (YAML metadata)
- Renders Jinja2 templates
- Manages file I/O for the build process

### Configuration (`parameters.py`)
- Loads `bakesite.yaml` configuration
- Provides site-wide parameters to templates

### Server (`server.py`)
- Simple local HTTP server for development
- Default port: 8200

## Configuration

### `bakesite.yaml` Structure
```yaml
base_path: ""              # Site base path
subtitle: "..."            # Site subtitle
author: "..."              # Default author
site_url: "..."            # Full site URL
current_year: 2025         # Year for footer/copyright
github_url: "..."          # Social links
linkedin_url: "..."
gtag_id: "..."             # Google Analytics
cname: "..."               # Custom domain for GitHub Pages
```

### Front Matter
Markdown files support YAML front matter:
```yaml
---
title: Post Title
author: Author Name
render: true              # Enable Jinja2 rendering in content
---
```

## Dependencies

**Runtime**:
- `click>=8.1.8` - CLI framework
- `jinja2>=3.1.5` - Template engine
- `markdown-it-py[plugins]` - Markdown parser
- `pyyaml>=6.0.2` - YAML configuration

**Development**:
- `pytest>=8.3.4` + `pytest-cov>=6.0.0` - Testing (89% coverage requirement)
- `ruff>=0.9.6` - Linting and formatting
- `pre-commit>=4.1.0` - Git hooks

## Development Workflow

1. **Make changes** to source files in `src/bakesite/`
2. **Run tests**: `pytest` (must maintain 89% coverage)
3. **Lint**: `ruff check .`
4. **Format**: `ruff format .`
5. **Pre-commit hooks**: Automatically run on commit

## Code Conventions

- **Simplicity First**: Keep code simple and readable. Avoid over-engineering.
- **Python 3.9+**: Support modern Python (3.9-3.13)
- **Minimal Dependencies**: Only essential packages
- **No Reactive HTML**: This is intentionally a simple, static-only generator

## Testing

- Test files in `src/tests/`
- Coverage requirement: 89% (omits `logging.py`)
- Run with: `pytest --cov=bakesite --cov-report=term`

### Test Coverage by Module
- `test_cli.py` - CLI commands
- `test_compile.py` / `test_bake.py` - Core compilation
- `test_content.py` - Content processing
- `test_render.py` - Template rendering
- `test_parameters.py` - Configuration loading
- `test_boilerplate.py` - Project initialization

## Build System

- Uses `uv_build>=0.9.2,<0.10.0` as build backend
- Entry point: `bakesite = "bakesite:main"`
- Version: 0.6.1

## Important Notes

- **Not for reactive HTML**: If you need reactive components, this isn't the right tool
- **Obsidian-friendly**: Designed to work well with Obsidian note workflows
- **Built to last**: Prioritizes longevity and simplicity over features
- **MIT Licensed**: Open source and hackable

## When Contributing

- Keep it simple - complexity is the enemy
- Maintain test coverage at 89%+
- Follow the existing patterns (Click for CLI, Jinja2 for templates)
- Document user-facing features in README.md
- Remember: "Make the easy things simple, and the hard things possible"
