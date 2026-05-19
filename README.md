# Ba Zi (八字) Skill for Claude Code

一个 Claude Code skill，用于八字排盘和古典命理解读。用户输入出生日期/时间/性别，自动计算四柱八字、十神、大运、神煞，并结合古典命理书籍进行深度解读。

## 功能

- **自动排盘**: 计算年柱、月柱、日柱、时柱（含天干、地支、纳音、空亡）
- **十神分析**: 日主十神、地支藏干十神
- **大运推算**: 起运岁数、顺逆排、八步大运
- **流年排算**: 当前年份前后共3年流年干支及十神
- **命宫胎元**: 命宫、胎元自动计算
- **神煞查表**: 天乙贵人、文昌、桃花、驿马、华盖、禄神、羊刃、将星
- **五行统计**: 命局五行力量分布
- **古书解读**: 滴天髓、三命通会、渊海子平、穷通宝鉴、子平真诠、神峰通考、命理约言

## 安装

将 `bazi` 文件夹复制到 Claude Code 的 skills 目录：

- **全局**（所有项目可用）: `~/.claude/skills/bazi/`
- **项目级**（单个项目）: `<project>/.claude/skills/bazi/`

## 使用

在 Claude Code 中输入：

```
/bazi
```

或直接描述出生日期：

> 我 1990 年 6 月 15 日下午 2:30 出生，男，帮我看看八字

## 文件结构

```
bazi/
├── SKILL.md                  # 主指令文件
├── scripts/
│   └── bazi_calculator.py    # Python 排盘引擎
├── references/               # 结构化知识库
│   ├── 00-overview.md        # 总目录
│   ├── 01-yinyang-wuxing.md  # 阴阳五行
│   ├── 02-tiangan-dizhi.md   # 天干地支
│   ├── 03-shishen.md         # 十神详解
│   ├── 04-geju.md            # 格局大全
│   ├── 05-yongshen.md        # 用神体系
│   ├── 06-dayun-liunian.md   # 大运流年
│   ├── 07-shensha.md         # 神煞大全
│   ├── 08-hunyin.md          # 婚姻专题
│   ├── 09-shiye-caifu.md     # 事业财运
│   ├── 10-jiankang.md        # 健康专题
│   └── classical-texts/      # 古书节选
│       ├── index.md
│       ├── ditiansui.md      # 滴天髓
│       ├── zipingzhenquan.md # 子平真诠
│       ├── qiongtongbaojian.md # 穷通宝鉴
│       ├── sanmingtonghui.md  # 三命通会
│       ├── yuanhaiziping.md   # 渊海子平
│       ├── shenfengtongkao.md # 神峰通考
│       └── mingliyueyan.md    # 命理约言
└── README.md
```

## 技术细节

排盘引擎 `bazi_calculator.py` 纯 Python 3 标准库，无外部依赖。JSON stdin/stdout 接口。

节气计算使用标准天文公式（精度 ±1 天），日柱以 1900-01-01（甲戌日）为基准计算。

```bash
echo '{"year":1990,"month":6,"day":15,"hour":14,"minute":30,"gender":"male"}' | python scripts/bazi_calculator.py
```

脚本强制 UTF-8 输出，Windows 中文环境下无乱码问题。如需手动设置编码：`PYTHONIOENCODING=utf-8`。
