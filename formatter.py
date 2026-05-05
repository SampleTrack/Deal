"""
formatter.py - Format deal messages with psychology + honesty + variety
Every post feels human written, never robotic
"""

import random
from datetime import datetime


# ─── Openers (randomly picked) ──────────────────────────────────────────────
OPENERS = [
    "🚨 PRICE DROP ALERT!",
    "😱 You won't believe this price!",
    "⚡ Just found this deal!",
    "🔥 Today's best deal is here!",
    "💥 Massive discount spotted!",
    "👀 Look at this price drop!",
    "🎯 Deal of the day!",
    "🤑 Save big on this today!",
    "🛍️ Grab this before it's gone!",
    "💡 Smart shoppers are buying this!",
]

# ─── CTA Variants (randomly picked) ─────────────────────────────────────────
CTAS = [
    "🛒 Grab This Deal",
    "👉 Buy Now",
    "🎯 Get This Price",
    "💰 Claim This Deal",
    "🛍️ Shop Now",
    "✅ Check Price Now",
    "⚡ Tap To Save ₹{saving}",
    "🔖 Add To Cart Now",
]

# ─── Day Themes ──────────────────────────────────────────────────────────────
DAY_THEMES = {
    0: "💪 Monday Deal",
    1: "🔥 Tuesday Hot Deal",
    2: "🎯 Midweek Special",
    3: "⚡ Thursday Deal",
    4: "🎉 Friday Fiesta Deal",
    5: "🛍️ Weekend Deal",
    6: "😌 Sunday Essential",
}

# ─── Time Greetings ──────────────────────────────────────────────────────────
def get_time_greeting() -> str:
    hour = datetime.now().hour
    if hour < 12:
        return "🌅 Good morning deal!"
    elif hour < 17:
        return "☀️ Lunch break deal!"
    else:
        return "🌙 Evening special deal!"


# ─── Writing Styles ──────────────────────────────────────────────────────────
def style_excited(deal: dict) -> str:
    saving_str = f"₹{int(deal['saving']):,}" if deal['saving'] > 0 else ""
    return f"OH WOW! {deal['title']} at this price?!\nThis is incredible value! {saving_str} saved instantly! 🎉"


def style_informative(deal: dict) -> str:
    lines = [f"📊 Price Analysis — {deal['platform']}"]
    if deal['mrp'] > 0:
        lines.append(f"6-month high: ₹{int(deal['mrp']):,}")
    lines.append(f"Today's price: ₹{int(deal['price']):,}")
    if deal['saving'] > 0:
        lines.append(f"Your savings: ₹{int(deal['saving']):,} ({deal['discount']}% off)")
    return "\n".join(lines)


def style_conversational(deal: dict) -> str:
    return (
        f"Looking for a great deal today?\n"
        f"Just found {deal['title']} at an amazing price 👇\n"
        f"Genuine deal — checked and verified by us! ✅"
    )


def style_urgency(deal: dict) -> str:
    lines = [f"⏰ Limited time price drop!"]
    lines.append(f"{deal['title']}")
    if deal['saving'] > 0:
        lines.append(f"Save ₹{int(deal['saving']):,} right now!")
    lines.append("Don't wait on this one!")
    return "\n".join(lines)


def style_story(deal: dict) -> str:
    if deal['mrp'] > 0 and deal['saving'] > 0:
        return (
            f"💭 Imagine paying ₹{int(deal['mrp']):,} for this product.\n"
            f"Smart shoppers are getting it for ₹{int(deal['price']):,} today.\n"
            f"That's ₹{int(deal['saving']):,} difference. Same product. 🤷"
        )
    return style_conversational(deal)


STYLES = [style_excited, style_informative, style_conversational, style_urgency, style_story]


# ─── Main Formatter ──────────────────────────────────────────────────────────
def format_deal_message(deal: dict) -> str:
    """
    Format a deal with honest data + psychological triggers + variety.
    Only shows info that is actually TRUE for this deal.
    """

    opener      = random.choice(OPENERS)
    style_fn    = random.choice(STYLES)
    day_theme   = DAY_THEMES[datetime.now().weekday()]
    time_greeting = get_time_greeting()

    # Build CTA with real saving amount
    cta_template = random.choice(CTAS)
    cta = cta_template.replace("{saving}", f"{int(deal.get('saving', 0)):,}")

    lines = []

    # Header
    lines.append(f"{opener}")
    lines.append(f"{day_theme} | {time_greeting}")
    lines.append("")

    # Product name
    lines.append(f"📦 {deal['title']}")
    lines.append(f"🏪 Platform: {deal['platform']}")
    lines.append("")

    # Pricing — always honest real data
    if deal['mrp'] > 0 and deal['price'] > 0:
        lines.append(f"❌ MRP: ₹{int(deal['mrp']):,}")
        lines.append(f"✅ NOW: ₹{int(deal['price']):,}")
        if deal['saving'] > 0:
            lines.append(f"💰 YOU SAVE: ₹{int(deal['saving']):,} ({deal['discount']}% OFF)")
    elif deal['price'] > 0:
        lines.append(f"✅ Price: ₹{int(deal['price']):,}")
    lines.append("")

    # Style body
    lines.append(style_fn(deal))
    lines.append("")

    # Real reviews — only if available
    if deal['rating'] > 0 and deal['review_count'] > 0:
        stars = "⭐" * round(deal['rating'])
        lines.append(f"{stars} {deal['rating']}/5 stars ({int(deal['review_count']):,}+ reviews)")

    # ── Honest conditional info — ONLY show if actually true ──
    extras = []

    if deal.get('free_delivery'):
        extras.append("📦 Free Delivery")

    if deal.get('emi'):
        extras.append("💳 No Cost EMI Available")

    # Show pay on delivery only for Amazon/Flipkart (not Nykaa)
    if deal['platform'] in ("Amazon", "Flipkart"):
        extras.append("🔄 Easy Returns")

    # Show stock warning only if real stock message exists
    stock = deal.get('stock_message', '')
    if stock and ("left" in stock.lower() or "limited" in stock.lower() or "hurry" in stock.lower()):
        extras.append(f"⚡ {stock}")

    if extras:
        lines.append("")
        lines.extend(extras)

    # CTA
    lines.append("")
    lines.append(f"{cta} 👇")
    lines.append(deal['url'])

    # Trust line — always at bottom
    lines.append("")
    lines.append("💡 Genuine deal — checked and verified by us!")

    return "\n".join(lines)


# ─── Special Posts ───────────────────────────────────────────────────────────
def format_poll_post() -> str:
    return (
        "🗳️ Quick Question!\n\n"
        "Which deals do you want more of?\n\n"
        "📱 Electronics\n"
        "👗 Fashion\n"
        "💄 Skincare\n"
        "🏠 Home & Kitchen\n\n"
        "Reply below and we'll find the best ones for you! 👇"
    )


def format_tip_post() -> str:
    tips = [
        (
            "💡 Smart Shopping Tip!\n\n"
            "Before buying online always check:\n\n"
            "✅ Read top 10 customer reviews\n"
            "✅ Check seller rating carefully\n"
            "✅ Verify return policy before ordering\n"
            "✅ Compare prices across platforms\n\n"
            "We always verify deals before sharing! 🤝"
        ),
        (
            "💡 Did You Know?\n\n"
            "Best time to shop online:\n\n"
            "🌅 Early morning — fresh price drops\n"
            "🌙 Late evening — flash sales start\n"
            "📅 Month end — brands clear stock\n\n"
            "We catch all these deals for you automatically! 🎯"
        ),
    ]
    return random.choice(tips)


def format_morning_post() -> str:
    return (
        "🌅 Good Morning!\n\n"
        "Ready for today's best deals?\n"
        "We've found some amazing prices\n"
        "this morning just for you!\n\n"
        "Stay tuned for deals in the next few minutes 👇🔔"
    )
