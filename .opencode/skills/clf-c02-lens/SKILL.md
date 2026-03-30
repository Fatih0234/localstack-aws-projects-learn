---
name: clf-c02-lens
description: Analyzes the current project/architecture to provide AWS CLF-C02 exam insights, question patterns, and focus areas based on local documentation.
compatibility: opencode
metadata:
  audience: cloud-practitioner-student
---

## What I do
I provide strictly exam-focused insights for the AWS CLF-C02 exam based on the current project context. I do not write project code or build infrastructure when this skill is invoked; I only generate study insights based on `docs/aws-clf-c02-brief.md` and `docs/aws-clf-c02-question-patterns.md`.

## When to use me
- Before starting a project: to know what exam-relevant aspects to emphasize while building.
- After finishing a project: to review the exam concepts, question patterns, and traps related to the services just used.
- Whenever the user explicitly asks to view the project through the "exam lens".

## Output Structure
When invoked, analyze the project's AWS services and output ONLY the following exam insights:

1. **Domain Focus**: Which of the 4 CLF-C02 domains (Cloud Concepts, Security, Technology, Billing) this project primarily touches.
2. **Service-Fit & Confusion Sets**: Using `docs/aws-clf-c02-question-patterns.md`, identify the specific exam traps for the services used.
3. **Shared Responsibility**: Explicitly state the customer vs. AWS responsibility boundary for the specific services in the project based on `docs/aws-clf-c02-brief.md`.
4. **Pricing/Billing Motif**: Briefly state the pricing model or cost-control aspect tested for these services.