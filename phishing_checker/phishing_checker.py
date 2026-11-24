"""
Day 6 - Phishing Link Analyzer
Part of the Cyber Toolkit (10-day build in public project)

What it does:
    Paste a link and the tool gives it a risk score from 0 to 100.
    It lists the red flags (bad signs) and green flags (good signs).

Safety:
    This tool only reads the TEXT of the link.
    It never opens the link, so it is safe to test with fake links.

Ethical use only. Educational project.
"""

from urllib.parse import urlparse
import re

SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "cutt.ly", "rb.gy"}

SUSPICIOUS_WORDS = [
    "login", "verify", "update", "secure", "account", "urgent",
    "suspended", "confirm", "bank", "password", "free", "winner", "claim",
]

TRUSTED_BRANDS = [
    "paypal", "google", "facebook", "instagram", "amazon",
    "microsoft", "apple", "netflix", "gtbank", "opay",
]

SUSPICIOUS_ENDINGS = (".xyz", ".top", ".click", ".tk", ".gq", ".ml")

LOOKALIKE_SWAPS = str.maketrans({"0": "o", "1": "l", "3": "e", "4": "a", "5": "s"})

LEVEL_INFO = {
    "DANGEROUS": ("🔴", "Very likely a scam. Do NOT click it and do NOT enter any details."),
    "SUSPICIOUS": ("🟡", "Something looks off. Don't click unless you can confirm the sender another way."),
    "LOW RISK": ("🟢", "No major red flags found, but this is not a guarantee. Stay careful."),
}


def normalize_url(url):
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def get_domain(url):
    parsed = urlparse(normalize_url(url))
    return parsed.hostname or ""


def is_shortener(domain):
    return domain in SHORTENERS


def uses_ip_address(domain):
    return re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", domain) is not None


def uses_https(url):
    return url.strip().lower().startswith("https://")


def has_suspicious_ending(domain):
    return domain.endswith(SUSPICIOUS_ENDINGS)


def has_at_symbol(url):
    return "@" in url


def has_too_many_dots(domain):
    return domain.count(".") >= 3


def clean_lookalikes(text):
    return text.translate(LOOKALIKE_SWAPS)


def find_fake_brand(domain):
    cleaned = clean_lookalikes(domain)
    for brand in TRUSTED_BRANDS:
        if brand in cleaned:
            is_real = domain == f"{brand}.com" or domain.endswith(f".{brand}.com")
            if not is_real:
                return brand
    return None


def find_suspicious_words(url):
    lowered = url.lower()
    return [word for word in SUSPICIOUS_WORDS if word in lowered]


def get_level(score):
    if score >= 50:
        return "DANGEROUS"
    if score >= 25:
        return "SUSPICIOUS"
    return "LOW RISK"


def make_bar(score):
    filled = score // 10
    return "█" * filled + "░" * (10 - filled)


def analyze_url(url):
    domain = get_domain(url)
    red_flags = []
    green_flags = []

    if is_shortener(domain):
        red_flags.append(("Shortened link hides the real destination", 25))
    else:
        green_flags.append("Link is not shortened")

    if uses_ip_address(domain):
        red_flags.append(("Uses a raw IP address instead of a name", 30))
    else:
        green_flags.append("Uses a normal website name")

    if uses_https(url):
        green_flags.append("Uses HTTPS (encrypted connection)")
    else:
        red_flags.append(("Not using HTTPS", 10))

    if has_suspicious_ending(domain):
        red_flags.append(("Cheap domain ending often used by scammers", 15))
    else:
        green_flags.append("Normal domain ending")

    if has_at_symbol(url):
        red_flags.append(("Contains @, which can hide the real site", 25))
    else:
        green_flags.append("No hidden @ trick")

    if has_too_many_dots(domain):
        red_flags.append(("Too many dots in the domain", 15))

    brand = find_fake_brand(domain)
    if brand:
        red_flags.append((f"Pretending to be {brand}", 50))
    else:
        green_flags.append("No brand impersonation found")

    words = find_suspicious_words(url)
    if words:
        points = min(len(words) * 5, 20)
        red_flags.append(("Scam words: " + ", ".join(words), points))
    else:
        green_flags.append("No scam words found")

    score = min(sum(points for _, points in red_flags), 100)

    return {
        "url": url,
        "domain": domain,
        "score": score,
        "level": get_level(score),
        "red_flags": red_flags,
        "green_flags": green_flags,
    }


def show_result(result):
    emoji, meaning = LEVEL_INFO[result["level"]]

    print()
    print("=" * 50)
    print("🔗 Link  :", result["url"])
    print("🌐 Domain:", result["domain"])
    print("=" * 50)
    print(f"{emoji} RISK SCORE: {result['score']}/100 - {result['level']}")
    print(f"   [{make_bar(result['score'])}]")
    print("   Scale: 0-24 🟢 low | 25-49 🟡 suspicious | 50+ 🔴 dangerous")
    print(f"   {meaning}")
    print()

    if result["red_flags"]:
        print("🚩 RED FLAGS (why it is risky):")
        for text, points in result["red_flags"]:
            print(f"   🚩 {text} (+{points} points)")
    else:
        print("🚩 RED FLAGS: none found")
    print()

    if result["green_flags"]:
        print("🟢 GREEN FLAGS (good signs):")
        for text in result["green_flags"]:
            print(f"   ✅ {text}")
    print()


def ask_to_continue():
    while True:
        answer = input("🔁 Check another link? (yes/no): ").strip().lower()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n", "quit", "exit", "q"):
            return False
        print("Please type yes or no.")


def main():
    print("🎣 PHISHING LINK ANALYZER")
    print("Paste a link to check it.")
    print("Type 'quit', 'exit' or 'q' any time to leave.")
    print("This tool only reads the text. It never opens the link.\n")

    while True:
        url = input("🔗 Paste a link (or type 'quit' to exit): ").strip()

        if url.lower() in ("quit", "exit", "q"):
            print("Stay safe out there! 🛡️")
            break

        if not url:
            print("Please paste a link.\n")
            continue

        show_result(analyze_url(url))

        if not ask_to_continue():
            print("Stay safe out there! 🛡️")
            break


if __name__ == "__main__":
    main()