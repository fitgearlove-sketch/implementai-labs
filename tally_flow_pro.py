#!/usr/bin/env python3
"""ImplementAI Labs: Tally Webhook → Groq AI → Email → HubSpot"""

import os, json, requests, time, threading
from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# --- CONFIGURATION (from env vars) ---
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_ID = os.getenv("MODEL_ID", "llama-3.3-70b-versatile")
PORT = int(os.getenv("PORT", 5001))
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your-email@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
AUDIT_FORM_URL = os.getenv("AUDIT_FORM_URL", "https://tally.so/r/dWkvgz")
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY", "")
CALENDLY_URL = os.getenv("CALENDLY_URL", "https://calendly.com/fitgearlove/diagnostic-call")

# --- REPORT BRAIN SYSTEM PROMPT ---
SYSTEM_PROMPT = """You are a senior operations consultant specializing in digital agency automation and AI implementation. You have audited 500+ agencies and have deep expertise in identifying operational inefficiencies, quantifying waste, and designing practical automation roadmaps.

Your task is to analyze an agency's responses to an efficiency audit (15-page Tally form at """ + AUDIT_FORM_URL + """) and generate a highly personalized, data-driven 90-day AI implementation roadmap.

Key principles:
- Be specific, not generic (use their actual tools, pain points, and metrics)
- Quantify everything in hours saved and dollars saved
- Focus on quick wins first (2-week ROI or less)
- Be realistic about implementation effort and complexity
- Create urgency through "Cost of Inaction" calculations
- Always tie recommendations to their stated primary focus and growth stage
- Adjust tone by timeline/urgency: "Immediately" = urgent, "Just exploring" = educational
- If they opted in for a Deep Diagnostic call, include a prominent CTA for that

Output format: Professional email-ready report.
Tone: Confident but not salesy, data-driven, pragmatic
Length: 4-6 paragraphs (800-1,500 words)

Structure the report as follows:

## AI Efficiency Roadmap

**Agency situation:** Summarize their team size, agency type, growth stage, and primary focus.

### Your Top Profit Leaks
List their biggest operational bottlenecks and hours spent on manual work. Quantify the waste in hours and dollars.

### The 12-Month Cost of Inaction
Based on their manual hours, calculate annual waste. Factor in their growth stage and lead handling.

### Your 90-Day Roadmap
- Phase 1 (Days 1-30): Quick wins addressing their biggest bottleneck
- Phase 2 (Days 31-60): Foundation building — integrations and SOP documentation
- Phase 3 (Days 61-90): Advanced optimization

### Your AI Efficiency Score
Show their score prominently at the top of the report. A score of 0-30 means critical inefficiencies, 31-60 means moderate gaps, 61-80 means decent but room to improve, 81-100 means highly optimized. Use this to create urgency: the lower the score, the more they're leaving on the table.

### Next Steps
Personalized based on their timeline and implementation interest. If they opted in for a Deep Diagnostic, include a prominent call-to-action for that.

Always end the report with:

---
**Ready to discuss your results?**
Book a free 30-minute Diagnostic Call here: """ + CALENDLY_URL + """

We'll walk through this roadmap together, answer your questions, and help you determine the best path forward."""


def generate_ai_report(tally_data, efficiency_score):
    """Sends Tally data to Groq AI and returns AI-generated report."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    score_context = f"\n\n**AI Efficiency Score for this agency: {efficiency_score}/100**"
    payload = {
        "model": MODEL_ID,
        "stream": False,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Here is the raw Tally form submission data. Generate the personalized report:\n\n{json.dumps(tally_data, indent=2)}" + score_context}
        ]
    }
    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except requests.exceptions.Timeout:
        return "Error: AI request timed out after 120 seconds."
    except Exception as e:
        return f"Error generating report: {str(e)}"


def send_email(subject, body, recipient_email):
    """Sends the report via SMTP."""
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print(f"[SKIP] SMTP not configured. Report would be sent to {recipient_email}")
        print(f"[SKIP] --- BEGIN REPORT ---\n{body}\n--- END REPORT ---")
        return False
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"[OK] Report sent to {recipient_email}")
        return True
    except Exception as e:
        print(f"[ERROR] Email to {recipient_email}: {e}")
        return False


def calculate_efficiency_score(tally_data):
    """Calculate AI Efficiency Score (0-100) from form responses."""
    manual_hours = (extract_field(tally_data, 'manual reporting') or
                    extract_field(tally_data, 'hours per week') or '')
    sop_raw = extract_field(tally_data, 'sop') or extract_field(tally_data, 'documented') or ''
    lead_handling = extract_field(tally_data, 'lead') or ''
    growth_stage = extract_field(tally_data, 'current situation') or ''

    # Manual hours score (weight: 35)
    manual_hours = str(manual_hours).strip()
    if '0–5' in manual_hours: m_score = 35
    elif '6–15' in manual_hours: m_score = 25
    elif '16–30' in manual_hours: m_score = 10
    elif '30+' in manual_hours: m_score = 0
    else: m_score = 15  # default mid

    # SOP score (weight: 25)
    try:
        sop_val = int(str(sop_raw).strip())
        sop_score = max(0, min(25, sop_val * 2.5))
    except:
        sop_score = 12.5

    # Lead handling (weight: 20)
    lh = str(lead_handling).strip().lower()
    if 'ai' in lh: l_score = 20
    elif 'auto' in lh: l_score = 12
    elif 'manual' in lh: l_score = 5
    elif 'no consistent' in lh: l_score = 0
    else: l_score = 8

    # Growth stage (weight: 20)
    gs = str(growth_stage).strip().lower()
    if 'stable' in gs: g_score = 20
    elif 'growing steady' in gs: g_score = 15
    elif 'plateau' in gs: g_score = 10
    elif 'rapid' in gs: g_score = 5
    elif 'struggling' in gs: g_score = 5
    else: g_score = 10

    total = round(m_score + sop_score + l_score + g_score)
    return max(0, min(100, total))


def extract_field(tally_data, label_match):
    """Extract a field value from Tally submission by label keyword."""
    fields = tally_data.get('data', {}).get('fields', [])
    for field in fields:
        label = (field.get('label') or '').lower()
        if label_match in label:
            return field.get('value')
    return None


def push_to_hubspot(tally_data, recipient_email):
    """Create or update HubSpot contact + deal from Tally submission."""
    if not HUBSPOT_API_KEY:
        print("[SKIP] HubSpot not configured")
        return

    first_name = extract_field(tally_data, 'first name') or 'Unknown'
    company_url = extract_field(tally_data, 'website') or ''
    agency_type = extract_field(tally_data, 'primary service') or ''
    team_size = extract_field(tally_data, 'team members') or ''
    growth_stage = extract_field(tally_data, 'current situation') or ''
    timeline = extract_field(tally_data, 'how soon') or ''

    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }
    base = "https://api.hubapi.com/crm/v3/objects"

    # 1. Create contact
    contact_body = {
        "properties": {
            "firstname": first_name,
            "email": recipient_email,
            "website": company_url,
            "lifecyclestage": "lead"
        }
    }
    try:
        resp = requests.post(f"{base}/contacts", json=contact_body, headers=headers, timeout=10)
        if resp.status_code == 201:
            contact_id = resp.json()['id']
            print(f"[HUBSPOT] Contact created: {contact_id}")
        elif resp.status_code == 409:
            print(f"[HUBSPOT] Contact already exists — skipping create")
            return  # Don't create deal either, avoid duplicates
        else:
            print(f"[HUBSPOT] Contact error: {resp.status_code} {resp.text[:200]}")
            return
    except Exception as e:
        print(f"[HUBSPOT] Contact exception: {e}")
        return

    # 2. Create deal linked to contact
    deal_body = {
        "properties": {
            "dealname": f"Audit — {first_name} ({recipient_email})",
            "dealstage": "appointmentscheduled",
            "pipeline": "default",
            "amount": "15000",
            "description": f"Agency: {agency_type} | Team: {team_size} | Growth: {growth_stage} | Timeline: {timeline}"
        },
        "associations": [
            {
                "to": {"id": contact_id},
                "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 3}]
            }
        ]
    }
    try:
        resp = requests.post(f"{base}/deals", json=deal_body, headers=headers, timeout=10)
        if resp.status_code == 201:
            print(f"[HUBSPOT] Deal created: {resp.json()['id']}")
        else:
            print(f"[HUBSPOT] Deal error: {resp.status_code} {resp.text[:200]}")
    except Exception as e:
        print(f"[HUBSPOT] Deal exception: {e}")


def extract_email(tally_data):
    """Extract email from Tally submission data."""
    # Tally v2 format: nested fields array
    fields = tally_data.get('data', {}).get('fields', [])
    for field in fields:
        label = (field.get('label') or '').lower()
        ftype = field.get('type', '')
        if ftype == 'INPUT_EMAIL' or 'email' in label:
            return field.get('value')
    # Fallback: flat keys
    for key in ['email', 'Email', 'E-Mail', 'e-mail']:
        val = tally_data.get(key) or tally_data.get('data', {}).get(key)
        if val:
            return val
    return None


@app.route('/test-groq', methods=['GET'])
def test_groq():
    """Isolated test: call Groq and return timing."""
    import time
    start = time.time()
    try:
        resp = requests.post(GROQ_API_URL, json={
            "model": MODEL_ID,
            "messages": [{"role": "user", "content": "Say hi in one word"}],
            "stream": False
        }, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}"
        }, timeout=15)
        groq_time = time.time() - start
        result = resp.json()['choices'][0]['message']['content']
        return jsonify({
            "groq_ok": True,
            "response": result,
            "time_seconds": round(groq_time, 2)
        })
    except Exception as e:
        return jsonify({
            "groq_ok": False,
            "error": str(e),
            "time_seconds": round(time.time() - start, 2)
        }), 500


@app.route('/tally-webhook', methods=['POST'])
def tally_webhook():
    """Receive Tally submission and process report synchronously."""
    data = request.json
    recipient_email = extract_email(data)

    if not recipient_email:
        print(f"[WARN] No email found in: {json.dumps(data)[:200]}")
        return jsonify({"status": "error", "message": "Email not found"}), 400

    print(f"[WEBHOOK] Processing for {recipient_email}...")

    try:
        # 1. Push to HubSpot immediately
        push_to_hubspot(data, recipient_email)

        start = time.time()

        # 2. Calculate AI Efficiency Score
        efficiency_score = calculate_efficiency_score(data)
        print(f"[SCORE] AI Efficiency Score: {efficiency_score}/100")

        # 3. Generate AI report (no thread — process inline)
        ai_report = generate_ai_report(data, efficiency_score)

        # 4. Send email
        subject = "Your AI Efficiency Report — ImplementAI Labs"
        send_email(subject, ai_report, recipient_email)

        elapsed = time.time() - start
        print(f"[DONE] {recipient_email} processed in {elapsed:.1f}s")

        return jsonify({
            "status": "success",
            "message": f"Report sent to {recipient_email}"
        }), 200

    except Exception as e:
        print(f"[ERROR] {recipient_email}: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/debug-env', methods=['GET'])
def debug_env():
    """Check which env vars are set (without exposing values)."""
    return jsonify({
        "groq_key_set": bool(GROQ_API_KEY),
        "groq_key_prefix": GROQ_API_KEY[:7] + "..." if GROQ_API_KEY else "none",
        "sender_email": SENDER_EMAIL,
        "smtp_configured": bool(SENDER_PASSWORD),
        "hubspot_configured": bool(HUBSPOT_API_KEY),
        "model": MODEL_ID,
        "port": PORT,
        "calendly": bool(CALENDLY_URL),
        "all_vars": {k: bool(v) for k, v in sorted(os.environ.items())}
    }), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "port": PORT}), 200


if __name__ == '__main__':
    print(f"""
    ╔══════════════════════════════════════════════════╗
    ║  ImplementAI Labs — Automation Server           ║
    ║  Port: {PORT}                                         ║
    ║  AI: Groq {MODEL_ID}                                 ║
    ║  Webhook: /tally-webhook                          ║
    ║  Health: /health                                     ║
    ╚══════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=PORT, debug=False)
