from hashlib import sha256

DISCLAIMER_VERSION = "2025-09-27.1"

RISK_NOTICE = (
    "⚠️ **Risk Notice**: This tool provides odds analysis and bankroll management "
    "calculations only. It does not guarantee profit or eliminate risk. Sports outcomes "
    "are uncertain, and losses may exceed expectations. Always wager responsibly and within your means."
)

CONSENT_TEXT = (
    f"{RISK_NOTICE}\n\n"
    "**By continuing, you acknowledge:**\n"
    "• Analysis only; not financial advice\n"
    "• You assume all risk and responsibility\n"
    "• You comply with local laws\n"
    "• Beta software may have defects\n"
)

DISCLAIMER_HASH = sha256(CONSENT_TEXT.encode("utf-8")).hexdigest()
