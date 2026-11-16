#!/usr/bin/env python3
"""Build a standalone explainer from content JSON and an optional theme JSON."""

import argparse
import json
import sys
from pathlib import Path
import re


MARKER = "/* EMBED_EXPLAINER_DATA */"
COLORS = {"background", "surface", "text", "muted", "border", "accent", "flow"}
EFFECTS = ("fade", "rise", "drop", "left", "right", "pop", "zoom")
SOUNDS = ("chime", "alert", "success", "none")
PHASES = ("before", "after")
ICON_ID = re.compile(r'<symbol id="icon-([a-z0-9-]+)"')


def check_icon(item, icons, where):
    if "icon" in item:
        require(item["icon"] in icons,
                f"{where}.icon: unknown icon {item['icon']!r} (available: {', '.join(sorted(icons))})")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_object(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    require(isinstance(data, dict), f"{path}: expected a JSON object")
    return data


def nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def number_between(value, low, high):
    return type(value) in (int, float) and low <= value <= high


def read_records(value, name):
    require(isinstance(value, list), f"{name}: expected an array")
    require(all(isinstance(item, dict) for item in value), f"{name}: expected objects")
    return value


def index_records(records, name):
    index = {}
    for item in read_records(records, name):
        identifier = item.get("id")
        require(nonempty_text(identifier), f"{name}: each object needs a string id")
        require(identifier not in index, f"{name}: duplicate id {identifier!r}")
        index[identifier] = item
    return index


def check_optional_text(item, keys, where):
    for key in keys:
        require(key not in item or isinstance(item[key], str), f"{where}.{key}: expected text")


def read_ids(value, available, where):
    require(isinstance(value, list), f"{where}: expected an array of ids")
    result = set()
    for identifier in value:
        require(isinstance(identifier, str) and identifier in available,
                f"{where}: unknown or hidden id {identifier!r}")
        require(identifier not in result, f"{where}: duplicate id {identifier!r}")
        result.add(identifier)
    return result


def validate_code(code, where):
    require(isinstance(code, dict), f"{where}: expected an object")
    lines = code.get("lines")
    require(isinstance(lines, list) and lines and all(isinstance(line, str) for line in lines),
            f"{where}.lines: expected a nonempty array of strings")
    highlight = code.get("highlight", [])
    require(isinstance(highlight, list) and
            all(type(line) is int and 1 <= line <= len(lines) for line in highlight),
            f"{where}.highlight: expected line numbers between 1 and {len(lines)}")
    check_optional_text(code, ("label",), where)


def validate_content(content, icons):
    warnings = []
    require(nonempty_text(content.get("title")), "title: expected nonempty text")
    check_optional_text(content, ("subtitle", "lang"), "content")
    require(re.fullmatch(r"[A-Za-z]{1,8}(?:-[A-Za-z0-9]{1,8})*", content.get("lang", "ja")),
            "lang: expected a language tag")

    nodes = index_records(content.get("nodes"), "nodes")
    for node_id, node in nodes.items():
        where = f"node {node_id!r}"
        require(nonempty_text(node.get("label")), f"{where}.label: expected nonempty text")
        for key in ("x", "y"):
            require(number_between(node.get(key), 0, 100), f"{where}.{key}: expected 0–100")
        require(number_between(node.get("width", 30), 1, 100), f"{where}.width: expected 1–100")
        check_optional_text(node, ("detail",), where)
        check_icon(node, icons, where)

    links = index_records(content.get("links", []), "links")
    for link_id, link in links.items():
        where = f"link {link_id!r}"
        start, end = link.get("from"), link.get("to")
        require(all(isinstance(node, str) and node in nodes for node in (start, end)) and start != end,
                f"{where}: expected two distinct node ids")
        require(link.get("style", "solid") in ("solid", "dashed"), f"{where}.style: expected solid or dashed")
        require(isinstance(link.get("directed", True), bool), f"{where}.directed: expected a boolean")
        require(isinstance(link.get("blocked", False), bool), f"{where}.blocked: expected a boolean")
        check_optional_text(link, ("label",), where)

    scenes = read_records(content.get("scenes"), "scenes")
    require(scenes, "scenes: expected at least one scene")
    for number, scene in enumerate(scenes, 1):
        where = f"scene {number}"
        require(nonempty_text(scene.get("caption")), f"{where}.caption: expected nonempty text")
        require(scene.get("effect", "fade") in EFFECTS,
                f"{where}.effect: expected one of {', '.join(EFFECTS)}")
        require(scene.get("sound", "chime") in SOUNDS,
                f"{where}.sound: expected one of {', '.join(SOUNDS)}")
        require(scene.get("phase") in (None, *PHASES), f"{where}.phase: expected one of {', '.join(PHASES)}")
        points = scene.get("points", [])
        require(isinstance(points, list), f"{where}.points: expected an array")
        for point in points:
            if isinstance(point, str):
                require(nonempty_text(point), f"{where}.points: expected nonempty text")
                continue
            require(isinstance(point, dict) and nonempty_text(point.get("text")),
                    f"{where}.points: each point needs text, as a string or an object with text")
            check_icon(point, icons, f"{where}.points")
        if len(points) > 4:
            warnings.append(f"{where}: {len(points)} points (about 4 fit in the frame)")
        if points and scene.get("nodes"):
            warnings.append(f"{where}: points and nodes share the figure area and may overlap")
        duration = scene.get("duration", 3)
        require(number_between(duration, 0, 2_147_483.647) and duration > 0,
                f"{where}.duration: expected positive seconds within the browser timer range")
        shown_nodes = read_ids(scene.get("nodes"), nodes, f"{where}.nodes")
        shown_links = read_ids(scene.get("links", []), links, f"{where}.links")
        for identifier in shown_links:
            link = links[identifier]
            require({link["from"], link["to"]} <= shown_nodes,
                    f"{where}: both endpoints of {identifier!r} must be visible")
        read_ids(scene.get("focus", []), shown_nodes, f"{where}.focus")
        read_ids(scene.get("flow", []), shown_links, f"{where}.flow")
        details = scene.get("details", {})
        require(isinstance(details, dict), f"{where}.details: expected an object")
        for identifier, detail in details.items():
            require(identifier in shown_nodes and isinstance(detail, str),
                    f"{where}.details: expected text for visible node {identifier!r}")
        positions = scene.get("positions", {})
        require(isinstance(positions, dict), f"{where}.positions: expected an object")
        for identifier, position in positions.items():
            require(identifier in shown_nodes,
                    f"{where}.positions: expected a visible node, got {identifier!r}")
            require(isinstance(position, dict) and position and position.keys() <= {"x", "y"},
                    f"{where}.positions: {identifier!r} needs x or y")
            for axis, value in position.items():
                require(number_between(value, 0, 100),
                        f"{where}.positions: {identifier}.{axis} must be 0–100")
        for metric in read_records(scene.get("metrics", []), f"{where}.metrics"):
            require(all(nonempty_text(metric.get(key)) for key in ("label", "value")),
                    f"{where}.metrics: each metric needs a text label and value")
            check_icon(metric, icons, f"{where}.metrics")
        if "code" in scene:
            validate_code(scene["code"], f"{where}.code")

        if len(shown_nodes) > 4:
            warnings.append(f"{where}: {len(shown_nodes)} nodes shown at once (about 4 fit in the frame)")
        if len(scene.get("metrics", [])) > 3:
            warnings.append(f"{where}: {len(scene['metrics'])} metrics (about 3 fit on one line)")
        if len(scene.get("code", {}).get("lines", [])) > 6:
            warnings.append(f"{where}.code: {len(scene['code']['lines'])} lines (about 6 fit without scrolling)")
    return warnings


def validate_theme(theme):
    require(theme.keys() <= {"mode", "light", "dark", "radius"}, "theme: unknown setting")
    require(theme.get("mode", "system") in ("system", "light", "dark"), "theme.mode: expected system, light or dark")
    require(number_between(theme.get("radius", 12), 0, 24), "theme.radius: expected 0–24")
    for mode in ("light", "dark"):
        palette = theme.get(mode, {})
        require(isinstance(palette, dict) and palette.keys() <= COLORS, f"theme.{mode}: unknown color setting")
        for key, value in palette.items():
            require(isinstance(value, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", value),
                    f"theme.{mode}.{key}: expected #RRGGBB")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--theme", type=Path)
    args = parser.parse_args()

    try:
        template = Path(__file__).resolve().parents[1] / "assets" / "template.html"
        html = template.read_text(encoding="utf-8")
        require(html.count(MARKER) == 1, "template must contain exactly one data marker")
        content = read_object(args.content)
        theme = read_object(args.theme) if args.theme else {}
        warnings = validate_content(content, set(ICON_ID.findall(html)))
        validate_theme(theme)
        payload = json.dumps({"content": content, "theme": theme}, ensure_ascii=False, allow_nan=False)
        payload = payload.replace("<", r"\u003c")
        args.output.write_text(html.replace(MARKER, payload), encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.exit(1, f"build: {error}\n")
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
