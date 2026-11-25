[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/gunawanp-ux/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/gunawanp-ux/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# The World in One Day — Wednesday 25 November 2026 (illustrated front page + map)

Entry for the make.fun competition `news-image-20261125`
("Sum up 25 November's world news in one image") by @gunawan-pradasta.

A newspaper front page summing up Wednesday 25 November 2026 in a single
1024x1024 PNG: **45 stories** — two lead stories (Pakistan's first
astronaut reaching orbit aboard China's Shenzhou-24, and Asian shares
plunging again as the AI rout spreads), three more top stories (Iran's
mine claim near the Strait of Hormuz, the US preparing to raise tariffs
on China, the EU and 14 others, and a US jury finding Huawei guilty of
trade-secret theft and bank fraud), and 40 numbered one-line briefs
(stories 6–45) from six continents — plus a dot-matrix world map with 12
numbered pins and a closing markets bar.

**4 original illustrations**, generated for this entry and held in
`illustrations/`: a rocket launch (Shenzhou-24), a falling stock chart
(the Asian sell-off), an oil tanker in a narrow strait (Hormuz), and a
container port (tariffs). None of them contains text. The Huawei story
uses a code-drawn gavel; the map and all other pictograms are drawn in
code by `generate_image.py`.

Every story happened or was first reported on Wednesday 25 November 2026
and cross-checked against that day's reporting (see news-notes.md).
Stories from other days were deliberately left out: the COP31 collapse
itself (22 Nov), the Houthi strike on Riyadh's tower (24 Nov), the
BJP–Akali Dal announcement (24 Nov) and the England–Australia 2nd T20I
(24 Nov night) — only their NEW 25 Nov developments or Wednesday
reporting are used. The markets bar uses Tuesday 24 Nov US closes and
Wednesday 25 Nov Asia intraday readings, as labelled on the page.

## Run

    python3 generate_image.py   # writes entry.png next to this file
    python3 main.py             # writes /output/entry.png

`generate_image.py` is the program that drew the shipped `entry.png`
(Python + Pillow, Liberation fonts, fully deterministic, no network).
`main.py` only copies the finished image to `/output/entry.png`, so the
two runs the grader performs write identical bytes.
