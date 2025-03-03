import datetime
import glob
import logging
import os
import pathlib
import re
import shutil

from jinja2 import Environment, FileSystemLoader
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
import yaml


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
    tokens = markdown_client().parse(text)
    front_matter_token = next((t for t in tokens if t.type == "front_matter"), None)
    default_headers = {"author": "Admin"}

    if front_matter_token:
        front_matter_content = front_matter_token.content
        return yaml.safe_load(front_matter_content)
    else:
        return default_headers


def rfc_2822_format(date_str):
    """Convert yyyy-mm-dd date string to RFC 2822 format date string."""
    d = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return d.strftime("%a, %d %b %Y %H:%M:%S +0000")


def markdown_client():
    md = MarkdownIt("js-default", {"breaks": True, "html": True})
    md.use(front_matter_plugin)
    return md


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
    headers = read_headers(text)

    content.update(headers)

    # Convert Markdown content to HTML.
    if filename.endswith((".md", ".mkd", ".mkdn", ".mdown", ".markdown")):
        text = markdown_client().render(text)

    # Update the dictionary with content and RFC 2822 date.
    content.update({"content": text, "rfc_2822_date": rfc_2822_format(content["date"])})

    return content


def format_file_path(path_str, **params):
    """Replace placeholders in template with values from params."""
    return path_str.format(**params)


def make_pages(
    src,
    dst,
    template,
    **params,
):
    """Generate pages from page content."""
    items = []

    for src_path in glob.glob(src):
        content = read_content(src_path)
        content.update(params)

        items.append(content)

        # Allow content to be rendered with template parameters and headers
        if content.get("render"):
            content["content"] = env.from_string(content["content"]).render(**content)
        output = env.get_template(template).render(**content)
        dst_path = format_file_path(dst, **content)
        logger.info(f"Rendering {src_path} => {dst_path} ...")
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
    dst_path = format_file_path(dst, **params)
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

    for path in glob.glob("content/*"):
        if os.path.isdir(path):
            dir_name = os.path.basename(path)
            blog_posts = make_pages(
                f"content/{dir_name}/*.md",
                target_dir + f"/{dir_name}" + "/{slug}/index.html",
                blog=dir_name,
                template="post.html",
                **params,
            )
            make_list(
                blog_posts,
                f"{target_dir}/{dir_name}/index.html",
                blog=f"{dir_name}",
                title=f"{dir_name.capitalize()}",
                **params,
            )
            make_list(
                blog_posts,
                f"{target_dir}/{dir_name}/rss.xml",
                list_item_template="item.xml",
                list_template="feed.xml",
                blog=f"{dir_name}",
                title=f"{dir_name.capitalize()}",
                **params,
            )
        else:
            file_name = os.path.basename(path).split(".")[0]
            make_pages(
                str(path),
                f"{target_dir}/{file_name}.html",
                template="page.html",
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
