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

### base_path
**Type:** `string`
**Default:** `""`
The base path for the site. Leave empty for the root directory.

### subtitle
**Type:** `string`
**Example:** `"My Awesome Website"`
A short descriptive subtitle for the site.

### author
**Type:** `string`
**Example:** `"John Doe"`
The name of the site author or owner.

### site_url
**Type:** `string`
**Example:** `"https://example.com"`
The full URL of the site.

### current_year
**Type:** `integer`
**Default:** `2025`
The current year for copyright or display purposes.

### github_url
**Type:** `string`
**Example:** `"https://github.com/yourusername"`
Link to the author's GitHub profile.

### linkedin_url
**Type:** `string`
**Example:** `"https://www.linkedin.com/in/yourprofile"`
Link to the author's LinkedIn profile.

### gtag_id
**Type:** `string`
**Example:** `"G-XXXXXXXXXX"`
Google Analytics tracking ID.

### cname
**Type:** `string`
**Example:** `"yourcustomdomain.com"`
Custom domain name for the site, if applicable.


### Motivation

While I have used Jekyll, Pelican and Hugo for different iterations of my personal blog, I always felt the solution to the simple problem of static site building was over-engineered.

If you look into the code bases of these projects, understanding, altering or contributing back is a daunting task.

Why did it have to be so complicated? And how hard could it be to build?

In addition, I wanted a workflow for publishing posts from my Obsidian notes to be simple and fast.

## Acknowledgements

Thanks to a previous project by Sunaina Pai, Makesite, for providing the foundations of this project.

## Philosophy

> Make the easy things simple, and the hard things possible.

## A Heads Up

If you are looking for a site generator with reactive html elements, this project is most likely not for you.
