import re
import logging
import urllib.request
import ssl
from typing import List, Optional, Dict, Tuple
from urllib.parse import urlparse
from app.models.schemas import UrlCheckSchema

logger = logging.getLogger(__name__)

# Known Official Domain Suffixes & Reliable Institutional Domains
OFFICIAL_SUFFIXES = (
    ".gov.in", ".nic.in", ".gov", ".edu.in", ".ac.in", ".edu", ".org.in", ".mil", ".gov.uk", ".gov.au"
)

VERIFIED_INSTITUTIONAL_DOMAINS = {
    "who.int", "isro.gov.in", "rbi.org.in", "pib.gov.in", "india.gov.in", "ncs.gov.in",
    "thehindu.com", "bbc.com", "reuters.com", "ndtv.com", "indianexpress.com",
    "altnews.in", "boomlive.in", "factly.in", "vanguard.org", "wikipedia.org", "w3.org",
    "vercel.app", "onrender.com", "render.com", "netlify.app", "github.io",
    "whatsapp.com", "instagram.com", "facebook.com", "twitter.com", "x.com", "linkedin.com", "telegram.org", "youtube.com"
}

KNOWN_SHORTENERS = {
    "bit.ly", "tinyurl.com", "goo.gl", "ow.ly", "is.gd", "buff.ly", "t.co", "t.me"
}

SUSPICIOUS_TLDS = {
    ".xyz", ".top", ".club", ".site", ".online", ".work", ".click", ".link", ".tech", ".download", ".vip", ".monster", ".buzz"
}

COMMON_TWO_PART_TLDS = {
    "co.in", "gov.in", "ac.in", "edu.in", "nic.in", "org.in", "net.in", "gen.in",
    "co.uk", "org.uk", "gov.uk", "ac.uk", "com.au", "net.au", "edu.au", "co.jp", "ne.jp"
}

STANDARD_SUBDOMAINS = {
    "www", "web", "chat", "my", "link", "go", "connect", "in", "uk", "us", "de", "fr", "ca", "au", "jp", "kr", "cn", "en", "eu", "ap",
    "shop", "store", "portal", "app", "m", "mobile", "account", "support", "help",
    "auth", "login", "api", "cdn", "mail", "dev", "docs", "learn", "blog", "news", "lifestyle"
}

# Comprehensive URL Regex Pattern preserving complete URLs intact (supports query params, ports, subdomains, paths, malformed prefixes)
URL_REGEX_PATTERN = r"(?:https?://https?://|https?://|www\.)[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(?::\d+)?(?:/[^\s]*)?"


# In-memory cache for live domain verification results
_LIVE_CHECK_CACHE: Dict[str, Tuple[bool, bool, int, str]] = {}

def extract_domain_parts(hostname: str) -> Tuple[str, str, str]:
    """
    Parses a hostname into (subdomain, root_registered_domain, tld_suffix).
    """
    host = hostname.lower().strip()
    if ":" in host:
        host = host.split(":")[0]

    parts = host.split(".")
    if len(parts) < 2:
        return "", host, ""

    # Check 2-part TLDs (e.g. co.in)
    two_part = ".".join(parts[-2:])
    if two_part in COMMON_TWO_PART_TLDS:
        if len(parts) >= 3:
            root_domain = ".".join(parts[-3:])
            subdomain = ".".join(parts[:-3])
            return subdomain, root_domain, two_part
        else:
            return "", host, two_part

    # 1-part TLD (e.g. com, in, org, gov, edu)
    tld = parts[-1]
    root_domain = ".".join(parts[-2:])
    subdomain = ".".join(parts[:-2])
    return subdomain, root_domain, tld

def check_domain_live_status(url: str, hostname: str, timeout: float = 2.5) -> Tuple[bool, bool, int, str]:
    """
    Checks HTTP/HTTPS reachability, SSL enforcement, status code, and site title.
    Returns: (is_reachable, is_https, status_code, site_title)
    """
    cache_key = hostname.lower().strip()
    if cache_key in _LIVE_CHECK_CACHE:
        return _LIVE_CHECK_CACHE[cache_key]

    parsed = urlparse(url)
    scheme = parsed.scheme.lower() if parsed.scheme else "https"

    test_urls = []
    if scheme == "https":
        test_urls.append(f"https://{hostname}{parsed.path or '/'}")
        test_urls.append(f"http://{hostname}{parsed.path or '/'}")
    else:
        test_urls.append(f"http://{hostname}{parsed.path or '/'}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for test_url in test_urls:
        try:
            req = urllib.request.Request(test_url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                status_code = resp.status
                final_url = resp.geturl()
                is_https = final_url.startswith("https://") or test_url.startswith("https://")

                if status_code in (200, 301, 302, 307, 308):
                    content = resp.read(8192).decode('utf-8', errors='ignore')
                    title_m = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
                    site_title = title_m.group(1).strip() if title_m else ""
                    site_title = re.sub(r'<[^>]+>', '', site_title).strip()

                    res = (True, is_https, status_code, site_title)
                    _LIVE_CHECK_CACHE[cache_key] = res
                    return res
        except Exception as e:
            logger.debug(f"Live reachability check failed for {test_url}: {e}")
            continue

    res = (False, False, 0, "")
    _LIVE_CHECK_CACHE[cache_key] = res
    return res

def normalize_ocr_url(url_raw: str) -> str:
    """
    Fixes common OCR glitches in extracted URLs safely without altering domain destination.
    """
    cleaned = url_raw.strip().rstrip(".,!?)\"';:]}")
    cleaned = re.sub(r"^hxxps?", "http", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"https?\s*:\s*/\s*/", "https://", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+\.\s+", ".", cleaned)
    cleaned = re.sub(r"([a-zA-Z0-9])\s+(gov|in|com|org|net|edu)\b", r"\1.\2", cleaned, flags=re.IGNORECASE)

    if not cleaned.startswith(("http://", "https://")):
        cleaned = "https://" + cleaned

    return cleaned

def extract_urls(text: str) -> List[str]:
    """
    Extracts HTTP/HTTPS URLs and standalone domain strings from text or OCR.
    Preserves complete URL intact (never split at '.', '/', ':', '?', '&', '=').
    """
    if not text:
        return []

    matches = re.findall(URL_REGEX_PATTERN, text, flags=re.IGNORECASE)

    naked_pattern = r"\b[a-zA-Z0-9\-]+\.(?:xyz|top|site|click|online|link|club)(?:/[^\s]*)?"
    naked_matches = re.findall(naked_pattern, text, flags=re.IGNORECASE)

    all_raw = matches + naked_matches
    results = []

    for raw in all_raw:
        norm = normalize_ocr_url(raw)
        if norm and norm not in results:
            results.append(norm)

    return results

def strip_urls_from_text(text: str) -> Tuple[str, List[str]]:
    """
    Extracts all intact URLs from text and returns (text_without_urls, extracted_urls).
    Prevents URLs from ever being split into sentence fragments or factual claims.
    """
    if not text:
        return "", []

    extracted_urls = extract_urls(text)
    text_clean = text

    # Remove matches intact
    for u in re.findall(URL_REGEX_PATTERN, text, flags=re.IGNORECASE):
        text_clean = text_clean.replace(u, " ")

    # Clean up leftover whitespace/punctuation
    text_clean = re.sub(r"\s+", " ", text_clean).strip()
    return text_clean, extracted_urls

def analyze_url_safety(url: str, text: str = "", claim_topic: str = "") -> Optional[UrlCheckSchema]:
    """
    Generalized URL Verification Pipeline.

    Verification Order:
    1. Parse URL correctly & check malformed syntax.
    2. Extract registrable/root domain & subdomain.
    3. Check HTTPS scheme.
    4. Check for obvious impersonation/lookalike indicators.
    5. Check official government / public institutional domains.
    6. Check shortened URL service.
    7. Perform dynamic reachability, SSL enforcement, and identity consistency check.
    8. Determine final status:
       - TRUSTED (🟢 VERIFIED / TRUSTED DOMAIN)
       - UNVERIFIED (🟡 UNKNOWN / UNVERIFIED URL)
       - SUSPICIOUS (🔴 SUSPICIOUS / POTENTIALLY MALICIOUS URL)
       - INVALID (⚠️ INVALID URL)
    """
    if not url:
        return None

    try:
        # Step 1: Check raw string syntax for obvious double dots or double protocols
        url_parts = url.split("/")
        host_segment = url_parts[2] if len(url_parts) > 2 else url_parts[0]
        if ".." in host_segment or url.count("://") > 1 or url.startswith("http://https://") or url.startswith("https://http://"):
            return UrlCheckSchema(
                url=url,
                status="INVALID",
                status_label="⚠️ INVALID URL",
                reason="The URL contains malformed syntax, multiple protocols, or invalid domain formatting."
            )

        parsed = urlparse(url)
        hostname = (parsed.netloc or parsed.path.split("/")[0]).lower().strip()
        if ":" in hostname and not hostname.startswith("http"):
            hostname = hostname.split(":")[0]

        clean_text = (text or "").lower()

        # Malformed / Unparseable Check
        if not hostname or len(hostname.split(".")) < 2 or "http://" in hostname or "https://" in hostname:
            return UrlCheckSchema(
                url=url,
                status="INVALID",
                status_label="⚠️ INVALID URL",
                reason="The extracted link contains malformed syntax or unreadable URL structure."
            )

        # Step 2: Extract Subdomain & Registrable Root Domain
        subdomain, root_domain, tld = extract_domain_parts(hostname)
        brand_token = root_domain.split(".")[0]  # e.g. 'programiz' from 'programiz.com', 'puma' from 'puma.com'

        # Step 3: Impersonation / Lookalike / Scam Indicators Check (SUSPICIOUS)
        has_suspicious_tld = any(hostname.endswith(stld) for stld in SUSPICIOUS_TLDS)
        scam_keywords = ["-gov-", "-scheme-", "-reward-", "-claim-", "-yojana-", "-scholarship-", "-discount-", "-free-", "-netbanking-", "-lottery-", "-cash-", "-gift-"]
        has_scam_hyphens = any(kw in root_domain for kw in scam_keywords)

        claims_government = any(kw in clean_text for kw in ["government", "pib", "ministry", "scheme", "rbi", "yojana", "ಸರ್ಕಾರ", "ಪ್ರಭುತ್ವ", "அரசு", "सरकार"])
        claims_bank = any(kw in clean_text for kw in ["bank", "sbi", "hdfc", "icici", "rbi", "account blocked"])

        if has_suspicious_tld or has_scam_hyphens:
            return UrlCheckSchema(
                url=url,
                status="SUSPICIOUS",
                status_label="🔴 SUSPICIOUS / POTENTIALLY MALICIOUS URL",
                reason=f"The domain '{root_domain}' uses a lookalike structure or high-risk extension associated with digital deception."
            )

        is_gov_or_edu = hostname.endswith(OFFICIAL_SUFFIXES) or any(inst in hostname for inst in VERIFIED_INSTITUTIONAL_DOMAINS)

        if (claims_government or claims_bank) and not is_gov_or_edu and any(kw in root_domain for kw in ["free", "reward", "claim"]):
            return UrlCheckSchema(
                url=url,
                status="SUSPICIOUS",
                status_label="🔴 SUSPICIOUS LINK MISMATCH",
                reason=f"The message claims an official government/banking notice, but points to an unverified commercial domain ('{root_domain}')."
            )

        # Step 4: Check Official Government / Public Institutional Suffixes & Domains
        if is_gov_or_edu:
            return UrlCheckSchema(
                url=url,
                status="TRUSTED",
                status_label="🟢 VERIFIED / TRUSTED DOMAIN",
                reason=f"The domain '{hostname}' is an established official or institutional domain."
            )

        # Step 5: Check Shortened URLs
        if any(shortener in hostname for shortener in KNOWN_SHORTENERS):
            return UrlCheckSchema(
                url=url,
                status="UNVERIFIED",
                status_label="🟡 UNVERIFIED SHORTENED LINK",
                reason=f"The link uses a URL shortener ('{hostname}'). The final destination cannot be confirmed without unshortening."
            )

        # Step 6: Subdomain & Clean Domain Check
        is_clean_root_domain = not ("-" in brand_token and any(k in brand_token for k in ["free", "cheap", "sale", "reward", "offer"]))
        is_standard_subdomain = not subdomain or subdomain in STANDARD_SUBDOMAINS or len(subdomain) == 2

        # Step 7: Dynamic Reachability, HTTPS Enforcement & Site Identity Verification
        is_reachable, live_https, status_code, site_title = check_domain_live_status(url, hostname)

        # Check for phishing / identity mismatch in site title
        if is_reachable and site_title:
            title_lower = site_title.lower()
            if any(term in title_lower for term in ["state bank of india", "reserve bank of india", "pib government portal", "official government yojana"]) and not is_gov_or_edu:
                return UrlCheckSchema(
                    url=url,
                    status="SUSPICIOUS",
                    status_label="🔴 SUSPICIOUS LINK MISMATCH",
                    reason=f"The website at '{hostname}' identifies itself as an official entity, which does not match its registered domain structure."
                )

        text_without_urls = re.sub(r'https?://[^\s]+', '', clean_text).strip()
        brand_mentioned_in_text = (len(brand_token) >= 3 and brand_token in text_without_urls)

        # General Legitimate Domain Verification
        if is_clean_root_domain and is_standard_subdomain:
            if (is_reachable and live_https) or brand_mentioned_in_text:
                sub_info = f" ({subdomain.upper()} subdomain)" if subdomain and subdomain != "www" else ""
                return UrlCheckSchema(
                    url=url,
                    status="TRUSTED",
                    status_label="🟢 VERIFIED / TRUSTED DOMAIN",
                    reason=f"The domain '{hostname}' is active, securely served over HTTPS, and verified as a legitimate website{sub_info}."
                )

        # Reachable via HTTP only (no HTTPS)
        if is_reachable and not live_https and is_clean_root_domain and is_standard_subdomain:
            return UrlCheckSchema(
                url=url,
                status="UNVERIFIED",
                status_label="🟡 UNKNOWN / UNVERIFIED URL",
                reason=f"The domain '{hostname}' is reachable, but does not enforce secure HTTPS connections."
            )

        # Unreachable or unconfirmed domain (Default Cautious Fallback)
        return UrlCheckSchema(
            url=url,
            status="UNVERIFIED",
            status_label="🟡 UNKNOWN / UNVERIFIED URL",
            reason=f"The domain '{hostname}' has a valid structure, but its official relationship or safety status could not be verified."
        )

    except Exception as e:
        logger.warning(f"URL safety analysis error for {url}: {e}")
        return UrlCheckSchema(
            url=url,
            status="UNVERIFIED",
            status_label="🟡 UNVERIFIED URL",
            reason="The URL could not be fully analyzed at this time."
        )

