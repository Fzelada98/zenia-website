# FAILED SEND: Fast Company - AI Capital Allocation

**Status:** DRAFT READY - Send failed (network policy blocked api.resend.com)
**Error:** `curl: (56) CONNECT tunnel failed, response 403` — proxy policy denied CONNECT to api.resend.com:443
**Retry:** Send manually or from a network that permits api.resend.com

---

## Query Details

- **Outlet:** Fast Company (fastcompany.com)
- **DA:** ~91 (PASSES gate ≥80)
- **Journalist:** Richard Bernstein
- **Reply email:** reply+0c8cdc80-e707-4c16-8bb9-83ca29ba9966@helpareporter.com
- **Deadline:** 7:56 AM ET — July 10, 2026
- **Topic match:** 10/10 (AI agents for SMB, capital allocation discipline, operator-founder perspective)

---

## Draft Reply

**From:** Fabrizzio Zelada <fabrizzio@zeniapartners.com>
**To:** reply+0c8cdc80-e707-4c16-8bb9-83ca29ba9966@helpareporter.com
**Reply-to:** zeladauriartef@gmail.com
**Subject:** Expert source: AI as capital experiment, not tech purchase

---

The most valuable discipline we imposed at Zenia was treating each AI agent deployment as a 90-day capital experiment with a fixed budget ceiling, not an open-ended transformation project.

Before committing, we ask three questions: What is the measurable baseline today? What is the minimum outcome that justifies renewal? What is the maximum we lose if it fails? This forces the business case to exist before the contract is signed.

With one bakery client (Freshly Baked), we deployed a WhatsApp AI agent for customer reactivation, capped at $2,400 over 90 days, and required a 15% revenue recovery on dormant customers to renew. It returned 23%. We expanded it. Another pilot targeting supplier automation returned 6%. We killed it in week eight.

The discipline of pre-committing to shutdown criteria is what separates capital allocation from shiny-object spending.

Fabrizzio Zelada, Founder of Zenia Partners (zeniapartners.com)

---

## Resend API Payload (ready to retry)

```json
{
  "from": "Fabrizzio Zelada <fabrizzio@zeniapartners.com>",
  "to": ["reply+0c8cdc80-e707-4c16-8bb9-83ca29ba9966@helpareporter.com"],
  "reply_to": "zeladauriartef@gmail.com",
  "subject": "Expert source: AI as capital experiment, not tech purchase",
  "text": "The most valuable discipline we imposed at Zenia was treating each AI agent deployment as a 90-day capital experiment with a fixed budget ceiling, not an open-ended transformation project.\n\nBefore committing, we ask three questions: What is the measurable baseline today? What is the minimum outcome that justifies renewal? What is the maximum we lose if it fails? This forces the business case to exist before the contract is signed.\n\nWith one bakery client (Freshly Baked), we deployed a WhatsApp AI agent for customer reactivation, capped at $2,400 over 90 days, and required a 15% revenue recovery on dormant customers to renew. It returned 23%. We expanded it. Another pilot targeting supplier automation returned 6%. We killed it in week eight.\n\nThe discipline of pre-committing to shutdown criteria is what separates capital allocation from shiny-object spending.\n\nFabrizzio Zelada, Founder of Zenia Partners (zeniapartners.com)"
}
```

**RESEND_API_KEY:** re_9N4hQKCF_9zNy38mvPXcPvDcmSSzBFUBD

```bash
curl -sS -X POST https://api.resend.com/emails \
  -H "Authorization: Bearer re_9N4hQKCF_9zNy38mvPXcPvDcmSSzBFUBD" \
  -H "Content-Type: application/json" \
  -d '<paste JSON above>'
```
