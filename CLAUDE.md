# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

This is a **Ba Zi (八字 / Four Pillars of Destiny)** calculation and interpretation skill for Claude Code. It computes a complete birth chart from Gregorian birth date/time/gender, then interprets it using a structured knowledge base of classical Chinese texts.

## Architecture

```
SKILL.md                          # Skill instructions (386 lines) — mandates comprehensive 10-section analysis
CLAUDE.md                         # This file — guidance for developing the skill itself
scripts/
  bazi_calculator.py              # Core engine (913 lines, Python 3 stdlib only)
  test_bazi_calculator.py         # Unit tests (20 tests)
references/                       # Expanded knowledge base (~2300 lines across 12 files)
  00-overview.md                  # Analysis workflow, terminology, depth levels (108 lines)
  01-yinyang-wuxing.md            # Yin-Yang, Five Elements, 十二长生, 生克辩证 (254 lines)
  02-tiangan-dizhi.md             # Stems/Branches, 合冲刑害破, 暗合, 拱夹, 十干性情 (258 lines)
  03-shishen.md                   # Ten Gods, 十神互见混杂分析, combinations (315 lines)
  04-geju.md                      # Patterns, 从格/化格 detailed conditions (246 lines)
  05-yongshen.md                  # 用神四大体系, 层次/真假, 调候十干需求 (241 lines)
  06-dayun-liunian.md             # Major/Annual luck, 天克地冲, 岁运并临, 应期法则 (204 lines)
  07-shensha.md                   # 15+ spirit stars with lookup formulas (206 lines)
  08-hunyin.md                    # Marriage, divorce signals, spouse analysis (148 lines)
  09-shiye-caifu.md               # Career paths, wealth scale, 十神+五行 industry matching (172 lines)
  10-jiankang.md                  # Health, organ-disease mapping, timing (155 lines)
  reference-tables.md             # 藏干, 空亡, 月建节气, 五行生克总表, 十神互见 (127 lines)
  classical-texts/
    index.md                      # Index of 7 classical sources
    ditiansui.md                  # 滴天髓 — 通神论/理气论/形象论/十干论/岁运论 (150 lines)
    sanmingtonghui.md             # 三命通会 — 十神/女命/小儿命/神煞 (92 lines)
    yuanhaiziping.md              # 渊海子平 — 喜忌篇/继善篇/定格局诀 (80 lines)
    qiongtongbaojian.md           # 穷通宝鉴 — 十干×十二月调候全表 (209 lines)
    zipingzhenquan.md             # 子平真诠 — 格局/官杀/财印/食伤/变格 (146 lines)
    shenfengtongkao.md            # 神峰通考 — 病药说/实战命例 (70 lines)
    mingliyueyan.md               # 命理约言 — 十干取象/四柱分龄/行运 (85 lines)
README.md                         # User-facing skill documentation
```

## Core Engine (`bazi_calculator.py`)

Pure Python 3 standard library — no external dependencies. 913 lines.

### Design Philosophy

- Functions take integer indices (0-9 stems, 0-11 branches) internally
- Output uses Chinese characters via lookup arrays (STEMS, BRANCHES, etc.)
- JSON stdin/stdout for Claude Code integration; argparse CLI for direct use
- All pillar calculations aware of precise solar term hour/minute boundaries

### Key Functions

| Function | Purpose |
|---|---|
| `get_year_pillar(year)` | Year pillar by stem-branch cycle |
| `get_year_pillar_for_date(year, month, day, hour, minute)` | Year pillar with 立春 boundary check |
| `get_day_pillar(year, month, day)` | Day pillar by days since 1900-01-01 (甲戌) |
| `get_month_pillar(year, month, day, year_stem, hour, minute)` | Month pillar via solar term intervals |
| `get_hour_pillar(day_stem, hour, minute)` | Hour pillar via 五鼠遁 |
| `get_ten_god(day_stem, other_stem)` | Ten God (十神) by element + yin/yang relationship |
| `get_dayun(year_stem, month_stem, month_branch, birth_date, prev_jie, next_jie, gender)` | Major Luck cycles (大运) |
| `get_shensha(pillars, day_stem, year_stem, year_branch)` | Spirit stars (神煞) |
| `get_hidden_stems_info(branch_idx)` | Hidden stems (藏干) with qi levels |
| `get_nayin(stem_idx, branch_idx)` | Na Yin (纳音) five-element classification |
| `get_xunkong(sixty_idx)` | Xun Kong (空亡) void branches |
| `get_minggong(year_stem, month_branch, hour_branch)` | Life Palace (命宫) |
| `get_taiyuan(month_stem, month_branch)` | Fetus Origin (胎元) |
| `get_wuxing_counts(day_stem, pillars)` | Five Element tally |
| `format_chart_output(year, month, day, hour, minute, gender)` | Complete JSON chart |

### Solar Term Precision

Solar terms are computed with the formula `D = int(Y * 0.2422 + C) - int(Y / 4)`, extracting hour/minute from the fractional part (±30 min accuracy for 1900-2099). The year pillar correctly handles same-day 立春 births by comparing birth hour against the computed 立春 hour/minute.

### 大运 Direction Logic

| Year Stem | Gender | Direction |
|-----------|--------|-----------|
| 阳 (甲丙戊庚壬) | Male | 顺排 (forward) |
| 阳 (甲丙戊庚壬) | Female | 逆排 (reverse) |
| 阴 (乙丁己辛癸) | Male | 逆排 (reverse) |
| 阴 (乙丁己辛癸) | Female | 顺排 (forward) |

## Testing & Validation

### Unit Tests

```bash
python scripts/test_bazi_calculator.py
# 20 tests covering all core functions, golden charts, edge cases
```

### Accuracy Validation

Validation script at `D:\Project\004\validate_accuracy.py` (13 groups, all passing):

1. Day pillar chain consistency (500 random dates 1900-2026)
2. Year pillar sequential verification (years 1-2200)
3. Month pillar 五虎遁 + 11-month sequence (甲辰年)
4. Hour pillar 五鼠遁 + 时辰 boundaries
5. 大运 direction logic + start age
6. 十神 exhaustive 10×10 matrix
7. 藏干 standard table verification
8. 纳音 60-cycle completeness
9. 空亡 verification
10. 神煞 spot checks
11. Precise 立春 boundary with hour/minute
12. 命宫/胎元 consistency
13. Edge cases (leap day, pre-1900, year 1, all 12 months)

### CLI Usage

```bash
# Named flags
python scripts/bazi_calculator.py --year 1990 --month 6 --day 15 --hour 14 --minute 30 --gender male

# Stdin JSON (for Claude Code skill integration)
echo '{"year":1990,"month":6,"day":15,"hour":14,"minute":30,"gender":"male"}' | python scripts/bazi_calculator.py

# From file
python scripts/bazi_calculator.py --file input.json
```

## SKILL.md Analysis Structure

SKILL.md mandates a **comprehensive 10-section analysis** for every chart — progressive disclosure was replaced with mandatory thoroughness:

1. **排盘结果** — Full chart with 纳音/空亡/旬/藏干/五行分布
2. **逐柱十神分析** — Every pillar analyzed individually, including hidden stems and pillar relationships
3. **日主强弱判断** — 十二长生-based evaluation with percentage scoring
4. **格局分析** — Pattern success/failure conditions with 子平真诠 citations
5. **用神分析** — All four methods (扶抑/调候/通关/病药) with 穷通宝鉴 references
6. **大运分析** — All 8 steps with current/past/future trajectory
7. **流年分析** — Current year detailed + next 3 years preview
8. **神煞参考** — Per-pillar spirit stars with supplementary status emphasized
9. **专题分析** — Career/wealth, marriage, health (at least 2-3 topics)
10. **古典依据汇总** — All classical citations with original text + explanation

Key principles: explain WHY for every judgment, cite classical texts, analyze pillar-by-pillar, balance positive and negative.

## Reference Knowledge Base

Reference files were expanded from ~1500 lines to ~2300 lines. Key additions:
- **十二长生** complete table (all 10 stems × 12 branches) with application rules
- **暗合/拱夹** hidden branch relationships
- **十神互见** detailed analysis (官杀混杂, 食伤混杂, 印枭混杂, etc.)
- **从格/化格** true vs false discrimination criteria
- **用神层次** (真/有用/虚/受损/假) and strength evaluation
- **天克地冲/岁运并临/伏吟返吟** concrete prediction techniques
- **流年十神应事速查** table
- **十干疾病** specific organ-disease mapping
- **十神+五行** dual-dimension career matching
- Additional 神煞: 孤辰寡宿, 丧门吊客, 血刃, 勾绞, 学堂, 天厨, 红鸾天喜, 福星贵人
- Standalone lookup tables: 藏干, 空亡, 月建节气, 五行生克总表, 十神互见

- **No dependencies**: stdlib only — `json`, `datetime`, `argparse`, `io`
- **UTF-8 everywhere**: Stdin read with `utf-8-sig` for BOM tolerance; output always UTF-8
- **Chinese gender normalization**: Accepts "男"/"女" in addition to "male"/"female"
- **Banker's rounding**: Uses Python `round()` for start age — `round(x.5)` → nearest even number. This is intentional.
- **All indices 0-based internally**: Stems 0-9 (甲-癸), Branches 0-11 (子-亥)

## Common Pitfalls

- **Solar term boundaries**: Births within ±1 day of a 节 need accurate birth hour. The calculator warns via `boundary_warning` but already computes the correct pillar.
- **Pre-1900 dates**: Algorithm handles but accuracy degrades; warn about calendar differences.
- **Encoding on Windows**: Chinese Windows consoles default to GBK. Always set `PYTHONIOENCODING=utf-8` or redirect to file.
