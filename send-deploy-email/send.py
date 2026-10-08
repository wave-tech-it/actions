"""Invia email riepilogativa esito deploy via SMTP SSL (stdlib only)."""

import os
import smtplib
import sys
from email.message import EmailMessage

REQUIRED = ["SMTP_HOST", "SMTP_USER", "SMTP_PASS", "SMTP_FROM", "MAIL_TO"]


def main() -> int:
    missing = [k for k in REQUIRED if not os.environ.get(k)]
    if missing:
        print(f"::error::Variabili mancanti: {', '.join(missing)}")
        return 1

    host = os.environ["SMTP_HOST"]
    port = int(os.environ.get("SMTP_PORT", "465"))
    status = os.environ.get("DEPLOY_STATUS", "unknown").lower()
    ok = status == "success"
    icon = "✅" if ok else "❌"
    label = "SUCCESS" if ok else "FAILURE"

    repo = os.environ.get("GH_REPO", "?")
    ref = os.environ.get("GH_REF", "?")
    sha = os.environ.get("GH_SHA", "?")[:7]
    actor = os.environ.get("GH_ACTOR", "?")
    event = os.environ.get("GH_EVENT", "?")
    tag = os.environ.get("DEPLOY_TAG", "") or "-"
    run_url = os.environ.get("GH_RUN_URL", "")

    msg = EmailMessage()
    msg["Subject"] = f"[deploy] {repo}@{ref}: {label} ({tag})"
    msg["From"] = os.environ["SMTP_FROM"]
    msg["To"] = os.environ["MAIL_TO"]
    msg.set_content(
        f"{icon} Deploy {label}\n"
        f"\n"
        f"Repo:    {repo}\n"
        f"Branch:  {ref}\n"
        f"Commit:  {sha} (by {actor}, via {event})\n"
        f"Tag:     {tag}\n"
        f"\n"
        f"Dettagli run: {run_url}\n"
    )

    with smtplib.SMTP_SSL(host, port, timeout=30) as smtp:
        smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        smtp.send_message(msg)

    print(f"Email {label} inviata a {os.environ['MAIL_TO']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
