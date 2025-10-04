# Bakesite :pie:

A refreshingly simple static site generator.

Write in Markdown, get HTML out.

# Installation
Install Bakesite using pip:

```
pip install bakesite
```

# Getting Started
To create a new site, run the following command:

```
bakesite init
```

This will create a couple of files, including the content directory and the `bakesite.yaml` file necessary for building the site.

To bake the site and view it locally, run

```
bakesite serve --bake
```

This will generate the static files and start a local server.

Then visit `http://localhost:8200`

## `bakesite.yaml` Configuration

Configure your site by editing the `bakesite.yaml` file in your project root:

```yaml
# Base path for the site (leave empty for root directory)
base_path: ""

# Site metadata
subtitle: "My Awesome Website"
author: "John Doe"
site_url: "https://example.com"
current_year: 2025

# Social links
github_url: "https://github.com/yourusername"
linkedin_url: "https://www.linkedin.com/in/yourprofile"

# Analytics
gtag_id: "G-XXXXXXXXXX"

# Custom domain (optional)
cname: "yourcustomdomain.com"
```

## Front Matter

Add metadata to your markdown files using YAML front matter at the top of each file:

```markdown
---
title: My First Blog Post
author: Jane Doe
render: true
---

Your content goes here...
```

### Available Front Matter Fields

- `title`: The title of your post or page
- `author`: Override the default author for this specific post
- `render`: Set to `true` to enable Jinja2 template rendering within your markdown content, allowing you to use template variables and parameters
- Any custom fields you define will be available in your templates

### Example with Template Rendering

When `render: true` is set, you can use template variables in your markdown:

```markdown
---
title: About {{ author }}
render: true
---

Welcome to {{ site_url }}! This site was built in {{ current_year }}.
```

### Motivation

While I have used Jekyll, Pelican and Hugo for different iterations of my personal blog, I always felt the solution to the simple problem of static site building was over-engineered.

If you look into the code bases of these projects, understanding, altering or contributing back is a daunting task.

Why did it have to be so complicated? And how hard could it be to build?

In addition, I wanted a workflow for publishing posts from my Obsidian notes to be simple and fast.

## Acknowledgements

Thanks to a previous project by Sunaina Pai, Makesite, for providing the foundations of this project.

## Philosophy

> Make the easy things simple, and the hard things possible.

> This site was built to last.

## A Heads Up

If you are looking for a site generator with reactive html elements, this project is most likely not for you.
