import datetime
import glob
import logging
import os
import pathlib
import re
import shutil

from jinja2 import Environment, FileSystemLoader
from markdown_it import MarkdownIt


current_path = pathlib.Path(__file__).parent
env = Environment(loader=FileSystemLoader(f"{current_path}/layouts/basic/templates"))

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
        md = MarkdownIt("js-default", {"breaks": True, "html": True})
        text = md.render(text)

    # Update the dictionary with content and RFC 2822 date.
    content.update({"content": text, "rfc_2822_date": rfc_2822_format(content["date"])})

    return content


def rename_file_with_slug(template, **params):
    """Replace placeholders in template with values from params."""
    return re.sub(
        r"{{\s*([^}\s]+)\s*}}",
        lambda match: str(params.get(match.group(1), match.group(0))),
        template,
    )


def make_pages(
    src,
    dst,
    template,
    write_file=True,
    **params,
):
    """Generate pages from page content."""
    items = []

    for src_path in glob.glob(src):
        content = read_content(src_path)

        page_params = dict(params, **content)

        # Populate placeholders in content if content-rendering is enabled.
        if page_params.get("render") == "yes":
            rendered_content = rename_file_with_slug(
                page_params["content"], **page_params
            )
            page_params["content"] = rendered_content
            content["content"] = rendered_content
        items.append(content)
        params["content"] = content["content"]
        output = env.get_template(template).render(**page_params)
        dst_path = rename_file_with_slug(dst, **page_params)
        logger.info(f"Rendering {src_path} => {dst_path} ...")
        if write_file:
            fwrite(dst_path, output)

    return sorted(items, key=lambda x: x["date"], reverse=True)


def make_list(
    posts, dst, list_item_template="item.html", list_template="list.html", **params
):
    """Generate list page for a blog."""
    items = []
    for post in posts:
        item_params = dict(params, **post)
        item_params["summary"] = truncate(post["content"])
        item = env.get_template(list_item_template).render(**item_params)

        items.append(item)

    params["content"] = "".join(items)
    dst_path = rename_file_with_slug(dst, **params)
    output = env.get_template(list_template).render(**params)

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

    # Create site pages.
    make_pages(
        "content/index.md", f"{target_dir}/index.html", template="page.html", **params
    )

    # Create blogs.
    blog_posts = make_pages(
        "content/blog/*.md",
        target_dir + "/blog/{{ slug }}/index.html",
        blog="blog",
        template="post.html",
        **params,
    )

    # # Create blog list pages.
    make_list(
        blog_posts,
        f"{target_dir}/blog/index.html",
        blog="blog",
        title="Blog",
        **params,
    )

    # # Create RSS feeds.
    make_list(
        blog_posts,
        f"{target_dir}/blog/rss.xml",
        list_item_template="item.xml",
        list_template="feed.xml",
        blog="blog",
        title="Blog",
        **params,
    )

    # Fix attachments
    if os.path.isdir("content/blog/attachment"):
        shutil.copytree("content/blog/attachment", f"{target_dir}/attachment")
    # Prefix all img src with /
    for src_path in glob.glob(f"{target_dir}/blog/*/index.html"):
        content = fread(src_path)
        content = content.replace('src="attachment/', 'src="/attachment/')
        fwrite(src_path, content)
