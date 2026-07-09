# AI Efficiency Audit — Tally Form (Live Version)

**Form URL:** https://tally.so/r/dWkvgz
**Estimated Completion Time:** 5–7 minutes
**Question Count:** 15 pages, ~18 questions (depending on conditional logic)
**Design:** Dark theme (#0b0d10), professional, mobile-friendly

---

## Page 1: Welcome & Agency Type

**Headline:** Free AI Efficiency Audit
**Bullets:**
- ✅ Find your operational leaks.
- ✅ Get your AI Score
- ✅ Top 3 Automation Fixes

**Heading:** Let's start

**Q1 — What is your Agency's primary service?** *(radio, required)*
- Lead Gen / Sales
- Full-Service Marketing
- SEO / Content
- Design / Development
- Other *(conditional text box appears)*

---

## Page 2: Team Size

**Q2 — How many full-time team members do you have?** *(radio, required)*
- 1–2
- 3–10
- 11–25
- 26–50
- 51+

---

## Page 3: Revenue

**Q3 — What is your current Monthly Revenue range?** *(radio, required)*
- Under $20k
- $20k–$50k
- $50k–$150k
- $150k+

---

## Page 4: Growth Stage

**Q4 — Which best describes your current situation?** *(radio, required)*
- Struggling to stay afloat / Inconsistent revenue
- Stable but not growing
- Growing steadily but stretched thin
- Rapid growth, can't keep up with demand
- Plateaued after growth phase

---

## Page 5: Primary Focus

**Q5 — What is your primary focus for the next 90 days?** *(radio, required)*
- Scale revenue without hiring more people
- Reclaim the founder/manager's time
- Improve service speed and quality
- Just get organized
- Rapid growth — struggling to keep up

---

## Page 6: Manual Time

**Heading:** You are halfway through...

**Q6 — How many hours per week does your team spend on manual reporting, data entry or lead follow-up?** *(radio, required)*
- 0–5 hours
- 6–15 hours
- 16–30 hours
- 30+ hours

---

## Page 7: Lead Handling

**Q7 — How do you currently handle new incoming leads?** *(radio, required)*
- Manual email response (whenever we see it)
- Standard auto-reply
- Full AI-powered qualification (SDR Agent)
- We don't have a consistent lead flow

---

## Page 8: SOP Documentation

**Q8 — How documented are your Agency's SOP's (Standard Operation Procedures)?** *(linear scale, required)*
- 0 = All in my head
- 10 = Fully documented and followed

---

## Page 9: Biggest Bottleneck

**Q9 — What is your biggest operational bottleneck?** *(radio, required)*
- Client Onboarding
- Proposal Creation / Scoping
- Weekly/Monthly Reporting
- Internal Project Coordination
- Other *(conditional text box: "Please specify" — short text)*

---

## Page 10: Ecosystem

**Q10 — Which ecosystem does your team primarily use?** *(radio, required)*
- Google Workspace
- Microsoft 365
- A messy mix of both
- Other *(conditional text box: "Please specify:" — short text)*

---

## Page 11: Time Spent

**Q11 — Where does your team spend the most time?** *(radio, required)*
- Slack
- Notion / ClickUp / Asana
- Gmail / Outlook
- Spreadsheets
- Other *(conditional text box: "Please specify:" — short text)*

---

## Page 12: Timeline

**Q12 — How soon are you looking to implement AI automation?** *(radio, required)*
- Immediately
- Within 1–3 months
- Within 3–6 months
- Just exploring for now

---

## Page 13: Contact Info

**Heading:** Where should we send the report?

**Q13 — First Name** *(text, required)*

**Q14 — E-Mail** *(email, required)*

**Q15 — Company Website (URL)** *(text, required)*

---

## Page 14: Commitment

**Heading:** Your AI Efficiency Score is being calculated...

**Q16 — If we identify 3 automations that save your team 20+ hours a week, would you want a partner to build and manage them for you?** *(radio, required)*
- Yes, I'm looking for an implementation partner
- Maybe, I want to see the audit results first
- No, my team will build everything ourselves

**Q17 — Would you like to apply for a Deep Diagnostic Blueprint? (This includes a full custom workflow map, ROI model, and 90-day implementation roadmap).** *(radio, required)*
- Yes, I'd like to apply for a Fit-Check call
- No, just send the free Audit Report for now

---

## Page 15: Last Question

**Heading:** Last but not least!

**Q18 — Optional: What is the #1 manual task you wish you could automate yesterday?** *(textarea)*

**Submit Button Label:** "Generate My Audit Results"

---

## Scoring Logic (Backend Calculations)

### Pain Score (0–100)
- Manual hours (Q6): 0–25 points
- SOP documentation (Q8): 0–20 points (inverse — less documented = higher pain)
- Bottleneck severity (Q9): 0–15 points
- Lead handling (Q7): 0–15 points (manual = higher pain)
- Growth stage (Q4): 0–15 points (stretched/rapid = higher pain)
- Primary focus (Q5): 0–10 points (scale/reclaim = higher opportunity)

### Opportunity Score (0–100)
- Team size (Q2): 3–25 employees = higher score
- Revenue range (Q3): higher = higher score
- Growth stage (Q4): growing/rapid = higher score
- Timeline urgency (Q12): sooner = higher score
- Commitment (Q16): "Yes, looking for partner" = higher score

### Lead Quality Score (A/B/C)
- **A-Grade:** Pain Score >60, Timeline ≤3 months, Growth = rapid/stretched
- **B-Grade:** Pain Score >40, Timeline ≤6 months
- **C-Grade:** All others

These scores feed into the AI "Report Brain" to generate personalized recommendations.
