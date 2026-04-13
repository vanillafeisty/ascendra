# Software Requirements Specification (SRS)
## Ascendra — Autonomous AI Career Intelligence Platform

**Version:** 2.0.0  
**Date:** 2026-04-08  
**Status:** Final  
**Classification:** Personal Use Only  
**Replaces:** CareerPilot AI SRS v1.0.0

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Architecture](#3-system-architecture)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [External Interfaces](#6-external-interfaces)
7. [Data Models](#7-data-models)
8. [Tool Catalog](#8-tool-catalog)
9. [Ethical & Legal Compliance](#9-ethical--legal-compliance)
10. [Security & Anti-Detection](#10-security--anti-detection)
11. [User Interaction Flows](#11-user-interaction-flows)
12. [Constraints & Assumptions](#12-constraints--assumptions)
13. [Risks & Mitigations](#13-risks--mitigations)

---

## 1. Introduction

### 1.1 Purpose
This document defines the complete software requirements for **Ascendra**, an autonomous AI-powered career intelligence platform. Ascendra replaces and fully supersedes the CareerPilot AI v1.0 SRS. All references to "CareerPilot AI" are hereby replaced by "Ascendra."

Ascendra is delivered as:
- A **Conversational AI Chatbot** (Claude/ChatGPT-style) — web and mobile
- A **Next.js 14 Web Application** (App Router, TypeScript)
- An **Expo React Native Mobile Application** (iOS + Android)
- A **FastAPI REST Backend** with MCP server compatibility

### 1.2 Scope
Ascendra autonomously manages a user's entire career lifecycle including LinkedIn automation, ATS-Semantic Resume Optimization, targeted HR outreach via LinkedIn and email, content scheduling, skill-gap analysis, and learning roadmap generation.

### 1.3 Brand Identity
- **Product Name:** Ascendra (only)
- **Tagline:** *Rise Without Limits*
- All code, documentation, and UI must use "Ascendra" exclusively

### 1.4 Definitions

| Term | Definition |
|------|-----------|
| ATS-Semantic Optimization Engine | NLP-powered resume engine that uses semantic keyword alignment, TF-IDF scoring, and contextual embedding matching to maximize ATS pass rates — replaces the legacy term "Waterproof Resume" |
| HITL | Human-in-the-Loop — a mandatory user review gate before any automated message or email is dispatched |
| Anti-Bot Stealth Layer | Playwright-based evasion system overriding browser fingerprints and simulating human behavior |
| ICP | Ideal Connection Profile — the target persona definition for LinkedIn outreach |
| MCP | Model Context Protocol — standard for LLM tool integration |
| SERP | Search Engine Result Page |

---

## 2. Overall Description

### 2.1 Product Perspective

```
User (Web / Mobile Chat Interface)
           │
           ▼
    Ascendra Chatbot UI
    (Next.js / React Native)
           │
           ▼ [REST / WebSocket]
    Ascendra FastAPI Backend
    ├── Content Moderation Middleware
    ├── Chat Engine (Anthropic Claude)
    ├── LinkedIn Automation Engine
    ├── ATS-Semantic Optimization Engine
    ├── Email Engine
    ├── Career Intelligence Engine
    └── Content Engine
           │
           ▼
    External APIs & Services
    (LinkedIn, Gmail, YouTube Data API v3, Web Search)
```

### 2.2 Product Functions (Summary)

| Category | Capability |
|----------|-----------|
| Chat | Conversational AI assistant for all career tasks |
| LinkedIn Profile | Optimize headline, about, experience, skills, banner, photo |
| LinkedIn Connections | Auto-search and connect with HRs, hiring managers, mentors |
| LinkedIn Messaging | HITL-gated cold messages, follow-ups, thank-you notes |
| LinkedIn Posts | Generate, create, and publish posts automatically |
| ATS Resume | Build semantically-optimized resume from user background |
| Resume Tailoring | Tailor resume to JD using NLP keyword alignment |
| Email | Find valid HR emails; draft and send cold emails directly |
| Career Roadmap | Personalized action plan with timeline and free course links |
| Course Finder | Find courses with YouTube Data API v3 link validation |
| Job Targeting | Identify target companies, roles, and contacts |
| Weekly Automation | HITL-gated weekly posts, connection bursts, follow-ups |
| Content Moderation | Block unethical, obscene, or harmful content generation |

### 2.3 User Classes

| Class | Description |
|-------|-------------|
| Fresher | College student/recent grad, 0 experience |
| Experienced | 1–10 years experience, looking to switch |
| Career Changer | Switching domains (e.g., non-IT to IT) |
| Freelancer | Building presence to attract clients |

---

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│               ASCENDRA CLIENT LAYER                           │
│                                                              │
│  ┌────────────────────┐    ┌──────────────────────────────┐  │
│  │  Next.js 14 Web    │    │  Expo React Native Mobile    │  │
│  │  (App Router, TS)  │    │  (iOS + Android)             │  │
│  │  Chat Interface    │    │  Chat Interface              │  │
│  └─────────┬──────────┘    └──────────────┬───────────────┘  │
└────────────┼─────────────────────────────┼────────────────────┘
             │ REST / WebSocket             │
┌────────────▼─────────────────────────────▼────────────────────┐
│               ASCENDRA BACKEND (FastAPI)                       │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Content Moderation Middleware  (Ethics Guard)         │  │
│  └──────────────────────────┬────────────────────────────┘  │
│                             │                               │
│  ┌──────────────────────────▼────────────────────────────┐  │
│  │  Chat Engine  (Anthropic Claude API)                   │  │
│  │  + Tool Router + HITL Gate                             │  │
│  └──┬────────┬────────┬────────┬────────┬────────┬───────┘  │
│     │        │        │        │        │        │          │
│  ┌──▼──┐ ┌──▼──┐ ┌───▼──┐ ┌──▼──┐ ┌──▼──┐ ┌──▼──┐       │
│  │ LI  │ │Email│ │ATS   │ │Career│ │Cont.│ │Course│       │
│  │Tools│ │Tools│ │Engine│ │Intel │ │Tools│ │Tools │       │
│  └──┬──┘ └──┬──┘ └───┬──┘ └──┬──┘ └──┬──┘ └──┬──┘       │
└─────┼───────┼─────────┼───────┼───────┼───────┼────────────┘
      │       │         │       │       │       │
      ▼       ▼         ▼       ▼       ▼       ▼
  LinkedIn  Gmail    DOCX/PDF  Web    Claude  YouTube
  API +     OAuth2   Engine   Search  API    Data API v3
  Playwright SMTP
```

### 3.2 Module Breakdown

#### 3.2.1 LinkedIn Automation Engine (`linkedin_tools.py`)
- Uses `linkedin-api` (unofficial Python library) for read/write operations
- Playwright browser automation with **Anti-Bot Stealth Layer** (see §10)
- Session persistence via encrypted cookie storage
- HITL gate: all bulk actions require user confirmation before execution

#### 3.2.2 ATS-Semantic Optimization Engine (`resume_tools.py`)
- **NLP Pipeline:** Uses `spaCy` + `scikit-learn` TF-IDF vectorizer to extract semantically significant keywords from job descriptions
- **Semantic Alignment:** Computes cosine similarity between JD embedding and resume embedding using `sentence-transformers`
- **Keyword Gap Analysis:** Identifies missing high-weight terms and injects them contextually (not stuffing)
- **Scoring:** Returns a 0–100 ATS-Semantic score combining: keyword match (40%), semantic similarity (40%), formatting compliance (20%)
- Outputs DOCX + PDF formats

#### 3.2.3 Email Engine (`email_tools.py`)
- Primary: Gmail API (OAuth2)
- Fallback: SMTP (TLS) for any provider
- **Email Discovery:** Uses Hunter.io API / web scraping to find valid HR email addresses
- HITL gate: email preview before sending

#### 3.2.4 Career Intelligence Engine (`career_tools.py`)
- Skill gap analysis against role-specific requirement matrices
- Ordered action plan generation with timeline estimates
- Target company and contact identification

#### 3.2.5 Content Engine (`content_tools.py`)
- LinkedIn post generation via Claude API
- Weekly content calendar management
- Image post support with AI-generated captions
- Ethics filter: all content passes moderation before publish

#### 3.2.6 Course & Certification Engine (`career_tools.py`)
- Curated course database + web search fallback
- **YouTube Data API v3 Integration:** Automated link health checks using `videos.list` endpoint; quality filtering by view count, like ratio, and channel authority (see FR-4.8)

---

## 4. Functional Requirements

> All requirements follow the format **FR-[Module].[Number]** and are verifiable by automated test.

### FR-1 — Chat Interface

| ID | Requirement | Verification |
|----|-------------|-------------|
| FR-1.1 | System SHALL provide a chat interface styled after leading LLM products (Claude, ChatGPT) | UI visual inspection + usability test |
| FR-1.2 | System SHALL accept natural language commands in a single message and map them to tool calls | Integration test: 20 command patterns |
| FR-1.3 | System SHALL display tool execution status in real-time (streaming) | Automated streaming test |
| FR-1.4 | System SHALL maintain conversation history across sessions (localStorage + backend) | Session persistence test |
| FR-1.5 | System SHALL support the same chat interface on web (Next.js) and mobile (React Native/Expo) | Cross-platform UI test |
| FR-1.6 | System SHALL detect and decline unethical, obscene, or harmful requests with a polite refusal | Moderation unit test: 50 adversarial inputs |
| FR-1.7 | System SHALL show a "Human-in-the-Loop" review screen before executing any bulk automated action | HITL integration test |

### FR-2 — LinkedIn Profile Management

| ID | Requirement | Verification |
|----|-------------|-------------|
| FR-2.1 | System SHALL read user's current LinkedIn profile data via authenticated session | API response assertion |
| FR-2.2 | System SHALL generate and apply an optimized headline to LinkedIn automatically | Playwright DOM update assertion |
| FR-2.3 | System SHALL generate and update the LinkedIn About/Summary section | Playwright DOM update assertion |
| FR-2.4 | System SHALL suggest profile photo criteria via AI-generated guidelines | Output contains ≥10 guidelines |
| FR-2.5 | System SHALL suggest and update the featured section | Playwright DOM assertion |
| FR-2.6 | System SHALL suggest skills to add/remove based on target role | Skill diff output assertion |
| FR-2.7 | System SHALL update experience bullets with action-oriented, quantified language | NLP bullet quality score ≥ 7/10 |
| FR-2.8 | System SHALL analyze and score the current profile on 10 defined criteria (0–100) | Score range assertion + criteria coverage |

### FR-3 — LinkedIn Connection Automation

| ID | Requirement | Verification |
|----|-------------|-------------|
| FR-3.1 | System SHALL search for HRs, hiring managers, recruiters by company/role/location | Search returns ≥1 result for valid inputs |
| FR-3.2 | System SHALL send connection requests with AI-personalized notes (≤300 chars) | Note length assertion + API call mock |
| FR-3.3 | System SHALL respect LinkedIn rate limits (≤40 connections/day) | Counter assertion in connection log |
| FR-3.4 | System SHALL filter already-connected profiles from outreach lists | Dedup test with pre-seeded log |
| FR-3.5 | System SHALL allow user to define Ideal Connection Profile (ICP) | ICP schema validation test |
| FR-3.6 | System SHALL prioritize 2nd-degree connections over 3rd-degree | Sort order assertion on search results |
| FR-3.7 | System SHALL log all connection activity with timestamp, status, and profile metadata | Log schema validation test |
| FR-3.8 | System SHALL require HITL confirmation before executing bulk connect (>5 connections) | UI confirmation modal assertion |

### FR-4 — LinkedIn Messaging

| ID | Requirement | Verification |
|----|-------------|-------------|
| FR-4.1 | System SHALL send cold messages to specified LinkedIn connections | Message delivery mock test |
| FR-4.2 | System SHALL generate role-specific cold message templates using Claude API | Template contains personalization tokens |
| FR-4.3 | System SHALL send follow-up messages to non-responding connections after N days | Follow-up scheduler test |
| FR-4.4 | System SHALL send thank-you messages after interviews | Template + delivery test |
| FR-4.5 | System SHALL support bulk messaging with personalization tokens ({name}, {company}) | Token substitution unit test |
| FR-4.6 | System SHALL NOT send duplicate messages to the same person | Dedup assertion in message log |
| FR-4.7 | System SHALL log all messages with response tracking | Log schema + response flag test |
| FR-4.8 | System SHALL require HITL message preview and approval before bulk send | UI approval gate assertion |

### FR-5 — LinkedIn Posts & Content

| ID | Requirement | Verification |
|----|-------------|-------------|
| FR-5.1 | System SHALL generate weekly LinkedIn posts on trending tech topics | Post quality score ≥ 6/10 |
| FR-5.2 | System SHALL publish posts directly to LinkedIn via Playwright without user visiting the site | Playwright network intercept test |
| FR-5.3 | System SHALL accept user-provided images and generate + publish AI-captioned posts | Image upload + caption generation test |
| FR-5.4 | System SHALL use engagement-optimized post format (hook → body → CTA → hashtags) | Format structure assertion |
| FR-5.5 | System SHALL maintain a 4-week content calendar | Calendar schema + date range test |
| FR-5.6 | System SHALL vary post formats (text, image, carousel, poll concept) | Format diversity assertion over 4-week calendar |
| FR-5.7 | System SHALL suggest trending hashtags (≥5) relevant to user's domain | Hashtag count assertion |
| FR-5.8 | System SHALL pass all posts through the Content Moderation Middleware before publishing | Moderation flag test on 50 inputs |

### FR-6 — ATS-Semantic Optimization Engine

| ID | Requirement | Verification |
|----|-------------|-------------|
| FR-6.1 | System SHALL build a complete resume from user profile data | DOCX output file existence + schema test |
| FR-6.2 | System SHALL generate an ATS-Semantic optimized resume for a target role/JD using NLP keyword alignment | Semantic score ≥ 75/100 on test JD |
| FR-6.3 | System SHALL inject JD keywords contextually using TF-IDF weighting (not keyword stuffing) | Keyword presence + readability score test |
| FR-6.4 | System SHALL score resume against JD using ATS-Semantic score (0–100): keyword match (40%) + semantic similarity (40%) + formatting (20%) | Score component breakdown assertion |
| FR-6.5 | System SHALL suggest specific improvements to achieve a score ≥ 90/100 | Improvement suggestion list length ≥ 3 |
| FR-6.6 | System SHALL generate multiple resume variants for different target roles | ≥2 variant files generated |
| FR-6.7 | System SHALL output resume as both DOCX and PDF | Both file extensions present |
| FR-6.8 | System SHALL use certifications and projects as primary differentiator sections | Section presence assertion |
| FR-6.9 | System SHALL quantify all achievement bullets (%, numbers, impact metrics) | NLP number detection in all bullets |
| FR-6.10 | System SHALL format resume to pass ATS parsing (no tables, no headers/footers, clean fonts) | ATS parse validation using textract |

### FR-7 — Email Automation

| ID | Requirement | Verification |
|----|-------------|-------------|
| FR-7.1 | System SHALL send cold emails to HRs/hiring managers directly via Gmail/SMTP | Email delivery mock test |
| FR-7.2 | System SHALL draft emails with personalized subject lines using Claude API | Subject line personalization assertion |
| FR-7.3 | System SHALL attach resume to emails when instructed | Attachment presence in MIME object |
| FR-7.4 | System SHALL send follow-up emails after X days of no response via scheduler | Scheduler trigger test |
| FR-7.5 | System SHALL support emailing a specific person about a specific situation | Free-form context injection test |
| FR-7.6 | System SHALL maintain email log with sent/replied/bounced status | Log status enum validation |
| FR-7.7 | System SHALL support Gmail OAuth2 and SMTP configurations | Auth method toggle test |
| FR-7.8 | System SHALL attempt to discover valid HR email addresses via Hunter.io API or web pattern matching | Email format validation + deliverability check |
| FR-7.9 | System SHALL require HITL email preview before sending to new recipients | Preview screen assertion |

### FR-8 — Career Intelligence & Roadmap

| ID | Requirement | Verification |
|----|-------------|-------------|
| FR-8.1 | System SHALL analyze user's current skills and experience | Skill array parsing test |
| FR-8.2 | System SHALL compare user profile against target role requirements | Gap list non-empty for incomplete profiles |
| FR-8.3 | System SHALL generate a prioritized skill gap list ordered by job-market demand | Gap list ordered by priority field |
| FR-8.4 | System SHALL produce a phased career roadmap with timeline estimates | Roadmap contains ≥4 phases |
| FR-8.5 | System SHALL tell the user what to do next based on their current state | Action plan contains ≥5 items |
| FR-8.6 | System SHALL recommend target companies based on user profile and preferences | Company list ≥3 per category |
| FR-8.7 | System SHALL identify the right people to contact at target companies | Person list with role filter |

### FR-9 — Course & Certification Finder

| ID | Requirement | Verification |
|----|-------------|-------------|
| FR-9.1 | System SHALL find free courses for any skill gap from a curated database | Course results non-empty for all supported skills |
| FR-9.2 | System SHALL validate YouTube course links using **YouTube Data API v3** (`videos.list` endpoint) before returning | API call mock + status code assertion |
| FR-9.3 | System SHALL filter courses by quality metrics via YouTube Data API v3: view count ≥ 50,000; like ratio ≥ 90%; channel subscriber count ≥ 10,000 | Quality filter assertion on API response |
| FR-9.4 | System SHALL perform automated link health checks every 24 hours for cached course links | Scheduler test + staleness flag assertion |
| FR-9.5 | System SHALL include certifications that add direct resume and LinkedIn profile value | Cert-to-role mapping assertion |
| FR-9.6 | System SHALL rank courses by: free (primary), recognized cert (secondary), duration (tertiary), relevance (quaternary) | Sort order assertion |
| FR-9.7 | System SHALL return structured data: name, platform, link, duration, cert (boolean), quality_score | Schema validation test |
| FR-9.8 | System SHALL differentiate between LinkedIn-recognized certifications and general certifications | Badge field assertion |

---

## 5. Non-Functional Requirements

### NFR-1 — Performance

| ID | Requirement |
|----|-------------|
| NFR-1.1 | Chat response first token: ≤ 1.5 seconds (streaming) |
| NFR-1.2 | LinkedIn operations: ≤ 10 seconds per action |
| NFR-1.3 | ATS-Semantic resume generation: ≤ 30 seconds |
| NFR-1.4 | Email send: ≤ 5 seconds |
| NFR-1.5 | Course search + YouTube validation: ≤ 15 seconds |

### NFR-2 — Reliability

| ID | Requirement |
|----|-------------|
| NFR-2.1 | Must handle LinkedIn session expiry gracefully (auto re-login with anti-bot stealth) |
| NFR-2.2 | Must retry failed API calls up to 3 times with exponential backoff |
| NFR-2.3 | All actions must be logged; partial failures must not lose data |
| NFR-2.4 | YouTube link cache must refresh every 24 hours |

### NFR-3 — Security

| ID | Requirement |
|----|-------------|
| NFR-3.1 | All credentials stored encrypted in local `.env` (never hardcoded) |
| NFR-3.2 | LinkedIn password never transmitted beyond the local machine |
| NFR-3.3 | Gmail uses OAuth2 only (no password storage) |
| NFR-3.4 | All logs stripped of PII before verbose output |
| NFR-3.5 | Content Moderation Middleware must intercept all LLM output before delivery to user |

---

## 6. External Interfaces

### 6.1 LinkedIn Integration

| Method | Purpose | Library |
|--------|---------|---------|
| `linkedin-api` (unofficial) | Search, connect, message, read profile | `linkedin-api` PyPI |
| Playwright + Stealth Layer | Posting, profile updates, anti-detection | `playwright` + `playwright-stealth` |
| Encrypted cookie store | Session persistence | `cryptography` + JSON |

### 6.2 Gmail / Email Integration

| Method | Purpose |
|--------|---------|
| Gmail API (OAuth2) | Send/read emails |
| SMTP (TLS) | Generic fallback |
| Hunter.io API | Email discovery for HR contacts |

### 6.3 YouTube Data API v3

| Endpoint | Purpose |
|----------|---------|
| `videos.list?part=statistics,snippet` | Validate link health, get view count, like count, channel info |
| `channels.list?part=statistics` | Get subscriber count for quality filtering |
| Quota: 10,000 units/day (free) | Managed via daily quota tracker |

### 6.4 AI Content Generation

| Component | Purpose |
|-----------|---------|
| Anthropic Claude API | Chat, post generation, email drafting, resume bullets |
| System prompt per tool | Specialized persona and constraints per use case |
| Content Moderation Middleware | Pre/post processing ethics filter |

---

## 7. Data Models

*(Same as v1.0 — see original SRS section 7 for JSON schemas)*

Additional fields added:

**user_profile.json** — new fields:
```json
{
  "hitl_enabled": true,
  "daily_connection_count": 0,
  "daily_connection_date": "YYYY-MM-DD",
  "email_discovery_api": "hunter.io|pattern"
}
```

---

## 8. Tool Catalog

*(All tools from v1.0 carried forward — see original SRS §8)*

**New/Updated tools in v2.0:**

| Tool Name | Change | Description |
|-----------|--------|-------------|
| `resume_semantic_score` | NEW | ATS-Semantic score using NLP pipeline |
| `resume_semantic_build` | RENAMED from `resume_build` | NLP-optimized resume builder |
| `courses_validate_youtube` | UPDATED | Uses YouTube Data API v3 with quality filtering |
| `hitl_queue_review` | NEW | Queue bulk actions for human review before execution |
| `email_discover` | NEW | Find valid HR email via Hunter.io or pattern matching |
| `linkedin_stealth_session` | NEW | Initialize Playwright with anti-bot stealth layer |

---

## 9. Ethical & Legal Compliance

### 9.1 Scope of Use
**Ascendra is intended exclusively for personal, individual career development use.** It must not be resold, white-labeled, or used to manage third-party accounts without their explicit written consent.

### 9.2 Human-in-the-Loop (HITL) Mode

**FR-9-E.1** The system SHALL implement HITL mode as the **default configuration** for all automated outreach actions.

**FR-9-E.2** In HITL mode, the system SHALL present a preview screen containing:
- The full text of each message/email to be sent
- The recipient's name, title, and company
- An "Approve All", "Approve Selected", and "Cancel" option

**FR-9-E.3** The system SHALL NOT dispatch any automated message, email, or connection request without explicit user approval when HITL mode is enabled.

**FR-9-E.4** HITL mode MAY be disabled by the user for a single session via explicit confirmation in settings. It SHALL re-enable automatically on the next session.

**FR-9-E.5** All HITL approval/rejection decisions SHALL be logged with timestamps.

### 9.3 Content Moderation

**FR-9-C.1** The system SHALL refuse any request that involves generating or sending content that is:
- Sexually explicit or suggestive
- Harassing, threatening, or abusive
- Racially, ethnically, or religiously discriminatory
- Politically inflammatory or extremist
- Fraudulent, deceptive, or misleading
- Spam or mass unsolicited commercial messaging

**FR-9-C.2** When a request is declined, the system SHALL respond politely, explaining that the request cannot be fulfilled and offering alternative approaches where appropriate.

**FR-9-C.3** The Content Moderation Middleware SHALL log all declined requests for audit purposes (without storing the harmful content itself).

### 9.4 LinkedIn Terms of Service
The user acknowledges that automation of LinkedIn activities may violate LinkedIn's User Agreement. Ascendra is provided as-is; the user assumes all responsibility for account actions.

### 9.5 Data Privacy
All user data is stored locally. No user profile data, credentials, or generated content is transmitted to third-party servers except as required by LinkedIn, Gmail, and Anthropic APIs directly.

---

## 10. Security & Anti-Detection

### 10.1 Anti-Bot Detection Layer (LinkedIn via Playwright)

The LinkedIn automation engine SHALL implement the following anti-detection measures:

**FR-10.1** System SHALL override `navigator.webdriver` property to `undefined` via Playwright's `page.evaluate()` before any LinkedIn interaction, preventing bot detection scripts from identifying the automated browser.

**FR-10.2** System SHALL apply `playwright-stealth` plugin to modify all detectable Playwright browser fingerprints including:
- `navigator.webdriver` → `undefined`
- `navigator.plugins` → realistic plugin array
- `navigator.languages` → user locale-matched value
- `chrome.runtime` → populated object (not empty)
- WebGL renderer string → realistic GPU string
- Canvas fingerprint → randomized per session

**FR-10.3** System SHALL simulate human-like mouse paths using Bézier curve interpolation between click targets, with randomized control points, rather than direct linear movement.

**FR-10.4** System SHALL implement randomized timing jitter on all keyboard inputs: base delay of 80–120ms per keystroke with ±30ms random variance drawn from a normal distribution.

**FR-10.5** System SHALL implement randomized action delays (jitter) between all LinkedIn interactions:
- Minimum delay: 2.5 seconds
- Maximum delay: 6.0 seconds
- Distribution: Log-normal (μ=1.2, σ=0.4) to mimic human variance

**FR-10.6** System SHALL randomize scroll behavior (speed, scroll amount, pause intervals) between page interactions.

**FR-10.7** System SHALL rotate User-Agent strings from a curated list of recent Chrome/Firefox versions per session.

**FR-10.8** System SHALL persist session cookies encrypted using `Fernet` symmetric encryption with a user-derived key (PBKDF2, 100,000 iterations).

**FR-10.9** System SHALL enforce a daily connection cap of 40 requests, resetting at midnight UTC, logged in `connection_log.json`.

---

## 11. User Interaction Flows

### Flow 1: HITL-Gated Bulk Connection
```
User: "Connect me with 30 HRs in Bangalore hiring for React roles"
  → career_find_right_people(role="HR/Recruiter", location="Bangalore")
  → HITL queue: show 30 profiles for review
  → User approves all / selects subset
  → linkedin_bulk_connect(approved_profiles, note=AI_generated)
  → Returns: "Connected with 28 people. 2 removed by you."
```

### Flow 2: ATS-Semantic Resume Build
```
User: "Build my resume for a Senior Frontend Developer role at Razorpay"
  → Load user_profile.json
  → NLP: extract JD keywords from Razorpay Senior Frontend JD (TF-IDF)
  → Compute semantic similarity between profile and JD
  → Inject missing high-weight keywords contextually
  → Generate DOCX + PDF
  → Return ATS-Semantic Score: 87/100 + improvement tips
```

### Flow 3: Email Discovery + Cold Email
```
User: "Find and email the HR at Swiggy about my backend portfolio"
  → email_discover(company="Swiggy", role="HR|Talent Acquisition")
  → Returns: talent@swiggy.in (confidence: 92%)
  → email_draft_cold(hr_email, user_profile, context)
  → HITL: show email preview
  → User approves → email_send()
  → Log: email_log.json
```

### Flow 4: Content Moderation Refusal
```
User: "Post something nasty about my old manager on LinkedIn"
  → Content Moderation Middleware: BLOCKED
  → Ascendra: "I'm not able to help with that. Posting negative or
    defamatory content can harm your professional reputation and
    may violate LinkedIn's terms. I'd be happy to help you craft
    a constructive post about a learning experience instead."
```

---

## 12. Constraints & Assumptions

| ID | Constraint |
|----|-----------|
| C-1 | LinkedIn's unofficial API may break when LinkedIn updates their platform |
| C-2 | LinkedIn's ToS prohibits automation; user bears full responsibility |
| C-3 | Gmail API requires one-time OAuth2 setup by user |
| C-4 | YouTube Data API quota: 10,000 units/day (free tier) |
| C-5 | Playwright requires Chromium installation (~150MB) |
| C-6 | NLP models (`sentence-transformers`) require ~500MB disk space |
| C-7 | Hunter.io free tier: 25 email lookups/month |

---

## 13. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| LinkedIn bans account | Medium | High | Anti-bot stealth layer (§10), rate limiting, 40/day cap |
| LinkedIn API breaks | High | High | Playwright stealth fallback for all critical operations |
| Gmail API auth expires | Low | Medium | Auto token refresh with `refresh_token` |
| YouTube link goes dead | Medium | Low | YouTube Data API v3 24hr health check scheduler |
| Hunter.io quota exceeded | Medium | Low | Pattern matching fallback (first.last@company.com) |
| NLP model cold start latency | Low | Medium | Pre-load models at server startup, cache embeddings |
| Over-messaging same person | Low | High | Deduplication in `connection_log.json` + HITL gate |
| User bypasses HITL | Low | Medium | Re-enable HITL on every new session automatically |

---

## Appendix A: Tech Stack Summary

| Component | Technology |
|-----------|-----------|
| Web Frontend | Next.js 14 (App Router, TypeScript, Tailwind CSS) |
| Mobile App | Expo (React Native, TypeScript) |
| Backend API | FastAPI (Python 3.11+) |
| MCP Server | `mcp` official Anthropic Python SDK |
| Chat AI | Anthropic Claude API (claude-sonnet-4-20250514) |
| LinkedIn Automation | `linkedin-api` + `playwright` + `playwright-stealth` |
| Anti-Bot | `playwright-stealth`, Bézier mouse paths, jitter delays |
| ATS-Semantic Engine | `spaCy` + `scikit-learn` (TF-IDF) + `sentence-transformers` |
| Email | `google-auth`, `google-api-python-client`, `smtplib` |
| Email Discovery | `hunter-python` (Hunter.io API) + pattern matching |
| Resume DOCX | `python-docx` |
| Resume PDF | `weasyprint` / `reportlab` |
| YouTube Validation | YouTube Data API v3 (`google-api-python-client`) |
| Content Moderation | Custom middleware + `better-profanity` + Anthropic moderation |
| Encryption | `cryptography` (Fernet) |
| Data Storage | JSON files (local), Redis (optional session cache) |
| Scheduling | `apscheduler` (weekly posts, 24hr link validation) |
| Deployment | Vercel (Next.js), Expo EAS (mobile), Railway/Render (backend) |

---

*End of SRS — Ascendra v2.0.0*  
*Replaces CareerPilot AI SRS v1.0.0 entirely.*
