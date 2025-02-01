import logging
import os
import pathlib
import shutil
import re
import glob
import datetime

logger = logging.getLogger(__name__)


def fread(filename):
    """Read file and close the file."""
    with open(filename, "r") as f:
        return f.read()


def fwrite(filename, text):
    """Write content to file and close the file."""
    basedir = os.path.dirname(filename)
    if not os.path.isdir(basedir):
        os.makedirs(basedir)

    with open(filename, "w") as f:
        f.write(text)


def truncate(text, words=25):
    """Remove tags and truncate text to the specified number of words."""
    return " ".join(re.sub("(?s)<.*?>", " ", text).split()[:words])


def read_headers(text):
    """Parse headers in text and yield (key, value, end-index) tuples."""
    for match in re.finditer(r"\s*<!--\s*(.+?)\s*:\s*(.+?)\s*-->\s*|.+", text):
        if not match.group(1):
            break
        yield match.group(1), match.group(2), match.end()


def rfc_2822_format(date_str):
    """Convert yyyy-mm-dd date string to RFC 2822 format date string."""
    d = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return d.strftime("%a, %d %b %Y %H:%M:%S +0000")


def read_content(filename):
    """Read content and metadata from file into a dictionary."""
    # Read file content.
    text = fread(filename)

    # Read metadata and save it in a dictionary.
    date_slug = os.path.basename(filename).split(".")[0]
    match = re.search(r"^(?:(\d\d\d\d-\d\d-\d\d)-)?(.+)$", date_slug)
    content = {
        "date": match.group(1) or "1970-01-01",
        "slug": match.group(2),
    }

    # Read headers.
    end = 0
    for key, val, end in read_headers(text):
        content[key] = val

    # Separate content from headers.
    text = text[end:]

    # Convert Markdown content to HTML.
    if filename.endswith((".md", ".mkd", ".mkdn", ".mdown", ".markdown")):
        try:
            from markdown_it import MarkdownIt

            md = MarkdownIt("js-default", {"breaks": True, "html": True})
            text = md.render(text)
        except ImportError:
            logger.warning(f"Cannot render Markdown in {filename}", exc_info=True)

    # Update the dictionary with content and RFC 2822 date.
    content.update({"content": text, "rfc_2822_date": rfc_2822_format(content["date"])})

    return content


def render(template, **params):
    """Replace placeholders in template with values from params."""
    return re.sub(
        r"{{\s*([^}\s]+)\s*}}",
        lambda match: str(params.get(match.group(1), match.group(0))),
        template,
    )


def make_pages(src, dst, layout, **params):
    """Generate pages from page content."""
    items = []

    for src_path in glob.glob(src):
        content = read_content(src_path)

        page_params = dict(params, **content)

        # Populate placeholders in content if content-rendering is enabled.
        if page_params.get("render") == "yes":
            rendered_content = render(page_params["content"], **page_params)
            page_params["content"] = rendered_content
            content["content"] = rendered_content

        items.append(content)

        dst_path = render(dst, **page_params)
        output = render(layout, **page_params)

        logger.info(f"Rendering {src_path} => {dst_path} ...")
        fwrite(dst_path, output)

    return sorted(items, key=lambda x: x["date"], reverse=True)


def make_list(posts, dst, list_layout, item_layout, **params):
    """Generate list page for a blog."""
    items = []
    for post in posts:
        item_params = dict(params, **post)
        item_params["summary"] = truncate(post["content"])
        item = render(item_layout, **item_params)
        items.append(item)

    params["content"] = "".join(items)
    dst_path = render(dst, **params)
    output = render(list_layout, **params)

    logger.info(f"Rendering list => {dst_path} ...")
    fwrite(dst_path, output)


def write_cname(params, target_dir):
    with open(f"{target_dir}/CNAME", "w") as f:
        f.write(params["cname"])


def bake(params, target_dir="_site"):
    # Create a new _site directory from scratch.
    if os.path.isdir(f"{target_dir}"):
        shutil.rmtree(f"{target_dir}")

    current_path = pathlib.Path(__file__).parent
    shutil.copytree(f"{current_path}/layouts/basic/static", f"{target_dir}")
    write_cname(params, target_dir)
    open(f"{target_dir}/.nojekyll", "a").close()

    # Load layouts.
    page_layout = fread(f"{current_path}/layouts/basic/templates/page.html")
    post_layout = fread(f"{current_path}/layouts/basic/templates/post.html")
    list_layout = fread(f"{current_path}/layouts/basic/templates/list.html")
    item_layout = fread(f"{current_path}/layouts/basic/templates/item.html")
    feed_xml = fread(f"{current_path}/layouts/basic/templates/feed.xml")
    item_xml = fread(f"{current_path}/layouts/basic/templates/item.xml")

    # Combine layouts to form final layouts.
    post_layout = render(page_layout, content=post_layout)
    list_layout = render(page_layout, content=list_layout)
    # Create site pages.
    make_pages("content/index.md", f"{target_dir}/index.html", page_layout, **params)
    make_pages(
        "content/[!_]*.html",
        target_dir + "{{ slug }}/index.html",
        page_layout,
        **params,
    )

    # Create blogs.
    blog_posts = make_pages(
        "content/blog/*.md",
        target_dir + "/blog/{{ slug }}/index.html",
        post_layout,
        blog="blog",
        **params,
    )

    # Create blog list pages.
    make_list(
        blog_posts,
        f"{target_dir}/blog/index.html",
        list_layout,
        item_layout,
        blog="blog",
        title="Blog",
        **params,
    )

    # Create RSS feeds.
    make_list(
        blog_posts,
        f"{target_dir}/blog/rss.xml",
        feed_xml,
        item_xml,
        blog="blog",
        title="Blog",
        **params,
    )

    # Fix attachments
    shutil.copytree("content/blog/attachment", f"{target_dir}/attachment")
    # Prefix all img src with /
    for src_path in glob.glob(f"{target_dir}/blog/*/index.html"):
        content = fread(src_path)
        content = content.replace('src="attachment/', 'src="/attachment/')
        fwrite(src_path, content)
