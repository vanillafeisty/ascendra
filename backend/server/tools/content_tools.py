"""
CareerPilot AI - Content Engine
Generates and publishes LinkedIn posts. Creates weekly content calendars.
"""

import json
import random
from datetime import datetime, timedelta
from typing import Optional

from config import ANTHROPIC_API_KEY, load_content_calendar, save_content_calendar


# ─── Trending Tech Topics (Updated periodically) ──────────────────────────────
TRENDING_TOPICS = {
    "ai_ml": [
        "How I built my first RAG application using LangChain and free APIs",
        "5 things I learned building with Claude API this week",
        "Why every developer should learn prompt engineering in 2025",
        "From zero to deployed: My first AI-powered web app in 48 hours",
        "Vibe coding with Cursor AI — what changed in my workflow",
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
        "The one freeCodeCamp certification that changed how recruiters saw me",
    ],
    "tools": [
        "My entire dev setup in 2025 (free tools only)",
        "I switched from VS Code to Cursor — here's my honest review after 1 month",
        "Docker in 10 minutes — the only tutorial you actually need",
        "How I use Notion to track my job search (template included)",
        "Git best practices that junior developers rarely know",
    ]
}

ENGAGEMENT_HOOKS = [
    "Nobody talks about this, but —",
    "I made a mistake that cost me 3 months. Learn from it:",
    "Honest take:",
    "This might be controversial, but —",
    "6 months ago I didn't know this. Today it got me noticed by a recruiter:",
    "Stop scrolling. This took me too long to figure out:",
    "I wish someone had told me this when I started:",
    "Small thing. Big difference:",
]

HASHTAG_SETS = {
    "frontend": ["#WebDevelopment", "#React", "#JavaScript", "#Frontend", "#CSS", "#100DaysOfCode"],
    "backend": ["#BackendDevelopment", "#Python", "#NodeJS", "#API", "#DatabaseDesign", "#100DaysOfCode"],
    "career": ["#CareerGrowth", "#TechJobs", "#JobSearch", "#Resume", "#LinkedIn", "#TechCareers"],
    "ai": ["#AI", "#MachineLearning", "#GenAI", "#LLM", "#Coding", "#TechTrends"],
    "learning": ["#Learning", "#100DaysOfCode", "#OpenToWork", "#CodingJourney", "#DevLife"],
    "general": ["#SoftwareEngineering", "#Programming", "#TechCommunity", "#Developer", "#BuildInPublic"]
}


# ─────────────────────────────────────────────────────────────────────────────
# POST GENERATORS
# ─────────────────────────────────────────────────────────────────────────────

def generate_post(topic: str, user_context: Optional[str] = None, domain: str = "general") -> dict:
    """
    Generate an engaging LinkedIn post on a given topic.
    Uses Claude API for generation.
    """
    if not ANTHROPIC_API_KEY:
        # Fallback: template-based generation
        return _generate_template_post(topic, domain)

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        system_prompt = """You are a LinkedIn content expert who writes viral, authentic posts for developers and tech professionals.

Write a LinkedIn post that:
1. Opens with a HOOK (1-2 lines that make people stop scrolling)
2. Shares a genuine insight, lesson, or value (3-5 short paragraphs or bullets)
3. Ends with a strong CTA (question, call to share, or invitation to comment)
4. Is 150–300 words — not too long, not too short
5. Feels personal and authentic, NOT corporate or generic
6. Uses occasional line breaks for readability

DO NOT use: generic phrases like "In today's fast-paced world", hollow buzzwords, excessive emojis.
DO use: specific examples, numbers, personal experiences, direct language.

Return ONLY the post text, no labels or explanations."""

        user_msg = f"Write a LinkedIn post about: {topic}"
        if user_context:
            user_msg += f"\n\nContext about the author: {user_context}"

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            system=system_prompt,
            messages=[{"role": "user", "content": user_msg}]
        )

        post_content = message.content[0].text

        # Select hashtags
        hashtags = _get_hashtags_for_domain(domain)

        return {
            "success": True,
            "content": post_content,
            "hashtags": hashtags,
            "full_post": post_content + "\n\n" + " ".join(hashtags),
            "character_count": len(post_content),
            "topic": topic
        }

    except Exception as e:
        return _generate_template_post(topic, domain)


def _generate_template_post(topic: str, domain: str = "general") -> dict:
    """Fallback template-based post generation (no API needed)."""
    hook = random.choice(ENGAGEMENT_HOOKS)

    # Pick a relevant trending topic if the input is vague
    all_topics = []
    for t_list in TRENDING_TOPICS.values():
        all_topics.extend(t_list)

    suggested_topics = [t for t in all_topics if any(word in t.lower() for word in topic.lower().split())]
    if not suggested_topics:
        suggested_topics = random.sample(TRENDING_TOPICS.get("career", []), 2)

    post = f"""{hook}

{topic}

Here's what I've learned from working on this:

→ Start with the fundamentals before jumping to frameworks
→ Build in public — your journey inspires others AND attracts opportunities  
→ Consistency > intensity. 30 min/day beats 8hr Sundays.

If you're on a similar path, drop a 🙋 below — let's connect and grow together.

What's YOUR biggest challenge with {topic.split()[0] if topic else 'this'}? Reply below 👇"""

    hashtags = _get_hashtags_for_domain(domain)

    return {
        "success": True,
        "content": post,
        "hashtags": hashtags,
        "full_post": post + "\n\n" + " ".join(hashtags),
        "character_count": len(post),
        "topic": topic,
        "note": "Generated from template (set ANTHROPIC_API_KEY for AI-generated posts)"
    }


def _get_hashtags_for_domain(domain: str) -> list[str]:
    """Return relevant hashtags for a domain."""
    domain_lower = domain.lower()
    for key, tags in HASHTAG_SETS.items():
        if key in domain_lower:
            return tags
    return HASHTAG_SETS["general"]


def generate_weekly_content_calendar(domain: str = "general", weeks: int = 4) -> dict:
    """
    Generate a 4-week LinkedIn content calendar.
    Returns scheduled posts with topics, content, and hashtags.
    """
    calendar = {"posts": []}
    topics_pool = []

    for t_list in TRENDING_TOPICS.values():
        topics_pool.extend(t_list)
    random.shuffle(topics_pool)

    start_date = datetime.now()
    # Post on Tue, Thu, Sat (high engagement days)
    post_days = [1, 3, 5]  # Mon=0, Tue=1, ...

    post_index = 0
    for week in range(weeks):
        for day_offset in post_days:
            if post_index >= len(topics_pool):
                break

            # Find next occurrence of the day
            days_ahead = day_offset - start_date.weekday()
            if days_ahead < 0:
                days_ahead += 7
            post_date = start_date + timedelta(weeks=week, days=days_ahead)

            topic = topics_pool[post_index]
            post_result = generate_post(topic=topic, domain=domain)

            calendar["posts"].append({
                "scheduled_date": post_date.strftime("%Y-%m-%d"),
                "day": post_date.strftime("%A"),
                "topic": topic,
                "content": post_result.get("content", ""),
                "hashtags": post_result.get("hashtags", []),
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
        "message": f"Generated {len(calendar['posts'])} posts for the next {weeks} weeks. Review and publish when ready.",
        "tip": "Run linkedin_create_text_post with each post's content to publish them directly."
    }


def get_trending_topics(domain: str = "general") -> dict:
    """Return trending tech topics to post about."""
    all_topics = {}
    domain_lower = domain.lower()

    for key, topics in TRENDING_TOPICS.items():
        if domain_lower == "all" or domain_lower == "general" or key in domain_lower or domain_lower in key:
            all_topics[key] = topics

    if not all_topics:
        all_topics = TRENDING_TOPICS

    return {
        "domain": domain,
        "topic_categories": all_topics,
        "quick_picks": random.sample([t for tl in all_topics.values() for t in tl], min(5, sum(len(tl) for tl in all_topics.values()))),
        "tip": "Pick a topic and run generate_post to create your LinkedIn content instantly."
    }


def generate_image_post_caption(image_context: str, domain: str = "general") -> dict:
    """
    Generate a LinkedIn caption for an image the user wants to post.
    image_context: user's description of what the image shows.
    """
    if ANTHROPIC_API_KEY:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=400,
                system="You write viral LinkedIn captions for tech professional posts. Be authentic, specific, and end with a CTA or question. 100-200 words. No generic intros.",
                messages=[{"role": "user", "content": f"Write a LinkedIn caption for this image/content: {image_context}"}]
            )
            caption = message.content[0].text
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
