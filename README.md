**English** | [简体中文](README.zh.md)

<p align="center">
  <img src="assets/banner-en.png" alt="AngusTester — One Test Language. Test Everything." width="100%" />
</p>

<p align="center">
  <a href="https://www.anguskit.com/en/pricing"><img alt="Community Edition" src="https://img.shields.io/badge/Community-Free-b3873f"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/License-GPL--3.0-blue"></a>
  <a href="https://www.anguskit.com/en/docs/tester"><img alt="Docs" src="https://img.shields.io/badge/docs-anguskit.com-b3873f"></a>
  <a href="https://www.anguskit.com"><img alt="Website" src="https://img.shields.io/badge/website-anguskit.com-c96128"></a>
</p>

# AngusTester

**One Test Language. Test Everything.**

AI-Native Software Testing — the Test product in [AngusKit](https://github.com/AngusKit/AngusKit).

> **This repository hosts documentation only.** AngusTester source code is distributed through private deployment packages, not through this GitHub repository. Earlier revisions of this repository contained application source; as of this update, distribution has moved to AngusKit's packaging pipeline (see [Get the Community Edition](#get-the-community-edition-free) below). This repository now focuses on product information, quickstart guides, and links to the full documentation site.

## What is AngusTester

AngusTester replaces tool sprawl and code-script barriers with one declarative test language — **AngusScript YAML** — that runs API, Web, mobile, messaging, data, and LLM tests through a single engine. Test assets (plans, cases, scripts, reports) live on one collaborative surface, and automated runs feed results straight into release decisions.

## Key capabilities

- **One engine, many scenarios** — API, Web, mobile, messaging, data, and LLM tests on a single execution model
- **YAML instead of code** — declare requests, assertions, and extractors in AngusScript; no Java/JS/Python scripting required
- **Plan · case · script · report** — one path from scoping to writing cases to attaching scripts to shipping reports
- **Test plugin extensions** — protocol / Web / mobile / LLM plugins plug into the same engine
- **One-click automation** — run smoke and regression suites across environments, reproducible and CI-ready
- **Performance testing** — multi-thread concurrency and ramp-up load with SLA threshold checks and live metrics

## Screenshot

<p align="center">
  <img src="assets/screenshot-en.png" alt="AngusTester console" width="100%" />
</p>

## Get the Community Edition (free)

About **290 MB**. This zip is **AngusGM + AngusTester**. At least **2 cores / 4 GB** RAM and **40 GB** disk (execution logs/plugins extra). Docker Engine + Compose v2.

This first-run path matches the official docs: Docker Compose, the install wizard, **access mode 2** (bundled Caddy), HTTP `:80` (no certificate).

1. Resolve names to this machine (or add to `/etc/hosts` for a local trial). Public DNS name in the wizard is the **suffix** (e.g. `example.com`), not `gm.example.com`.

```bash
127.0.0.1 gm.example.com tester.example.com
```

Open host **80**. Open **7100** only when you execute scripts. Do not use `localhost:8801`. Stop Nginx/Caddy/IIS if they already bind 80. On macOS + Docker Desktop, do not run `./install.sh` with `sudo`.

2. Download, unzip, and run the wizard from the package root:

```bash
curl --fail --location --progress-bar -o AngusTester-Community-2.0.0.zip \
  https://repo.anguskit.com/raw/raw-public/AngusKit/tester/AngusTester-Community-2.0.0.zip
unzip AngusTester-Community-2.0.0.zip
cd AngusTester-2.0.0
./install.sh
```

Answer: Install mode `1` (Compose) → Access **`2`** (bundled reverse proxy — do not press Enter) → Proxy `1` (Caddy) → TLS **`4`** (HTTP `:80`, no certificate) → Database `1` (MySQL 8 in Compose) → Public DNS name = `example.com` → set admin password (default user `admin`). Wait for `Install finished.`

3. Confirm health, then open the console:

```bash
./bin/angusctl.sh doctor
```

Look for `doctor: OK`. Open `http://gm.example.com/`, sign in, then open `http://tester.example.com/`.

Need the full suite? Use `AngusKit-Community-1.0.0.zip` from [AngusKit](https://github.com/AngusKit/AngusKit).

First-run guide: **[tester quickstart](https://www.anguskit.com/en/docs/tester/get-started/quickstart)** · Full install (host ZIP, Helm preview, TLS, offline): **[install docs](https://www.anguskit.com/en/docs/tester/latest/en/manual/02-install-deploy)**

## Community vs. Team / Enterprise vs. SaaS

| | Community | Team / Enterprise | SaaS |
|---|---|---|---|
| Price | Free | Paid, private deployment | Paid, hosted |
| Users | Up to 10 | Higher / unlimited seats | Per plan |
| Test projects | Up to 20 | Higher / unlimited | Per plan |
| Test concurrency | Up to 1,000 | Higher / unlimited | Per plan |
| Web / mobile / messaging / LLM plugins, report gating, Testing Copilot, MCP | Not included (API + basic performance only) | Included | Per plan |

Community Edition source is licensed under GPL-3.0 and distributed with each Community installation package. Team and Enterprise editions are proprietary, governed by the **[XCan Business License, Version 1.0](https://www.anguskit.com/licenses/XCBL-1.0)** (XCBL-1.0), distributed only under a paid subscription.

Full pricing and feature comparison: **[anguskit.com/pricing](https://www.anguskit.com/en/pricing)**

## Related AngusKit products

| Product | Focus | Repository |
|---|---|---|
| AngusKit | The full suite (this product + 5 others + AngusGM) | [AngusKit/AngusKit](https://github.com/AngusKit/AngusKit) |
| AngusAI | AI agent development | [AngusKit/AngusAI](https://github.com/AngusKit/AngusAI) |
| AngusGit | AI-native code collaboration | [AngusKit/AngusGit](https://github.com/AngusKit/AngusGit) |
| AngusRepo | Universal artifact management | [AngusKit/AngusRepo](https://github.com/AngusKit/AngusRepo) |
| AngusSecurity | Application security & governance | [AngusKit/AngusSecurity](https://github.com/AngusKit/AngusSecurity) |
| AngusInsight | Private product analytics | [AngusKit/AngusInsight](https://github.com/AngusKit/AngusInsight) |

## Documentation & support

- Full docs: [anguskit.com/docs/tester](https://www.anguskit.com/en/docs/tester)
- Contact / sales: [anguskit.com/contact](https://www.anguskit.com/en/contact) · `sales@anguskit.com`
- This repository's Issues are for **documentation feedback and install troubleshooting**. This repository does not accept source code pull requests — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

- This repository's documentation content: see [LICENSE](LICENSE) (GPL-3.0, matching the Community Edition source it describes).
- AngusTester Community Edition product source: GPL-3.0, distributed with each Community installation package.
- AngusTester Team / Enterprise Edition: proprietary, [XCan Business License, Version 1.0](LICENSE-XCBL-1.0) (XCBL-1.0) — see https://www.anguskit.com/licenses/XCBL-1.0. Distributed under a paid subscription only.
