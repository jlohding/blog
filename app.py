import datetime as dt
from flask import Flask, render_template, redirect
from flask_flatpages import FlatPages

app = Flask(__name__)
app.config['FLATPAGES_EXTENSION'] = '.html' #'.md'
pages = FlatPages(app)

@app.route("/")
@app.route("/home")
def home_page():
    posts = [x for x in pages if "date" in x.meta]
    sorted_pages=sorted(posts, reverse=True, key=lambda page: dt.datetime.strptime(page.meta["date"], "%d %b %Y"))
    return render_template("home.html", pages=sorted_pages)
 
@app.route("/projects")
def projects_page():
    return render_template("projects.html")

@app.route("/blog/")
@app.route("/blog/<filter_tag>")
def blog_page(filter_tag=None):
    posts = [x for x in pages if "date" in x.meta]
    sorted_pages=sorted(posts, reverse=True, key=lambda page: dt.datetime.strptime(page.meta["date"], "%d %b %Y"))

    if filter_tag:
        filter_pages = [page for page in sorted_pages if filter_tag in page.meta["tags"] or filter_tag in page.meta["date"]]
    else:
        filter_pages = sorted_pages

    return render_template("blog.html", pages=sorted_pages, filter_pages=filter_pages)

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/blog/<path:path>.html")
def blog_post(path):
    page = pages.get_or_404(path)
    return render_template("post.html", page=page)

@app.route("/external_links/<site>")
def ext_links(site):
    sites = {
        "github": "https://www.github.com/jlohding",
        "arbitrade": "https://www.github.com/jlohding/arbitrade",
        "blog_github": "https://www.github.com/jlohding/blog",
        "linkedin": "https://www.linkedin.com/in/jerryloh2000",
    }
    return redirect(sites[site], code=302)

if __name__ == "__main__":
    app.run(debug=False, use_reloader=True)