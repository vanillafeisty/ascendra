"""
Ascendra — Content Engine (Groq Edition)
Generates LinkedIn posts and content calendars using Groq (free).
"""

import json
import random
from datetime import datetime, timedelta
from typing import Optional

from config import GROQ_API_KEY, load_content_calendar, save_content_calendar


TRENDING_TOPICS = {
    "ai_ml": [
        "How I built my first RAG application using free APIs",
        "Why every developer should learn prompt engineering in 2025",
        "From zero to deployed: My first AI-powered web app in 48 hours",
        "Vibe coding with AI tools — what changed in my dev workflow",
        "5 things I learned shipping a production LLM app",
    ],
    "web_dev": [
        "React vs Next.js — when should you pick which? My honest take",
        "I refactored my messy useState code to Zustand — here's what changed",
        "TailwindCSS just made this layout in 3 lines that took me 30 before",
        "Why TypeScript saved me 4 hours of debugging this week",
        "Web performance wins: 5 small changes that halved my load time",
    ],
    "career": [
        "How I got my first developer role without a CS degree (my exact path)",
        "The cold LinkedIn message that actually got me a response — template inside",
        "3 resume mistakes I see in 90% of fresher resumes (and how to fix them)",
        "I applied to 50 jobs in 2 weeks. Here's what actually worked.",
        "Your GitHub profile is your resume — here's how I optimized mine",
    ],
    "learning": [
        "Free resource that taught me system design better than any paid course",
        "I finished CS50 in 6 weeks while working — here's how",
        "DSA doesn't have to be scary — the exact order I studied it",
        "Weekend project: I built a full-stack app and deployed it for free",
        "The one free certification that changed how recruiters saw my profile",
    ],
    "tools": [
        "My entire dev setup in 2025 (free tools only)",
        "Docker in 10 minutes — the only tutorial you actually need",
        "How I use Notion to track my job search (template included)",
        "Git best practices that junior developers rarely know",
        "VS Code extensions that made me 2x faster this month",
    ]
}

ENGAGEMENT_HOOKS = [
    "Nobody talks about this, but —",
    "I made a mistake that cost me 3 months. Learn from it:",
    "Honest take:",
    "Stop scrolling. This took me too long to figure out:",
    "I wish someone had told me this when I started:",
    "Small thing. Big difference:",
    "6 months ago I didn't know this. Today it got me noticed by a recruiter:",
]

HASHTAG_SETS = {
    "frontend":  ["#WebDevelopment", "#React", "#JavaScript", "#Frontend", "#CSS", "#100DaysOfCode"],
    "backend":   ["#BackendDevelopment", "#Python", "#NodeJS", "#API", "#DatabaseDesign", "#100DaysOfCode"],
    "career":    ["#CareerGrowth", "#TechJobs", "#JobSearch", "#Resume", "#LinkedIn", "#TechCareers"],
    "ai":        ["#AI", "#MachineLearning", "#GenAI", "#LLM", "#Coding", "#TechTrends"],
    "learning":  ["#Learning", "#100DaysOfCode", "#OpenToWork", "#CodingJourney", "#DevLife"],
    "general":   ["#SoftwareEngineering", "#Programming", "#TechCommunity", "#Developer", "#BuildInPublic"]
}


def _get_groq_client():
    from groq import Groq
    return Groq(api_key=GROQ_API_KEY)


def _get_hashtags_for_domain(domain: str) -> list:
    d = domain.lower()
    for key, tags in HASHTAG_SETS.items():
        if key in d:
            return tags
    return HASHTAG_SETS["general"]


def generate_post(topic: str, user_context: Optional[str] = None, domain: str = "general") -> dict:
    """Generate an engaging LinkedIn post using Groq (free)."""
    if not GROQ_API_KEY:
        return _generate_template_post(topic, domain)

    try:
        client = _get_groq_client()

        system = """You are a LinkedIn content expert who writes viral, authentic posts for developers and tech professionals.

Write a LinkedIn post that:
1. Opens with a HOOK (1-2 lines that stop the scroll)
2. Shares a genuine insight or value (3-5 short paragraphs or bullets)
3. Ends with a CTA (question or invitation to comment)
4. Is 150–300 words — focused and punchy
5. Feels personal and authentic, NOT corporate

DO NOT use: "In today's fast-paced world", hollow buzzwords, excessive emojis.
Return ONLY the post text, no labels."""

        user_msg = f"Write a LinkedIn post about: {topic}"
        if user_context:
            user_msg += f"\n\nAuthor context: {user_context}"

        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user_msg}],
            max_tokens=600,
            temperature=0.75,
        )
        content = resp.choices[0].message.content
        hashtags = _get_hashtags_for_domain(domain)
        return {
            "success": True, "content": content, "hashtags": hashtags,
            "full_post": content + "\n\n" + " ".join(hashtags),
            "character_count": len(content), "topic": topic
        }
    except Exception:
        return _generate_template_post(topic, domain)


def _generate_template_post(topic: str, domain: str = "general") -> dict:
    """Template fallback when Groq is unavailable."""
    hook = random.choice(ENGAGEMENT_HOOKS)
    first_word = topic.split()[0] if topic else "this"
    post = f"""{hook}

{topic}

Here's what I've learned:

→ Start with the fundamentals before jumping to frameworks
→ Build in public — your journey inspires others AND attracts opportunities
→ Consistency > intensity. 30 min/day beats 8hr Sundays.

If you're on a similar path, drop a 🙋 below — let's connect and grow together.

What's YOUR biggest challenge with {first_word}? Reply below 👇"""

    hashtags = _get_hashtags_for_domain(domain)
    return {
        "success": True, "content": post, "hashtags": hashtags,
        "full_post": post + "\n\n" + " ".join(hashtags),
        "character_count": len(post), "topic": topic
    }


def generate_weekly_content_calendar(domain: str = "general", weeks: int = 4) -> dict:
    """Generate a weeks-long LinkedIn content calendar."""
    calendar = {"posts": []}
    topics_pool = [t for tl in TRENDING_TOPICS.values() for t in tl]
    random.shuffle(topics_pool)

    start_date = datetime.now()
    post_days = [1, 3, 5]  # Tue, Thu, Sat
    post_index = 0

    for week in range(weeks):
        for day_offset in post_days:
            if post_index >= len(topics_pool):
                break
            days_ahead = day_offset - start_date.weekday()
            if days_ahead < 0:
                days_ahead += 7
            post_date = start_date + timedelta(weeks=week, days=days_ahead)
            topic = topics_pool[post_index]
            result = generate_post(topic=topic, domain=domain)
            calendar["posts"].append({
                "scheduled_date": post_date.strftime("%Y-%m-%d"),
                "day": post_date.strftime("%A"),
                "topic": topic,
                "content": result.get("content", ""),
                "hashtags": result.get("hashtags", []),
                "status": "draft",
                "post_id": None
            })
            post_index += 1

    save_content_calendar(calendar)
    return {
        "success": True,
        "total_posts": len(calendar["posts"]),
        "weeks_covered": weeks,
        "calendar": calendar["posts"],
        "message": f"Generated {len(calendar['posts'])} posts for {weeks} weeks."
    }


def get_trending_topics(domain: str = "general") -> dict:
    """Return trending tech topics to post about."""
    d = domain.lower()
    topics = {}
    for key, vals in TRENDING_TOPICS.items():
        if d in ("all", "general") or key in d or d in key:
            topics[key] = vals
    if not topics:
        topics = TRENDING_TOPICS
    all_flat = [t for tl in topics.values() for t in tl]
    return {
        "domain": domain,
        "topic_categories": topics,
        "quick_picks": random.sample(all_flat, min(5, len(all_flat))),
        "tip": "Pick a topic and ask Ascendra to generate a post."
    }


def generate_image_post_caption(image_context: str, domain: str = "general") -> dict:
    """Generate a LinkedIn caption for an image."""
    if GROQ_API_KEY:
        try:
            client = _get_groq_client()
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Write viral LinkedIn captions for tech professionals. Authentic, specific, 100-200 words, end with a CTA. No generic intros."},
                    {"role": "user", "content": f"Write a LinkedIn caption for: {image_context}"}
                ],
                max_tokens=350,
                temperature=0.7,
            )
            caption = resp.choices[0].message.content
        except Exception:
            caption = f"Sharing something I've been working on: {image_context}\n\nThis journey has been full of learnings — would love to hear your thoughts! 💬"
    else:
        caption = f"Sharing something I've been working on: {image_context}\n\nThis journey has been full of learnings — would love to hear your thoughts! 💬"

    hashtags = _get_hashtags_for_domain(domain)
    return {
        "success": True,
        "caption": caption,
        "hashtags": hashtags,
        "full_caption": caption + "\n\n" + " ".join(hashtags)
    }
