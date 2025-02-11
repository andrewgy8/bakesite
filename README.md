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

This will create a couple of files, including the content directory and the `settings.py` file necessary for building the site.

To bake the site and view it locally, run

```
bakesite serve --bake
```

This will generate the static files and start a local server.

Then visit `http://localhost:8200`


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
