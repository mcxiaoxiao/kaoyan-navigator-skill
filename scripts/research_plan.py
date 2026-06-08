#!/usr/bin/env python3
"""Generate a concrete research plan for kaoyan historical data collection."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Iterable


DEFAULT_TARGET_FIELDS = [
    "national_line",
    "retest_line",
    "planned_total",
    "recommended_exempt",
    "unified_quota",
    "applicants",
    "retest_count",
    "admitted_count",
    "admitted_min",
    "admitted_median",
    "admitted_mean",
    "subject_change",
]

SOURCE_ORDER = [
    {
        "grade": "A",
        "sources": ["学校研究生院", "招生网", "学院官网", "官方 PDF / 公示"],
        "use": "核心结论首选",
    },
    {
        "grade": "B",
        "sources": ["学校官方公众号", "政府媒体", "可复核名单统计"],
        "use": "补强核心结论",
    },
    {
        "grade": "C",
        "sources": ["教育媒体", "考研机构", "可靠聚合站"],
        "use": "发现线索并回源",
    },
    {
        "grade": "D",
        "sources": ["知乎", "小红书", "B 站", "论坛", "自媒体"],
        "use": "只作热度或个体体验",
    },
]

QUERY_TEMPLATES = [
    "site:{site_prefix} {major_code_or_name} {year} 招生专业目录",
    "site:{site_prefix} {major_code_or_name} {year} 复试录取工作实施细则",
    "site:{site_prefix} {major_code_or_name} {year} 拟录取名单",
    "site:{site_prefix} {major_code_or_name} {year} 推免 拟录取",
    "{school} {college} {major_code_or_name} {year} 复试线 招生人数",
    "{school} {college} {major_code_or_name} {year} 报录比 报考人数 上线人数",
    "{school} {college} {major_code_or_name} {year} 初试科目 调整 改考",
]

FIELD_QUESTIONS = {
    "national_line": "我还没找到该年的国家线或对应学科分数线，请提供相关官方公告或允许我继续检索。",
    "retest_line": "我已经找到部分资料，但没找到该专业的复试线，请上传复试细则、学院公告或截图。",
    "planned_total": "我已经找到招生目录，但没法确认该年总计划招生数，请补充招生专业目录或学院说明。",
    "recommended_exempt": "我暂时没找到推免拟录取人数，请补充推免公示或学院公告。",
    "unified_quota": "我暂时没法确认统考名额，请补充招生计划脚注、推免名单或拟录取公示。",
    "applicants": "我还没找到报考人数或报录比，请补充一志愿统计、学院说明或可复核来源。",
    "retest_count": "我还没找到进入复试的人数，请补充复试名单或复试公示。",
    "admitted_count": "我还没找到最终录取人数，请补充拟录取公示或名单截图。",
    "admitted_min": "我还没找到录取最低分，请补充拟录取名单或成绩列表。",
    "admitted_median": "我还没找到录取中位数，若有名单可直接提取后计算。",
    "admitted_mean": "我还没找到录取平均分，若有名单可直接提取后计算。",
    "subject_change": "我还没确认是否改考或调整科目，请补充招生目录或考试大纲变更说明。",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate kaoyan research plan")
    parser.add_argument("--school", required=True, help="Target school name")
    parser.add_argument("--school-domain", default="", help="Optional official website domain")
    parser.add_argument("--college", required=True, help="Target college name")
    parser.add_argument("--major-code", default="", help="Major code")
    parser.add_argument("--major-name", default="", help="Major name")
    parser.add_argument("--year", required=True, type=int, help="Enrollment year")
    parser.add_argument("--study-mode", default="", help="Full-time / part-time")
    parser.add_argument("--degree-type", default="", help="Academic / professional")
    parser.add_argument("--have", nargs="*", default=[], help="Fields already available")
    parser.add_argument("--need", nargs="*", default=DEFAULT_TARGET_FIELDS, help="Fields to collect")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Output format")
    return parser.parse_args()


def normalize_year_window(year: int) -> list[int]:
    return [year - 3, year - 2, year - 1]


def build_query_subject(major_code: str, major_name: str) -> str:
    if major_code and major_name:
        return f"{major_code} {major_name}"
    return major_code or major_name or "专业"


def build_site_prefix(school_domain: str) -> str:
    return school_domain or "学校官方域名"


def build_queries(args: argparse.Namespace, years: Iterable[int]) -> list[str]:
    subject = build_query_subject(args.major_code, args.major_name)
    site_prefix = build_site_prefix(args.school_domain)
    queries: list[str] = []
    for year in years:
        for template in QUERY_TEMPLATES:
            queries.append(
                template.format(
                    school=args.school,
                    college=args.college,
                    major_code_or_name=subject,
                    year=year,
                    site_prefix=site_prefix,
                )
            )
    return queries


def build_missing_fields(need: Iterable[str], have: Iterable[str]) -> list[str]:
    have_set = {item.strip() for item in have if item.strip()}
    seen: set[str] = set()
    missing: list[str] = []
    for field in need:
        if field in have_set or field in seen:
            continue
        seen.add(field)
        missing.append(field)
    return missing


def build_plan(args: argparse.Namespace) -> dict[str, object]:
    years = normalize_year_window(args.year)
    missing_fields = build_missing_fields(args.need, args.have)
    subject = build_query_subject(args.major_code, args.major_name)
    fallback_questions = [FIELD_QUESTIONS[field] for field in missing_fields if field in FIELD_QUESTIONS]

    return {
        "research_object": {
            "school": args.school,
            "school_domain": args.school_domain or None,
            "college": args.college,
            "major_code": args.major_code or None,
            "major_name": args.major_name or None,
            "subject": subject,
            "study_mode": args.study_mode or None,
            "degree_type": args.degree_type or None,
            "target_year": args.year,
        },
        "data_window": years,
        "source_order": SOURCE_ORDER,
        "query_templates": build_queries(args, years),
        "need_fields": list(args.need),
        "have_fields": [field for field in args.have if field.strip()],
        "missing_fields": missing_fields,
        "fallback_questions": fallback_questions,
        "collection_rules": [
            "先官方，再补强，再线索，再弱信号。",
            "每条记录保留来源标题、URL、发布日期/访问日期和来源等级。",
            "不同学院、代码、培养方式不合并。",
            "未知留空，不要用 0 代替。",
        ],
    }


def format_text(plan: dict[str, object]) -> str:
    object_info = plan["research_object"]
    lines = [
        "研究对象:",
        f"  学校: {object_info['school']}",
        f"  官方域名: {object_info['school_domain'] or '未指定'}",
        f"  学院: {object_info['college']}",
        f"  专业: {object_info['subject']}",
        f"  培养方式: {object_info['study_mode'] or '未指定'}",
        f"  学位类型: {object_info['degree_type'] or '未指定'}",
        f"  目标年份: {object_info['target_year']}",
        "",
        f"数据窗口: {plan['data_window'][0]}-{plan['data_window'][-1]}",
        "来源顺序:",
    ]
    for item in plan["source_order"]:
        lines.append(f"  {item['grade']}: {', '.join(item['sources'])}（{item['use']}）")
    lines.extend(
        [
            "",
            "查询模板:",
        ]
    )
    for index, query in enumerate(plan["query_templates"], start=1):
        lines.append(f"  {index}. {query}")
    lines.extend(
        [
            "",
            "需要补齐的字段:",
            "  " + (", ".join(plan["missing_fields"]) if plan["missing_fields"] else "无"),
            "",
            "追问模板:",
        ]
    )
    if plan["fallback_questions"]:
        for question in plan["fallback_questions"]:
            lines.append(f"  - {question}")
    else:
        lines.append("  - 无")
    lines.extend(
        [
            "",
            "收集规则:",
        ]
    )
    for rule in plan["collection_rules"]:
        lines.append(f"  - {rule}")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    plan = build_plan(args)
    if args.format == "json":
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(format_text(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
