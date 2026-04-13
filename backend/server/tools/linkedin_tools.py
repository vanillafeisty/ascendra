"""
Ascendra — LinkedIn Automation Engine v2.0
FR-10.1–FR-10.9: Full Anti-Bot Stealth Layer
"""
import time, math, random, json
from pathlib import Path
from datetime import datetime
from typing import Optional
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import (LINKEDIN_EMAIL, LINKEDIN_PASSWORD, LINKEDIN_MAX_CONNECTIONS_PER_DAY,
                    load_connection_log, save_connection_log, load_user_profile)

STEALTH_JS = """
Object.defineProperty(navigator,'webdriver',{get:()=>undefined});
Object.defineProperty(navigator,'plugins',{get:()=>{const a=[{name:'Chrome PDF Plugin',filename:'internal-pdf-viewer'},{name:'Native Client',filename:'internal-nacl-plugin'}];a.__proto__=PluginArray.prototype;return a;}});
Object.defineProperty(navigator,'languages',{get:()=>['en-US','en','hi']});
if(!window.chrome)window.chrome={};window.chrome.runtime={onConnect:null,onMessage:null};
const g=WebGLRenderingContext.prototype.getParameter;WebGLRenderingContext.prototype.getParameter=function(p){if(p===37445)return'Intel Open Source Technology Center';if(p===37446)return'Mesa DRI Intel(R) Iris(R) Plus';return g.call(this,p);};
"""

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
]

def _jitter(mu=1.2, sigma=0.4, lo=2.5, hi=6.0):
    """FR-10.5: Log-normal jitter delay."""
    return max(lo, min(hi, random.lognormvariate(mu, sigma)))

def _bezier_path(start, end, steps=16):
    """FR-10.3: Bézier curve mouse path."""
    x0,y0 = start; x3,y3 = end; dx,dy = x3-x0, y3-y0
    cx1=x0+dx*random.uniform(0.15,0.35)+random.randint(-18,18)
    cy1=y0+dy*random.uniform(0.1,0.3)+random.randint(-18,18)
    cx2=x0+dx*random.uniform(0.65,0.85)+random.randint(-18,18)
    cy2=y0+dy*random.uniform(0.65,0.85)+random.randint(-18,18)
    path=[]
    for i in range(steps+1):
        t=i/steps; inv=1-t
        x=int(inv**3*x0+3*inv**2*t*cx1+3*inv*t**2*cx2+t**3*x3)
        y=int(inv**3*y0+3*inv**2*t*cy1+3*inv*t**2*cy2+t**3*y3)
        path.append((x,y))
    return path

def _type_jitter(page, selector, text):
    """FR-10.4: Keystroke jitter (80–120ms ±30ms normal)."""
    page.click(selector)
    for ch in text:
        page.keyboard.type(ch)
        time.sleep(max(0.05, min(0.18, random.gauss(0.1, 0.03))))

def _stealth_page(playwright):
    """FR-10.1–10.7: Full stealth browser context."""
    ua = random.choice(USER_AGENTS)
    browser = playwright.chromium.launch(headless=True, args=[
        '--disable-blink-features=AutomationControlled','--disable-infobars',
        '--no-sandbox','--disable-dev-shm-usage',])
    ctx = browser.new_context(user_agent=ua,
        viewport={'width':random.randint(1200,1440),'height':random.randint(760,900)},
        locale='en-US', timezone_id='Asia/Kolkata',
        extra_http_headers={'Accept-Language':'en-US,en;q=0.9'})
    page = ctx.new_page()
    page.add_init_script(STEALTH_JS)
    return browser, ctx, page

def _login(page):
    page.goto('https://www.linkedin.com/login', wait_until='domcontentloaded')
    time.sleep(_jitter(0.8,0.2,1.0,2.5))
    _type_jitter(page,'#username',LINKEDIN_EMAIL)
    time.sleep(_jitter(0.5,0.2,0.5,1.5))
    _type_jitter(page,'#password',LINKEDIN_PASSWORD)
    time.sleep(_jitter(0.5,0.2,0.8,1.8))
    page.keyboard.press('Enter')
    page.wait_for_url('**/feed/**',timeout=20000)
    time.sleep(_jitter(1.0,0.3,1.5,3.0))

def _get_client():
    try:
        from linkedin_api import Linkedin
        return Linkedin(LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
    except ImportError:
        raise RuntimeError("pip install linkedin-api")
    except Exception as e:
        raise RuntimeError(f"LinkedIn login failed: {e}")

def get_my_profile():
    c=_get_client(); p=c.get_profile()
    return {"name":f"{p.get('firstName','')} {p.get('lastName','')}".strip(),
            "headline":p.get("headline",""),"summary":p.get("summary",""),
            "location":p.get("locationName",""),"connections":p.get("connections",0),
            "skills":p.get("skills",[]),"experience":p.get("experience",[]),
            "education":p.get("education",[]),"certifications":p.get("certifications",[])}

def score_linkedin_profile():
    profile=get_my_profile(); score=0; suggestions=[]
    checks=[("name",bool(profile.get("name")),10,"[+10] Add full name"),
            ("headline",len(profile.get("headline",""))>30,15,"[+15] Write compelling 120-char headline"),
            ("summary",len(profile.get("summary",""))>150,15,"[+15] Add 3-paragraph About section"),
            ("location",bool(profile.get("location")),5,"[+5] Add location"),
            ("experience",len(profile.get("experience",[]))>0,15,"[+15] Add experience/projects"),
            ("education",len(profile.get("education",[]))>0,10,"[+10] Add education"),
            ("skills",len(profile.get("skills",[]))>=5,10,"[+10] Add 5+ skills"),
            ("certifications",len(profile.get("certifications",[]))>0,10,"[+10] Add certifications"),
            ("connections",profile.get("connections",0)>=50,5,"[+5] Grow to 500+ connections"),
            ("profile_complete",bool(profile.get("summary")),5,"[+5] Complete all sections")]
    for _,cond,pts,sug in checks:
        if cond: score+=pts
        else: suggestions.append(sug)
    return {"score":score,"grade":"A"if score>=90 else"B"if score>=75 else"C"if score>=60 else"D","suggestions":suggestions}

def suggest_profile_photo_guidelines():
    return {"guidelines":["✅ Recent photo (last 2 years)","✅ Professional attire — solid colors","✅ Face 60–70% of frame","✅ Neutral background","✅ Natural confident smile","✅ Min 400x400px","✅ Square crop","❌ No group photos","❌ No selfies","❌ No casual settings"],"pro_tip":"Professional headshot = 21x more profile views."}

def search_people(role,company=None,location=None,limit=20):
    c=_get_client(); kw=role+(f" {company}" if company else "")
    results=c.search_people(keywords=kw,network_depths=["F","S"],regions=[location] if location else None,limit=limit)
    return [{"profile_id":r.get("public_id") or r.get("entityUrn","").split(":")[-1],
             "name":f"{r.get('firstName','')} {r.get('lastName','')}".strip(),
             "title":r.get("headline",""),"location":r.get("subLine",""),
             "connection_degree":r.get("distance",{}).get("value","UNKNOWN")} for r in results]

def send_connection_request(profile_id,note="",person_name=""):
    log=load_connection_log()
    if profile_id in {c["profile_id"] for c in log["connections"]}:
        return {"success":False,"reason":"Already connected/pending"}
    today=datetime.utcnow().date().isoformat()
    today_count=sum(1 for c in log["connections"] if c.get("sent_at","")[:10]==today and c["status"]=="pending")
    if today_count>=LINKEDIN_MAX_CONNECTIONS_PER_DAY:
        return {"success":False,"reason":f"Daily limit of {LINKEDIN_MAX_CONNECTIONS_PER_DAY} reached"}
    c=_get_client(); time.sleep(_jitter())
    try:
        c.add_connection(profile_id,message=note[:300])
        log["connections"].append({"profile_id":profile_id,"name":person_name,"status":"pending",
            "sent_at":datetime.utcnow().isoformat(),"note_sent":note[:300],"message_sent":False})
        save_connection_log(log)
        return {"success":True,"message":f"Connection sent to {person_name or profile_id}"}
    except Exception as e:
        return {"success":False,"reason":str(e)}

def bulk_connect(role,company=None,location=None,count=20,note_template=""):
    people=search_people(role=role,company=company,location=location,limit=count*2)
    sent=skipped=failed=0; details=[]
    for person in people:
        if sent>=count: break
        note=note_template.replace("{name}",(person["name"].split()[0] if person["name"] else "there"))
        result=send_connection_request(person["profile_id"],note,person["name"])
        if result["success"]: sent+=1; details.append(f"✅ {person['name']}")
        elif "Already" in result.get("reason",""): skipped+=1
        else: failed+=1; details.append(f"❌ {person['name']}: {result.get('reason','')}")
        time.sleep(_jitter())
    return {"sent":sent,"skipped_duplicates":skipped,"failed":failed,"details":details,"summary":f"Sent {sent}, {skipped} duplicates, {failed} failed."}

def send_message(profile_id,message,person_name=""):
    log=load_connection_log()
    for conn in log["connections"]:
        if conn["profile_id"]==profile_id and conn.get("message_sent"):
            return {"success":False,"reason":f"Already messaged {person_name or profile_id}"}
    c=_get_client(); time.sleep(_jitter())
    try:
        pd=c.get_profile(public_id=profile_id); urn=pd.get("entityUrn","")
        c.send_message(message_body=message,recipients=[urn])
        for conn in log["connections"]:
            if conn["profile_id"]==profile_id: conn["message_sent"]=True; conn["last_message"]=message[:100]
        save_connection_log(log)
        return {"success":True,"message":f"Message sent to {person_name or profile_id}"}
    except Exception as e:
        return {"success":False,"reason":str(e)}

def bulk_message(profile_ids,message_template,names=None):
    sent=failed=0; details=[]
    for i,pid in enumerate(profile_ids):
        name=names[i] if names and i<len(names) else ""
        first=name.split()[0] if name else "there"
        msg=message_template.replace("{name}",first).replace("{first_name}",first)
        result=send_message(pid,msg,name)
        if result["success"]: sent+=1; details.append(f"✅ {name or pid}")
        else: failed+=1; details.append(f"❌ {name or pid}: {result.get('reason','')}")
        time.sleep(_jitter())
    return {"sent":sent,"failed":failed,"details":details,"summary":f"Messages sent: {sent}/{len(profile_ids)}"}

def update_headline(headline):
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser,ctx,page=_stealth_page(p)
            _login(page)
            page.goto("https://www.linkedin.com/in/me/"); time.sleep(_jitter())
            page.click("button[aria-label='Edit intro']")
            page.wait_for_selector("#headline",timeout=6000)
            page.fill("#headline",""); _type_jitter(page,"#headline",headline[:220])
            time.sleep(_jitter(0.6,0.2,0.8,1.5))
            page.click("button[aria-label='Save']"); time.sleep(1.5); browser.close()
        return {"success":True,"headline":headline,"message":"Headline updated!"}
    except Exception as e:
        return {"success":False,"reason":str(e)}

def create_text_post(content,hashtags=None):
    try:
        from playwright.sync_api import sync_playwright
        full=content
        if hashtags: full+="\n\n"+" ".join(f"#{t.strip('#')}" for t in hashtags)
        with sync_playwright() as p:
            browser,ctx,page=_stealth_page(p)
            _login(page); time.sleep(_jitter())
            page.click(".share-box-feed-entry__trigger")
            page.wait_for_selector(".ql-editor",timeout=8000)
            _type_jitter(page,".ql-editor",full); time.sleep(_jitter())
            page.click("button.share-actions__primary-action"); time.sleep(2.5); browser.close()
        return {"success":True,"message":"Post published!","preview":full[:120]}
    except Exception as e:
        return {"success":False,"reason":str(e)}
