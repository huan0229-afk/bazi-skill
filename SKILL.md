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

Use bash to pipe JSON to the calculator:

```
echo '{"year":1990,"month":6,"day":15,"hour":14,"minute":30,"gender":"male"}' | python scripts/bazi_calculator.py
```

The script outputs a complete JSON chart with: pillars, day_master, ten_gods, hidden_stems, five_elements, wuxing_counts, dayun, shensha, solar_terms, start_age, boundary_warning.

### Step 3: Present the Chart

Format the four pillars clearly:

```
四柱:
  年柱: [stem][branch] ([nayin])
  月柱: [stem][branch] ([nayin])
  日柱: [stem][branch] ([nayin])
  时柱: [stem][branch] ([nayin])

日主: [stem] ([element], [yin_yang])

五行统计: 木:X 火:X 土:X 金:X 水:X

大运: [start_age]岁起运, [direction]
  [start_age]-[start_age+9]岁: [stem][branch]
  ...
```

### Step 4: Analyze by Topic

Use progressive disclosure. Read reference files based on what the user asks:

| User asks about... | Read |
|---|---|
| Basic chart structure, terms, concepts | references/00-overview.md, references/01-yinyang-wuxing.md |
| Stem-branch interactions, hidden stems | references/02-tiangan-dizhi.md |
| Personality, relationships, life patterns | references/03-shishen.md |
| 格局 (pattern), career type, life direction | references/04-geju.md |
| 用神 (favorable elements), remedies | references/05-yongshen.md |
| Timing, luck cycles, life stages | references/06-dayun-liunian.md |
| 神煞 (spirit stars) | references/07-shensha.md |
| Marriage, spouse compatibility | references/08-hunyin.md |
| Career, wealth, business | references/09-shiye-caifu.md |
| Health, illness, constitution | references/10-jiankang.md |
| Classical text backing for interpretations | references/classical-texts/index.md → specific text |

For comprehensive analysis, read in this order: 03-shishen → 04-geju → 05-yongshen → 06-dayun-liunian.

### Step 5: Synthesize and Present

Structure the analysis:

1. **Chart summary**: Four pillars, day master, element tally
2. **Day master strength**: 得令? 得地? 得生? 得助? → 身强/身弱
3. **格局 identification**: From month pillar, per 04-geju.md
4. **用神 recommendation**: Per 05-yongshen.md — what the chart needs
5. **大运 trajectory**: Current luck cycle and upcoming ones
6. **Topic-specific analysis**: Answer the user's specific question
7. **Classical citations**: Quote relevant classical texts to support interpretations

## Built-in Reference Tables

### The 60 Jia Zi Cycle (六十甲子)

```
 0:甲子  1:乙丑  2:丙寅  3:丁卯  4:戊辰  5:己巳
 6:庚午  7:辛未  8:壬申  9:癸酉 10:甲戌 11:乙亥
12:丙子 13:丁丑 14:戊寅 15:己卯 16:庚辰 17:辛巳
18:壬午 19:癸未 20:甲申 21:乙酉 22:丙戌 23:丁亥
24:戊子 25:己丑 26:庚寅 27:辛卯 28:壬辰 29:癸巳
30:甲午 31:乙未 32:丙申 33:丁酉 34:戊戌 35:己亥
36:庚子 37:辛丑 38:壬寅 39:癸卯 40:甲辰 41:乙巳
42:丙午 43:丁未 44:戊申 45:己酉 46:庚戌 47:辛亥
48:壬子 49:癸丑 50:甲寅 51:乙卯 52:丙辰 53:丁巳
54:戊午 55:己未 56:庚申 57:辛酉 58:壬戌 59:癸亥
```

### 纳音 (Na Yin)

Each pair shares a nayin. The 30 nayin:
```
海中金(0-1) 炉中火(2-3) 大林木(4-5) 路旁土(6-7) 剑锋金(8-9)
山头火(10-11) 涧下水(12-13) 城头土(14-15) 白蜡金(16-17) 杨柳木(18-19)
泉中水(20-21) 屋上土(22-23) 霹雳火(24-25) 松柏木(26-27) 长流水(28-29)
沙中金(30-31) 山下火(32-33) 平地木(34-35) 壁上土(36-37) 金箔金(38-39)
覆灯火(40-41) 天河水(42-43) 大驿土(44-45) 钗钏金(46-47) 桑柘木(48-49)
大溪水(50-51) 沙中土(52-53) 天上火(54-55) 石榴木(56-57) 大海水(58-59)
```

### Five Tiger Chasing Month (五虎遁)

Year stem → first month (寅月) stem:
- 甲(0)己(5) → 丙(2)  |  乙(1)庚(6) → 戊(4)
- 丙(2)辛(7) → 庚(6)  |  丁(3)壬(8) → 壬(8)
- 戊(4)癸(9) → 甲(0)

### Five Rat Chasing Hour (五鼠遁)

Day stem → first hour (子时) stem:
- 甲(0)己(5) → 甲(0)  |  乙(1)庚(6) → 丙(2)
- 丙(2)辛(7) → 戊(4)  |  丁(3)壬(8) → 庚(6)
- 戊(4)癸(9) → 壬(8)

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

### Ten Gods by Element (Stem-level lookup)

For each day stem, the ten god categories for other stems:

| Day\|Other | 甲 | 乙 | 丙 | 丁 | 戊 | 己 | 庚 | 辛 | 壬 | 癸 |
|-----------|---|---|---|---|---|---|---|---|---|---|---|
| 甲(木阳) | 比 | 劫 | 食 | 伤 | 偏财 | 正财 | 七杀 | 正官 | 偏印 | 正印 |
| 乙(木阴) | 劫 | 比 | 伤 | 食 | 正财 | 偏财 | 正官 | 七杀 | 正印 | 偏印 |
| 丙(火阳) | 偏印 | 正印 | 比 | 劫 | 食 | 伤 | 偏财 | 正财 | 七杀 | 正官 |
| 丁(火阴) | 正印 | 偏印 | 劫 | 比 | 伤 | 食 | 正财 | 偏财 | 正官 | 七杀 |
| 戊(土阳) | 七杀 | 正官 | 偏印 | 正印 | 比 | 劫 | 食 | 伤 | 偏财 | 正财 |
| 己(土阴) | 正官 | 七杀 | 正印 | 偏印 | 劫 | 比 | 伤 | 食 | 正财 | 偏财 |
| 庚(金阳) | 偏财 | 正财 | 七杀 | 正官 | 偏印 | 正印 | 比 | 劫 | 食 | 伤 |
| 辛(金阴) | 正财 | 偏财 | 正官 | 七杀 | 正印 | 偏印 | 劫 | 比 | 伤 | 食 |
| 壬(水阳) | 食 | 伤 | 偏财 | 正财 | 七杀 | 正官 | 偏印 | 正印 | 比 | 劫 |
| 癸(水阴) | 伤 | 食 | 正财 | 偏财 | 正官 | 七杀 | 正印 | 偏印 | 劫 | 比 |

## Important Analysis Principles

1. **First judge day master strength** (得令/得地/得生/得助) — this determines everything
2. **Then identify the 格局** from month pillar
3. **Then find the 用神** — what the chart needs most
4. **Then check 大运 timing** — when things manifest
5. **神煞 last** — supplementary, never override 十神 analysis
6. **Always ground interpretations in classical texts**, citing the source
7. **Flag boundary cases**: if boundary_warning is not null, tell the user the month pillar may differ based on exact birth time relative to the solar term

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

- **Solar term boundary births** (±1 day): flag with boundary_warning, ask user to verify
- **Pre-1900 dates**: algorithm handles but warn about calendar differences
- **Missing birth hour**: default to 子时 (23:00-01:00) but note the limitation
- **Unknown gender**: assume male but note 大运 direction might be wrong
- **If chart seems off**: validate against known online排盘 tools
