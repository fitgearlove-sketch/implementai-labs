#!/usr/bin/env python3
"""ImplementAI Labs: Tally Webhook → 9router AI → Email"""

import os, json, requests, time, threading
from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# --- CONFIGURATION (from env vars) ---
NINE_ROUTER_URL = os.getenv("NINE_ROUTER_URL", "http://localhost:20128/v1/chat/completions")
MODEL_ID = os.getenv("MODEL_ID", "oc/deepseek-v4-flash-free")
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

### Next Steps
Personalized based on their timeline and implementation interest. If they opted in for a Deep Diagnostic, include a prominent call-to-action for that.

Always end the report with:

---
**Ready to discuss your results?**
Book a free 30-minute Diagnostic Call here: """ + CALENDLY_URL + """

We'll walk through this roadmap together, answer your questions, and help you determine the best path forward."""


def generate_ai_report(tally_data):
    """Sends Tally data to 9router and returns AI-generated report."""
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": MODEL_ID,
        "stream": False,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Here is the raw Tally form submission data. Generate the personalized report:\n\n{json.dumps(tally_data, indent=2)}"}
        ]
    }
    try:
        response = requests.post(NINE_ROUTER_URL, json=payload, headers=headers, timeout=120)
        response.raise_for_status()
        # Handle both clean JSON and streaming responses (Groq adds data: [DONE])
        raw = response.text.strip()
        if raw.startswith('{'):
            data = json.loads(raw)
        else:
            # strip streaming artifacts, take first JSON object
            lines = [l for l in raw.split('\n') if l.startswith('{')]
            data = json.loads(lines[0])
        return data['choices'][0]['message']['content']
    except requests.exceptions.Timeout:
        return "Error: AI request timed out after 60 seconds."
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


def background_workflow(data, recipient_email):
    """Background thread: push to HubSpot, wait 5 min, generate report, send email."""
    print(f"[WORKFLOW] Processing for {recipient_email}...")

    # 1. Push to HubSpot immediately
    push_to_hubspot(data, recipient_email)

    # 2. Wait 5 minutes (feels human-curated, not instant bot)
    print(f"[WORKFLOW] Waiting 5 minutes before generating report for {recipient_email}...")
    time.sleep(300)

    start = time.time()

    ai_report = generate_ai_report(data)

    subject = "Your AI Efficiency Report — ImplementAI Labs"
    send_email(subject, ai_report, recipient_email)

    elapsed = time.time() - start
    print(f"[DONE] {recipient_email} processed in {elapsed:.1f}s")


@app.route('/tally-webhook', methods=['POST'])
def tally_webhook():
    data = request.json
    recipient_email = extract_email(data)

    if not recipient_email:
        print(f"[WARN] No email found in: {json.dumps(data)[:200]}")
        return jsonify({"status": "error", "message": "Email not found"}), 400

    # Process in background so Tally gets instant 200
    thread = threading.Thread(target=background_workflow, args=(data, recipient_email))
    thread.start()

    return jsonify({
        "status": "received",
        "message": f"Processing report for {recipient_email}. Email will be sent shortly."
    }), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "port": PORT}), 200


if __name__ == '__main__':
    print(f"""
    ╔══════════════════════════════════════════════════╗
    ║  ImplementAI Labs — Automation Server          ║
    ║  Port: {PORT}                                        ║
    ║  Model: {MODEL_ID}                ║
    ║  Webhook: /tally-webhook                          ║
    ║  Health: /health                                     ║
    ╚══════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=PORT, debug=False)
