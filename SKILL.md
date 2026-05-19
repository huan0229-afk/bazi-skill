---
name: bazi
description: >
  Chinese Ba Zi (八字 / Four Pillars of Destiny) chart calculation and classical text
  interpretation. Use for: birth chart analysis, 排盘, destiny analysis, 命理,
  十神 analysis, 格局 analysis, marriage compatibility, career fortune, health
  analysis, luck cycles (大运/流年). Automatically computes the full birth chart
  from birth date/time/gender, then interprets using a structured knowledge base
  of classical texts (滴天髓, 三命通会, 渊海子平, 穷通宝鉴, 子平真诠, 神峰通考,
  命理约言). Also use when the user mentions their birth chart, 生辰八字,
  fortune telling, 算命, 运势, asks about destiny/life path, or provides a birth
  date and time for analysis of any kind related to fate, luck, personality, or
  life patterns.
---

# Ba Zi (八字) Analysis Skill

## Overview

This skill computes a complete Four Pillars chart from the user's birth date/time/gender, then interprets it using classical Chinese Ba Zi texts organized as a structured knowledge base.

## Workflow

### Step 1: Gather Birth Information

Ask the user for:

- **Birth year, month, day** (Gregorian calendar, e.g. 1990-06-15)
- **Birth time** (exact time like 14:30, or Chinese 时辰 like 未时)
- **Gender** (male/female — required for 大运 direction)

Why gender matters: 阳男阴女顺排, 阴男阳女逆排. The 大运 direction depends on gender AND year stem yin/yang.

时辰 conversion:
| 时辰 | Time | | 时辰 | Time |
|------|------|-|------|------|
| 子时 | 23:00-01:00 | | 午时 | 11:00-13:00 |
| 丑时 | 01:00-03:00 | | 未时 | 13:00-15:00 |
| 寅时 | 03:00-05:00 | | 申时 | 15:00-17:00 |
| 卯时 | 05:00-07:00 | | 酉时 | 17:00-19:00 |
| 辰时 | 07:00-09:00 | | 戌时 | 19:00-21:00 |
| 巳时 | 09:00-11:00 | | 亥时 | 21:00-23:00 |

### Step 2: Run the Calculator

Pipe JSON to the calculator script. The script uses UTF-8 stdout internally, but for cross-platform safety, always set `PYTHONIOENCODING=utf-8`:

**On Linux/macOS (Bash):**
```bash
echo '{"year":1990,"month":6,"day":15,"hour":14,"minute":30,"gender":"male"}' | python scripts/bazi_calculator.py
```

**On Windows (PowerShell): use variable capture to avoid pipe + path-with-spaces issues:**
```powershell
$env:PYTHONIOENCODING = 'utf-8'
$inputJson = '{"year":1990,"month":6,"day":15,"hour":14,"minute":30,"gender":"male"}'
$inputJson | Set-Content -Path bazi_input.json -Encoding utf8
$output = python scripts/bazi_calculator.py --file bazi_input.json 2>&1
$output | Out-File -FilePath bazi_output.json -Encoding utf8
```

**Why variable capture instead of pipe:**
- PowerShell 5.1 cannot pipe into a quoted executable path (`... | & "path with spaces\script.py"` fails with `CantActivateDocumentInPipeline`)
- PowerShell's `>` redirect uses UTF-16 LE, garbling UTF-8 output from Python
- Capturing to a variable (`$output = python ...`) then piping to `Out-File -Encoding utf8` avoids both issues
- Works regardless of whether the user's name or skill path contains spaces

If the output contains garbled characters (common on Chinese Windows), ensure `PYTHONIOENCODING=utf-8` is set before running.

The script outputs a complete JSON chart with: pillars (with xunkong), day_master, ten_gods, hidden_stems, five_elements, wuxing_counts, dayun, shensha, solar_terms (with precise hour/minute times), start_age, boundary_warning, liunian (current year ±1), minggong, taiyuan.

**Precise solar term times**: The calculator computes the approximate hour/minute of each solar term (accuracy ±30 min). Year and month pillar boundaries are determined by comparing the birth hour against the solar term hour, not just the date. This means same-day births on 立春 get the correct year pillar based on whether birth time is before or after the exact 立春 moment.

### Step 3: Present the Chart

Format the four pillars clearly:

```
四柱:
  年柱: [stem][branch] ([nayin]) 空亡: [xunkong_branches]
  月柱: [stem][branch] ([nayin]) 空亡: [xunkong_branches]
  日柱: [stem][branch] ([nayin]) 空亡: [xunkong_branches]
  时柱: [stem][branch] ([nayin]) 空亡: [xunkong_branches]

日主: [stem] ([element], [yin_yang])

命宫: [stem][branch]  胎元: [stem][branch]

五行统计: 木:X 火:X 土:X 金:X 水:X

大运: [start_age]岁起运, [direction]
  [start_age]-[start_age+9]岁: [stem][branch]
  ...

流年:
  202x: [stem][branch] ([ten_god])
  202x: [stem][branch] ([ten_god])
  202x: [stem][branch] ([ten_god])
```

### Step 4: Read All Relevant References

**You MUST read ALL of the following reference files for EVERY chart analysis.** Do not skip any — each file contains essential information for a complete, professional-grade interpretation:

Read in this order:
1. `references/01-yinyang-wuxing.md` — for 十二长生, 五行生克辩证, 日主强弱判断
2. `references/02-tiangan-dizhi.md` — for 干支关系, 暗合, 十干性情, 藏干分析
3. `references/03-shishen.md` — for 十神含义, 互见关系, 组合要诀
4. `references/04-geju.md` — for 格局判定, 成败, 变格
5. `references/05-yongshen.md` — for 用神选取, 喜忌神辩证
6. `references/06-dayun-liunian.md` — for 大运流年分析
7. `references/07-shensha.md` — for 神煞辅助判断
8. `references/classical-texts/zipingzhenquan.md` — for 格局古典依据
9. `references/classical-texts/ditiansui.md` — for 五行/用神古典依据
10. `references/classical-texts/qiongtongbaojian.md` — for 调候用神

Then, based on what the user asks about or what the chart reveals, also read:
| Topic | Read |
|---|---|
| Marriage/relationships | references/08-hunyin.md |
| Career/wealth | references/09-shiye-caifu.md |
| Health | references/10-jiankang.md |
| Specific classical backing | references/classical-texts/sanmingtonghui.md, yuanhaiziping.md, shenfengtongkao.md, mingliyueyan.md |

### Step 5: Produce Comprehensive Analysis

**CRITICAL: The output MUST be thorough and detailed.** This is a professional Ba Zi consultation, not a quick summary. Every judgment must be explained with reasoning, not just stated. Every pillar must be analyzed individually. Every ten god must be discussed. Classical texts MUST be quoted to support key interpretations.

The analysis MUST include ALL of the following sections in order:

---

#### 一、排盘结果 (Chart Output)

Present the complete chart with full detail:

**四柱**:
- 年柱: [stem][branch] (纳音: [nayin], 空亡: [xunkong], 旬: [xun_name])
- 月柱: [stem][branch] (纳音: [nayin], 空亡: [xunkong], 旬: [xun_name])
- 日柱: [stem][branch] (纳音: [nayin], 空亡: [xunkong], 旬: [xun_name])
- 时柱: [stem][branch] (纳音: [nayin], 空亡: [xunkong], 旬: [xun_name])

**日主**: [stem] ([element], [yin_yang]) — 简要说明日主的基本含义和代表性情

**命宫**: [stem][branch] (纳音: [nayin]) — 说明命宫的含义
**胎元**: [stem][branch] (纳音: [nayin]) — 说明胎元的含义

**五行统计**: 木:X 火:X 土:X 金:X 水:X — 说明五行分布的特征（偏枯/平衡，哪行过旺/过弱）

**节气**: 出生于「[prev_jie]」之后、「[next_jie]」之前。说明节气时刻及对月柱的影响。如有 boundary_warning，详加说明。

---

#### 二、逐柱十神分析 (Pillar-by-Pillar Ten God Analysis)

Analyze EVERY pillar's stem and branch ten god in detail:

**年柱 [stem][branch]**:
- 天干 [stem]: [ten_god] — 含义，在年柱的位置意义
- 地支 [branch]: 主气 [ten_god] — 含义
- 藏干分析: 逐一说明本气/中气/余气及其十神
- 年柱为祖上、童年宫位，说明对命主早年的影响

**月柱 [stem][branch]**:
- 天干 [stem]: [ten_god] — 含义，在月柱的位置意义
- 地支 [branch]: 主气 [ten_god] — 含义
- 藏干分析: 逐一说明
- 月柱为父母、事业宫位，说明对青年时期的影响

**日柱 [stem][branch]**:
- 天干 [stem]: 日主本身 — 十干性情详细描述（性格、思维、体质）
- 地支 [branch] (夫妻宫): 主气 [ten_god] — 对婚姻的影响
- 藏干分析: 逐一说明
- 日柱为自身、配偶宫位

**时柱 [stem][branch]**:
- 天干 [stem]: [ten_god] — 含义，在时柱的位置意义
- 地支 [branch]: 主气 [ten_god] — 含义
- 藏干分析: 逐一说明
- 时柱为子女、晚年宫位

**柱间关系**: 分析年月日时四柱之间的合冲刑害关系（如年月干合、日时支冲等）

---

#### 三、日主强弱详细判断 (Day Master Strength Analysis)

逐项分析，不可只给结论：

1. **得令（月令）**: 日主在月令处于什么状态？引用十二长生（如"壬水生于午月，处胎地，不得令"）。月令旺相休囚死如何？
2. **得地（通根）**: 日主在地支中有哪些根气？逐一列出（长生/禄/旺/库/余气），并评估每个根的强弱
3. **得生（印星）**: 天干和地支藏干中有无印星生扶？印星是否有根？远近如何？
4. **得助（比劫）**: 有无同五行天干或地支藏干帮扶？比劫是否有力量？
5. **综合评分**: 得令(40%) + 得地(30%) + 得生(20%) + 得助(10%) → 给出身强/身弱/中和的明确结论
6. **调候因素**: 生于何季？寒暖燥湿如何？是否需要调候？

---

#### 四、格局分析 (Pattern Analysis)

1. **月令定格**: 月令主气是什么十神？是否透干？以此定格局
2. **格局成败**: 引用子平真诠的判定标准，分析格局是否成立
   - 成格的条件是什么？本命是否满足？
   - 有无破格之因素（如正官格遇伤官、财格遇比劫夺财等）
   - 如有败破，有无救应？
3. **格局高低**: 有情？有力？清纯？判断格局层次
4. **变格考察**: 是否可能为从格/化格/专旺格？逐一排除或确认
5. **引用古典**: 引用子平真诠、渊海子平关于此格局的原文

---

#### 五、用神分析 (Favorable Element Analysis)

1. **用神选取**: 基于日主强弱和格局，用扶抑法/调候法/通关法/病药法综合分析
   - 扶抑角度: 该扶还是该抑？
   - 调候角度: 生于何季，需要什么五行调候？（引用穷通宝鉴该日主该月令的用神建议）
   - 病药角度: 命局最大的"病"是什么？"药"是什么？
2. **用神五行**: 明确第一用神、第二用神（如"第一用神为金，第二用神为水"）
3. **喜神**: 生助用神者
4. **忌神**: 克制用神者，并说明忌神在命局中的位置和力量
5. **用神力度**: 用神是否得令？透干？通根？被克？评定用神的力量等级
6. **引用古典**: 引用滴天髓、穷通宝鉴的用神原则

---

#### 六、大运分析 (Major Luck Cycles)

1. **起运**: 说明起运年龄和排运方向（阳/阴年+男/女→顺/逆排）
2. **当前大运**: 详细分析当前所在的大运（干支、十神、与原局的互动）
   - 此运天干是何十神？有何影响？
   - 此运地支与原局各柱有何关系？（合冲刑害）
   - 此运对事业、财运、婚姻的总体影响
3. **每步大运**: 列表分析每步大运（至少列出前6步），每步说明：
   - 干支+纳音
   - 十神
   - 与原局的关系
   - 该运的吉凶总体判断
4. **一生运势曲线**: 描述整体运势走向（先苦后甜/步步高升/起伏不定等）

---

#### 七、流年分析 (Current & Upcoming Years)

1. **当前流年**: 详细分析当年的干支、十神、与原局和大运的互动
   - 流年天干含义，流年地支含义
   - 流年与命局的合冲刑害
   - 流年与大运的关系（天克地冲？岁运并临？伏吟？）
   - 当年具体注意事项（事业/财运/感情/健康）
2. **未来三年**: 未来三年的简要运程提示

---

#### 八、神煞参考 (Spirit Stars)

列出四柱神煞，说明每个神煞的含义：
- 贵人类（天乙、太极、文昌等）
- 桃花驿马类
- 吉神类（禄神、将星等）
- 凶煞类（羊刃、劫煞等，如有）
- **注意**: 强调神煞只是辅助参考

---

#### 九、专题分析 (Topic Analysis)

根据命局特点和用户需求，涵盖以下至少2-3个专题：

**事业财运**:
- 适合的行业方向（基于十神组合+五行日主）
- 官运/财运信号
- 创业 vs 打工建议
- 财富规模评估
- 引用子平真诠、滴天髓关于财官的分析

**婚姻感情**:
- 配偶星和夫妻宫分析
- 婚期信号
- 婚姻质量评估
- 如有不利信号，说明化解方向
- 引用三命通会关于婚姻的论述

**健康**:
- 五行偏枯对应的脏腑问题
- 地支冲刑的健康隐患
- 大运中的疾病应期提示
- 养生建议

**性格**:
- 日主十干性情 + 十神组合特征
- 优势与劣势
- 人际关系模式

---

#### 十、古典依据汇总 (Classical References)

汇总分析中引用的所有古典文献原文：
- 滴天髓引文 + 解释
- 子平真诠引文 + 解释
- 穷通宝鉴的调候建议
- 其他古典的相关论述

---

### 输出原则

1. **解释"为什么"**: 每个判断都要附上推理过程，不要只给结论。例如"身弱"要说清楚为什么弱（不得令+无根+无生扶）
2. **引用古典**: 关键判断必须引用古典原文，然后解释如何应用于此命局
3. **逐柱分析**: 不要笼统说"四柱如何"，要一柱一柱详细分析
4. **正反兼顾**: 既要看好的一面，也要指出问题和不顺
5. **给方向不给妄念**: 指出问题和挑战时，同时给出化解方向，但不要过度承诺
6. **语言专业但易懂**: 使用专业术语（十神、格局等），但用白话解释含义

## Built-in Reference Tables

### Solar Terms (12 节, used for month pillar)

| Jie | Approx Date | Month Branch |
|-----|-------------|--------------|
| 立春 | Feb 4 ±1 | 寅 |
| 惊蛰 | Mar 6 ±1 | 卯 |
| 清明 | Apr 5 ±1 | 辰 |
| 立夏 | May 6 ±1 | 巳 |
| 芒种 | Jun 6 ±1 | 午 |
| 小暑 | Jul 7 ±1 | 未 |
| 立秋 | Aug 8 ±1 | 申 |
| 白露 | Sep 8 ±1 | 酉 |
| 寒露 | Oct 8 ±1 | 戌 |
| 立冬 | Nov 7 ±1 | 亥 |
| 大雪 | Dec 7 ±1 | 子 |
| 小寒 | Jan 6 ±1 | 丑 |

### Ten Gods Quick Reference

With day stem as "Self":
- Same element, same yin/yang → 比肩
- Same element, different yin/yang → 劫财
- I generate, same yin/yang → 食神
- I generate, different yin/yang → 伤官
- I control, same yin/yang → 偏财
- I control, different yin/yang → 正财
- Controls me, same yin/yang → 七杀
- Controls me, different yin/yang → 正官
- Generates me, same yin/yang → 偏印
- Generates me, different yin/yang → 正印

> **Note**: Full lookup tables (六十甲子, 纳音, 五虎遁, 五鼠遁, 十神天干表) are in [references/reference-tables.md](references/reference-tables.md). These are already implemented in the calculator — no need to manually reference them during analysis.

## Important Analysis Principles

**THIS IS A COMPREHENSIVE ANALYSIS — NOT A QUICK SUMMARY.**

1. **First judge day master strength** (得令/得地/得生/得助) — this determines everything. Use 十二长生 to evaluate each pillar's real strength, not just simple 五行 counting.
2. **Then identify the 格局** from month pillar — with detailed success/failure conditions from 子平真诠
3. **Then find the 用神** — what the chart needs most, using all four methods (扶抑 / 调候 / 通关 / 病药)
4. **Then check 大运 timing** — when things manifest, each step analyzed individually
5. **神煞 last** — supplementary, never override 十神 analysis
6. **Always ground interpretations in classical texts**, citing the specific source and quoting the original text
7. **Explain WHY for every judgment** — don't just state "身弱", explain why each factor contributes
8. **Flag boundary cases**: The calculator uses precise solar term hour/minute for year and month pillar boundaries. When boundary_warning is not null, the chart already accounts for exact hour — but tell the user they are near a solar term transition and verify the time is correct
9. **Read ALL core references before analyzing** — the references contain essential information. Do not analyze from memory alone.

## Gender and 大运 Direction

| Year Stem | Gender | Direction |
|-----------|--------|-----------|
| 阳 (甲丙戊庚壬) | Male | 顺排 (forward) |
| 阳 (甲丙戊庚壬) | Female | 逆排 (reverse) |
| 阴 (乙丁己辛癸) | Male | 逆排 (reverse) |
| 阴 (乙丁己辛癸) | Female | 顺排 (forward) |

## Common Pattern Quick Reference

| Pattern | Key Feature | Classical Source |
|---------|------------|-----------------|
| 正官格 | Month is 正官, with 印 or 财 support | 子平真诠 |
| 七杀格 | Month is 七杀, with 食制 or 印化 | 子平真诠, 滴天髓 |
| 财格 | Month is 财星, body strong enough | 子平真诠 |
| 印格 | Month is 印星, with 官生 | 子平真诠 |
| 食神格 | Month is 食神, body strong | 子平真诠 |
| 伤官格 | Month is 伤官, with 印 or 财 | 子平真诠 |
| 建禄格 | Month is day master's 禄 | 子平真诠 |
| 从格 | Day master has NO root, follows dominant qi | 滴天髓 |
| 化格 | Day master合化成功 | 滴天髓, 三命通会 |
| 专旺格 | Day master's element dominates everything | 滴天髓 |

## Troubleshooting

- **Solar term boundary births** (±1 day): the calculator now correctly determines the pillar using precise solar term hour/minute (e.g., 立春 at 13:02 means AM births get old year, PM births get new year). The boundary_warning still fires but the chart is already correct — just verify the birth hour is accurate
- **Pre-1900 dates**: algorithm handles but warn about calendar differences
- **Missing birth hour**: default to 子时 (23:00-01:00) but note the limitation
- **Unknown gender**: assume male but note 大运 direction might be wrong
- **If chart seems off**: validate against known online排盘 tools
- **Garbled output (Chinese characters appear as `��`)**: the script outputs UTF-8 — ensure `PYTHONIOENCODING=utf-8` is set or redirect to file. This is most common on Chinese Windows where the console defaults to GBK.
- **Python script path contains spaces** (e.g. `C:\Users\HUAN YIQUN\...`): PowerShell 5.1 cannot pipe into a quoted path. Use `--file` mode instead — write JSON to a temp file, then call the script with `--file`. See the Windows PowerShell example above.
