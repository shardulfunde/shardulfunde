"""Generate the profile README and its light/dark SVGs from resume-based data."""

import json
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
ET.register_namespace("", "http://www.w3.org/2000/svg")
NS = "{http://www.w3.org/2000/svg}"
THEMES = {
    "light": {"ink": "#171717", "muted": "#555555", "rule": "#c4c4c4", "ghost": "#b4b4b4"},
    "dark": {"ink": "#f0f0f0", "muted": "#b5b5b5", "rule": "#484848", "ghost": "#767676"},
}


class Visual:
    def __init__(self, height, label, theme):
        self.root = ET.Element(
            NS + "svg",
            {"viewBox": f"0 0 1000 {height}", "fill": "none", "role": "img", "aria-label": label},
        )
        ET.SubElement(self.root, NS + "title").text = label
        palette = THEMES[theme]
        ET.SubElement(self.root, NS + "style").text = f"""
    :root {{ --ink:{palette["ink"]}; --muted:{palette["muted"]};
             --rule:{palette["rule"]}; --ghost:{palette["ghost"]}; }}
    text {{ font-family:Consolas,"Liberation Mono",monospace; letter-spacing:0; }}
    .reveal {{ animation:reveal .7s ease; }}
    .later {{ animation-delay:.15s; }}
    .last {{ animation-delay:.3s; }}
    .draw {{ animation:draw 1.3s ease; stroke-dasharray:1200; }}
    .flow {{ stroke-dasharray:4 10; animation:flow 2s linear infinite; }}
    .pulse {{ animation:pulse 2.8s ease-in-out infinite; }}
    @keyframes reveal {{ from {{ opacity:.65; transform:translateY(6px); }}
                         to {{ opacity:1; transform:translateY(0); }} }}
    @keyframes draw {{ from {{ stroke-dashoffset:150; }} to {{ stroke-dashoffset:0; }} }}
    @keyframes flow {{ to {{ stroke-dashoffset:-28; }} }}
    @keyframes pulse {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:.45; }} }}
    @media (prefers-reduced-motion:reduce) {{
      .reveal,.draw,.flow,.pulse {{ animation:none; }}
    }}
"""

    def node(self, tag, attrs, parent=None):
        return ET.SubElement(
            self.root if parent is None else parent,
            NS + tag,
            {key.replace("_", "-"): str(value) for key, value in attrs.items()},
        )

    def text(self, x, y, value, size=20, color="ink", anchor="start", weight=None, parent=None):
        attrs = {"x": x, "y": y, "font-size": size, "fill": f"var(--{color})", "text-anchor": anchor}
        if weight:
            attrs["font-weight"] = weight
        node = self.node("text", attrs, parent)
        node.text = value
        return node

    def line(self, x1, y1, x2, y2, animated=False, parent=None):
        attrs = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "stroke": "var(--rule)", "stroke-width": 1}
        if animated:
            attrs["class"] = "draw"
        return self.node("line", attrs, parent)

    def group(self, delay=""):
        return self.node("g", {"class": f"reveal {delay}".strip()})

    def top_rule(self, caption):
        self.text(48, 31, caption, 15, "muted")
        self.line(48, 48, 952, 48, animated=True)

    def save(self, name, theme):
        destination = ROOT / "assets" / ("dark" if theme == "dark" else "") / f"{name}.svg"
        destination.parent.mkdir(parents=True, exist_ok=True)
        ET.indent(self.root, space="  ")
        destination.write_text(ET.tostring(self.root, encoding="unicode") + "\n", encoding="utf-8")


def header(theme):
    v = Visual(380, f'{PROFILE["name"]} - AI & ML student and backend developer', theme)
    v.text(48, 38, "PROFILE / SHARDULFUNDE", 15, "muted")
    v.text(952, 38, "SANGLI, INDIA", 15, "muted", "end")
    v.line(48, 56, 952, 56, animated=True)
    g = v.group()
    v.text(46, 154, PROFILE["name"], 76, weight=700, parent=g)
    v.text(48, 201, PROFILE["headline"], 26, "muted", parent=g)
    g = v.group("later")
    v.text(48, 260, "Python backends / AI-powered products / AI evaluation", 22, parent=g)
    v.text(48, 296, "StudyMate AI builder / National hackathon achievements", 21, "muted", parent=g)
    v.line(48, 328, 952, 328, animated=True)
    v.text(48, 361, "WALCHAND COLLEGE OF ENGINEERING", 17, "muted")
    v.text(952, 361, "B.TECH AI & ML / 2024 - 2028", 17, "muted", "end")
    return v


def section(theme, number, title, path):
    v = Visual(100, f"Section {number:02d}: {title}", theme)
    v.text(48, 72, f"{number:02d}", 52, "ghost")
    v.text(140, 64, title, 23, weight=700)
    v.text(952, 64, f"~/{path}", 16, "muted", "end")
    v.line(48, 92, 952, 92, animated=True)
    return v


def whoami(theme):
    v = Visual(310, "About Shardul Funde: AI & ML student, backend development, education, and leadership", theme)
    g = v.group()
    for y, line in zip((40, 78, 116), PROFILE["about"]):
        v.text(48, y, line, 22, parent=g)
    v.line(48, 145, 952, 145)
    g = v.group("later")
    rows = [
        ("EDUCATION", "B.Tech AI & ML / 2024 - 2028 / CGPA 8.9 / 10"),
        ("EXPERIENCE", "Turing / Software Engineer / Aug - Sep 2026"),
        ("LEADERSHIP", "Young CXO Fellow / Technical Head, WCE ASTRA"),
    ]
    for y, (label, value) in zip((184, 229, 274), rows):
        v.text(48, y, label, 16, "muted", parent=g)
        v.text(210, y, value, 21, parent=g)
    return v


def ecosystem(theme):
    v = Visual(460, "Project map: StudyMate AI, ManahArogya, and CNN Visualization Tool", theme)
    v.top_rule("SYSTEM MAP / FROM DATA TO USEFUL PRODUCTS")
    center = (360, 92, 280, 74)
    v.node("rect", {"x": center[0], "y": center[1], "width": center[2], "height": center[3],
                    "rx": 2, "stroke": "var(--ink)"})
    v.text(500, 124, "SHARDULFUNDE", 23, anchor="middle", weight=700)
    v.text(500, 151, "AI / BACKEND / DATA", 16, "muted", "middle")
    for x, name, first, second in [
        (48, "StudyMate AI", "Learning platform", "FastAPI + PostgreSQL"),
        (360, "ManahArogya", "Mental health app", "APIs + deployment"),
        (672, "CNN Visualizer", "Digit classifier", "TensorFlow + Streamlit"),
    ]:
        mid = x + 140
        v.node("path", {"d": f"M500 166 V210 H{mid} V262", "stroke": "var(--rule)", "class": "flow"})
        g = v.group("later")
        v.node("rect", {"x": x, "y": 262, "width": 280, "height": 122, "rx": 2,
                        "stroke": "var(--rule)"}, parent=g)
        v.text(mid, 299, name, 23, anchor="middle", weight=700, parent=g)
        v.text(mid, 332, first, 19, "muted", "middle", parent=g)
        v.text(mid, 360, second, 17, "muted", "middle", parent=g)
    v.line(48, 417, 952, 417)
    v.text(48, 447, "REST APIs / PostgreSQL / AI workflows / Model visualization", 20, "muted")
    return v


def projects(theme):
    v = Visual(740, "Selected projects: StudyMate AI, ManahArogya, and CNN Visualization Tool", theme)
    for i, project in enumerate(PROFILE["projects"]):
        top = 35 + i * 240
        g = v.group(["", "later", "last"][i])
        v.text(48, top, f'{i + 1:02d} / {project["name"]}', 29, weight=700, parent=g)
        v.text(48, top + 37, project["category"], 19, "muted", parent=g)
        for offset, line in zip((81, 115), project["visual_lines"]):
            v.text(48, top + offset, line, 21, parent=g)
        v.text(48, top + 158, project["highlight"], 23, weight=700, parent=g)
        v.text(48, top + 191, project["stack"], 18, "muted", parent=g)
        v.line(48, top + 218, 952, top + 218, parent=g)
    return v


def telemetry(theme):
    v = Visual(375, "StudyMate AI launch metrics: 1,200+ users in 10 days, 8,000+ resource accesses, 750+ AI-generated tests, and $100,000 Azure credits", theme)
    v.top_rule("IMPACT / STUDYMATE AI")
    for x, y, number, label in [
        (48, 136, "1,200+", "USERS IN 10 DAYS"),
        (540, 136, "8,000+", "RESOURCE ACCESSES"),
        (48, 280, "750+", "AI-GENERATED TESTS"),
        (540, 280, "$100,000", "AZURE CREDITS"),
    ]:
        g = v.group("later")
        v.text(x, y, number, 58, weight=700, parent=g)
        v.text(x, y + 36, label, 18, "muted", parent=g)
    v.line(48, 205, 952, 205)
    v.text(540, 344, "Microsoft for Startups", 19, "muted")
    return v


def timeline(theme):
    v = Visual(320, "Journey: WCE AI & ML from 2024, products and Turing experience in 2026, expected graduation in 2028", theme)
    v.top_rule("THE ROUTE / EDUCATION TO ENGINEERING")
    v.line(105, 157, 890, 157, animated=True)
    milestones = [
        (105, "2024", "WCE", "AI & ML", True),
        (360, "2026", "StudyMate AI", "1,200+ users", False),
        (625, "AUG - SEP 2026", "Turing", "AI evaluation", True),
        (890, "2028", "B.Tech", "Expected graduation", False),
    ]
    for x, year, line1, line2, above in milestones:
        v.node("circle", {"cx": x, "cy": 157, "r": 5, "fill": "var(--ink)"})
        y1, y2, y3 = (91, 118, 141) if above else (205, 232, 260)
        v.text(x, y1, year, 18, "muted", "middle")
        v.text(x, y2, line1, 20, anchor="middle", weight=700)
        v.text(x, y3, line2, 16, "muted", "middle")
    return v


def experience(theme):
    v = Visual(320, "Turing: part-time Software Engineer, August 17 to September 30, 2026; Python, Docker, Linux, and Git", theme)
    v.top_rule("EXPERIENCE / TURING")
    g = v.group()
    v.text(48, 97, "Software Engineer / Python & Docker / Part-time", 25, weight=700, parent=g)
    v.text(48, 134, PROFILE["experience"]["dates"], 21, "muted", parent=g)
    lines = [
        "Hardened 5+ programming tasks for AI coding-agent evaluation.",
        "Calibrated difficulty; debugged solutions, grading, and environments.",
        "Separated model failures from task issues and verified fixes.",
        "Python / Docker / Linux / Git",
    ]
    for y, line in zip((182, 219, 256, 297), lines):
        v.text(48, y, line, 21 if y != 297 else 19, "muted" if y == 297 else "ink", parent=g)
    return v


def stack(theme):
    v = Visual(320, "Technical stack: C++, Python, Java, C; FastAPI, PostgreSQL; PyTorch, LangChain, LangGraph, RAG; Docker, Git, AWS, Azure, Render", theme)
    v.line(205, 12, 205, 308)
    for y, (label, values) in zip((38, 91, 144, 197, 250, 303), PROFILE["skills"].items()):
        v.text(48, y, label.upper(), 17, "muted")
        text = " / ".join(values)
        if label == "Core CS":
            text = "DSA / OOP / Operating Systems / DBMS / Debugging"
        if label == "AI / ML":
            text = "PyTorch / Scikit-Learn / NumPy / Pandas"
            v.text(227, y - 8, text, 20)
            v.text(227, y + 18, "LangChain / LangGraph / RAG", 20)
        else:
            v.text(227, y, text, 20)
    return v


def footer(theme):
    v = Visual(120, "Shardul Funde: AI, backend engineering, and products; github.com/shardulfunde", theme)
    v.line(48, 24, 952, 24, animated=True)
    v.node("circle", {"cx": 57, "cy": 66, "r": 4, "fill": "var(--ink)", "class": "pulse"})
    v.text(78, 73, "AI / BACKEND / PRODUCTS", 20)
    v.text(952, 73, "@shardulfunde", 20, "muted", "end")
    return v


def picture(name, alt):
    return (
        f'<picture>\n'
        f'  <source media="(prefers-color-scheme: dark)" srcset="assets/dark/{name}.svg"/>\n'
        f'  <img src="assets/{name}.svg" width="100%" alt="{alt}"/>\n'
        f'</picture>'
    )


def badge(label, target):
    encoded = label.replace(" ", "%20")
    return (
        f'<a href="{target}"><picture>'
        f'<source media="(prefers-color-scheme: dark)" '
        f'srcset="https://img.shields.io/badge/{encoded}-0d1117?style=flat-square&amp;logoColor=ffffff"/>'
        f'<img src="https://img.shields.io/badge/{encoded}-ffffff?style=flat-square&amp;logoColor=171717" '
        f'alt="{label}" height="24"/>'
        f'</picture></a>'
    )


def text_version():
    p = PROFILE
    lines = [
        "<details>",
        "<summary>Profile in text</summary>",
        "",
        "## About",
        "",
        f'**{p["name"]}** | {p["headline"]} | {p["location"]}',
        "",
        " ".join(p["about"]),
        "",
        "## Education",
        "",
        f'**{p["education"]["college"]}**  ',
        f'{p["education"]["degree"]} | {p["education"]["years"]} | CGPA: {p["education"]["cgpa"]}',
        "",
        "## Projects",
        "",
    ]
    for project in p["projects"]:
        lines += [
            f'### [{project["name"]}]({project["url"]})',
            "",
            project["description"],
            "",
            *(f"- {detail}" for detail in project["details"]),
            "",
            f'**Stack:** {project["stack"]}  ',
            f'[Source code]({project["repository"]})',
            "",
        ]
    lines += [
        "## Experience",
        "",
        f'**{p["experience"]["company"]} | {p["experience"]["role"]} | {p["experience"]["type"]}**  ',
        p["experience"]["dates"],
        "",
        *(f"- {detail}" for detail in p["experience"]["details"]),
        "",
        "## Technical Skills",
        "",
        "| Area | Technologies |",
        "| :--- | :--- |",
        *(f'| {label} | {", ".join(values)} |' for label, values in p["skills"].items()),
        "",
        "## Contact",
        "",
        f'[Email]({p["links"]["email"]}) | [LinkedIn]({p["links"]["linkedin"]}) | '
        f'[GitHub]({p["links"]["github"]}) | [LeetCode]({p["links"]["leetcode"]}) | '
        f'[CodeChef (2-Star, per resume)]({p["links"]["codechef"]})',
        "",
        "</details>",
    ]
    return "\n".join(lines)


def readme():
    p = PROFILE
    blocks = [
        "<div align=\"center\">\n",
        picture("header-v1", "Shardul Funde - AI & ML student and backend developer"),
        "",
        " ".join(badge(label, target) for label, target in [
            ("LINKEDIN", p["links"]["linkedin"]),
            ("EMAIL", p["links"]["email"]),
            ("LEETCODE", p["links"]["leetcode"]),
            ("CODECHEF", p["links"]["codechef"]),
            ("STUDYMATE AI", p["projects"][0]["url"]),
        ]),
        "\n</div>",
        "",
        picture("s01", "01 - Whoami"),
        picture("whoami", "Third-year AI & ML student at WCE; CGPA 8.9/10; Turing experience; Young CXO Fellow and ASTRA Technical Head"),
        "",
        picture("s02", "02 - System map"),
        picture("ecosystem", "StudyMate AI, ManahArogya, and CNN Visualization Tool: AI, backend, and data"),
        "",
        picture("s03", "03 - Projects"),
        picture("projects", "StudyMate AI: 1,200+ users in 10 days; ManahArogya: 3rd among 350+ teams; CNN tool: feature-map visualization"),
        "",
    ]
    for project in p["projects"]:
        blocks += [f'**{project["name"]}:** [Live app]({project["url"]}) | [Source code]({project["repository"]})', ""]
    blocks += [
        picture("s04", "04 - Impact"),
        picture("telemetry", "StudyMate AI: 1,200+ users in 10 days, 8,000+ resource accesses, 750+ AI-generated tests, $100,000 Azure credits"),
        "",
        picture("s05", "05 - The route"),
        picture("timeline", "WCE from 2024; StudyMate AI and Turing experience in 2026; expected graduation in 2028"),
        picture("experience", "Turing Software Engineer, part-time, August 17 - September 30, 2026; hardened 5+ AI evaluation tasks"),
        "",
        "### Achievements",
        "",
    ]
    for item in p["achievements"]:
        detail = f' {item["detail"]}' if item["detail"] else ""
        blocks += [f'- **{item["name"]}:** {item["result"]}.{detail}']
    blocks += ["", "### Leadership & Programs", ""]
    for item in p["leadership"]:
        blocks += [
            f'**{item["role"]} | {item["organization"]} | {item["dates"]}**  ',
            item["detail"],
            "",
        ]
    blocks += [
        picture("s06", "06 - Stack"),
        picture("stack", "C++, Python, Java, C; DSA and core CS; FastAPI, PostgreSQL; PyTorch, LangChain, LangGraph, RAG; Docker, Git; AWS, Azure, Render"),
        "",
        "### Certifications",
        "",
    ]
    for cert in p["certifications"]:
        blocks += [f'- [{cert["name"]}]({cert["url"]}) | {cert["issuer"]}']
    blocks += ["", text_version(), "", picture("footer", "Shardul Funde / AI, backend, and products / @shardulfunde"), ""]
    return "\n".join(blocks)


def generate():
    visuals = {
        "header-v1": header,
        "whoami": whoami,
        "ecosystem": ecosystem,
        "projects": projects,
        "telemetry": telemetry,
        "timeline": timeline,
        "experience": experience,
        "stack": stack,
        "footer": footer,
    }
    sections = [
        ("WHOAMI", "01-whoami"),
        ("SYSTEM MAP", "02-ecosystem"),
        ("PROJECTS", "03-projects"),
        ("IMPACT", "04-impact"),
        ("THE ROUTE", "05-journey"),
        ("STACK", "06-stack"),
    ]
    for theme in THEMES:
        for name, builder in visuals.items():
            builder(theme).save(name, theme)
        for i, (title, path) in enumerate(sections, start=1):
            section(theme, i, title, path).save(f"s{i:02d}", theme)
    (ROOT / "README.md").write_text(readme(), encoding="utf-8")
    print("Generated README.md and 30 SVG assets.")


if __name__ == "__main__":
    generate()
