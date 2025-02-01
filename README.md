# Bakesite

A refreshingly simple static site/blog generator. 

Markdown in. HTML out.

# Getting Started

```
pip install bakesite
```

Create a `content` directory with a `blog` directory that contains all your markdown files. And then create a `content/index.md` file. 

```
bakesite bake
```

And then 

```
bakesite serve
```

View the site on `http://localhost:8003`



### Yet Another Static Site Generator

While I used both Jekyll, Pelican and Hugo for different iterations of my personal blog, I always felt the solution to the simple problem of static site building was over-engineered.

If you look into the code bases of any other aforementioned projects, understanding, altering or contributing back is a daunting task. 

Why did it have to be so complicated? And how hard could it be to build?

## Acknowledgements

Thanks to a previous project by Sunaina Pai, Makesite, for providing the foundations of this project. 


