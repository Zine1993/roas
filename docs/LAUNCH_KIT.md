# Game Growth Toolkit — Launch Kit

This file contains ready-to-use launch copy for the first public milestone. Adapt the opening sentence to each community instead of pasting the exact same post everywhere.

## One-line description

Open-source mobile growth modeling: turn early retention cohorts plus CPI/monetization assumptions into payback, ROAS, break-even CPI, and sensitivity scenarios.

## Short description

Game Growth Toolkit is a local Streamlit app for indie mobile developers, UA teams, and growth analysts. Import a few retention points, add CPI and monetization assumptions, and get transparent D7–D180 ROAS, payback, break-even CPI, and sensitivity outputs. The formulas live in a reusable Python core with tests and CI.

## Show HN

### Title

Show HN: Game Growth Toolkit – open-source payback and ROAS modeling for mobile apps/games

### Post

I built Game Growth Toolkit because I kept seeing early UA decisions made with either oversized analytics stacks or spreadsheets whose assumptions were hard to audit.

The idea is intentionally small: give it a few retention points (for example D1/D7/D30), CPI, payer-rate/ARPPU assumptions, organic lift, and platform cut. It fits a retention curve and shows:

- D7 / D14 / D30 / D60 / D90 / D180 ROAS
- estimated payback day
- D30 / D90 / D180 break-even paid CPI
- one-way sensitivity for CPI, payer rate, and ARPPU

Everything runs locally in Streamlit. The calculation layer is separated into Python functions with tests and CI, because I want the assumptions to be inspectable rather than hidden behind a dashboard.

It is not an attribution system and it is definitely not a claim that sparse cohorts can predict D180 perfectly. The current power-law model is deliberately simple, and the next work includes comparing alternative retention models and adding import templates for common MMP cohort exports.

I would especially value feedback from people doing mobile game/app UA: what assumption or import step would make this useful enough to replace one of your spreadsheets?

Repo: https://github.com/Zine1993/roas

## Reddit — r/gamedev / mobile development communities

### Title

I open-sourced the ROAS/payback model I use for early mobile game UA decisions

### Post

I turned one of my internal mobile growth spreadsheets/tools into an open-source Streamlit app: Game Growth Toolkit.

The problem it tries to solve is pretty specific: you have early cohort data but not months of mature revenue yet, and still need to decide whether a CPI is remotely sustainable.

You can enter/import retention points, set payer rate + ARPPU assumptions, CPI, organic lift, and platform cut, then it calculates payback, D7–D180 ROAS, D30/D90/D180 break-even CPI, and a simple sensitivity view for CPI/payer rate/ARPPU.

I deliberately kept the first model transparent rather than clever. It uses a power-law retention fit, shows R², and exposes the assumptions. It also has a reusable Python core, unit tests, and GitHub Actions CI.

Big caveat: this is scenario planning, not attribution and not a magic LTV predictor. Payer timing, repeat purchases, whales, ad revenue, campaign mix, etc. can move real LTV a lot.

I’m looking for practical feedback from people shipping mobile games/apps — especially which cohort export formats or decision outputs you’d want next.

GitHub: https://github.com/Zine1993/roas

## Indie Hackers

### Title

I turned my mobile UA forecasting workflow into an open-source growth toolkit

### Post

I’ve been turning a small internal ROAS/payback model into a public open-source project called Game Growth Toolkit.

It is aimed at indie app/game teams that have some early retention and monetization signals but don’t want to build a full analytics stack just to answer “can I afford this CPI?”

Current workflow:

1. import a few cohort retention points
2. enter CPI + monetization assumptions
3. get payback and D7–D180 ROAS
4. see D30/D90/D180 break-even CPI
5. stress-test CPI, payer rate, and ARPPU

The important part for me is that the assumptions stay visible. The model code is separated from the UI, tested, and runs locally.

I’m trying to get the first few real users now. If you do paid acquisition for a mobile app/game, I’d love to know which piece of your current spreadsheet or reporting workflow this would need to replace before you’d actually use it.

https://github.com/Zine1993/roas

## X / Twitter

Open-sourced a tool I use to reason about early mobile UA economics.

Drop in retention + CPI/monetization assumptions → get payback, D7–D180 ROAS, break-even CPI, and sensitivity analysis.

Local Streamlit app, transparent formulas, Python core + tests. No black-box “AI LTV” claims.

https://github.com/Zine1993/roas

## LinkedIn

I’ve open-sourced a small mobile growth modeling project I’ve been rebuilding from an internal prototype: **Game Growth Toolkit**.

It is designed for a very practical early-stage question: when you only have partial cohort data, what do your current assumptions imply about payback, ROAS, and the CPI you can afford?

The current version supports retention-curve fitting, D7–D180 ROAS, payback estimation, D30/D90/D180 break-even CPI, and sensitivity analysis for CPI, payer rate, and ARPPU.

I intentionally kept the model transparent and inspectable. It runs locally, the calculation layer is separated from the Streamlit UI, and the repo includes tests and CI. It is a scenario-planning tool, not an attribution system or a promise that sparse cohorts can perfectly predict long-term LTV.

I’m now looking for feedback from mobile app/game developers and UA teams. The most valuable input is concrete: which cohort export, assumption, or decision output would make this useful in your real workflow?

https://github.com/Zine1993/roas

## Chinese developer / growth community copy

### Title

把我自己做手游买量回收预估的工具开源了：早期留存也能快速算 Payback 和 Break-even CPI

### Post

我把自己原来用于手游/App 买量判断的一套小工具整理成开源项目了，叫 **Game Growth Toolkit**。

它解决的问题很具体：新品早期只有 D1/D7/D30 之类的留存和一些付费假设，但你已经要判断 CPI 能不能继续买、多久回本、D30/D90/D180 大概能到什么 ROAS。

目前可以：

- 导入留存 Cohort
- 拟合到 D180
- 算 Payback
- 算 D7/D14/D30/D60/D90/D180 ROAS
- 算 D30/D90/D180 Break-even CPI
- 看 CPI、付费率、ARPPU 的敏感性
- 导出结果 CSV

我刻意没有做成“AI 黑盒预测”。现在模型很简单，所有假设都能看到，核心计算拆成 Python 函数并有测试和 CI。

它也不是归因平台，真正的 LTV 会受到付费时点、复购、大 R、广告变现、国家/渠道质量等很多因素影响。

现在更想找真实做手游/App 买量的人来挑毛病：你现在表格里最希望被工具替掉的是哪一步？

GitHub: https://github.com/Zine1993/roas

## Comment replies

### “Why not just use Excel?”

Excel is completely fine for many teams. The project is useful when you want the assumptions and calculations versioned, tested, reusable, and easy to share without passing around another spreadsheet copy.

### “Is D180 from a few retention points reliable?”

Not by itself. The current model exposes R² for in-sample fit, but that does not prove extrapolation accuracy. The forecast should be treated as a scenario, and comparing alternative retention models is already an open roadmap item.

### “Does it connect to AppsFlyer / Adjust / Singular?”

Not directly yet. The current input is a normalized aggregated cohort CSV. Import templates/adapters for common MMP exports are an active roadmap item.

### “Is this AI-powered?”

No. The current project favors explicit deterministic modeling over a black-box AI forecast. AI may be useful later for workflow assistance, but the numerical assumptions should remain inspectable.

## Suggested launch order

1. GitHub release/tag `v0.1.0`
2. Show HN
3. one relevant gamedev/mobile developer subreddit (respect each community's self-promotion rules)
4. Indie Hackers
5. X / LinkedIn
6. Chinese developer/growth communities

Do not mass-post the exact same copy at the same time. Use the community-specific version and stay in the replies to collect concrete workflow feedback.