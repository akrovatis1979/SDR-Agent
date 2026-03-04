from config import Config
DEFAULT_TEXT= """SDR Playbook:
- Focus on business outcomes and relevance to the prospect.
- Keep initial outreach under 120 words with a clear, soft CTA.
- Personalize with a recent company milestone if possible.
"""

def ensure_playbook(cfg: Config):
    cfg.ensure_dirs()
    if not cfg.DOC_PATH.exists():
        cfg.DOCS_PATH.write_text(DEFAULT_TEXT, encoding="utf-8")
        