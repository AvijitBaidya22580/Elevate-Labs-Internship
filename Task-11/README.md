# Task-11-Phishing-Attack-Simulation-Detection
  
**Author:** AVIJIT  BAIDYA  
**Date:** February 02, 2026  
**Purpose:** Personal cybersecurity awareness exercise (only self / test accounts used)

## ⚠️ Important Ethical & Legal Notice

This is a **personal educational simulation only**.  
No real people, real companies, or real email accounts (except my own test ones) were involved.  
**Never send phishing emails to anyone without explicit written permission** — it is illegal in most countries.

## Goal of This Lab

- Understand how phishing emails & landing pages are built
- Create realistic (but fake) examples
- Self-test detection skills
- Document red flags & lessons learned
- Practice writing a simple simulation report

## Tools Used / Recommended (2026)

- GoPhish (open-source phishing framework)  
- Local SMTP or Mailtrap / Mailgun free tier (for testing only)  
- Text editor + browser  
- Targets: only myself or lab/test email accounts

## Simulated Campaign (Self-run – February 2026)

**Theme:** Fake Microsoft 365 – "Mailbox Almost Full – Action Required"  
**Campaign name:** M365-Storage-Test-2026  
**Date simulated:** 2026-02-02  
**Targets:** 1 (myself – test mailbox)  
**Result summary:**

| Metric                  | Value | %     |
|-------------------------|-------|-------|
| Emails Sent             | 1     | —     |
| Emails Delivered        | 1     | 100%  |
| Emails Opened           | 1     | 100%  |
| Links Clicked           | 1     | 100%  |
| Credentials Submitted   | 0     | 0%    |

Time to click: ~40 seconds  
Red flags spotted before clicking: 4–5 out of 8  
Biggest weakness: urgency + curiosity

## 1. Fake Email Template (HTML – ready for GoPhish or similar)

<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Microsoft 365 – Storage Alert</title>
</head>
<body style="font-family:Segoe UI,Helvetica,Arial,sans-serif; background:#f3f2f1; margin:0; padding:20px;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" border="0" style="background:#ffffff; border:1px solid #e8e8e8;">
          <tr>
            <td style="padding:20px; background:#0078d4; color:white; text-align:center;">
              <h2>Microsoft 365 Storage Alert</h2>
            </td>
          </tr>
          <tr>
            <td style="padding:30px 40px; color:#333;">
              <p>Dear User,</p>
              <p>Your mailbox is almost full (94% used). To avoid service interruption, please take action before <strong>February 05, 2026</strong>.</p>
              <p style="text-align:center; margin:30px 0;">
                <a href="{{.URL}}" style="background:#0078d4; color:white; padding:14px 32px; text-decoration:none; border-radius:4px; font-weight:bold; font-size:16px;">
                  Review & Free Up Space Now
                </a>
              </p>
              <p>If not resolved in 72 hours, sending/receiving email may be limited.</p>
              <p>Microsoft Account Team</p>
              <hr style="border:none; border-top:1px solid #eee; margin:30px 0;">
              <p style="font-size:12px; color:#666; text-align:center;">
                © 2026 Microsoft Corporation. All rights reserved.<br>
                This is an automated security notice. Do not reply.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
(Note: {{.URL}} is replaced by the phishing framework tracking link)


## 2. Fake Landing Page (Awareness version – shows instantly you were "caught")
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>SIMULATION – You Got Phished</title>
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <style>
    /* Fixed CSS and markup issues:
       - use `body { ... }` selector (not `<body>` inside style)
       - clean, single <body> and single .box container
       - proper nesting and no duplicate tags
    */
    body { font-family: Arial, sans-serif; text-align: center; background: #f8d7da; color: #721c24; padding: 40px; margin: 0; }
    .box { max-width: 720px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); }
    h1 { color: #dc3545; }
    ul { text-align: left; line-height: 1.6; }
  </style>
</head>
<body>
  <div class="box">
    <h1>🚨 THIS WAS A PHISHING SIMULATION 🚨</h1>
    <p style="font-size:1.4em; margin:20px 0;">
      Congratulations — you just clicked a fake phishing link!<br>
      (But don't worry — this is only a personal training exercise.)
    </p>

    <h2>Red Flags You Should Have Noticed (2026)</h2>
    <ul>
      <li>Urgent deadline / threat ("before Feb 05" or lose access)</li>
      <li>Generic greeting ("Dear User" instead of your name)</li>
      <li>Sender address usually suspicious (not ending in @microsoft.com)</li>
      <li>Link looks real but goes somewhere else (always hover!)</li>
      <li>No real company context or tenant name</li>
      <li>Pressure + fear ("service will be limited")</li>
      <li>Unexpected email about account/security/storage</li>
    </ul>

    <p style="margin-top:40px; font-size:1.1em;">
      <strong>Best habit:</strong> Never click links in urgent security emails.<br>
      Go directly to office.com or the official app instead.
    </p>

    <p style="margin-top:30px; color:#444;">
      Made for personal learning – Task 11 – February 2026
    </p>
  </div>
</body>
</html>

## Quick Red Flags Checklist (2026 edition)

Urgency + short deadline  
Suspicious sender / reply-to address  
Hover shows different URL  
"Dear User / Customer" greeting  
Requests password / MFA / payment via link  
Unexpected attachment  
Emotional manipulation (fear, curiosity, greed)  
Grammar / branding slightly off (less common now)

## Personal Lessons from This Run

Urgency still works even when you know it's fake  
Hovering the link is the #1 easiest defense  
Immediate feedback page (like above) helps learning a lot  
Next time: try HR theme, delivery scam, or fake Teams invite

## Final Note
This repo/page is only for education and self-improvement.  
Stay curious, stay suspicious, stay safe. 🛡️