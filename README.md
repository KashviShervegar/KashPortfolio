# Kashvi Shervegar — Portfolio

## File Structure

```
portfolio/
├── kashvi_portfolio.py     ← Python template engine (run this to rebuild)
├── index.html              ← Landing page (auto-generated)
├── about.html              ← About page (auto-generated)
├── sidequests.html         ← Side Quests page (auto-generated)
├── project-one.html        ← Example project page (auto-generated)
├── static/
│   ├── css/style.css       ← All styles
│   ├── js/main.js          ← Scroll interactions
│   ├── fonts/
│   │   └── Enclosed-Regular.otf
│   ├── images/
│   │   └── self.png        ← About page photo
│   └── files/              ← Place resume PDF here
└── README.md
```

## How to Add a New Project

### Option A — Interactive wizard (recommended)
```bash
python kashvi_portfolio.py --new
```
Follow the prompts. The site rebuilds automatically.

### Option B — Edit manually
1. Open `kashvi_portfolio.py`
2. Find the `PROJECTS` list near the top
3. Add a new dict at the **top** of the list (newest projects show first)
4. Run `python kashvi_portfolio.py` to rebuild

### Project dict format
```python
{
    "slug":        "my-project-slug",    # used for the URL: my-project-slug.html
    "title":       "Project Title",
    "description": "Short description of the project and your process.",
    "year":        "2025",
    "tags":        ["Publication Design", "Typography"],
    "hero":        "static/images/myproject_hero.jpg",  # landing page thumbnail
    "visuals": [
        {"type": "image", "src": "static/images/myproject_01.jpg", "caption": "Caption"},
        {"type": "video", "src": "static/images/myproject_02.mp4", "caption": "Caption"},
        {"type": "gif",   "src": "static/images/myproject_03.gif", "caption": "Caption"},
        # add as many as needed
    ],
}
```

## Adding Theo's Stop Motion Animation

In `index.html` find the `<div class="animation-container">` comment block.

**Option A — GIF (simplest):**
Replace the placeholder paragraph with:
```html
<img src="static/images/theo.gif" alt="Theo the cat" />
```

**Option B — Video:**
```html
<video autoplay loop muted playsinline>
  <source src="static/images/theo.mp4" type="video/mp4" />
</video>
```

**Option C — Frame-by-frame (scroll-driven):**
```html
<img class="frame active" src="static/images/theo_01.png" alt="" />
<img class="frame" src="static/images/theo_02.png" alt="" />
<img class="frame" src="static/images/theo_03.png" alt="" />
```
Scrolling will cycle through the frames.

## Adding Side Quests

In `kashvi_portfolio.py` find `SIDE_QUESTS = [...]` and add items:
```python
{"src": "static/images/sidequest_01.jpg", "caption": "My experiment"},
```
Then rebuild: `python kashvi_portfolio.py`

## Updating Links

- **Instagram / LinkedIn**: edit `build_about()` in `kashvi_portfolio.py`
- **Resume**: place your PDF at `static/files/kashvi_shervegar_resume.pdf`
