# Agent Skills

[Agent Skills](https://agentskills.io) are a simple, open format for giving agents new capabilities and expertise.

Skills are folders of instructions, scripts, and resources that agents can discover and use to perform better at specific tasks. Write once, use everywhere.

## Getting Started

- [Documentation](https://agentskills.io) - Guides and tutorials
- [Specification](https://agentskills.io/specification) - Format details
- [Example Skills](https://github.com/anthropics/skills) - See what's possible
- [Automation Features](docs/automation.md) - Autonomous PR review and management

This repo contains the specification, documentation, and reference SDK. Also see a list of example skills [here](https://github.com/anthropics/skills).

## Autonomous Development Features

This repository includes automated workflows for seamless PR management:

- 🤖 **Automated PR Reviews** - Quality checks, test runs, and review comments on every PR
- ⚡ **Auto-Fix** - Comment `/fix` on PRs to automatically resolve linting and formatting issues
- 📊 **Continuous Monitoring** - Daily health checks and dependency update notifications
- 🔍 **Conflict Detection** - Automatic merge conflict detection

See [docs/automation.md](docs/automation.md) for full details.

## About

Agent Skills is an open format maintained by [Anthropic](https://anthropic.com) and open to contributions from the community.

## License

Code in this repository is licensed under [Apache 2.0](LICENSE). Documentation is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/). See individual directories for details.