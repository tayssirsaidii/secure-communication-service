from typing import List
import filetype
from typing import Tuple
# Define unauthorized extensions and phrases
BLOCKED_EXTENSIONS = {".exe", ".bat", ".sh", ".js", ".dll"}
BLACKLISTED_PHRASES = {
    "malware", "unauthorized", "hack", "attack", "stupid", "backdoor",
    "virus", "exploit", "phishing", "trojan", "ddos", "ransomware",
    "scam", "spam", "abuse", "terrorist", "bomb", "kill", "hate",
    "racist", "sexist", "porn", "nsfw", "drugs", "alcohol",
    "gambling", "fraud", "piracy", "illegal", "banned", "threat",
    "weapon", "gun", "child abuse", "extremist", "offensive",
    "violence", "pedophilia", "kidnapping"
}

def is_extension_blocked(filename: str) -> bool:
    ext = filename.lower().split('.')[-1]
    return f".{ext}" in BLOCKED_EXTENSIONS

def contains_blacklisted_content(content: bytes) -> bool:
    try:
        # Attempt to decode as text
        text = content.decode('utf-8', errors='ignore').lower()
        return any(bad in text for bad in BLACKLISTED_PHRASES)
    except Exception:
        return False  # Binary files assumed safe unless blocked by extension

def is_content_authorized(filename: str, content: bytes) -> Tuple[bool, str]:
    if is_extension_blocked(filename):
        return False, "File extension is blocked"
    if contains_blacklisted_content(content):
        return False, "The content you are trying to send is unauthorized"
    return True, ""
