from __future__ import annotations

import json
import os
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from urllib.parse import quote
from zipfile import ZipFile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
KB_DIR = ROOT / "知识库"
PRODUCT_DIR = KB_DIR / "products"
AGENT_DIR = KB_DIR / "agent"
GITHUB_RAW_BASE = os.environ.get("KB_GITHUB_RAW_BASE", "").rstrip("/")
GITHUB_TREE_BASE = os.environ.get("KB_GITHUB_TREE_BASE", "").rstrip("/")

NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "pkgrel": "http://schemas.openxmlformats.org/package/2006/relationships",
}

DOC_LABELS = {
    "单页_pdf": "单页 PDF",
    "单页_xlsx": "单页源文档",
    "官网文档_xlsx": "官网文档",
    "参数_xlsx": "参数表",
    "快速指南_pdf": "快速指南",
    "说明书_pdf": "说明书",
    "竞品分析_xlsx": "竞品分析",
    "产品ID图_dir": "产品 ID 图",
}

DOC_LABELS_EN = {
    "单页_pdf": "Brochure PDF",
    "单页_xlsx": "Brochure Source",
    "官网文档_xlsx": "Website Copy",
    "参数_xlsx": "Specification Sheet",
    "快速指南_pdf": "Quick Start Guide",
    "说明书_pdf": "User Manual",
    "竞品分析_xlsx": "Competitor Analysis",
    "产品ID图_dir": "Product ID Images",
}

DOC_ORDER = [
    "单页_xlsx",
    "单页_pdf",
    "官网文档_xlsx",
    "参数_xlsx",
    "快速指南_pdf",
    "说明书_pdf",
    "竞品分析_xlsx",
    "产品ID图_dir",
]

PRODUCT_ORDER = ["RCM01", "RM21", "Titan", "FRX", "FR4000", "FL3000", "FV2000"]

PRODUCT_META = {
    "FL3000": {
        "full_name": "FJD FL3000",
        "classification": "家用 / 轻商用 LiDAR 智能割草机（基于现有文案推断）",
        "scenarios": "家庭庭院",
    },
    "FR4000": {
        "full_name": "FJD FR4000",
        "classification": "大面积住宅 / 轻商用智能割草机（基于参数与资料分布推断）",
        "scenarios": "大宅草坪、轻商用园林",
    },
    "FRX": {
        "full_name": "FJD FRX",
        "classification": "专业运动场 / 高尔夫割草机器人（基于单页文案推断）",
        "scenarios": "运动场、高尔夫球场",
    },
    "FV2000": {
        "full_name": "FJD FV2000",
        "classification": "家用智能割草机（基于单页文案推断）",
        "scenarios": "家庭庭院",
    },
    "RCM01": {
        "full_name": "FJD RCM01",
        "classification": "高端滚刀式专业草坪机器人（基于单页与官网文案推断）",
        "scenarios": "高尔夫球场、体育场 premium turf",
    },
    "RM21": {
        "full_name": "FJD RM21",
        "classification": "多功能平台型草坪机器人（基于单页与官网文案推断）",
        "scenarios": "运动场、高尔夫球场、果园、草皮农场",
    },
    "Titan": {
        "full_name": "FJD Titan",
        "classification": "大型场地旗舰级割草 / 划线二合一平台（基于单页与官网文案推断）",
        "scenarios": "高尔夫球场、运动场、公共绿地",
    },
}

PRODUCT_META_EN = {
    "FL3000": {
        "classification": "Residential / light commercial LiDAR robotic mower",
        "scenarios": "Home gardens",
    },
    "FR4000": {
        "classification": "Large-property residential / light commercial robotic mower",
        "scenarios": "Large private lawns, light commercial landscaping",
    },
    "FRX": {
        "classification": "Professional sports field / golf-course robotic mower",
        "scenarios": "Sports fields, golf courses",
    },
    "FV2000": {
        "classification": "Residential robotic mower",
        "scenarios": "Home gardens",
    },
    "RCM01": {
        "classification": "Premium reel-based turf robot",
        "scenarios": "Golf courses, stadium premium turf",
    },
    "RM21": {
        "classification": "Multi-function robotic turf platform",
        "scenarios": "Sports fields, golf courses, orchards, turf farms",
    },
    "Titan": {
        "classification": "Flagship large-area mowing and line-marking platform",
        "scenarios": "Golf courses, sports fields, public green spaces",
    },
}

PRODUCT_ALIASES = {
    "fl3000": "FL3000",
    "fr4000": "FR4000",
    "frx": "FRX",
    "fv2000": "FV2000",
    "rcm01": "RCM01",
    "rm21": "RM21",
    "rm21combo": "RM21",
    "rm21comboidimages": "RM21",
    "rm21comboquickstartguide": "RM21",
    "titan": "Titan",
}

TOP_LEVELS = {"单页", "官网文档", "参数", "快速指南", "说明书", "竞品分析", "产品ID图"}


@dataclass
class ProductRecord:
    key: str
    meta: dict
    docs: dict[str, list[Path]] = field(default_factory=lambda: defaultdict(list))
    image_dirs: list[Path] = field(default_factory=list)


def normalize_token(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def find_product(path: Path) -> str | None:
    joined = " ".join(path.parts)
    for chunk in re.split(r"[\\/._()\\-\\s]+", joined):
        token = normalize_token(chunk)
        if token in PRODUCT_ALIASES:
            return PRODUCT_ALIASES[token]
    compact = normalize_token(joined)
    for alias, product in PRODUCT_ALIASES.items():
        if alias and alias in compact:
            return product
    return None


def column_key(cell_ref: str) -> str:
    letters = []
    for char in cell_ref:
        if char.isalpha():
            letters.append(char)
        else:
            break
    return "".join(letters)


def read_xlsx(path: Path) -> list[list[dict[str, str]]]:
    sheets: list[list[dict[str, str]]] = []
    with ZipFile(path) as archive:
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for si in shared_root.findall("main:si", NS):
                text = "".join(
                    node.text or ""
                    for node in si.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")
                )
                shared_strings.append(text)

        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        relationship_map = {
            rel.attrib["Id"]: rel.attrib["Target"]
            for rel in rels.findall("{http://schemas.openxmlformats.org/package/2006/relationships}Relationship")
        }

        for sheet in workbook.findall("main:sheets/main:sheet", NS):
            rel_id = sheet.attrib[
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            ]
            sheet_path = "xl/" + relationship_map[rel_id]
            sheet_root = ET.fromstring(archive.read(sheet_path))
            rows: list[dict[str, str]] = []
            for row in sheet_root.findall(".//main:sheetData/main:row", NS):
                row_data: dict[str, str] = {}
                for cell in row.findall("main:c", NS):
                    key = column_key(cell.attrib.get("r", ""))
                    value_node = cell.find("main:v", NS)
                    if value_node is None:
                        inline = cell.find("main:is", NS)
                        value = (
                            "".join(
                                node.text or ""
                                for node in inline.iter(
                                    "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"
                                )
                            )
                            if inline is not None
                            else ""
                        )
                    else:
                        value = value_node.text or ""
                        if cell.attrib.get("t") == "s" and value.isdigit():
                            index = int(value)
                            if index < len(shared_strings):
                                value = shared_strings[index]
                    value = clean_text(value)
                    if value:
                        row_data[key] = value
                if row_data:
                    rows.append(row_data)
            sheets.append(rows)
    return sheets


def read_xlsx_workbook(path: Path) -> list[tuple[str, list[dict[str, str]]]]:
    workbook_data: list[tuple[str, list[dict[str, str]]]] = []
    with ZipFile(path) as archive:
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for si in shared_root.findall("main:si", NS):
                text = "".join(
                    node.text or ""
                    for node in si.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")
                )
                shared_strings.append(text)

        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        relationship_map = {
            rel.attrib["Id"]: rel.attrib["Target"]
            for rel in rels.findall("{http://schemas.openxmlformats.org/package/2006/relationships}Relationship")
        }

        for sheet in workbook.findall("main:sheets/main:sheet", NS):
            name = sheet.attrib.get("name", "Sheet")
            rel_id = sheet.attrib[
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            ]
            sheet_path = "xl/" + relationship_map[rel_id]
            sheet_root = ET.fromstring(archive.read(sheet_path))
            rows: list[dict[str, str]] = []
            for row in sheet_root.findall(".//main:sheetData/main:row", NS):
                row_data: dict[str, str] = {}
                for cell in row.findall("main:c", NS):
                    key = column_key(cell.attrib.get("r", ""))
                    value_node = cell.find("main:v", NS)
                    if value_node is None:
                        inline = cell.find("main:is", NS)
                        value = (
                            "".join(
                                node.text or ""
                                for node in inline.iter(
                                    "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"
                                )
                            )
                            if inline is not None
                            else ""
                        )
                    else:
                        value = value_node.text or ""
                        if cell.attrib.get("t") == "s" and value.isdigit():
                            index = int(value)
                            if index < len(shared_strings):
                                value = shared_strings[index]
                    value = clean_text(value)
                    if value:
                        row_data[key] = value
                if row_data:
                    rows.append(row_data)
            workbook_data.append((name, rows))
    return workbook_data


def clean_text(value: str) -> str:
    text = value.replace("\r", "\n")
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def sheet_rows(path: Path) -> list[dict[str, str]]:
    try:
        sheets = read_xlsx(path)
    except Exception:
        return []
    return sheets[0] if sheets else []


def row_text(row: dict[str, str]) -> str:
    return " / ".join(row.values())


def preferred_value(row: dict[str, str], columns: Iterable[str]) -> str:
    for column in columns:
        value = clean_text(row.get(column, ""))
        if value:
            return value
    return ""


def contains_cjk(value: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", value))


def choose_text(row: dict[str, str], language: str = "cn", strict: bool = False) -> str:
    if language == "en":
        columns = ("E", "D", "B", "A", "C")
        for column in columns:
            value = clean_text(row.get(column, ""))
            if value and not contains_cjk(value):
                return value
        if strict:
            return ""
        return preferred_value(row, columns)
    return preferred_value(row, ("C", "A", "B", "D", "E"))


def choose_cn_text(row: dict[str, str]) -> str:
    return choose_text(row, "cn")


def choose_en_text(row: dict[str, str]) -> str:
    return choose_text(row, "en")


def compact_line(value: str) -> str:
    text = clean_text(value).replace("\n", " / ")
    text = re.sub(r"\s*/\s*", " / ", text)
    return text.strip(" /")


def sanitize_spec_line(value: str) -> str:
    text = compact_line(value)
    text = text.replace("（小字注释放在参数表格的最下面，左下角）", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_description(rows: list[dict[str, str]], language: str = "cn") -> str:
    keywords = ("产品描述", "Description（一句话概括介绍产品）", "Description")
    for row in rows:
        if any(keyword in row_text(row) for keyword in keywords):
            candidate = choose_text(row, language, strict=(language == "en"))
            if candidate and all(keyword not in candidate for keyword in keywords):
                return compact_line(candidate)
            candidate = choose_en_text(row) if language == "cn" else choose_text(row, "en", strict=False)
            if candidate:
                return compact_line(candidate)
    for row in rows:
        candidate = choose_text(row, language, strict=(language == "en"))
        if len(candidate) >= 40:
            return compact_line(candidate)
    return "English description not extracted from current source files." if language == "en" else "未在结构化资料中提取到产品描述。"


def extract_slogan(rows: list[dict[str, str]], language: str = "cn") -> str | None:
    for row in rows:
        if "slogan" in row_text(row).lower() or "Positioning or Slogan" in row_text(row):
            candidate = choose_text(row, language, strict=(language == "en"))
            if candidate and "slogan" not in candidate.lower():
                return compact_line(candidate)
            candidate = choose_en_text(row) if language == "cn" else choose_text(row, "en", strict=False)
            if candidate:
                return compact_line(candidate)
    return None


def extract_highlights(rows: list[dict[str, str]], limit: int = 6, language: str = "cn") -> list[str]:
    highlights: list[str] = []
    seen: set[str] = set()
    skip_tokens = (
        "页数",
        "参数",
        "规格",
        "Specification",
        "Specifications",
        "Product Name",
        "标题",
        "Banner",
        "Product Showcase",
        "SPECS",
        "KV",
        "Accessories List",
        "Factory Configuration",
        "菜单栏",
        "卖点标题",
        "归类大标题",
        "板块标题",
        "application scenarios",
        "Title（",
        "Description（",
        "Keywords（三",
        "Quick intro",
        "Product Showcase",
        "Features",
        "What's in box",
    )
    for row in rows:
        candidate = choose_text(row, language, strict=(language == "en"))
        candidate = compact_line(candidate)
        if not candidate:
            continue
        if language == "en" and contains_cjk(candidate):
            continue
        if any(token in candidate for token in skip_tokens):
            continue
        if len(candidate) < 6 or candidate in PRODUCT_META:
            continue
        if candidate.startswith("FJD ") or candidate.startswith("RM21 ") or candidate.startswith("Titan"):
            continue
        if candidate in {"Robotic Mower", "Robotic Cylinder Mower", "FJD", "FRX", "FV2000", "RCM01"}:
            continue
        if "KIT" in candidate and re.fullmatch(r"[A-Z0-9 .&+/_-]+", candidate):
            continue
        if " / " not in candidate and len(candidate) < 18:
            continue
        if " / " not in candidate and re.fullmatch(r"[A-Za-z0-9 .&+-]+", candidate):
            continue
        if candidate in seen:
            continue
        seen.add(candidate)
        highlights.append(candidate)
        if len(highlights) >= limit:
            break
    return highlights


SPEC_PRIORITY = [
    ("recommended mowing area", "推荐割草面积"),
    ("max mowing area", "最大割草面积"),
    ("72-hour max mowing area", "72小时"),
    ("24-hour max coverage", "24h"),
    ("max mowing area per charge", "单次"),
    ("cutting height", "割草高度"),
    ("cutting width", "割草宽度"),
    ("max climbing ability", "最大爬坡"),
    ("max mowing slope", "作业坡度"),
    ("boundary type", "边界类型"),
    ("connectivity", "连接"),
    ("ip rating", "防护等级"),
    ("battery capacity", "电池容量"),
    ("charging time", "充电时长"),
]


def extract_specs(rows: list[dict[str, str]], limit: int = 8) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for english_keyword, chinese_keyword in SPEC_PRIORITY:
        for row in rows:
            haystack = row_text(row).lower()
            if english_keyword not in haystack and chinese_keyword not in row_text(row):
                continue
            value = sanitize_spec_line(choose_en_text(row))
            if not value:
                value = sanitize_spec_line(choose_cn_text(row))
            if not value or value.startswith("*") or value in seen:
                continue
            seen.add(value)
            ordered.append(value)
            break
        if len(ordered) >= limit:
            return ordered

    for row in rows:
        value = sanitize_spec_line(choose_en_text(row))
        if not value or value in seen:
            continue
        if len(value) < 12:
            continue
        seen.add(value)
        ordered.append(value)
        if len(ordered) >= limit:
            break
    return ordered


def extract_competitors(rows: list[dict[str, str]], product_key: str) -> list[str]:
    if not rows:
        return []
    first_row = rows[0]
    values = [compact_line(value) for value in first_row.values()]
    competitors: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not value or value == product_key or PRODUCT_META[product_key]["full_name"] in value:
            continue
        if value.lower() == product_key.lower():
            continue
        if value in seen:
            continue
        seen.add(value)
        competitors.append(value)
    return competitors


def englishize_text(value: str) -> str:
    replacements = [
        ("-瑞士", "-Switzerland"),
        ("-美国", "-United States"),
        ("-葡萄牙", "-Portugal"),
        ("（LiDAR）", "(LiDAR)"),
        ("㎡", " m²"),
        ("英亩", " acres"),
        ("平米", " m²"),
        ("毫米", " mm"),
    ]
    output = value
    for source, target in replacements:
        output = output.replace(source, target)
    return output


def url_for(path: Path, base: Path) -> str:
    if GITHUB_RAW_BASE:
        try:
            is_agent_file = path.resolve().is_relative_to(AGENT_DIR.resolve())
        except FileNotFoundError:
            is_agent_file = False
        if not is_agent_file:
            repo_relative = quote(os.path.relpath(path, ROOT).replace(os.sep, "/"), safe="/()")
            if path.is_dir() and GITHUB_TREE_BASE:
                return f"{GITHUB_TREE_BASE}/{repo_relative}"
            return f"{GITHUB_RAW_BASE}/{repo_relative}"
    relative = os.path.relpath(path, base).replace(os.sep, "/")
    return quote(relative, safe="/()")


def md_link(path: Path, base: Path) -> str:
    return f"[{path.name}]({url_for(path, base)})"


def coverage_label(present_count: int) -> str:
    if present_count >= 7:
        return "高"
    if present_count >= 5:
        return "中高"
    if present_count >= 3:
        return "中"
    return "低"


def coverage_label_en(present_count: int) -> str:
    if present_count >= 7:
        return "High"
    if present_count >= 5:
        return "Medium-High"
    if present_count >= 3:
        return "Medium"
    return "Low"


def collect_records() -> dict[str, ProductRecord]:
    records = {
        key: ProductRecord(key=key, meta=meta)
        for key, meta in PRODUCT_META.items()
    }

    for path in ROOT.rglob("*"):
        if "知识库" in path.parts or path.name.startswith("."):
            continue
        if not path.exists():
            continue
        product = find_product(path)
        if not product:
            continue
        if path.is_file():
            top_level = path.parts[len(ROOT.parts)]
            if top_level not in TOP_LEVELS:
                continue
            suffix = path.suffix.lower()
            if top_level == "产品ID图":
                continue
            if suffix not in {".pdf", ".xlsx"}:
                continue
            key = f"{top_level}_{'pdf' if suffix == '.pdf' else 'xlsx'}"
            if path.name.startswith("~$") or path.name.startswith(".~"):
                continue
            records[product].docs[key].append(path)
        elif (
            path.is_dir()
            and path.parts[len(ROOT.parts)] == "产品ID图"
            and path.parent == ROOT / "产品ID图"
        ):
            if any(file.is_file() and not file.name.startswith(".") for file in path.rglob("*")):
                records[product].image_dirs.append(path)

    for record in records.values():
        for values in record.docs.values():
            values.sort()
        record.image_dirs.sort()
    return records


def key_metric(specs: list[str]) -> str:
    if not specs:
        return "待补充"
    for line in specs:
        lower = line.lower()
        if "recommended mowing area" in lower or "max mowing area" in lower:
            return line
    return specs[0]


def truncate_text(value: str, limit: int = 88) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "…"


def collect_gaps(record: ProductRecord) -> list[str]:
    gaps: list[str] = []
    for doc_type in DOC_ORDER:
        if doc_type == "产品ID图_dir":
            present = bool(record.image_dirs)
        else:
            present = bool(record.docs.get(doc_type))
        if not present:
            gaps.append(f"缺少 {DOC_LABELS[doc_type]}")
    return gaps


def collect_gaps_en(record: ProductRecord) -> list[str]:
    gaps: list[str] = []
    for doc_type in DOC_ORDER:
        if doc_type == "产品ID图_dir":
            present = bool(record.image_dirs)
        else:
            present = bool(record.docs.get(doc_type))
        if not present:
            gaps.append(f"Missing {DOC_LABELS_EN[doc_type]}")
    return gaps


def brochure_versions(paths: list[Path], base: Path) -> list[str]:
    versions: list[str] = []
    for path in paths:
        versions.append(f"- {md_link(path, base)}")
    return versions


def count_image_files(path: Path) -> int:
    return sum(1 for file in path.rglob("*") if file.is_file() and not file.name.startswith("."))


def list_image_files(path: Path) -> list[Path]:
    return sorted(file for file in path.rglob("*") if file.is_file() and not file.name.startswith("."))


def preview_document_type(doc_type: str) -> str:
    if doc_type == "产品ID图_dir":
        return "gallery"
    if doc_type.endswith("_pdf"):
        return "pdf"
    if doc_type.endswith("_xlsx"):
        return "spreadsheet"
    return "link"


def brochure_priority(item: dict) -> tuple[int, str]:
    title = item.get("title", "")
    upper = title.upper()
    if item.get("group") != DOC_LABELS["单页_pdf"] or item.get("type") != "pdf":
        return (99, title)
    if upper.startswith("EN_") and "(FOR PRINT)" not in upper:
        return (0, title)
    if upper.startswith("EN_") and "(FOR PRINT)" in upper:
        return (1, title)
    if "(FOR PRINT)" not in upper:
        return (2, title)
    return (3, title)


def xlsx_preview_payload(path: Path, base: Path) -> dict:
    sheets = []
    try:
        workbook_data = read_xlsx_workbook(path)
    except Exception:
        workbook_data = []
    for name, rows in workbook_data[:3]:
        trimmed_rows = rows[:40]
        headers = select_english_headers(trimmed_rows)
        if not headers:
            headers = select_all_headers(trimmed_rows)
        sheets.append(
            {
                "name": name,
                "headers": headers,
                "rows": [{header: row.get(header, "") for header in headers} for row in trimmed_rows],
                "rowCount": len(rows),
            }
        )
    return {
        "name": path.name,
        "path": url_for(path, base),
        "sheets": sheets,
    }


def select_all_headers(rows: list[dict[str, str]]) -> list[str]:
    headers: list[str] = []
    seen_headers: set[str] = set()
    for row in rows:
        for header in row.keys():
            if header not in seen_headers:
                headers.append(header)
                seen_headers.add(header)
    return headers


def select_english_headers(rows: list[dict[str, str]]) -> list[str]:
    stats: dict[str, dict[str, int]] = defaultdict(lambda: {"english": 0, "cjk": 0, "total": 0})
    for row in rows:
        for header, value in row.items():
            stats[header]["total"] += 1
            if contains_cjk(value):
                stats[header]["cjk"] += 1
            elif re.search(r"[A-Za-z]", value):
                stats[header]["english"] += 1
    headers = []
    for header in select_all_headers(rows):
        english = stats[header]["english"]
        cjk = stats[header]["cjk"]
        if english == 0 and cjk > 0:
            continue
        if english > 0 and english >= cjk:
            headers.append(header)
    return headers


def build_agent_data(records: dict[str, ProductRecord]) -> dict:
    products: list[dict] = []

    for key in PRODUCT_ORDER:
        record = records[key]
        knowledge_content = build_product_page(record, language="en")

        brochure_rows = []
        for path in record.docs.get("单页_xlsx", []):
            brochure_rows.extend(sheet_rows(path))

        website_rows = []
        for path in record.docs.get("官网文档_xlsx", []):
            website_rows.extend(sheet_rows(path))

        spec_rows = []
        for path in record.docs.get("参数_xlsx", []):
            spec_rows.extend(sheet_rows(path))

        competitor_rows = []
        for path in record.docs.get("竞品分析_xlsx", []):
            competitor_rows.extend(sheet_rows(path))

        slogan = extract_slogan(brochure_rows, language="en") or extract_slogan(website_rows, language="en") or "Not extracted"
        description = extract_description(brochure_rows, language="en") if brochure_rows else extract_description(website_rows, language="en")
        highlights = extract_highlights(brochure_rows, language="en")
        if len(highlights) < 4:
            for item in extract_highlights(website_rows, language="en"):
                if item not in highlights:
                    highlights.append(item)
                if len(highlights) >= 6:
                    break
        highlights = [item for item in highlights if item not in {slogan, description}]
        specs = [englishize_text(item) for item in extract_specs(spec_rows)]
        competitors = [englishize_text(item) for item in extract_competitors(competitor_rows, record.key)]
        present_count = sum(bool(record.docs.get(doc_type)) for doc_type in DOC_ORDER[:-1]) + int(bool(record.image_dirs))
        gaps = collect_gaps_en(record)

        document_groups = []
        preview_candidates = []
        for doc_type in DOC_ORDER:
            if doc_type == "产品ID图_dir":
                if not record.image_dirs:
                    continue
                items = []
                for image_dir in record.image_dirs:
                    image_files = list_image_files(image_dir)
                    item = {
                        "type": "gallery",
                        "title": image_dir.name,
                        "path": url_for(image_dir, AGENT_DIR),
                        "count": len(image_files),
                        "images": [
                            {
                                "name": image_file.name,
                                "path": url_for(image_file, AGENT_DIR),
                            }
                            for image_file in image_files
                        ],
                    }
                    items.append(item)
                    preview_candidates.append(
                        {
                            "group": DOC_LABELS[doc_type],
                            "groupEn": DOC_LABELS_EN[doc_type],
                            "type": "gallery",
                            "title": image_dir.name,
                            "count": len(image_files),
                            "images": item["images"],
                        }
                    )
                document_groups.append(
                    {
                        "key": doc_type,
                        "label": DOC_LABELS[doc_type],
                        "labelEn": DOC_LABELS_EN[doc_type],
                        "items": items,
                    }
                )
                continue

            paths = record.docs.get(doc_type, [])
            if not paths:
                continue
            items = []
            for path in paths:
                item = {
                    "type": preview_document_type(doc_type),
                    "title": path.name,
                    "path": url_for(path, AGENT_DIR),
                }
                if item["type"] == "spreadsheet":
                    item["preview"] = xlsx_preview_payload(path, AGENT_DIR)
                items.append(item)
                preview_candidates.append(
                        {
                            "group": DOC_LABELS[doc_type],
                            "groupEn": DOC_LABELS_EN[doc_type],
                            **item,
                        }
                    )
            document_groups.append(
                {
                    "key": doc_type,
                    "label": DOC_LABELS[doc_type],
                    "labelEn": DOC_LABELS_EN[doc_type],
                    "items": items,
                }
            )

        default_preview = None
        brochure_pdfs = [
            candidate
            for candidate in preview_candidates
            if candidate["group"] == DOC_LABELS["单页_pdf"] and candidate["type"] == "pdf"
        ]
        if brochure_pdfs:
            default_preview = sorted(brochure_pdfs, key=brochure_priority)[0]
        else:
            default_preview = next(
                (candidate for candidate in preview_candidates if candidate["type"] == "pdf"),
                preview_candidates[0] if preview_candidates else None,
            )

        product_page = PRODUCT_DIR / f"{key}.md"
        knowledge_group = {
            "key": "知识页_md",
            "label": "知识页",
            "labelEn": "Knowledge Page",
            "items": [
                {
                    "type": "markdown",
                    "title": f"{key} Knowledge Page",
                    "path": url_for(product_page, AGENT_DIR),
                    "content": knowledge_content,
                }
            ],
        }
        document_groups.insert(0, knowledge_group)
        products.append(
            {
                "key": key,
                "fullName": record.meta["full_name"],
                "classification": PRODUCT_META_EN[key]["classification"],
                "scenarios": PRODUCT_META_EN[key]["scenarios"],
                "slogan": slogan,
                "description": description,
                "highlights": highlights[:6],
                "specs": specs[:8],
                "competitors": competitors,
                "gaps": gaps,
                "coverageLabel": coverage_label_en(present_count),
                "coverageCount": present_count,
                "knowledgePage": url_for(product_page, AGENT_DIR),
                "documentGroups": document_groups,
                "defaultPreview": default_preview,
                "docCount": sum(len(group["items"]) for group in document_groups),
            }
        )

    return {
        "title": "FJD Robotic Mower Asset Hub",
        "description": "A central library for FJD robotic mower brochures, guides, manuals, specs, and supporting sales materials.",
        "products": products,
    }


def build_product_page(record: ProductRecord, language: str = "cn") -> str:
    brochure_rows = []
    for path in record.docs.get("单页_xlsx", []):
        brochure_rows.extend(sheet_rows(path))

    website_rows = []
    for path in record.docs.get("官网文档_xlsx", []):
        website_rows.extend(sheet_rows(path))

    spec_rows = []
    for path in record.docs.get("参数_xlsx", []):
        spec_rows.extend(sheet_rows(path))

    competitor_rows = []
    for path in record.docs.get("竞品分析_xlsx", []):
        competitor_rows.extend(sheet_rows(path))

    doc_labels = DOC_LABELS_EN if language == "en" else DOC_LABELS
    meta = PRODUCT_META_EN[record.key] if language == "en" else record.meta
    slogan = extract_slogan(brochure_rows, language=language) or extract_slogan(website_rows, language=language) or ("Not extracted" if language == "en" else "未提取到")
    description = extract_description(brochure_rows, language=language) if brochure_rows else extract_description(website_rows, language=language)
    highlights = extract_highlights(brochure_rows, language=language)
    if len(highlights) < 4:
        for item in extract_highlights(website_rows, language=language):
            if item not in highlights:
                highlights.append(item)
            if len(highlights) >= 6:
                break
    specs = extract_specs(spec_rows)
    if language == "en":
        specs = [englishize_text(item) for item in specs]
    competitors = extract_competitors(competitor_rows, record.key)
    if language == "en":
        competitors = [englishize_text(item) for item in competitors]
    present_count = sum(bool(record.docs.get(doc_type)) for doc_type in DOC_ORDER[:-1]) + int(bool(record.image_dirs))
    gaps = collect_gaps_en(record) if language == "en" else collect_gaps(record)
    file_base = PRODUCT_DIR
    highlights = [item for item in highlights if item not in {slogan, description}]

    if language == "en":
        lines: list[str] = [
            f"# {record.meta['full_name']} Knowledge Page",
            "",
            "## Positioning Summary",
            f"- One-line Positioning: {slogan}",
            f"- Product Classification: {meta['classification']}",
            f"- Primary Scenarios: {meta['scenarios']}",
            f"- Description Summary: {description}",
            "",
            "## Core Highlights",
        ]
    else:
        lines = [
            f"# {record.meta['full_name']} 知识页",
            "",
            "## 定位摘要",
            f"- 一句话定位：{slogan}",
            f"- 产品分类：{meta['classification']}",
            f"- 主要场景：{meta['scenarios']}",
            f"- 描述摘要：{description}",
            "",
            "## 核心卖点",
        ]
    if highlights:
        lines.extend(f"- {item}" for item in highlights[:6])
    else:
        lines.append("- No sufficient highlights were extracted from structured source files." if language == "en" else "- 暂未从结构化资料中提取到足够卖点。")

    lines.extend(["", "## Key Specs" if language == "en" else "## 关键参数"])
    if specs:
        lines.extend(f"- {item}" for item in specs)
    else:
        lines.append("- No key specifications were extracted from the spec sheet." if language == "en" else "- 暂未从参数表中提取到关键参数。")

    lines.extend([
        "",
        "## Material Coverage" if language == "en" else "## 资料覆盖",
        f"- Coverage: {coverage_label_en(present_count)} ({present_count}/8 core material types covered)" if language == "en" else f"- 完备度：{coverage_label(present_count)}（已覆盖 {present_count}/8 类核心资料）",
    ])
    if gaps:
        lines.append(f"- Current Gaps: {'; '.join(gaps)}" if language == "en" else f"- 当前缺口：{'；'.join(gaps)}")

    lines.extend(["", "## File Index" if language == "en" else "## 文件索引"])
    for doc_type in DOC_ORDER:
        if doc_type == "产品ID图_dir":
            if not record.image_dirs:
                continue
            lines.append(f"### {doc_labels[doc_type]}")
            for image_dir in record.image_dirs:
                count = sum(1 for file in image_dir.rglob("*") if file.is_file() and not file.name.startswith("."))
                lines.append(f"- {md_link(image_dir, file_base)} ({count} images)" if language == "en" else f"- {md_link(image_dir, file_base)}（{count} 张）")
            continue

        paths = record.docs.get(doc_type, [])
        if not paths:
            continue
        lines.append(f"### {doc_labels[doc_type]}")
        if doc_type == "单页_pdf":
            lines.extend(brochure_versions(paths, file_base))
        else:
            lines.extend(f"- {md_link(path, file_base)}" for path in paths)

    lines.extend(["", "## Competitor Reference" if language == "en" else "## 竞品参考"])
    if competitors:
        lines.extend(f"- {name}" for name in competitors)
    else:
        lines.append("- No competitor analysis sheet was found for this product, or competitor names could not be extracted from the header." if language == "en" else "- 当前目录下未发现该产品的竞品分析表，或表头未提取到竞品名称。")

    lines.extend([
        "",
        "## Operations Note" if language == "en" else "## 运营备注",
        "- The product classification and some scenario tags on this page are internal organizing inferences based on current copy, spec sheets, and file coverage. Please confirm the latest official messaging before external use." if language == "en" else "- 本页中的“产品分类”与部分“主要场景”为基于现有文案、参数表和资料分布做的整理性推断，适合用于内部知识沉淀，正式对外口径建议再结合最新版本物料确认。",
    ])
    return "\n".join(lines) + "\n"


def build_readme(records: dict[str, ProductRecord]) -> str:
    lines = [
        "# 割草机产品知识库",
        "",
        "本知识库基于当前工程目录中的单页、官网文档、参数表、快速指南、说明书、竞品分析与产品 ID 图自动整理生成。",
        "",
        "## 使用说明",
        "- 适合产品运营、市场、售前在内部快速查找产品定位、卖点、参数与素材覆盖情况。",
        "- 产品分类与部分场景标签为基于现有资料的整理性推断，不等同于最终对外发布口径。",
        "- 如目录内新增或替换资料，可重新运行 `python3 知识库/scripts/build_knowledge_base.py` 刷新。",
        "",
        "## 产品总览",
        "",
        "| 产品 | 推断分类 | 主要场景 | 关键指标 | 资料完备度 | 页面 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for key in PRODUCT_ORDER:
        record = records[key]
        spec_rows = []
        for path in record.docs.get("参数_xlsx", []):
            spec_rows.extend(sheet_rows(path))
        metric = key_metric(extract_specs(spec_rows))
        present_count = sum(bool(record.docs.get(doc_type)) for doc_type in DOC_ORDER[:-1]) + int(bool(record.image_dirs))
        page = PRODUCT_DIR / f"{key}.md"
        lines.append(
            "| {product} | {classification} | {scenarios} | {metric} | {coverage} | [{page_name}]({page_url}) |".format(
                product=key,
                classification=record.meta["classification"],
                scenarios=record.meta["scenarios"],
                metric=truncate_text(metric.replace("|", "\\|")),
                coverage=f"{coverage_label(present_count)}（{present_count}/8）",
                page_name=f"{key}.md",
                page_url=quote(f"products/{page.name}", safe="/"),
            )
        )

    lines.extend(
        [
            "",
            "## 资料缺口提醒",
        ]
    )

    for key in PRODUCT_ORDER:
        record = records[key]
        gaps = collect_gaps(record)
        if gaps:
            lines.append(f"- {key}：{'；'.join(gaps)}")
        else:
            lines.append(f"- {key}：核心资料已基本齐全。")

    lines.extend(
        [
            "",
            "## 目录说明",
            "- `products/`：每个产品一页，包含定位摘要、核心卖点、参数、资料索引和竞品参考。",
            "- `agent/`：深色产品资料集成网页，支持搜索、点选和在线预览。",
            "- `scripts/`：知识库生成脚本，便于后续重复整理。",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(records: dict[str, ProductRecord]) -> None:
    PRODUCT_DIR.mkdir(parents=True, exist_ok=True)
    AGENT_DIR.mkdir(parents=True, exist_ok=True)
    for key, record in records.items():
        product_path = PRODUCT_DIR / f"{key}.md"
        product_path.write_text(build_product_page(record), encoding="utf-8")
    (KB_DIR / "README.md").write_text(build_readme(records), encoding="utf-8")
    data_payload = "window.__FJD_AGENT_DATA__ = " + json.dumps(
        build_agent_data(records),
        ensure_ascii=False,
        indent=2,
    ) + ";\n"
    (AGENT_DIR / "data.js").write_text(data_payload, encoding="utf-8")


def main() -> None:
    records = collect_records()
    write_outputs(records)
    print(f"知识库已生成：{KB_DIR}")


if __name__ == "__main__":
    main()
