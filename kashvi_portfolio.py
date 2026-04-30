"""
kashvi_portfolio.py
====================
Python template system for Kashvi Shervegar's portfolio website.

Usage
-----
python kashvi_portfolio.py           # Build all pages
python kashvi_portfolio.py --new     # Interactive wizard to add a new project

The script reads project data from projects/project_data.py and regenerates
every HTML page. New projects appear at the TOP of the landing page scroll.
"""

import os
import shutil
import sys
import argparse
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
OUT_DIR    = BASE_DIR  # output HTML files sit in the root portfolio folder

# ── Project registry ───────────────────────────────────────────────────────
# Each dict represents one project. Add new ones at the TOP of this list to
# make them appear first on the landing page. The generator also creates an
# individual <slug>.html for each project.

PROJECTS = [
    # ── Add new projects at the TOP of this list — newest appears first ──
    {
        "slug":        "project-four",
        "title":       "Project Four",
        "description": "Project description will go here.",
        "year":        "2025",
        "tags":        [],
        "hero":        "",
        "visuals":     [{"type": "image", "src": "", "caption": "Visual 1"}],
    },
    {
        "slug":        "project-three",
        "title":       "Project Three",
        "description": "Project description will go here.",
        "year":        "2025",
        "tags":        [],
        "hero":        "",
        "visuals":     [{"type": "image", "src": "", "caption": "Visual 1"}],
    },
    {
        "slug":        "project-two",
        "title":       "Project Two",
        "description": "Project description will go here.",
        "year":        "2025",
        "tags":        [],
        "hero":        "",
        "visuals":     [{"type": "image", "src": "", "caption": "Visual 1"}],
    },
    {
        "slug":        "project-one",
        "title":       "Project One",
        "description": "Project Description will go here. Anything that will describe "
                       "this project briefly and explain my process in some way.",
        "year":        "2025",
        "tags":        ["Publication Design", "Typography"],
        "hero":        "",
        "visuals": [
            {"type": "image", "src": "", "caption": "Visual 1"},
            {"type": "image", "src": "", "caption": "Visual 2"},
        ],
    },
    # ── Add more projects above this line ──
]

# ── Shared HTML snippets ────────────────────────────────────────────────────

def _nav_header(active: str = "") -> str:
    """
    Returns the site-wide <header> HTML.
    active: "about" | "sidequests" | "" (home)
    On the landing page the bio text replaces the right nav.
    On interior pages the right side shows the nav links.
    """
    is_landing = (active == "home")

    left_nav = ""  # landing page shows nav inline with logo
    right_content = ""

    if is_landing:
        left_nav = """
        <nav class="header-nav-inline">
          <a href="about.html" data-nav>ABOUT</a>
          <a href="sidequests.html" data-nav>SIDE QUESTS</a>
        </nav>"""
        right_content = """
        <p class="header-bio">
          Kashvi Shervegar is from Bangalore, now based in New York City.<br>
          She is a multidisciplinary designer who focuses on Publication Design, Motion &amp; typography.
        </p>"""
    else:
        right_content = """
        <nav class="header-nav-right">
          <a href="about.html" data-nav {about_active}>ABOUT</a>
          <a href="sidequests.html" data-nav {sq_active}>SIDE QUESTS</a>
        </nav>""".format(
            about_active='class="active"' if active == "about" else "",
            sq_active='class="active"' if active == "sidequests" else "",
        )

    return f"""
  <header class="site-header">
    <div class="header-inner">
      <div class="header-left">
        <a href="index.html" class="logo-link" aria-label="Home">
          <span class="logo-text">k</span>
        </a>
        {left_nav}
      </div>
      <div class="header-right">
        {right_content}
      </div>
    </div>
  </header>"""


def _footer() -> str:
    return """
  <footer class="site-footer">
    <div class="footer-left">
      <a href="mailto:kashvi.shervegar@gmail.com">kashvi.shervegar@gmail.com</a><br>
      All Work On Site &copy; Kashvi Shervegar 2026
    </div>
  </footer>"""


def _html_shell(title: str, body: str, extra_css: str = "", body_class: str = "") -> str:
    cls = f' class="{body_class}"' if body_class else ""
    # Landing page is full-viewport; interior pages use a max-width wrapper
    wrap_open  = "" if body_class == "landing" else '<div class="site-wrapper">'
    wrap_close = "" if body_class == "landing" else "</div>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — Kashvi Shervegar</title>
  <link rel="stylesheet" href="static/css/style.css" />
  {extra_css}
</head>
<body{cls}>
{wrap_open}
{body}
{wrap_close}
<script src="static/js/main.js"></script>
</body>
</html>"""


# ── Media helper ────────────────────────────────────────────────────────────

def _media_or_placeholder(src: str, alt: str = "", placeholder_label: str = "Visual",
                           extra_class: str = "", mime_hint: str = "") -> str:
    """Return an <img>, <video>, or placeholder div."""
    if not src:
        return f'<div class="visual-placeholder {extra_class}"><span>{placeholder_label}</span></div>'

    ext = Path(src).suffix.lower()
    if ext in (".mp4", ".webm", ".mov"):
        return f'<video src="{src}" autoplay loop muted playsinline class="{extra_class}"></video>'
    elif ext in (".gif",):
        return f'<img src="{src}" alt="{alt}" class="{extra_class}" />'
    else:
        return f'<img src="{src}" alt="{alt}" class="{extra_class}" />'


# ── Landing page ────────────────────────────────────────────────────────────

def build_index() -> str:
    project_previews_html = ""
    for p in PROJECTS:
        hero_html = _media_or_placeholder(
            p.get("hero", ""),
            alt=p["title"],
            placeholder_label=p["title"],
        )
        project_previews_html += f"""
      <div class="project-preview">
        <a href="{p['slug']}.html" class="project-preview-link">
          {hero_html}
          <span class="project-preview-label">{p['title']}</span>
        </a>
      </div>"""

    body = f"""
  <!-- LANDING: full-viewport two-panel layout -->
  <div class="landing-page">

    <!-- LEFT PANEL: fixed, never scrolls, shows everything -->
    <aside class="landing-panel-left">

      <div class="lp-header">
        <a href="index.html" class="logo-link" aria-label="Home">
          <span class="logo-text">k</span>
        </a>
        <nav class="lp-nav">
          <a href="about.html">ABOUT</a>
          <a href="sidequests.html">SIDE QUESTS</a>
        </nav>
      </div>

      <div class="lp-center">
        <div class="animation-container" data-slot="theo-animation">
          <!--
            Option A: <img src="static/images/theo.gif" alt="Theo the cat" />
            Option B: <video autoplay loop muted playsinline><source src="static/images/theo.mp4" type="video/mp4" /></video>
            Option C (frame-by-frame):
              <img class="frame active" src="static/images/theo_01.png" alt="" />
              <img class="frame" src="static/images/theo_02.png" alt="" />
          -->
          <p class="animation-placeholder-text">(small stop motion<br>illustration of my cat Theo<br>will be inserted here)</p>
        </div>
        <p class="scroll-hint">Scroll to make Theo move</p>
      </div>

      <div class="lp-footer">
        <a href="mailto:kashvi.shervegar@gmail.com">kashvi.shervegar@gmail.com</a>
        <span>All Work On Site &copy; Kashvi Shervegar 2026</span>
      </div>

    </aside>

    <!-- RIGHT PANEL: bio strip at top, projects scroll below -->
    <div class="landing-panel-right">

      <div class="lp-bio">
        <p>Kashvi Shervegar is from Bangalore, now based in New York City.<br>
        She is a multidisciplinary designer who focuses on Publication Design, Motion &amp; typography.</p>
      </div>

      <div class="lp-projects">
        {project_previews_html}
      </div>

    </div>

  </div>"""

    return _html_shell("Portfolio", body, body_class="landing")


# ── Project page ─────────────────────────────────────────────────────────────

def build_project_page(p: dict) -> str:
    visuals_html = ""
    for i, vis in enumerate(p.get("visuals", [])):
        label = vis.get("caption", f"Visual {i+1}")
        media = _media_or_placeholder(
            vis.get("src", ""),
            alt=label,
            placeholder_label=label,
        )
        visuals_html += f'<div class="visual-item">{media}</div>\n'

    if not visuals_html:
        visuals_html = '<div class="visual-item"><div class="visual-placeholder"><span>Visuals coming soon</span></div></div>'

    tags_html = ""
    if p.get("tags"):
        tags_html = "".join(f"<span>{t}</span>" for t in p["tags"])

    body = f"""
  {_nav_header()}
  <main class="site-main">
    <div class="project-page-layout">

      <!-- LEFT: title + description (sticky) -->
      <div class="project-info">
        <h1 class="project-title">{p['title']}</h1>
        <p class="project-description">{p['description']}</p>
        <div class="project-meta">
          {"<span>" + p.get("year","") + "</span>" if p.get("year") else ""}
          {tags_html}
        </div>
      </div>

      <!-- RIGHT: visuals scroll -->
      <div class="project-visuals">
        {visuals_html}
      </div>

    </div>
  </main>
  {_footer()}"""

    return _html_shell(p["title"], body, body_class="interior")


# ── About page ──────────────────────────────────────────────────────────────

def build_about() -> str:
    body = f"""
  {_nav_header("about")}
  <main class="site-main">
    <div class="about-layout">

      <!-- LEFT: photo -->
      <div class="about-photo-col">
        <img
          src="static/images/self.png"
          alt="Kashvi Shervegar"
          class="about-photo"
        />
      </div>

      <!-- RIGHT: bio + links -->
      <div class="about-text-col">
        <div class="about-bio">
          <p>
            <strong>Kashvi Shervegar</strong> is a visual designer from Bangalore, India,
            currently based in New York City.
          </p>
          <p>
            Her practice begins with how she sees: stories that unfold through image,
            rhythm, and material. She works across print and digital forms, crafting
            handmade publications and coded websites that carry traces of both touch
            and technology. Drawn to the timeless practice of traditional crafts like
            knitting and the layered textures of music and motion, she weaves together
            the sensory and the structural.
          </p>
          <p>
            In a time when the hands-on is fading, Kashvi leans into code and craft
            alike&mdash;preserving what is tactile, while embracing what is evolving.
          </p>
        </div>

        <div class="about-links">
          <a href="mailto:kashvi.shervegar@gmail.com">Email</a>
          <a href="https://www.instagram.com/kashmakesart/" target="_blank" rel="noopener">Instagram</a>
          <a href="https://www.linkedin.com/in/kashvi-shervegar/" target="_blank" rel="noopener">LinkedIn</a>
        </div>

        <div class="about-resume">
          <a href="static/files/kashvi_shervegar_resume.pdf" target="_blank">Download resume here</a>
        </div>
      </div>

    </div>
  </main>
  <footer class="about-footer">
    <p>All Work On Site &copy; Kashvi Shervegar 2026</p>
  </footer>"""

    return _html_shell("About", body, body_class="interior")


# ── Side Quests page ─────────────────────────────────────────────────────────

# Add side quest items here. Each is a dict: {"src": "...", "caption": "..."}
SIDE_QUESTS = [
    {"src": "", "caption": "Side Quest 1"},
    {"src": "", "caption": "Side Quest 2"},
    {"src": "", "caption": "Side Quest 3"},
    {"src": "", "caption": "Side Quest 4"},
    # Add more…
]


def build_sidequests() -> str:
    items_html = ""
    for sq in SIDE_QUESTS:
        media = _media_or_placeholder(sq.get("src", ""), placeholder_label=sq.get("caption", ""))
        caption = f'<p class="sidequest-caption">{sq["caption"]}</p>' if sq.get("caption") else ""
        items_html += f"""
      <div class="sidequest-item">
        {media}
        {caption}
      </div>"""

    body = f"""
  {_nav_header("sidequests")}
  <main class="site-main">
    <div class="sidequests-header">
      <h1>Side Quests</h1>
      <p>Experimental work, personal projects, and joyful tangents.</p>
    </div>
    <div class="sidequests-grid">
      {items_html}
    </div>
  </main>
  {_footer()}"""

    return _html_shell("Side Quests", body, body_class="interior")


# ── Builder ──────────────────────────────────────────────────────────────────

def build_all():
    print("Building portfolio…")

    # index
    (OUT_DIR / "index.html").write_text(build_index(), encoding="utf-8")
    print("  ✓  index.html")

    # project pages
    for p in PROJECTS:
        path = OUT_DIR / f"{p['slug']}.html"
        path.write_text(build_project_page(p), encoding="utf-8")
        print(f"  ✓  {p['slug']}.html")

    # about
    (OUT_DIR / "about.html").write_text(build_about(), encoding="utf-8")
    print("  ✓  about.html")

    # sidequests
    (OUT_DIR / "sidequests.html").write_text(build_sidequests(), encoding="utf-8")
    print("  ✓  sidequests.html")

    print("\nDone! Open index.html in your browser.")


# ── Interactive new-project wizard ───────────────────────────────────────────

def new_project_wizard():
    print("\n── Add a New Project ──────────────────────────────────────────")
    print("(Press Enter to skip optional fields)\n")

    slug  = input("Project slug (URL-safe name, e.g. 'my-cool-zine'): ").strip()
    title = input("Project title: ").strip()
    desc  = input("Short description: ").strip()
    year  = input("Year (optional): ").strip() or str(datetime.now().year)
    tags  = input("Tags, comma-separated (optional): ").strip()
    hero  = input("Hero image path relative to portfolio folder (optional): ").strip()

    n_visuals = input("How many visuals/images/videos? (default 1): ").strip()
    try:
        n_visuals = int(n_visuals)
    except ValueError:
        n_visuals = 1

    visuals = []
    for i in range(n_visuals):
        src  = input(f"  Visual {i+1} src path (optional): ").strip()
        cap  = input(f"  Visual {i+1} caption (optional): ").strip() or f"Visual {i+1}"
        visuals.append({"src": src, "caption": cap})

    project = {
        "slug":        slug,
        "title":       title,
        "description": desc,
        "year":        year,
        "tags":        [t.strip() for t in tags.split(",") if t.strip()],
        "hero":        hero,
        "visuals":     visuals,
    }

    # Insert at top of PROJECTS list
    PROJECTS.insert(0, project)

    # Rewrite this file with the new project included
    _append_project_to_registry(project)

    build_all()
    print(f"\nProject '{title}' added and site rebuilt!")


def _append_project_to_registry(p: dict):
    """
    Rewrites the PROJECTS list in this file to prepend the new project.
    Simple string manipulation — keeps human-readable formatting.
    """
    script_path = Path(__file__)
    src = script_path.read_text(encoding="utf-8")

    vis_lines = ""
    for v in p["visuals"]:
        vis_lines += f'            {{"type": "image", "src": "{v["src"]}", "caption": "{v["caption"]}"}},\n'

    tags_repr = repr(p["tags"])
    new_entry = f'''    {{
        "slug":        "{p['slug']}",
        "title":       "{p['title']}",
        "description": "{p['description']}",
        "year":        "{p['year']}",
        "tags":        {tags_repr},
        "hero":        "{p['hero']}",
        "visuals": [
{vis_lines}        ],
    }},\n'''

    marker = 'PROJECTS = [\n'
    idx = src.find(marker)
    if idx == -1:
        print("Warning: could not auto-update PROJECTS list. Add your project manually.")
        return

    insert_at = idx + len(marker)
    src = src[:insert_at] + new_entry + src[insert_at:]
    script_path.write_text(src, encoding="utf-8")


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kashvi Portfolio Builder")
    parser.add_argument("--new", action="store_true", help="Add a new project interactively")
    args = parser.parse_args()

    if args.new:
        new_project_wizard()
    else:
        build_all()
