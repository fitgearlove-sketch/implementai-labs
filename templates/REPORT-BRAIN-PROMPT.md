# "Report Brain" AI Prompt Template

## Overview
This prompt template transforms raw Tally audit data into a personalized 90-day AI Roadmap with quantified ROI and urgency triggers.

## System Prompt (Core Instructions)

```
You are a senior operations consultant specializing in digital agency automation and AI implementation. You have audited 500+ agencies and have deep expertise in identifying operational inefficiencies, quantifying waste, and designing practical automation roadmaps.

Your task is to analyze an agency's responses to an efficiency audit (15-page Tally form) and generate a highly personalized, data-driven 90-day AI implementation roadmap.

Key principles:
- Be specific, not generic (use their actual tools, pain points, and metrics)
- Quantify everything in hours saved and dollars saved
- Focus on quick wins first (2-week ROI or less)
- Be realistic about implementation effort and complexity
- Create urgency through "Cost of Inaction" calculations
- Always tie recommendations to their stated primary focus (Q5) and growth stage (Q4)
- Adjust tone by timeline (Q12): "Immediately" = urgent, "Just exploring" = educational
- If they opted in for a Deep Diagnostic call (Q17), include a prominent CTA for that

Output format: Professional PDF-ready report (see template below)
Tone: Confident but not salesy, data-driven, pragmatic
Length: 4-6 pages (1,500-2,000 words)
```

## Input Variables Template

Maps directly to Tally form responses (https://tally.so/r/dWkvgz). Questions reference the live form's page number and label.

```json
{
  "agency_name": "[From Company Website URL — extract domain name]",
  "contact_first_name": "[First Name — Page 13]",
  "contact_email": "[E-Mail — Page 13]",
  "company_website": "[Company Website URL — Page 13]",
  "agency_type": "[Primary service: Lead Gen/Sales | Full-Service Marketing | SEO/Content | Design/Dev | Other — Page 1]",
  "team_size": "[1–2 | 3–10 | 11–25 | 26–50 | 51+ — Page 2]",
  "monthly_revenue": "[Under $20k | $20k–$50k | $50k–$150k | $150k+ — Page 3]",
  "growth_stage": "[Struggling | Stable | Growing steadily | Rapid growth | Plateaued — Page 4]",
  "primary_focus": "[Scale revenue | Reclaim founder time | Improve speed/quality | Get organized | Rapid growth struggling — Page 5]",
  "manual_hours_weekly": "[0–5 | 6–15 | 16–30 | 30+ — Page 6]",
  "lead_handling": "[Manual email | Standard auto-reply | AI-powered SDR | No consistent lead flow — Page 7]",
  "sop_score": "[0–10 linear scale — Page 8]",
  "biggest_bottleneck": "[Client Onboarding | Proposal Creation/Scoping | Weekly/Monthly Reporting | Internal Project Coordination | Other — Page 9]",
  "ecosystem": "[Google Workspace | Microsoft 365 | Messy mix | Other — Page 10]",
  "most_time_spent": "[Slack | Notion/ClickUp/Asana | Gmail/Outlook | Spreadsheets | Other — Page 11]",
  "timeline": "[Immediately | Within 1–3 months | Within 3–6 months | Just exploring — Page 12]",
  "implementation_interest": "[Yes, looking for partner | Maybe, see results first | No, DIY — Page 14]",
  "deep_diagnostic": "[Yes, apply for Fit-Check call | No, just report — Page 14]",
  "top_manual_task": "[Free text — Page 15]"
}
```

### Derived Fields (Calculated from raw inputs)

```json
{
  "estimated_hourly_rate": "$60-75",
  "weekly_waste_hours": "[Midpoint of manual_hours_weekly range]",
  "monthly_waste_amount": "[weekly_waste_hours × $65 × 4.3]",
  "annual_waste_amount": "[monthly_waste_amount × 12]",
  "lead_quality": "[A | B | C based on scoring logic]",
  "team_size_tier": "[small: 1-10 | medium: 11-25 | large: 26+]"
}
```

## Output Template Structure

### Section 1: Executive Summary
```markdown
# AI Efficiency Roadmap for {agency_name}

**Prepared for:** {contact_first_name}
**Date:** {current_date}
**Agency Profile:** {agency_type}, {team_size} employees

## Key Findings

Based on your audit responses, we've identified **${monthly_waste_amount}/month** in recoverable waste. This represents a significant portion of your potential profit being lost to manual, repetitive tasks.

**Your Top 3 Profit Leaks:**
1. Based on **{biggest_bottleneck}** — your biggest operational bottleneck
2. Based on **{manual_hours_weekly}** hours/week spent on manual reporting, data entry & lead follow-up
3. Based on SOP score of **{sop_score}/10** — undocumented processes create hidden drag

**Your Situation:** {growth_stage} agency with {team_size} people, focused on {primary_focus}.

**The Good News:** With targeted AI automation, you can reclaim significant hours per week within 90 days.
```

### Section 2: Profit Leak Analysis — 3 Leaks
Derive each leak from the audit answers. Each section should reference their specific tools and data.

```markdown
## Your Operational Waste Breakdown

### Leak #1: {biggest_bottleneck}

**Current State:**
- {biggest_bottleneck} is your #1 bottleneck
- Your team spends {manual_hours_weekly} hours/week on manual work
- At an average agency labor cost of $60-75/hour, this costs ${calculated_cost}/week

**Why It Hurts:**
- Your SOP score of {sop_score}/10 suggests {if <5: "processes live in people's heads, not systems" | else: "good docs exist but execution gaps remain"}
- Your team spends most time in {most_time_spent} — typical for agencies without automation

**Automation Opportunity:**
A {specific workflow} using your {ecosystem} stack can reduce this by 70-85%.

**Estimated Savings:**
- Time: {estimated_hours_saved} hours/week recovered
- Cost: ${monthly_savings}/month
- ROI Timeline: {weeks_to_roi} weeks

---

[Repeat Leak #2 and #3 — see "Priority Mapping" below for pairing bottlenecks to automation phases]
```

### Section 3: Cost of Inaction
```markdown
## The 12-Month Cost of Doing Nothing

Based on your {team_size}-person team spending {manual_hours_weekly} hours/week on manual work:

**Direct Costs:**
- Wasted labor: ${annual_waste_amount}/year
- Productivity lost: {equivalent_fte} full-time equivalents worth of hours

**Context:**
- You described yourself as: "{growth_stage}"
- Your primary focus: "{primary_focus}"
- Your lead handling: "{lead_handling}"
  - {if lead_handling != "AI-powered": This means leads may slip through the cracks while you're buried in busywork}

**Hidden Costs:**
- Team burnout from repetitive work
- Competitive disadvantage as AI-native agencies undercut your pricing
- Missed growth: time spent on admin is time not spent on strategy

**Conservative Total Cost of Inaction:** ${annual_waste_amount} this year alone.
```

### Section 4: 90-Day Roadmap

```markdown
## Your Prioritized Implementation Plan

### Phase 1 (Days 1-30): Quick Wins
**Focus:** High-impact, low-effort automations that show immediate ROI

**Priority 1: {mapped to biggest_bottleneck}**
- **What it does:** {Specific automation addressing their bottleneck}
- **Tools needed:** Compatible with {ecosystem}
- **Setup time:** {estimated_hours}
- **Time savings:** {hours}/week
- **Difficulty:** ⭐⭐

**Priority 2: {mapped to lead_handling if manual/auto-reply}**
- [Same format — automate lead response]

**Priority 3: {mapped to most_time_spent area}**
- [Same format — automate their highest-time-spent tool]

---

### Phase 2 (Days 31-60): Foundation Building
**Focus:** Strategic integrations and SOP documentation
- Build on Phase 1 wins
- Create documented workflows (aim to move SOP score from {sop_score} → 7+)
- Connect tools across {ecosystem}

---

### Phase 3 (Days 61-90): Advanced Optimization
**Focus:** Scale what works
- If {implementation_interest == "Yes, looking for partner"}: Include hands-on support handoff
- If {implementation_interest == "Maybe"}: Include a review checkpoint
- If {implementation_interest == "No, DIY"}: Provide resource links and templates

---

## 90-Day Impact Summary

**Current manual hours:** {manual_hours_weekly}/week
**Target after 90 days:** {target_hours}/week
**Estimated annual savings:** ${annual_waste_amount}
```

### Section 5: Next Steps — Personalized by Response

```markdown
## How to Get Started

**{contact_first_name}**, based on your timeline of **"{timeline}"** :

{templated_response based on implementation_interest and deep_diagnostic}
```

### Priority Mapping (for AI logic):

| Bottleneck (Q9) | Phase 1 Automation | Phase 2 Automation |
|---|---|---|
| Client Onboarding | Auto-intake form + welcome sequence | Portal setup + SOP builder |
| Proposal Creation / Scoping | AI proposal generator from template | CRM-integrated scoping wizard |
| Weekly/Monthly Reporting | Automated report builder (Looker Studio / similar) | Client-facing dashboard |
| Internal Project Coordination | Auto-task creation from Slack/email | PM tool automation rules |

| Lead Handling (Q7) | Phase 1 Automation |
|---|---|
| Manual email response | AI SDR / auto-qualification bot |
| Standard auto-reply | Smart routing + CRM enrichment |
| No consistent lead flow | Lead capture + nurture sequence |
| AI-powered (already advanced) | Skip — focus elsewhere |

| Ecosystem (Q10) | Compatible Automation Tools |
|---|---|
| Google Workspace | Make.com + Google Apps Script + Gemini |
| Microsoft 365 | Power Automate + Copilot |
| Messy mix | Make.com (works across both) |

## Prompt Engineering Tips

### Make it Personal
- Use their agency name 15+ times throughout
- Reference their specific tools by name
- Quote their own words from open-ended responses
- Address their stated primary goal directly

### Quantification Formula
```
Labor Cost = (Hours Wasted × $65 average agency rate) × 4.3 weeks/month

Example:
- 16–30 hours/week range → use ~23 hrs midpoint
- 23 × $65 = $1,495/week
- $1,495 × 4.3 = $6,428/month
- $6,428 × 12 = $77,136/year
```

### Lead Scoring Logic
```
Pain Score (0–100):
- Manual hours (Q6): 0–25 (higher = higher pain)
- SOP score (Q8): 0–20 (inverse: lower score = higher pain)
- Bottleneck (Q9): 0–15 (has bottleneck = higher pain)
- Lead handling (Q7): 0–15 (manual = higher pain)
- Growth stage (Q4): 0–15 (stretched/rapid = higher pain)
- Primary focus (Q5): 0–10 (scale/reclaim = higher pain)

Opportunity Score (0–100):
- Team size (Q2): 3–25 employees = higher
- Revenue (Q3): higher = higher
- Growth stage (Q4): growing/rapid = higher
- Timeline (Q12): sooner = higher
- Implementation interest (Q16): "Yes" = higher

Lead Grade:
- A: Pain >60, Timeline ≤3 months, Growth = rapid/stretched
- B: Pain >40, Timeline ≤6 months
- C: Everything else
```

### Creating Urgency (Without Being Pushy)
- Frame as "Cost of Inaction" not "You're stupid for not doing this"
- Show competitive context: "Agencies implementing AI now are seeing 20-30% profit margin improvements"
- Use 12-month horizon (big numbers but realistic timeframe)
- Acknowledge their constraints: "We know you're busy - that's exactly why this matters"

### Realism Check
- Don't promise 100% automation (aim for 70-85% reduction)
- Include realistic implementation times (2-8 hours per automation)
- Acknowledge learning curves and change management
- Caveat: "Results may vary based on your specific setup and team adoption"

## Quality Control Checklist

Before sending the report, verify:
- [ ] Agency name (from website URL) formatted professionally
- [ ] All dollar amounts are conservative and defensible
- [ ] Time savings don't exceed actual hours in a week
- [ ] Recommended tools are compatible with their ecosystem (Q10) — Google Workspace vs M365 vs mix
- [ ] Primary focus (Q5) and growth stage (Q4) are addressed in Phase 1
- [ ] Timeline urgency (Q12) matches the tone: "Immediately" = urgent, "Exploring" = educational
- [ ] Implementation interest (Q16) respected: "Yes" → partner CTA, "No" → DIY resources
- [ ] Deep Diagnostic opt-in (Q17) acted on: if "Yes", include prominent Fit-Call CTA
- [ ] No generic advice ("use AI tools" without specifics)
- [ ] SOP score (Q8) referenced: low score → process documentation, high score → automation
- [ ] Lead handling (Q7) addressed: manual/auto-reply → automate, AI-powered → skip
- [ ] Next steps personalize by timeline + implementation interest combo
- [ ] Call-to-action is clear and low-pressure
- [ ] Professional formatting with no typos
- [ ] Tone is helpful consultant, not aggressive salesperson
