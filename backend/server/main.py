#!/usr/bin/env python3
"""
CareerPilot AI — MCP Server
============================
An autonomous AI career growth engine that manages LinkedIn, email, 
resume building, networking, and career roadmaps — completely hands-free.

Usage:
    python main.py                    # stdio transport (for Claude Desktop)
    python main.py --transport sse    # SSE transport (for remote/HTTP)

Configure via .env:
    ANTHROPIC_API_KEY=...
    LINKEDIN_EMAIL=...
    LINKEDIN_PASSWORD=...
    SMTP_USER=...
    SMTP_PASS=...
    YOUTUBE_API_KEY=...
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Any

# Add server dir to path
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types

from config import validate_config, load_user_profile, save_user_profile

# ─── Import tool modules ──────────────────────────────────────────────────────
from tools.linkedin_tools import (
    get_my_profile, score_linkedin_profile, suggest_profile_photo_guidelines,
    search_people, send_connection_request, bulk_connect,
    send_message, bulk_message,
    create_text_post, create_image_post, update_headline
)
from tools.email_tools import (
    send_email, send_cold_email_to_hr, send_bulk_cold_emails,
    send_follow_up_email, get_email_log
)
from tools.resume_tools import (
    build_resume, tailor_resume_to_jd, score_resume_against_jd,
    analyze_resume, extract_jd_keywords
)
from tools.career_tools import (
    what_to_do_next, career_roadmap, find_target_companies,
    find_free_courses, get_must_do_certs
)
from tools.content_tools import (
    generate_post, generate_weekly_content_calendar,
    get_trending_topics, generate_image_post_caption
)

# ─── MCP Server Setup ─────────────────────────────────────────────────────────
server = Server("careerpilot-ai")


# ─────────────────────────────────────────────────────────────────────────────
# TOOL DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [

        # ── SETUP & CONFIG ───────────────────────────────────────────────────
        types.Tool(
            name="setup_profile",
            description="Set up or update your career profile (name, skills, experience, target role, etc.). Must be done before most other tools.",
            inputSchema={
                "type": "object",
                "properties": {
                    "profile": {
                        "type": "object",
                        "description": "User profile data (name, email, skills, experience, education, target_role, etc.)",
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                            "phone": {"type": "string"},
                            "location": {"type": "string"},
                            "target_role": {"type": "string"},
                            "skills": {"type": "array", "items": {"type": "string"}},
                            "summary": {"type": "string"},
                            "linkedin_url": {"type": "string"},
                            "github_url": {"type": "string"},
                            "portfolio_url": {"type": "string"}
                        }
                    }
                },
                "required": ["profile"]
            }
        ),

        types.Tool(
            name="check_config",
            description="Check which integrations are configured (LinkedIn, Gmail, etc.) and what's missing.",
            inputSchema={"type": "object", "properties": {}}
        ),

        # ── LINKEDIN PROFILE ─────────────────────────────────────────────────
        types.Tool(
            name="linkedin_get_profile",
            description="Read the authenticated user's current LinkedIn profile data.",
            inputSchema={"type": "object", "properties": {}}
        ),

        types.Tool(
            name="linkedin_score_profile",
            description="Score the user's LinkedIn profile out of 100 and get specific improvement suggestions.",
            inputSchema={"type": "object", "properties": {}}
        ),

        types.Tool(
            name="linkedin_update_headline",
            description="Automatically update the LinkedIn headline. The AI tailors it to the user's target role.",
            inputSchema={
                "type": "object",
                "properties": {
                    "headline": {"type": "string", "description": "The new headline (max 220 chars). E.g. 'React Developer | Building fast UIs | Open to SDE roles'"}
                },
                "required": ["headline"]
            }
        ),

        types.Tool(
            name="linkedin_suggest_photo_guidelines",
            description="Get AI-powered guidelines for the perfect LinkedIn profile photo.",
            inputSchema={"type": "object", "properties": {}}
        ),

        # ── LINKEDIN CONNECTIONS ─────────────────────────────────────────────
        types.Tool(
            name="linkedin_search_people",
            description="Search LinkedIn for HRs, hiring managers, or professionals by role, company, and location.",
            inputSchema={
                "type": "object",
                "properties": {
                    "role": {"type": "string", "description": "Job title or role to search (e.g. 'HR Manager', 'Hiring Manager', 'Frontend Developer')"},
                    "company": {"type": "string", "description": "Company name (optional)"},
                    "location": {"type": "string", "description": "Location filter (optional)"},
                    "limit": {"type": "integer", "description": "Max results (default 20)", "default": 20}
                },
                "required": ["role"]
            }
        ),

        types.Tool(
            name="linkedin_send_connection",
            description="Send a personalized connection request to a specific LinkedIn profile.",
            inputSchema={
                "type": "object",
                "properties": {
                    "profile_id": {"type": "string", "description": "LinkedIn public profile ID (from search results)"},
                    "note": {"type": "string", "description": "Personalized connection note (max 300 chars)"},
                    "person_name": {"type": "string", "description": "Person's name for logging"}
                },
                "required": ["profile_id"]
            }
        ),

        types.Tool(
            name="linkedin_bulk_connect",
            description="Search and automatically connect with N people matching your criteria (HRs, hiring managers, developers). AI writes the connection note.",
            inputSchema={
                "type": "object",
                "properties": {
                    "role": {"type": "string", "description": "Target role/title (e.g. 'HR', 'Tech Recruiter', 'Engineering Manager')"},
                    "company": {"type": "string", "description": "Target company (optional)"},
                    "location": {"type": "string", "description": "Location (optional)"},
                    "count": {"type": "integer", "description": "Number of connections to send (max 40/day)", "default": 20},
                    "note_template": {"type": "string", "description": "Connection note template (use {name} for personalization). Leave blank for AI-generated note."}
                },
                "required": ["role"]
            }
        ),

        # ── LINKEDIN MESSAGING ───────────────────────────────────────────────
        types.Tool(
            name="linkedin_send_message",
            description="Send a direct message to a LinkedIn connection.",
            inputSchema={
                "type": "object",
                "properties": {
                    "profile_id": {"type": "string", "description": "LinkedIn profile ID"},
                    "message": {"type": "string", "description": "Message content"},
                    "person_name": {"type": "string"}
                },
                "required": ["profile_id", "message"]
            }
        ),

        types.Tool(
            name="linkedin_bulk_message",
            description="Send personalized messages to multiple LinkedIn connections at once.",
            inputSchema={
                "type": "object",
                "properties": {
                    "profile_ids": {"type": "array", "items": {"type": "string"}, "description": "List of LinkedIn profile IDs"},
                    "message_template": {"type": "string", "description": "Message template (use {name} or {first_name} for personalization)"},
                    "names": {"type": "array", "items": {"type": "string"}, "description": "Names corresponding to profile_ids (optional)"}
                },
                "required": ["profile_ids", "message_template"]
            }
        ),

        # ── LINKEDIN POSTING ─────────────────────────────────────────────────
        types.Tool(
            name="linkedin_create_post",
            description="Create and publish a text post on LinkedIn directly — no need to visit the website.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Post content"},
                    "hashtags": {"type": "array", "items": {"type": "string"}, "description": "Hashtags to append"}
                },
                "required": ["content"]
            }
        ),

        types.Tool(
            name="linkedin_post_image",
            description="Post an image with an AI-generated caption directly to LinkedIn. User just provides the image path.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "Path to the image file"},
                    "caption": {"type": "string", "description": "Caption text (or leave blank for AI to generate from context)"},
                    "image_context": {"type": "string", "description": "What does the image show? (used to generate caption if blank)"},
                    "hashtags": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["image_path"]
            }
        ),

        types.Tool(
            name="linkedin_generate_post",
            description="Generate an engaging LinkedIn post on a given topic (doesn't publish — just generates the text).",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "What to post about"},
                    "domain": {"type": "string", "description": "Your domain (frontend, backend, ai, career, etc.)", "default": "general"}
                },
                "required": ["topic"]
            }
        ),

        # ── EMAIL ─────────────────────────────────────────────────────────────
        types.Tool(
            name="email_send",
            description="Send an email directly without going to Gmail. AI can draft it for you.",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email address"},
                    "subject": {"type": "string", "description": "Email subject"},
                    "body": {"type": "string", "description": "Email body"},
                    "attachment_path": {"type": "string", "description": "Path to file to attach (e.g. resume)"}
                },
                "required": ["to", "subject", "body"]
            }
        ),

        types.Tool(
            name="email_cold_to_hr",
            description="Draft and send a cold email to an HR or hiring manager about a role opportunity.",
            inputSchema={
                "type": "object",
                "properties": {
                    "hr_name": {"type": "string", "description": "HR's full name"},
                    "hr_email": {"type": "string", "description": "HR's email address"},
                    "company": {"type": "string", "description": "Company name"},
                    "role": {"type": "string", "description": "Role you're interested in"},
                    "resume_path": {"type": "string", "description": "Path to your resume (optional, for attachment)"}
                },
                "required": ["hr_name", "hr_email", "company", "role"]
            }
        ),

        types.Tool(
            name="email_bulk_cold",
            description="Send cold emails to multiple HRs/hiring managers at once.",
            inputSchema={
                "type": "object",
                "properties": {
                    "recipients": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "email": {"type": "string"},
                                "company": {"type": "string"}
                            }
                        },
                        "description": "List of recipients with name, email, company"
                    },
                    "role": {"type": "string"},
                    "resume_path": {"type": "string"}
                },
                "required": ["recipients", "role"]
            }
        ),

        types.Tool(
            name="email_follow_up",
            description="Send a follow-up email to someone who hasn't responded.",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {"type": "string"},
                    "original_subject": {"type": "string"},
                    "days_since": {"type": "integer", "default": 5}
                },
                "required": ["to", "original_subject"]
            }
        ),

        # ── RESUME ────────────────────────────────────────────────────────────
        types.Tool(
            name="resume_build",
            description="Build a complete ATS-optimized, waterproof resume from your profile. Outputs DOCX file.",
            inputSchema={"type": "object", "properties": {}}
        ),

        types.Tool(
            name="resume_tailor",
            description="Tailor your existing resume to a specific job description for maximum ATS score.",
            inputSchema={
                "type": "object",
                "properties": {
                    "resume_path": {"type": "string", "description": "Path to your current resume DOCX"},
                    "job_description": {"type": "string", "description": "Full job description text"}
                },
                "required": ["resume_path", "job_description"]
            }
        ),

        types.Tool(
            name="resume_score",
            description="Score your resume against a job description (0-100 ATS score).",
            inputSchema={
                "type": "object",
                "properties": {
                    "resume_text": {"type": "string", "description": "Your resume text content"},
                    "job_description": {"type": "string", "description": "Job description to score against"}
                },
                "required": ["resume_text", "job_description"]
            }
        ),

        types.Tool(
            name="resume_analyze",
            description="Analyze an uploaded resume for issues, quality, and improvement suggestions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "resume_path": {"type": "string", "description": "Path to resume DOCX file"}
                },
                "required": ["resume_path"]
            }
        ),

        # ── CAREER INTELLIGENCE ───────────────────────────────────────────────
        types.Tool(
            name="career_what_to_do_next",
            description="Tell me what to do next based on my current skills and target role. Returns ordered action plan with free course links.",
            inputSchema={
                "type": "object",
                "properties": {
                    "current_skills": {"type": "array", "items": {"type": "string"}, "description": "Your current skills list"},
                    "target_role": {"type": "string", "description": "Your target job role"},
                    "experience_years": {"type": "integer", "default": 0}
                },
                "required": ["current_skills", "target_role"]
            }
        ),

        types.Tool(
            name="career_roadmap",
            description="Get a complete, phased career roadmap to reach your goal.",
            inputSchema={
                "type": "object",
                "properties": {
                    "goal": {"type": "string", "description": "Your career goal (e.g. 'SDE at product company', 'Data Scientist at FAANG')"}
                },
                "required": ["goal"]
            }
        ),

        types.Tool(
            name="career_find_companies",
            description="Find target companies to apply to for a given role.",
            inputSchema={
                "type": "object",
                "properties": {
                    "role": {"type": "string", "description": "Target role"},
                    "location": {"type": "string", "description": "Preferred location (optional)"}
                },
                "required": ["role"]
            }
        ),

        # ── COURSES & CERTS ───────────────────────────────────────────────────
        types.Tool(
            name="courses_find",
            description="Find free courses and YouTube tutorials for any skill with valid links.",
            inputSchema={
                "type": "object",
                "properties": {
                    "skill": {"type": "string", "description": "Skill to learn (e.g. 'React', 'Python', 'System Design')"},
                    "limit": {"type": "integer", "default": 5}
                },
                "required": ["skill"]
            }
        ),

        types.Tool(
            name="courses_must_do",
            description="Get must-do free certifications for a target role that will directly boost your resume and LinkedIn.",
            inputSchema={
                "type": "object",
                "properties": {
                    "target_role": {"type": "string", "description": "Your target job role"}
                },
                "required": ["target_role"]
            }
        ),

        # ── CONTENT ───────────────────────────────────────────────────────────
        types.Tool(
            name="content_weekly_calendar",
            description="Generate a 4-week LinkedIn content calendar with trending topics and ready-to-post content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "Your domain (frontend, backend, ai, data science, etc.)", "default": "general"},
                    "weeks": {"type": "integer", "default": 4}
                }
            }
        ),

        types.Tool(
            name="content_trending_topics",
            description="Get currently trending topics to post about in your domain.",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "default": "general"}
                }
            }
        ),

        types.Tool(
            name="content_generate_image_caption",
            description="Generate a LinkedIn post caption for an image you want to share.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_context": {"type": "string", "description": "Describe what the image shows or what you want to share"},
                    "domain": {"type": "string", "default": "general"}
                },
                "required": ["image_context"]
            }
        ),
    ]


# ─────────────────────────────────────────────────────────────────────────────
# TOOL HANDLER (Routes tool calls to the right function)
# ─────────────────────────────────────────────────────────────────────────────

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        result = await asyncio.get_event_loop().run_in_executor(
            None, _handle_tool, name, arguments
        )
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        error_result = {"success": False, "error": str(e), "tool": name}
        return [types.TextContent(type="text", text=json.dumps(error_result, indent=2))]


def _handle_tool(name: str, args: dict) -> Any:
    """Synchronous tool handler — dispatches to tool modules."""

    # ── SETUP ─────────────────────────────────────────────────────────────────
    if name == "check_config":
        return validate_config()

    if name == "setup_profile":
        profile = args["profile"]
        existing = load_user_profile()
        existing.update(profile)
        save_user_profile(existing)
        return {"success": True, "message": "Profile saved!", "profile": existing}

    # ── LINKEDIN PROFILE ──────────────────────────────────────────────────────
    if name == "linkedin_get_profile":
        return get_my_profile()

    if name == "linkedin_score_profile":
        return score_linkedin_profile()

    if name == "linkedin_update_headline":
        return update_headline(args["headline"])

    if name == "linkedin_suggest_photo_guidelines":
        return suggest_profile_photo_guidelines()

    # ── LINKEDIN CONNECTIONS ──────────────────────────────────────────────────
    if name == "linkedin_search_people":
        return search_people(
            role=args["role"],
            company=args.get("company"),
            location=args.get("location"),
            limit=args.get("limit", 20)
        )

    if name == "linkedin_send_connection":
        return send_connection_request(
            profile_id=args["profile_id"],
            note=args.get("note", ""),
            person_name=args.get("person_name", "")
        )

    if name == "linkedin_bulk_connect":
        return bulk_connect(
            role=args["role"],
            company=args.get("company"),
            location=args.get("location"),
            count=args.get("count", 20),
            note_template=args.get("note_template", "Hi {name}, I came across your profile and would love to connect and learn from your experience!")
        )

    # ── LINKEDIN MESSAGING ────────────────────────────────────────────────────
    if name == "linkedin_send_message":
        return send_message(
            profile_id=args["profile_id"],
            message=args["message"],
            person_name=args.get("person_name", "")
        )

    if name == "linkedin_bulk_message":
        return bulk_message(
            profile_ids=args["profile_ids"],
            message_template=args["message_template"],
            names=args.get("names")
        )

    # ── LINKEDIN POSTING ──────────────────────────────────────────────────────
    if name == "linkedin_create_post":
        return create_text_post(
            content=args["content"],
            hashtags=args.get("hashtags", [])
        )

    if name == "linkedin_post_image":
        image_path = args["image_path"]
        caption = args.get("caption", "")
        if not caption and args.get("image_context"):
            cap_result = generate_image_post_caption(args["image_context"], args.get("domain", "general"))
            caption = cap_result.get("full_caption", "")
        return create_image_post(
            image_path=image_path,
            caption=caption,
            hashtags=args.get("hashtags", [])
        )

    if name == "linkedin_generate_post":
        return generate_post(
            topic=args["topic"],
            domain=args.get("domain", "general")
        )

    # ── EMAIL ─────────────────────────────────────────────────────────────────
    if name == "email_send":
        return send_email(
            to=args["to"],
            subject=args["subject"],
            body=args["body"],
            attachment_path=args.get("attachment_path")
        )

    if name == "email_cold_to_hr":
        profile = load_user_profile()
        return send_cold_email_to_hr(
            hr_name=args["hr_name"],
            hr_email=args["hr_email"],
            company=args["company"],
            role=args["role"],
            user_name=profile.get("name", ""),
            user_summary=profile.get("summary", "I'm a passionate developer looking to contribute to great teams."),
            resume_path=args.get("resume_path")
        )

    if name == "email_bulk_cold":
        profile = load_user_profile()
        return send_bulk_cold_emails(
            recipients=args["recipients"],
            role=args["role"],
            user_name=profile.get("name", ""),
            user_summary=profile.get("summary", ""),
            resume_path=args.get("resume_path")
        )

    if name == "email_follow_up":
        profile = load_user_profile()
        return send_follow_up_email(
            original_thread_to=args["to"],
            original_subject=args["original_subject"],
            user_name=profile.get("name", ""),
            days_since=args.get("days_since", 5)
        )

    # ── RESUME ────────────────────────────────────────────────────────────────
    if name == "resume_build":
        return build_resume()

    if name == "resume_tailor":
        return tailor_resume_to_jd(
            resume_path=args["resume_path"],
            job_description=args["job_description"]
        )

    if name == "resume_score":
        return score_resume_against_jd(
            resume_text=args["resume_text"],
            job_description=args["job_description"]
        )

    if name == "resume_analyze":
        return analyze_resume(args["resume_path"])

    # ── CAREER INTELLIGENCE ───────────────────────────────────────────────────
    if name == "career_what_to_do_next":
        return what_to_do_next(
            current_skills=args["current_skills"],
            target_role=args["target_role"],
            experience_years=args.get("experience_years", 0)
        )

    if name == "career_roadmap":
        return career_roadmap(args["goal"])

    if name == "career_find_companies":
        return find_target_companies(
            role=args["role"],
            preferences={"location": args.get("location")}
        )

    # ── COURSES ───────────────────────────────────────────────────────────────
    if name == "courses_find":
        return find_free_courses(
            skill=args["skill"],
            limit=args.get("limit", 5)
        )

    if name == "courses_must_do":
        return get_must_do_certs(args["target_role"])

    # ── CONTENT ───────────────────────────────────────────────────────────────
    if name == "content_weekly_calendar":
        return generate_weekly_content_calendar(
            domain=args.get("domain", "general"),
            weeks=args.get("weeks", 4)
        )

    if name == "content_trending_topics":
        return get_trending_topics(args.get("domain", "general"))

    if name == "content_generate_image_caption":
        return generate_image_post_caption(
            image_context=args["image_context"],
            domain=args.get("domain", "general")
        )

    return {"error": f"Unknown tool: {name}"}


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="careerpilot-ai",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
