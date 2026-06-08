# 数据格式

推荐 CSV 一行表示一个“年份 + 同口径专业”：

```csv
year,school,college,major_code,major_name,study_mode,degree_type,national_line,retest_line,planned_total,recommended_exempt,unified_quota,applicants,retest_count,admitted_count,admitted_min,admitted_median,admitted_mean,subject_change,source_url,source_grade,notes
2026,示例大学,计算机学院,085404,计算机技术,全日制,专硕,260,315,60,18,42,380,56,42,326,351,353.4,改考408,https://example.edu.cn,A,
```

## 必需字段

- `year`
- `school`
- `college`
- `major_code` 或可唯一定位的 `major_name`
- `study_mode`
- 至少一个可分析指标

## 推荐字段

- 分数：`national_line`, `retest_line`, `admitted_min`, `admitted_median`, `admitted_mean`
- 供给：`planned_total`, `recommended_exempt`, `unified_quota`
- 竞争：`applicants`, `retest_count`, `admitted_count`
- 变化：`subject_change`
- 证据：`source_url`, `source_grade`, `notes`

空值留空，不填 `0`。`0` 只表示官方明确为零。

JSON 可以是记录数组，字段名与 CSV 相同：

```json
[
  {
    "year": 2026,
    "school": "示例大学",
    "college": "计算机学院",
    "major_code": "085404",
    "study_mode": "全日制",
    "retest_line": 315,
    "unified_quota": 42,
    "source_grade": "A"
  }
]
```

