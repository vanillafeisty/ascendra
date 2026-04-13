"""
CareerPilot AI - Career Intelligence & Course Finder
Roadmaps, skill gap analysis, what-to-do-next, and free course/cert finder.
"""

import json
import re
import requests
from typing import Optional
from config import ANTHROPIC_API_KEY, YOUTUBE_API_KEY


# ─── Curated Free Courses Database ────────────────────────────────────────────
# These are verified, high-quality free resources (validated at build time)
CURATED_COURSES = {
    "web development": [
        {"name": "The Odin Project – Full Stack", "platform": "The Odin Project", "link": "https://www.theodinproject.com", "cert": False, "free": True, "duration": "Self-paced"},
        {"name": "freeCodeCamp – Responsive Web Design", "platform": "freeCodeCamp", "link": "https://www.freecodecamp.org/learn/2022/responsive-web-design/", "cert": True, "free": True, "duration": "300 hrs"},
        {"name": "CS50's Web Programming with Python & JS", "platform": "edX / Harvard", "link": "https://cs50.harvard.edu/web/", "cert": True, "free": True, "duration": "12 weeks"},
        {"name": "HTML & CSS Full Course – Beginner to Pro", "platform": "YouTube / SuperSimpleDev", "link": "https://www.youtube.com/watch?v=G3e-cpL7ofc", "cert": False, "free": True, "duration": "6.5 hrs"},
    ],
    "python": [
        {"name": "Python for Everybody (Dr. Chuck)", "platform": "Coursera (audit free)", "link": "https://www.coursera.org/specializations/python", "cert": True, "free": True, "duration": "8 months"},
        {"name": "100 Days of Code – Python Bootcamp", "platform": "YouTube / Angela Yu", "link": "https://www.youtube.com/watch?v=kqtD5dpn9C8", "cert": False, "free": True, "duration": "2 hrs preview"},
        {"name": "CS50P – Introduction to Programming with Python", "platform": "edX / Harvard", "link": "https://cs50.harvard.edu/python/", "cert": True, "free": True, "duration": "10 weeks"},
    ],
    "react": [
        {"name": "React Course – Full Tutorial", "platform": "YouTube / freeCodeCamp", "link": "https://www.youtube.com/watch?v=bMknfKXIFA8", "cert": False, "free": True, "duration": "12 hrs"},
        {"name": "React Official Docs & Tutorial", "platform": "React.dev", "link": "https://react.dev/learn", "cert": False, "free": True, "duration": "Self-paced"},
        {"name": "Full Stack Open – React", "platform": "University of Helsinki", "link": "https://fullstackopen.com/en/", "cert": True, "free": True, "duration": "Self-paced"},
    ],
    "javascript": [
        {"name": "JavaScript Algorithms & Data Structures", "platform": "freeCodeCamp", "link": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "cert": True, "free": True, "duration": "300 hrs"},
        {"name": "The Complete JavaScript Course", "platform": "YouTube / Traversy Media", "link": "https://www.youtube.com/watch?v=hdI2bqOjy3c", "cert": False, "free": True, "duration": "3.5 hrs"},
        {"name": "JavaScript.info – Modern JS Tutorial", "platform": "javascript.info", "link": "https://javascript.info", "cert": False, "free": True, "duration": "Self-paced"},
    ],
    "data structures algorithms": [
        {"name": "CS50 – Introduction to Computer Science", "platform": "Harvard / edX", "link": "https://cs50.harvard.edu/x/", "cert": True, "free": True, "duration": "10 weeks"},
        {"name": "Data Structures – Full Course Using C and C++", "platform": "YouTube / freeCodeCamp", "link": "https://www.youtube.com/watch?v=B31LgI4Y4DQ", "cert": False, "free": True, "duration": "9.5 hrs"},
        {"name": "Algorithms Course – Graph Theory + DS", "platform": "YouTube / William Fiset", "link": "https://www.youtube.com/watch?v=09_LlHjoEiY", "cert": False, "free": True, "duration": "9 hrs"},
        {"name": "Neetcode 150 – DSA Practice", "platform": "neetcode.io", "link": "https://neetcode.io/practice", "cert": False, "free": True, "duration": "Self-paced"},
    ],
    "machine learning": [
        {"name": "Machine Learning Specialization – Andrew Ng", "platform": "Coursera (audit free)", "link": "https://www.coursera.org/specializations/machine-learning-introduction", "cert": True, "free": True, "duration": "3 months"},
        {"name": "fast.ai – Practical Deep Learning for Coders", "platform": "fast.ai", "link": "https://course.fast.ai", "cert": False, "free": True, "duration": "7 weeks"},
        {"name": "Machine Learning Crash Course", "platform": "Google", "link": "https://developers.google.com/machine-learning/crash-course", "cert": False, "free": True, "duration": "15 hrs"},
    ],
    "cloud aws": [
        {"name": "AWS Cloud Practitioner Essentials", "platform": "AWS Training", "link": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/", "cert": True, "free": True, "duration": "6 hrs"},
        {"name": "AWS Cloud Quest – Cloud Practitioner", "platform": "AWS Skill Builder", "link": "https://explore.skillbuilder.aws/learn/course/11458", "cert": False, "free": True, "duration": "Self-paced"},
    ],
    "sql database": [
        {"name": "SQL Tutorial – Full Database Course", "platform": "YouTube / freeCodeCamp", "link": "https://www.youtube.com/watch?v=HXV3zeQKqGY", "cert": False, "free": True, "duration": "4.5 hrs"},
        {"name": "Intro to SQL – Kaggle", "platform": "Kaggle", "link": "https://www.kaggle.com/learn/intro-to-sql", "cert": True, "free": True, "duration": "3 hrs"},
    ],
    "git github": [
        {"name": "Git and GitHub for Beginners – Crash Course", "platform": "YouTube / freeCodeCamp", "link": "https://www.youtube.com/watch?v=RGOj5yH7evk", "cert": False, "free": True, "duration": "1 hr"},
        {"name": "GitHub Skills", "platform": "GitHub", "link": "https://skills.github.com/", "cert": True, "free": True, "duration": "Self-paced"},
    ],
    "docker kubernetes": [
        {"name": "Docker Tutorial for Beginners", "platform": "YouTube / TechWorld with Nana", "link": "https://www.youtube.com/watch?v=3c-iBn73dDE", "cert": False, "free": True, "duration": "3 hrs"},
        {"name": "Kubernetes Tutorial for Beginners", "platform": "YouTube / TechWorld with Nana", "link": "https://www.youtube.com/watch?v=X48VuDVv0do", "cert": False, "free": True, "duration": "4 hrs"},
    ],
    "system design": [
        {"name": "System Design Primer", "platform": "GitHub / donnemartin", "link": "https://github.com/donnemartin/system-design-primer", "cert": False, "free": True, "duration": "Self-paced"},
        {"name": "System Design for Beginners", "platform": "YouTube / ByteByteGo", "link": "https://www.youtube.com/watch?v=m8Icp_Cid5o", "cert": False, "free": True, "duration": "1 hr"},
    ],
    "node js backend": [
        {"name": "Node.js and Express.js – Full Course", "platform": "YouTube / freeCodeCamp", "link": "https://www.youtube.com/watch?v=Oe421EPjeBE", "cert": False, "free": True, "duration": "8 hrs"},
        {"name": "Backend Development with Node.js", "platform": "freeCodeCamp", "link": "https://www.freecodecamp.org/learn/back-end-development-and-apis/", "cert": True, "free": True, "duration": "300 hrs"},
    ],
    "typescript": [
        {"name": "TypeScript Full Course for Beginners", "platform": "YouTube / freeCodeCamp", "link": "https://www.youtube.com/watch?v=30LWjhZzg50", "cert": False, "free": True, "duration": "2 hrs"},
        {"name": "TypeScript Handbook", "platform": "typescriptlang.org", "link": "https://www.typescriptlang.org/docs/handbook/intro.html", "cert": False, "free": True, "duration": "Self-paced"},
    ],
    "devops cicd": [
        {"name": "DevOps Prerequisites Course", "platform": "YouTube / KodeKloud", "link": "https://www.youtube.com/watch?v=Wvf0mBNGjXY", "cert": False, "free": True, "duration": "3 hrs"},
        {"name": "GitHub Actions Tutorial", "platform": "YouTube / TechWorld with Nana", "link": "https://www.youtube.com/watch?v=R8_veQiYBjI", "cert": False, "free": True, "duration": "2.5 hrs"},
    ],
}

# ─── Role → Must-Do Certifications Mapping ────────────────────────────────────
ROLE_CERTIFICATIONS = {
    "frontend developer": [
        "freeCodeCamp – Responsive Web Design Certification",
        "freeCodeCamp – JavaScript Algorithms & Data Structures",
        "Meta Frontend Developer Certificate (Coursera – audit free)",
        "Google UX Design Certificate (Coursera – audit free)",
    ],
    "backend developer": [
        "freeCodeCamp – Back End Development & APIs",
        "CS50P – Harvard Python Certificate (free)",
        "AWS Cloud Practitioner (free tier exam prep)",
        "Meta Backend Developer Certificate (Coursera – audit free)",
    ],
    "full stack developer": [
        "Full Stack Open Certificate (University of Helsinki – 100% free)",
        "freeCodeCamp Full Stack Certification",
        "CS50 Web Programming with Python & JavaScript (Harvard – free)",
        "Google Project Management Certificate (Coursera – audit free)",
    ],
    "data scientist": [
        "Google Data Analytics Certificate (Coursera – audit free)",
        "Kaggle Data Science Certificates (100% free)",
        "IBM Data Science Certificate (Coursera – audit free)",
        "DeepLearning.AI ML Specialization (Coursera – audit free)",
    ],
    "machine learning engineer": [
        "DeepLearning.AI ML Specialization – Andrew Ng (Coursera – audit free)",
        "fast.ai Practical Deep Learning for Coders (100% free)",
        "Google ML Crash Course Certificate (100% free)",
        "Kaggle ML Certificates (100% free)",
    ],
    "devops engineer": [
        "Google IT Support Certificate (Coursera – audit free)",
        "AWS Cloud Practitioner (free prep available)",
        "GitHub Actions Certification (free)",
        "Linux Foundation Free Courses (LFS101 – 100% free)",
    ],
    "android developer": [
        "Google Android Basics with Compose (developer.android.com – free)",
        "Meta Android Developer Certificate (Coursera – audit free)",
        "Kotlin Certification – JetBrains (free)",
    ],
}


# ─────────────────────────────────────────────────────────────────────────────
# COURSE FINDER
# ─────────────────────────────────────────────────────────────────────────────

def find_free_courses(skill: str, limit: int = 5) -> dict:
    """
    Find free courses for a given skill.
    Returns courses from curated database + web search fallback.
    """
    skill_lower = skill.lower()
    found_courses = []

    # Match curated courses
    for key, courses in CURATED_COURSES.items():
        if any(word in skill_lower for word in key.split()) or any(word in key for word in skill_lower.split()):
            found_courses.extend(courses)

    # Deduplicate by name
    seen = set()
    unique_courses = []
    for c in found_courses:
        if c["name"] not in seen:
            seen.add(c["name"])
            unique_courses.append(c)

    if not unique_courses:
        # Fallback: generic search result
        unique_courses = [{
            "name": f"{skill} – Free Course Search",
            "platform": "Google Search",
            "link": f"https://www.google.com/search?q=free+{skill.replace(' ', '+')}+course+youtube+2024",
            "cert": False,
            "free": True,
            "duration": "Varies",
            "note": "Search for free courses on YouTube, Coursera (audit), or edX (audit)"
        }]

    return {
        "skill": skill,
        "courses_found": len(unique_courses[:limit]),
        "courses": unique_courses[:limit],
        "tip": "For Coursera courses: click 'Audit Course' to access content for free (no certificate). For a certificate, apply for Financial Aid."
    }


def get_must_do_certs(target_role: str) -> dict:
    """
    Return must-do free certifications for a target role.
    """
    role_lower = target_role.lower()
    matched_certs = []
    matched_role = None

    for role_key, certs in ROLE_CERTIFICATIONS.items():
        if any(word in role_lower for word in role_key.split()):
            matched_certs = certs
            matched_role = role_key
            break

    if not matched_certs:
        # Generic recommendations
        matched_certs = [
            "CS50 – Introduction to Computer Science (Harvard – 100% free)",
            "Google IT Support Certificate (Coursera – audit free)",
            "freeCodeCamp Certifications (100% free)",
            "LinkedIn Learning – 1 month free trial (great for ATS)",
        ]
        matched_role = "general tech"

    return {
        "target_role": target_role,
        "matched_role": matched_role,
        "certifications": matched_certs,
        "note": "Each of these certifications is FREE or auditable for free. They add direct value to your LinkedIn and resume.",
        "linkedin_tip": "Add certifications to LinkedIn profile → 'Licenses & Certifications' section for maximum visibility."
    }


# ─────────────────────────────────────────────────────────────────────────────
# CAREER INTELLIGENCE
# ─────────────────────────────────────────────────────────────────────────────

def what_to_do_next(current_skills: list[str], target_role: str, experience_years: int = 0) -> dict:
    """
    Tell the user their next action steps based on current state and target role.
    Returns ordered action plan with course links.
    """
    role_lower = target_role.lower()

    # Role-specific skill requirements
    ROLE_SKILLS = {
        "frontend": ["HTML", "CSS", "JavaScript", "React", "TypeScript", "Git", "Responsive Design", "REST APIs"],
        "backend": ["Python or Node.js", "SQL", "REST APIs", "Git", "Docker", "Authentication", "Cloud basics"],
        "full stack": ["HTML/CSS/JS", "React", "Node.js or Python", "SQL", "MongoDB", "Git", "Docker", "REST APIs"],
        "data scientist": ["Python", "Statistics", "Pandas", "NumPy", "ML algorithms", "SQL", "Data Visualization"],
        "ml engineer": ["Python", "TensorFlow/PyTorch", "ML theory", "Data preprocessing", "Model deployment", "Cloud"],
        "devops": ["Linux", "Git", "Docker", "Kubernetes", "CI/CD", "Cloud (AWS/GCP/Azure)", "Scripting"],
    }

    # Find matching role
    required_skills = []
    for key, skills in ROLE_SKILLS.items():
        if key in role_lower:
            required_skills = skills
            break

    if not required_skills:
        required_skills = ["Core programming (Python or JS)", "Data structures & algorithms", "Git", "A popular framework", "Cloud basics"]

    # Identify gaps
    current_lower = [s.lower() for s in current_skills]
    gaps = [s for s in required_skills if not any(c in s.lower() or s.lower() in c for c in current_lower)]

    # Build action plan
    actions = []

    # Priority 1: Fill skill gaps
    for i, gap in enumerate(gaps[:5], 1):
        courses = find_free_courses(gap)
        first_course = courses["courses"][0] if courses["courses"] else None
        action = {
            "priority": i,
            "action": f"Learn {gap}",
            "why": f"Required for {target_role} and missing from your current skill set",
            "how": first_course["name"] if first_course else f"Search 'free {gap} tutorial' on YouTube",
            "link": first_course["link"] if first_course else f"https://www.youtube.com/results?search_query={gap.replace(' ', '+')}+tutorial",
            "estimated_time": first_course.get("duration", "2–4 weeks")
        }
        actions.append(action)

    # Priority: Build projects
    actions.append({
        "priority": len(gaps) + 1,
        "action": "Build 2–3 portfolio projects",
        "why": "Projects are the #1 thing recruiters look for; certifications without projects don't convert",
        "how": "Build real-world projects relevant to your target role. Push to GitHub.",
        "link": "https://github.com/practical-tutorials/project-based-learning",
        "estimated_time": "4–8 weeks"
    })

    # Priority: LinkedIn & Resume
    actions.append({
        "priority": len(gaps) + 2,
        "action": "Optimize LinkedIn profile and resume",
        "why": "70% of jobs are found through LinkedIn. An optimized profile = 5x more recruiter views.",
        "how": "Use this AI tool to tailor your headline, about, and experience sections",
        "link": "https://linkedin.com",
        "estimated_time": "1–2 hours"
    })

    # Priority: Networking
    actions.append({
        "priority": len(gaps) + 3,
        "action": f"Connect with 50+ {target_role} professionals and HRs",
        "why": "Referrals account for 40–60% of all hires. Your network is your net worth.",
        "how": "Use this AI tool to auto-connect with relevant people",
        "link": "https://linkedin.com/search/results/people/",
        "estimated_time": "30 min/week"
    })

    return {
        "target_role": target_role,
        "current_skills": current_skills,
        "skill_gaps": gaps,
        "action_plan": actions,
        "summary": f"You have {len(current_skills)} skills and need {len(gaps)} more for {target_role}. Follow the priority order above.",
        "estimated_total_time": f"{len(gaps) * 3}–{len(gaps) * 6} weeks to be job-ready"
    }


def career_roadmap(goal: str) -> dict:
    """
    Generate a complete career roadmap for a target goal.
    """
    roadmap = {
        "goal": goal,
        "phases": [
            {
                "phase": 1,
                "name": "Foundation (Weeks 1–4)",
                "focus": "Core skills and fundamentals",
                "tasks": [
                    "Identify the required tech stack for your target role",
                    "Complete a foundational free course (CS50, freeCodeCamp, etc.)",
                    "Set up development environment (VS Code, Git, GitHub)",
                    "Join communities: Discord, Reddit r/learnprogramming, LinkedIn groups"
                ]
            },
            {
                "phase": 2,
                "name": "Skill Building (Weeks 5–12)",
                "focus": "Hands-on learning + projects",
                "tasks": [
                    "Complete role-specific skills (see what_to_do_next for details)",
                    "Build Project #1: A simple but complete app (deploy it!)",
                    "Get 1–2 free certifications from the must-do list",
                    "Start posting weekly on LinkedIn to build presence"
                ]
            },
            {
                "phase": 3,
                "name": "Portfolio & Presence (Weeks 13–16)",
                "focus": "Make yourself discoverable",
                "tasks": [
                    "Build Project #2: A more complex, real-world project",
                    "Optimize GitHub profile (pinned repos, README, activity)",
                    "Build or update personal portfolio website",
                    "Optimize LinkedIn profile fully (use AI tools here)",
                    "Build ATS-optimized resume"
                ]
            },
            {
                "phase": 4,
                "name": "Active Job Search (Weeks 17–24)",
                "focus": "Apply, network, interview",
                "tasks": [
                    "Connect with 200+ target HRs and hiring managers",
                    "Send tailored cold emails to 50+ companies",
                    "Apply to jobs with tailored resumes (use AI tailoring)",
                    "Prepare for technical interviews (DSA, system design, behavioral)",
                    "Follow up with all connections after 1 week"
                ]
            }
        ],
        "key_metrics": {
            "connections_target": "500+",
            "applications_per_week": "10–20",
            "follow_ups": "Every unanswered application after 7 days",
            "posts_per_week": "1–2 LinkedIn posts"
        },
        "pro_tips": [
            "Apply quality over quantity — tailor each resume to the JD",
            "Referrals convert 5x better than cold applications",
            "Post on LinkedIn consistently — even 1 post/week compounds over months",
            "Don't wait to be 100% ready — apply when you're 70% there"
        ]
    }

    return roadmap


def find_target_companies(role: str, preferences: Optional[dict] = None) -> dict:
    """
    Find companies to target for a given role.
    """
    # Curated by role type
    COMPANIES_BY_ROLE = {
        "frontend": {
            "product": ["Razorpay", "Swiggy", "Zomato", "CRED", "Meesho", "Groww", "PhonePe", "Zerodha"],
            "mnc": ["Google", "Microsoft", "Amazon", "Flipkart", "Adobe", "Thoughtworks", "Sapient"],
            "startup": ["Unstop", "Internshala", "Springworks", "Darwinbox", "Chargebee"]
        },
        "backend": {
            "product": ["Razorpay", "Zepto", "BharatPe", "OlaMoney", "Paytm", "Juspay"],
            "mnc": ["Atlassian", "Nutanix", "Cisco", "Oracle", "Infosys", "Wipro"],
            "startup": ["Hasura", "Postman", "Middlewarehq", "Supabase India"]
        },
        "data": {
            "product": ["Freshworks", "Clevertap", "MoEngage", "WebEngage"],
            "mnc": ["Walmart Labs", "Uber India", "LinkedIn India", "Samsung R&D"],
            "startup": ["Atlan", "Superset", "Datahub"]
        }
    }

    matched_companies = {"product": [], "mnc": [], "startup": []}
    for key, val in COMPANIES_BY_ROLE.items():
        if key in role.lower():
            matched_companies = val
            break

    # Default if no match
    if not any(matched_companies.values()):
        matched_companies = {
            "product": ["Razorpay", "Swiggy", "Zomato", "CRED", "Meesho"],
            "mnc": ["TCS", "Infosys", "Wipro", "Cognizant", "Accenture"],
            "startup": ["Search AngelList India", "YC India startups", "LinkedIn #hiring"]
        }

    return {
        "role": role,
        "companies": matched_companies,
        "how_to_find_more": [
            "Search LinkedIn: '{role} hiring' with location filter",
            "Check LinkedIn company pages → 'Open Jobs' tab",
            "AngelList India (now Wellfound): https://wellfound.com",
            "Glassdoor: https://www.glassdoor.co.in",
            "Instahyre: https://www.instahyre.com"
        ]
    }
