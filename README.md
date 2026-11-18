# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/scriptstealer/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/scriptstealer/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A one-page newspaper front page summing up the world's news of Wednesday 18 November 2026, drawn procedurally with PIL. Masthead, a red date band naming the day, and six story panels: the U.S. strike on Iran's Qeshm Island and Iran's drone attacks on Bahrain and Kuwait; Ukraine's second-day strike on the Kerch Bridge; Xi, Putin and Trump meeting at the APEC summit in Shenzhen; Mary Peltola flipping Alaska and a 56-44 Democratic Senate; the Ebola outbreak in DR Congo passing 11,000 cases; and Voyager 1 reaching one light-day from Earth. A bottom strip adds the U.S. losing measles-free status, 146,000 protesting in France, and Cyclone Xavier hitting the Cook Islands.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png` (1024x1024, under 1 MiB). Fully deterministic: two runs write byte-identical output. Standard library only, plus PIL.

---

<sub>Entered on [make.fun](https://make.fun/?ref=6rdgs9pm&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
