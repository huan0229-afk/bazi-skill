#!/usr/bin/env python3
"""Golden chart test cases for bazi_calculator.py.
Run: python test_bazi_calculator.py
"""

import json
import sys
import os

# Ensure the script directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bazi_calculator import (
    STEMS, BRANCHES, ELEMENTS, STEM_YY,
    NAYIN, NAYIN_IDX_MAP, FIVE_TIGER, FIVE_RAT,
    get_year_pillar, get_year_pillar_for_date,
    get_day_pillar, get_month_pillar, get_hour_pillar,
    get_nayin, get_ten_god, get_xunkong,
    get_hidden_stems_info, get_minggong, get_taiyuan,
    get_dayun, get_shensha, get_wuxing_counts,
    format_chart_output,
)

PASS = 0
FAIL = 0


def check(name: str, actual, expected):
    global PASS, FAIL
    if actual == expected:
        PASS += 1
    else:
        FAIL += 1
        print(f"  FAIL {name}: got {actual!r}, expected {expected!r}")


def check_approx(name: str, actual, expected, tolerance=1):
    global PASS, FAIL
    if abs(actual - expected) <= tolerance:
        PASS += 1
    else:
        FAIL += 1
        print(f"  FAIL {name}: got {actual!r}, expected ~{expected!r}")


# ============================================================
# Day Pillar — the foundation of the entire chart
# ============================================================

def test_day_pillar():
    print("Day Pillar")
    # 1900-01-01 = 甲戌日 (甲=0, 戌=10), sixty-cycle index 10
    s, b = get_day_pillar(1900, 1, 1)
    check("1900-01-01 stem", s, 0)
    check("1900-01-01 branch", b, 10)
    check("1900-01-01 cycle", NAYIN_IDX_MAP[(s, b)], 10)

    # 1900-01-02 = 乙亥日 (乙=1, 亥=11)
    s, b = get_day_pillar(1900, 1, 2)
    check("1900-01-02 stem", s, 1)
    check("1900-01-02 branch", b, 11)

    # 1900-01-31 = 1900-01-01 + 30 days = 甲戌(10) + 30 = 40 → 甲辰 (甲=0, 辰=4)
    s, b = get_day_pillar(1900, 1, 31)
    check("1900-01-31 stem", s, 0)
    check("1900-01-31 branch", b, 4)

    # 2000-01-01: 60-year cycle repeats every 60 days
    # 1900-01-01 to 2000-01-01 = 36524 days (including 25 leap days)
    # 36524 % 60 = 44, so 10 + 44 = 54 → stem 4=戊, branch 6=午
    s, b = get_day_pillar(2000, 1, 1)
    check("2000-01-01 stem", s, 4)
    check("2000-01-01 branch", b, 6)

    # Same day next year should advance 5 or 6 (depending on leap year)
    # 1999-01-01: 1999-1900=99 years, but we need exact days
    # 1999 is not leap. From 1900 to 1999 = 99 years = 24 leap days
    # Days = 99*365 + 24 = 36135 + 24 = 36159
    s1, b1 = get_day_pillar(1999, 1, 1)
    s2, b2 = get_day_pillar(2000, 1, 1)
    # 1999-01-01 to 2000-01-01 = 365 days (2000 is leap but 1999 is not)
    # 365 % 60 = 5, so stem shifts +5, branch shifts +5
    check("year boundary stem", s2, (s1 + 5) % 10)
    check("year boundary branch", b2, (b1 + 5) % 12)


# ============================================================
# Year Pillar
# ============================================================

def test_year_pillar():
    print("Year Pillar")
    # 1984 = 甲子年
    s, b = get_year_pillar(1984)
    check("1984 stem (甲)", s, 0)
    check("1984 branch (子)", b, 0)

    # 2024 = 甲辰年
    s, b = get_year_pillar(2024)
    check("2024 stem (甲)", s, 0)
    check("2024 branch (辰)", b, 4)

    # 2025 = 乙巳年
    s, b = get_year_pillar(2025)
    check("2025 stem (乙)", s, 1)
    check("2025 branch (巳)", b, 5)

    # Pre-立春: 2024-01-15 → 2023 = 癸卯年
    s, b = get_year_pillar_for_date(2024, 1, 15)
    check("2024-01-15 stem (癸)", s, 9)
    check("2024-01-15 branch (卯)", b, 3)

    # Post-立春: 2024-02-10 → 2024 = 甲辰年
    s, b = get_year_pillar_for_date(2024, 2, 10)
    check("2024-02-10 stem (甲)", s, 0)
    check("2024-02-10 branch (辰)", b, 4)


# ============================================================
# Month Pillar (五虎遁)
# ============================================================

def test_month_pillar():
    print("Month Pillar")
    # 甲年 → 寅月 = 丙寅
    s, b, _, _ = get_month_pillar(2024, 2, 10, 0)
    check("甲年寅月 stem (丙)", s, 2)
    check("甲年寅月 branch (寅)", b, 2)

    # 乙年 → 寅月 = 戊寅
    s, b, _, _ = get_month_pillar(2025, 2, 10, 1)
    check("乙年寅月 stem (戊)", s, 4)
    check("乙年寅月 branch (寅)", b, 2)

    # The month pillar for 1995-05-05 14:00 should match bazi_output.json
    # 立夏 1995 ≈ May 5 12:42, so 14:00 is after → 巳月
    y_s, y_b = get_year_pillar_for_date(1995, 5, 5, 14, 0)
    m_s, m_b, prev, next_ = get_month_pillar(1995, 5, 5, y_s, 14, 0)
    check("1995-05-05 month stem (辛)", m_s, 7)
    check("1995-05-05 month branch (巳)", m_b, 5)
    check("1995-05-05 prev jie (立夏)", prev[0], "立夏")
    check("1995-05-05 next jie (芒种)", next_[0], "芒种")


# ============================================================
# Hour Pillar (五鼠遁)
# ============================================================

def test_hour_pillar():
    print("Hour Pillar")
    # 甲日 → 子时 = 甲子
    s, b = get_hour_pillar(0, 0, 0)
    check("甲日子时 stem (甲)", s, 0)
    check("甲日子时 branch (子)", b, 0)

    # 甲日 → 午时 = 庚午
    s, b = get_hour_pillar(0, 12, 0)
    check("甲日午时 stem (庚)", s, 6)
    check("甲日午时 branch (午)", b, 6)

    # 乙日 → 子时 = 丙子
    s, b = get_hour_pillar(1, 0, 0)
    check("乙日子时 stem (丙)", s, 2)
    check("乙日子时 branch (子)", b, 0)

    # 时辰 boundaries
    # 23:30 → 子时 (branch 0)
    s, b = get_hour_pillar(0, 23, 30)
    check("23:30 branch (子)", b, 0)

    # 00:30 → 子时 (branch 0)
    s, b = get_hour_pillar(0, 0, 30)
    check("00:30 branch (子)", b, 0)

    # 01:30 → 丑时 (branch 1)
    s, b = get_hour_pillar(0, 1, 30)
    check("01:30 branch (丑)", b, 1)

    # 11:30 → 午时 (branch 6)
    s, b = get_hour_pillar(0, 11, 30)
    check("11:30 branch (午)", b, 6)

    # 1995-05-05 14:00 → 未时 (stem depends on day stem)
    d_s, d_b = get_day_pillar(1995, 5, 5)
    h_s, h_b = get_hour_pillar(d_s, 14, 0)
    check("1995-05-05 14:00 hour stem (乙)", h_s, 1)
    check("1995-05-05 14:00 hour branch (未)", h_b, 7)


# ============================================================
# Na Yin
# ============================================================

def test_nayin():
    print("Na Yin")
    # 甲子/乙丑 = 海中金 (indices 0,1)
    check("甲子 nayin", get_nayin(0, 0), "海中金")
    check("乙丑 nayin", get_nayin(1, 1), "海中金")
    # 丙寅/丁卯 = 炉中火 (indices 2,3)
    check("丙寅 nayin", get_nayin(2, 2), "炉中火")
    check("丁卯 nayin", get_nayin(3, 3), "炉中火")
    # 戊辰/己巳 = 大林木 (indices 4,5)
    check("戊辰 nayin", get_nayin(4, 4), "大林木")
    # 壬戌/癸亥 = 大海水 (indices 58,59)
    check("壬戌 nayin", get_nayin(8, 10), "大海水")
    check("癸亥 nayin", get_nayin(9, 11), "大海水")


# ============================================================
# Ten Gods (十神)
# ============================================================

def test_ten_god():
    print("Ten Gods")
    # Day stem = 甲(0, 木阳)
    # 甲 = 比肩
    check("甲见甲 → 比肩", get_ten_god(0, 0), "比肩")
    # 乙 = 劫财 (same element 木, opposite yin/yang)
    check("甲见乙 → 劫财", get_ten_god(0, 1), "劫财")
    # 丙 = 食神 (甲生丙, same yin/yang)
    check("甲见丙 → 食神", get_ten_god(0, 2), "食神")
    # 丁 = 伤官 (甲生丁, opposite yin/yang)
    check("甲见丁 → 伤官", get_ten_god(0, 3), "伤官")
    # 戊 = 偏财 (甲克戊, same yin/yang)
    check("甲见戊 → 偏财", get_ten_god(0, 4), "偏财")
    # 己 = 正财 (甲克己, opposite yin/yang)
    check("甲见己 → 正财", get_ten_god(0, 5), "正财")
    # 庚 = 七杀 (庚克甲, same yin/yang)
    check("甲见庚 → 七杀", get_ten_god(0, 6), "七杀")
    # 辛 = 正官 (辛克甲, opposite yin/yang)
    check("甲见辛 → 正官", get_ten_god(0, 7), "正官")
    # 壬 = 偏印 (壬生甲, same yin/yang)
    check("甲见壬 → 偏印", get_ten_god(0, 8), "偏印")
    # 癸 = 正印 (癸生甲, opposite yin/yang)
    check("甲见癸 → 正印", get_ten_god(0, 9), "正印")


# ============================================================
# Hidden Stems (地支藏干)
# ============================================================

def test_hidden_stems():
    print("Hidden Stems")
    # 子: 癸(本气)
    hs = get_hidden_stems_info(0)
    check("子 hidden count", len(hs), 1)
    check("子 本气 stem", hs[0][0], 9)
    check("子 本气 strength", hs[0][1], "本气")

    # 丑: 己(本气) 癸(中气) 辛(余气)
    hs = get_hidden_stems_info(1)
    check("丑 hidden count", len(hs), 3)
    check("丑 本气", hs[0][0], 5)
    check("丑 中气", hs[1][0], 9)
    check("丑 余气", hs[2][0], 7)

    # 寅: 甲(本气) 丙(中气) 戊(余气)
    hs = get_hidden_stems_info(2)
    check("寅 本气", hs[0][0], 0)
    check("寅 中气", hs[1][0], 2)
    check("寅 余气", hs[2][0], 4)

    # 午: 丁(本气) 己(中气)
    hs = get_hidden_stems_info(6)
    check("午 hidden count", len(hs), 2)
    check("午 本气", hs[0][0], 3)
    check("午 中气", hs[1][0], 5)

    # 亥: 壬(本气) 甲(中气)
    hs = get_hidden_stems_info(11)
    check("亥 hidden count", len(hs), 2)
    check("亥 本气", hs[0][0], 8)
    check("亥 中气", hs[1][0], 0)


# ============================================================
# 空亡
# ============================================================

def test_xunkong():
    print("Xun Kong")
    # 甲子旬 (0-9): missing 戌(10)亥(11)
    name, voids, idxs = get_xunkong(0)
    check("甲子旬 name", name, "甲子旬")
    check("甲子旬 voids", voids, ["戌", "亥"])

    # 甲寅旬 (50-59): missing 子(0)丑(1)
    name, voids, idxs = get_xunkong(50)
    check("甲寅旬 name", name, "甲寅旬")
    check("甲寅旬 voids", voids, ["子", "丑"])


# ============================================================
# 命宫 and 胎元
# ============================================================

def test_minggong_taiyuan():
    print("Ming Gong / Tai Yuan")
    # 命宫: year_stem=0(甲), month_branch=2(寅), hour_branch=0(子)
    # mg_branch = (2 - 0 - 1) % 12 = 1(丑)
    # mg_stem = first_month(甲年丙寅→丙=2) + (1 - 2) % 10 = 2 - 1 = 1(乙)
    mg_s, mg_b = get_minggong(0, 2, 0)
    check("命宫 stem (乙)", mg_s, 1)
    check("命宫 branch (丑)", mg_b, 1)

    # 胎元: month_stem=2(丙), month_branch=2(寅)
    # ty_stem = (2+1)%10 = 3(丁), ty_branch = (2+3)%12 = 5(巳)
    ty_s, ty_b = get_taiyuan(2, 2)
    check("胎元 stem (丁)", ty_s, 3)
    check("胎元 branch (巳)", ty_b, 5)


# ============================================================
# Wuxing Counts
# ============================================================

def test_wuxing_counts():
    print("Wuxing Counts")
    # For 甲子年甲子月甲子日甲子时:
    # Day stem 甲=木, Year stem 甲=木, Month stem 甲=木, Hour stem 甲=木
    # Year branch 子=水, Month branch 子=水, Day branch 子=水, Hour branch 子=水
    # Total: 木=4, 水=4
    pillars = [("year", 0, 0), ("month", 0, 0), ("day", 0, 0), ("hour", 0, 0)]
    counts = get_wuxing_counts(0, pillars)
    check("甲子×4 木", counts["木"], 5)  # day stem + 4 pillars stems = 5
    check("甲子×4 水", counts["水"], 4)  # 4 branches
    check("甲子×4 火", counts["火"], 0)
    check("甲子×4 土", counts["土"], 0)
    check("甲子×4 金", counts["金"], 0)


# ============================================================
# Full Chart Golden References
# ============================================================

def test_golden_chart_1995():
    """Golden chart: 1995-05-05 14:00 female — verified against bazi_output.json."""
    print("Golden Chart: 1995-05-05 14:00 female")
    result = format_chart_output(1995, 5, 5, 14, 0, "female")

    # Birth
    check("birth year", result["birth"]["year"], 1995)
    check("shichen", result["birth"]["shichen"], "未时")

    # Day master
    check("day master stem", result["day_master"]["stem"], "丙")
    check("day master element", result["day_master"]["element"], "火")
    check("day master yin_yang", result["day_master"]["yin_yang"], "阳")

    # Year pillar
    check("year stem", result["pillars"]["year"]["stem"], "乙")
    check("year branch", result["pillars"]["year"]["branch"], "亥")
    check("year nayin", result["pillars"]["year"]["nayin"], "山头火")

    # Month pillar
    check("month stem", result["pillars"]["month"]["stem"], "辛")
    check("month branch", result["pillars"]["month"]["branch"], "巳")
    check("month nayin", result["pillars"]["month"]["nayin"], "白蜡金")

    # Day pillar
    check("day stem", result["pillars"]["day"]["stem"], "丙")
    check("day branch", result["pillars"]["day"]["branch"], "申")

    # Hour pillar
    check("hour stem", result["pillars"]["hour"]["stem"], "乙")
    check("hour branch", result["pillars"]["hour"]["branch"], "未")

    # Ten gods
    check("year stem_tg", result["ten_gods"]["year"]["stem_tg"], "正印")
    check("month stem_tg", result["ten_gods"]["month"]["stem_tg"], "正财")
    check("hour stem_tg", result["ten_gods"]["hour"]["stem_tg"], "正印")

    # Hidden stems
    year_hs = result["hidden_stems"]["year"]
    check("year hidden count", len(year_hs), 2)
    check("year hidden 本气", year_hs[0]["stem"], "壬")
    check("year hidden 本气 tg", year_hs[0]["ten_god"], "七杀")

    month_hs = result["hidden_stems"]["month"]
    check("month hidden count", len(month_hs), 3)
    check("month hidden 本气", month_hs[0]["stem"], "丙")

    # Wuxing counts
    check("木 count", result["wuxing_counts"]["木"], 2)
    check("火 count", result["wuxing_counts"]["火"], 3)
    check("土 count", result["wuxing_counts"]["土"], 1)
    check("金 count", result["wuxing_counts"]["金"], 2)
    check("水 count", result["wuxing_counts"]["水"], 1)

    # Dayun
    check("dayun count", len(result["dayun"]), 8)
    check("start age", result["start_age"], 10)
    check("dayun 1 stem", result["dayun"][0]["stem"], "壬")
    check("dayun 1 direction", result["dayun"][0]["direction"], "顺排")

    # Shensha
    check("month 驿马", "驿马" in result["shensha"]["month"], True)
    check("day 天乙贵人", "天乙贵人" in result["shensha"]["day"], True)

    # Solar terms
    check("prev_jie", result["solar_terms"]["prev_jie"], "立夏")
    check("next_jie", result["solar_terms"]["next_jie"], "芒种")

    # Minggong / Taiyuan
    check("minggong stem", result["minggong"]["stem"], "乙")
    check("minggong branch", result["minggong"]["branch"], "酉")
    check("taiyuan stem", result["taiyuan"]["stem"], "壬")


def test_golden_chart_1997():
    """Golden chart: 1997-06-19 12:00 male."""
    print("Golden Chart: 1997-06-19 12:00 male")
    result = format_chart_output(1997, 6, 19, 12, 0, "male")

    check("day master stem", result["day_master"]["stem"], "壬")
    check("day master element", result["day_master"]["element"], "水")

    check("year stem", result["pillars"]["year"]["stem"], "丁")
    check("year branch", result["pillars"]["year"]["branch"], "丑")
    check("month stem", result["pillars"]["month"]["stem"], "丙")
    check("month branch", result["pillars"]["month"]["branch"], "午")
    check("day stem", result["pillars"]["day"]["stem"], "壬")
    check("day branch", result["pillars"]["day"]["branch"], "辰")
    check("hour stem", result["pillars"]["hour"]["stem"], "丙")
    check("hour branch", result["pillars"]["hour"]["branch"], "午")

    # Dayun: 丁丑年 male (阴年男 → 逆排)
    check("dayun direction", result["dayun"][0]["direction"], "逆排")
    check("start age", result["start_age"], 5)

    # Wuxing
    check("火 count", result["wuxing_counts"]["火"], 5)
    check("水 count", result["wuxing_counts"]["水"], 2)
    check("木 count", result["wuxing_counts"]["木"], 0)


def test_golden_chart_1984():
    """Golden chart: 1984-02-04 18:00 (立春当天) male.
    1984 is the start of 甲子 cycle."""
    print("Golden Chart: 1984-02-04 18:00 male")
    result = format_chart_output(1984, 2, 4, 18, 0, "male")

    check("year stem", result["pillars"]["year"]["stem"], "甲")
    check("year branch", result["pillars"]["year"]["branch"], "子")
    check("day master stem", result["day_master"]["stem"], "戊")

    # 立春 day — should have boundary warning
    check("boundary warning not null", result["boundary_warning"] is not None, True)


def test_golden_chart_pre_lichun():
    """Birth before 立春: year pillar should use previous year."""
    print("Golden Chart: Pre-立春")
    # 2024-01-15 is before 立春 (Feb 4), so year = 2023 (癸卯)
    result = format_chart_output(2024, 1, 15, 8, 0, "male")

    check("year stem (癸)", result["pillars"]["year"]["stem"], "癸")
    check("year branch (卯)", result["pillars"]["year"]["branch"], "卯")


def test_precise_lichun_boundary():
    """Precise 立春 boundary: year pillar changes at exact solar term time.
    2024 立春 ≈ Feb 4 13:02, so 08:00 uses old year, 16:00 uses new year."""
    print("Precise 立春 boundary")

    # Before 立春 (08:00 < 13:02) → 癸卯年
    r = format_chart_output(2024, 2, 4, 8, 0, "male")
    check("2024-02-04 08:00 year stem (癸)", r["pillars"]["year"]["stem"], "癸")
    check("2024-02-04 08:00 year branch (卯)", r["pillars"]["year"]["branch"], "卯")

    # After 立春 (16:00 > 13:02) → 甲辰年
    r = format_chart_output(2024, 2, 4, 16, 0, "male")
    check("2024-02-04 16:00 year stem (甲)", r["pillars"]["year"]["stem"], "甲")
    check("2024-02-04 16:00 year branch (辰)", r["pillars"]["year"]["branch"], "辰")
    check("2024-02-04 16:00 month stem (丙)", r["pillars"]["month"]["stem"], "丙")
    check("2024-02-04 16:00 month branch (寅)", r["pillars"]["month"]["branch"], "寅")

    # Boundary warning should mention 立春 time
    check("boundary_warning mentions 立春", "立春" in (r["boundary_warning"] or ""), True)
    check("solar term time in output", r["solar_terms"]["next_jie_time"] != "", True)


def test_solar_term_times_in_output():
    """Solar term output now includes precise times."""
    print("Solar term times in output")
    r = format_chart_output(2000, 6, 15, 12, 0, "male")

    check("prev_jie_time present", "prev_jie_time" in r["solar_terms"], True)
    check("next_jie_time present", "next_jie_time" in r["solar_terms"], True)
    check("prev_jie_time format HH:MM",
          len(r["solar_terms"]["prev_jie_time"]) == 5, True)
    check("next_jie_time format HH:MM",
          len(r["solar_terms"]["next_jie_time"]) == 5, True)


# ============================================================
# Consistency checks
# ============================================================

def test_five_tiger_consistency():
    """五虎遁: 甲己之年丙作首, 乙庚之年戊为头, 丙辛之年庚起, 丁壬之年壬起, 戊癸之年甲起"""
    print("Five Tiger consistency")
    expected = {0: 2, 5: 2,  1: 4, 6: 4,  2: 6, 7: 6,  3: 8, 8: 8,  4: 0, 9: 0}
    check("五虎遁 table", FIVE_TIGER, expected)


def test_five_rat_consistency():
    """五鼠遁: 甲己之日甲起, 乙庚之日丙起, 丙辛之日戊起, 丁壬之日庚起, 戊癸之日壬起"""
    print("Five Rat consistency")
    expected = {0: 0, 5: 0,  1: 2, 6: 2,  2: 4, 7: 4,  3: 6, 8: 6,  4: 8, 9: 8}
    check("五鼠遁 table", FIVE_RAT, expected)


def test_sixty_cycle_nayin_consistency():
    """Every valid stem-branch pair must have a nayin and a cycle index.
    Only pairs with matching parity exist in the 60-cycle (e.g., 甲子 yes, 甲丑 no)."""
    print("60-cycle consistency")
    for stem_idx in range(10):
        for branch_idx in range(12):
            # Only same-parity pairs exist in the 60-cycle
            valid = (stem_idx % 2 == branch_idx % 2)
            pair = (stem_idx, branch_idx)
            idx = NAYIN_IDX_MAP.get(pair)
            name = f"{STEMS[stem_idx]}{BRANCHES[branch_idx]}"
            if valid:
                if idx is None:
                    print(f"  FAIL: missing cycle idx for valid pair {name}")
                    global FAIL; FAIL += 1
                    continue
                nayin = NAYIN[idx] if 0 <= idx < 60 else None
                if nayin is None:
                    print(f"  FAIL: missing nayin for cycle idx {idx}")
                    FAIL += 1
            else:
                if idx is not None:
                    print(f"  FAIL: invalid pair {name} should not be in 60-cycle")
                    FAIL += 1


def test_all_stems_branches():
    """Verify all ten stems and twelve branches have element and yin_yang."""
    print("Stems/Branches completeness")
    check("10 stems", len(STEMS), 10)
    check("12 branches", len(BRANCHES), 12)
    check("10 elements", len(ELEMENTS), 10)
    check("10 yin_yang", len(STEM_YY), 10)
    check("60 nayin", len(NAYIN), 60)


# ============================================================
# Runner
# ============================================================

if __name__ == "__main__":
    test_day_pillar()
    test_year_pillar()
    test_month_pillar()
    test_hour_pillar()
    test_nayin()
    test_ten_god()
    test_hidden_stems()
    test_xunkong()
    test_minggong_taiyuan()
    test_wuxing_counts()
    test_golden_chart_1995()
    test_golden_chart_1997()
    test_golden_chart_1984()
    test_golden_chart_pre_lichun()
    test_precise_lichun_boundary()
    test_solar_term_times_in_output()
    test_five_tiger_consistency()
    test_five_rat_consistency()
    test_sixty_cycle_nayin_consistency()
    test_all_stems_branches()

    total = PASS + FAIL
    print(f"\n{'='*50}")
    print(f"Results: {PASS}/{total} passed, {FAIL} failed")
    if FAIL > 0:
        print("SOME TESTS FAILED")
        sys.exit(1)
    else:
        print("All tests passed!")
        sys.exit(0)
