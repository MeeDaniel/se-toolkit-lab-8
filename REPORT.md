# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent
Using config: /home/operator/se-toolkit-lab-8/nanobot/config.json

🐈 nanobot
The agentic loop is the fundamental cycle that autonomous AI agents follow to accomplish
tasks. It typically consists of these core stages:

 1 Perceive — Gather information from the environment (user input, tool outputs,        
   external data)
 2 Reason/Plan — Analyze the situation, determine goals, and decide on actions
 3 Act — Execute actions using available tools (file operations, API calls, shell       
   commands, etc.)
 4 Observe — Receive feedback from the actions taken
 5 Repeat — Continue the loop until the goal is achieved or a stopping condition is met 

This loop enables agents to:

 • Break complex tasks into steps
 • Adapt based on feedback
 • Use tools autonomously
 • Handle multi-turn workflows

In my case, each time you give me a task, I go through this loop: I understand your     
request, decide what tools might help, execute them, observe the results, and either    
complete the task or iterate further.

The sophistication of an agent depends on how well it can reason, what tools it has     
access to, and how effectively it can learn from observations within this loop.

operator@se-toolkit008:~/se-toolkit-lab-8/nanobot$ uv run nanobot agent -c ./config.json
 -m "What labs are available in our LMS?"
Using config: /home/operator/se-toolkit-lab-8/nanobot/config.json

🐈 nanobot
Based on the lab tasks in your LMS system, here are the available labs:

Required Labs


 Lab     Title                                                                          
 ────────────────────────────────────────────────────────────────────────────────────── 
 Task 1  Set Up the Agent — Install nanobot, connect to LLM/LMS via MCP, write skill    
         prompts
 Task 2  Deploy the Agent and Add a Web Client — Docker gateway, WebSocket channel,     
         Flutter client
 Task 3  Give the Agent New Eyes — Structured logging, traces, observability MCP tools  
 Task 4  Diagnose a Failure and Make the Agent Proactive — Investigation, cron health   
         checks, bug fix
 Task 5  Merged into Task 4


Optional Labs


 Lab              Title                                                                 
 ────────────────────────────────────────────────────────────────────────────────────── 
 Optional Task 1  Add a Telegram Bot Client — Alternative client via Telegram (blocked  
                  from Russian VMs)


The LMS backend exposes these labs via MCP tools like lms_labs, lms_pass_rates, etc.,   
which your nanobot agent can query once configured.

Would you like details on a specific lab?

## Task 1B — Agent with LMS tools

operator@se-toolkit008:~/se-toolkit-lab-8$ cd nanobot && uv run nanobot agent -c ./config.json -m "What labs are
> available?"
Using config: /home/operator/se-toolkit-lab-8/nanobot/config.json
                                                                                        
🐈 nanobot
Here are the labs available in your LMS:


 ID  Lab Title
 ───────────────────────────────────────────────────────────
 1   Lab 01 – Products, Architecture & Roles
 2   Lab 02 — Run, Fix, and Deploy a Backend Service
 3   Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4   Lab 04 — Testing, Front-end, and AI Agents
 5   Lab 05 — Data Pipeline and Analytics Dashboard
 6   Lab 06 — Build Your Own Agent
 7   Lab 07 — Build a Client with an AI Coding Agent
 8   lab-08


You're currently working on Lab 08 (The Agent is the Interface) — setting up nanobot,   
deploying it with a web client, adding observability tools, and making the agent        
proactive.

Would you like details on any specific lab, such as pass rates, completion rates, or top
learners?

## Task 1C — Skill prompt

operator@se-toolkit008:~/se-toolkit-lab-8$ cd nanobot && uv run nanobot agent -c ./config.json -m "Show me the scores"
Using config: /home/operator/se-toolkit-lab-8/nanobot/config.json
⠙ nanobot is thinking...
                                                                                        
🐈 nanobot
Which lab would you like to see scores for?

Available labs:


 ID  Lab   
 ──────────
 1   lab-01
 2   lab-02
 3   lab-03
 4   lab-04
 5   lab-05
 6   lab-06
 7   lab-07
 8   lab-08


Just say something like:

 • "lab-04"
 • "Show scores for lab-06"
 • "All labs" (I'll fetch an overview)

## Task 2A — Deployed agent

```
nanobot-1  | 2026-03-27 13:05:29.665 | INFO     | nanobot.channels.manager:_init_channels:54 - WebChat channel enabled
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | 2026-03-27 13:05:30.605 | INFO     | nanobot_webchat.channel:start:72 - WebChat starting on 0.0.0.0:8765
nanobot-1  | 2026-03-27 13:05:32.412 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:182 - MCP server 'lms': connected, 9 tools registered
nanobot-1  | 2026-03-27 13:05:32.412 | INFO     | nanobot.agent.loop:run:260 - Agent loop started
```

## Task 2B — Web client

**Flutter client accessible at:** `http://<your-vm-ip>:42002/flutter/`

**Login with:** `NANOBOT_ACCESS_KEY` (set in `.env.docker.secret`)

**Test conversation:**

```
Q: "What can you do in this system?"

A: I'm nanobot 🐈, your AI assistant. Here's what I can do in this system:

## Core Capabilities

### 📁 File & Workspace Operations
- Read, write, and edit files
- List directory contents (including recursive exploration)
- Execute shell commands (with safety limits)

### 🌐 Web & Information
- Search the web for information
- Fetch and extract content from URLs

### ⏰ Scheduling & Reminders
- Create one-time or recurring reminders
- Manage scheduled tasks via cron

### 🤝 Communication
- Send messages to specific channels (Telegram, Discord, etc.)
- Spawn subagents for complex or long-running tasks

### 🧠 Memory System
- Store important facts in long-term memory (MEMORY.md)
- Log events in a searchable history (HISTORY.md)

## Available Skills

| Skill | Description |
|-------|-------------|
| **memory** | Two-layer memory with grep-based recall |
| **lms** | Learning Management System integration |
| **clawhub** | Search/install skills from public registry |
| **skill-creator** | Create or update custom skills |
| **cron** | Schedule reminders and recurring tasks |

## LMS Integration

I can access a Learning Management System to:
- List labs and learners
- Check pass rates, completion rates, and timelines
- View group performance and top learners
- Trigger sync pipelines
```

**WebSocket test:**
```bash
docker exec se-toolkit-lab-8-nanobot-1 /app/.venv/bin/python -c "
import asyncio, websockets, json
async def test():
    async with websockets.connect('ws://caddy:80/ws/chat?access_key=my-secret-nanobot-key') as ws:
        await ws.send(json.dumps({'content': 'What labs are available?'}))
        print(await asyncio.wait_for(ws.recv(), timeout=30))
asyncio.run(test())
"
```

Response:
```json
{"type":"text","content":"Here are the available labs:\n\n1. **Lab 01** – Products, Architecture & Roles\n2. **Lab 02** — Run, Fix, and Deploy a Backend Service\n...","format":"markdown"}
```

## Task 3A — Structured logging

**Happy-path log excerpt (PostgreSQL running):**

```
2026-03-27 14:45:03,506 INFO [app.main] [main.py:60] [trace_id=4be42e30b88c345492dd50a68f947656 span_id=cc151a40566d3ed2] - request_started
2026-03-27 14:45:03,507 INFO [app.auth] [auth.py:30] [trace_id=4be42e30b88c345492dd50a68f947656 span_id=cc151a40566d3ed2] - auth_success
2026-03-27 14:45:03,508 INFO [app.db.items] [items.py:16] [trace_id=4be42e30b88c345492dd50a68f947656 span_id=cc151a40566d3ed2] - db_query
2026-03-27 14:45:03,625 INFO [app.main] [main.py:68] [trace_id=4be42e30b88c345492dd50a68f947656 span_id=cc151a40566d3ed2] - request_completed
```

**Error-path log excerpt (PostgreSQL stopped):**

```
socket.gaierror: [Errno -2] Name or service not known
  File "/app/.venv/lib/python3.14/site-packages/asyncpg/connect_utils.py", line 1249, in _connect
    raise last_error or exceptions.TargetServerAttributeNotMatched
```

**VictoriaLogs query result:**

Query: `_time:1h`

```json
{"_msg":"request_completed","event":"request_completed","severity":"INFO","status":"200","trace_id":"4be42e30b88c345492dd50a68f947656"}
{"_msg":"db_query","event":"db_query","operation":"select","table":"item","trace_id":"4be42e30b88c345492dd50a68f947656"}
{"_msg":"unhandled_exception","event":"unhandled_exception","exception.message":"-2","severity":"ERROR"}
```

**VictoriaLogs UI:** Accessible at `http://localhost:42002/utils/victorialogs/select/vmui`

## Task 3B — Traces

**VictoriaTraces UI:** Accessible at `http://localhost:42002/utils/victoriatraces`

**Healthy trace structure:**
- `trace_id` links all spans for one request
- Span hierarchy: `request_started` → `auth_success` → `db_query` → `request_completed`
- Each span has `span_id`, `trace_id`, `service.name`, `severity`

**Error trace structure:**
- Same `trace_id` but includes `unhandled_exception` span
- Exception stack trace in log metadata
- `request_completed` with status 500

## Task 3C — Observability MCP tools

**Normal conditions response:**

```
Q: "Any errors in the last hour?"

A: I'll check for errors in the last hour using the observability tools.

Yes, there was **1 error** in the last hour:

**Error Summary:**
- **Time:** 2026-03-27 14:42 UTC
- **Service:** Learning Management Service
- **Type:** `socket.gaierror: [Errno -2] Name or service not known`
- **Endpoint:** `/pipeline/sync`

**What happened:**
The LMS sync pipeline failed because it couldn't resolve the database hostname. 
This is a DNS/connection issue when trying to connect to the PostgreSQL database 
via asyncpg. The error occurred during an ETL load operation (`load_items` → `sync`).

This appears to be a transient infrastructure issue rather than a code bug.
```

**After triggering failure (PostgreSQL stopped):**

```
Q: "Any errors in the last hour?"

A: Found 3 errors in the last hour, all from Learning Management Service.

Error details:
- socket.gaierror: Database connection failure
- unhandled_exception: Pipeline sync failed
- db_query: [Errno -2] Name or service not known
```

**MCP tools implemented:**
- `logs_search` — Search logs using LogsQL queries
- `logs_error_count` — Count errors per service over a time window

**Skill prompt:** `nanobot/workspace/skills/observability/SKILL.md`

## Task 4A — Multi-step investigation

**With PostgreSQL stopped, asked: "What went wrong?"**

```
🔍 System Failure Investigation

Summary

What went wrong: The LMS backend failed to connect to PostgreSQL database 
twice in the last 2 hours, causing the ETL pipeline sync to crash.

📊 Error Overview

 Metric                  Value
 ────────────────────────────────────────────────────────────────────────────
 Total Errors (2 hours)  2
 Affected Service        Learning Management Service
 Error Type              socket.gaierror: [Errno -2] Name or service not known
 Failed Endpoint         POST /pipeline/sync
 Root Cause              PostgreSQL container unreachable (DNS resolution failure)

📋 Log Evidence

Error 1 — Most Recent
 Time      2026-03-27T15:34:02
 Trace ID  36f90cf0946e174d5867001e0c2656c0
 Event     unhandled_exception
 Severity  ERROR
 Path      /pipeline/sync

🔬 Root Cause Analysis

What Happened (Call Chain)

 POST /pipeline/sync
   └─► app/routers/pipeline.py:19 (post_sync)
        └─► app/etl.py:230 (sync)
             └─► app/etl.py:112 (load_items)
                  └─► session.exec(...)  ← SQLModel/SQLAlchemy
                       └─► asyncpg.connect()
                            └─► socket.gaierror: [Errno -2] Name or service not known

Why It Happened

The backend tried to connect to PostgreSQL but DNS resolution failed. This means:
1. PostgreSQL container was stopped — the service name 'postgres' doesn't resolve
   when the container isn't running
2. Or network issue — containers can't reach each other on lms-network
```

**Investigation flow:**
1. Agent called `logs_error_count` to find errors in the last 2 hours
2. Called `logs_search` to get detailed error logs
3. Extracted trace IDs from error logs
4. Presented coherent narrative with call chain analysis

## Task 4B — Proactive health check

**Created health check via Flutter chat:**

```
Q: "Create a health check for this chat that runs every 2 minutes. Each run should 
check for backend errors in the last 2 minutes, and post a short summary here. If 
there are no recent errors, say the system looks healthy. Use your cron tool."

A: Created the health check job (ID: cac9855e) that runs every 2 minutes.
```

**Proactive health report from cron job (while PostgreSQL stopped):**

```
🐾 **Health Check** (2026-03-27 15:41 UTC)

⚠️ **System UNHEALTHY**

Issues detected in the last 2 minutes:
- LMS backend returning HTTP 404 errors
- Database connection failures (PostgreSQL unreachable)
- ETL pipeline sync failed

Root cause: PostgreSQL container is stopped, causing DNS resolution failure 
when backend tries to connect.

*Next check in 2 minutes...*
```

**Nanobot logs showing cron execution:**

```
2026-03-27 15:41:56.923 | INFO | nanobot.cron.service:_execute_job:248 - Cron: executing job 'Health check: Check backend er' (cac9855e)
2026-03-27 15:42:29.922 | INFO | nanobot.cron.service:_execute_job:257 - Cron: job 'Health check: Check backend er' completed
2026-03-27 15:42:29.921 | INFO | nanobot.utils.evaluator:evaluate_response:87 - evaluate_response: should_notify=True, reason=Health check detected actual backend errors (database connection failures) that require attention and action.
```

**Job removal:**

```
Q: "Remove the health check job"
A: [Job cac9855e removed]
```

## Task 4C — Bug fix and recovery

**1. Root cause — the planted bug:**

File: `backend/app/routers/items.py`, function `get_items()`

The bug was a **catch-all exception handler** that converted ALL exceptions to HTTP 404 "Items not found":

```python
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    """Get all items."""
    try:
        return await read_items(session)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Items not found",
        ) from exc  # ← BUG: Converts database errors to 404
```

**Problem:** When PostgreSQL was down, database connection errors (socket.gaierror) were being converted to 404 errors, masking the real issue and misleading both users and the agent.

**2. The fix:**

Removed the catch-all exception handler. Let the global exception handler in `main.py` handle errors properly as 500 Internal Server Error:

```python
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    """Get all items."""
    return await read_items(session)  # ← No try/except, let errors propagate
```

**3. Post-fix failure check (with PostgreSQL stopped):**

After redeploy, asked "What went wrong?":

```
🔍 System Failure Investigation

Summary: The LMS backend cannot connect to PostgreSQL. 4 errors in the last 2 hours,
all caused by database connection failures.

📊 Error Overview
 Metric                  Value
 ────────────────────────────────────────────────────
 Total Errors (2 hours)  4 ⚠️
 Affected Service        Learning Management Service
 Error Type              socket.gaierror: [Errno -2] Name or service not known
 Root Cause              PostgreSQL container unreachable (DNS resolution failure)
```

The agent now correctly identifies the **real database error** instead of seeing misleading 404s.

**4. Healthy follow-up (after PostgreSQL restarted):**

```
🏥 System Health Check

Time: 2026-03-27 18:49 MSK

✅ Good News — System Recovered!

 Component      Status          Details
 ─────────────────────────────────────────────────────
 LMS Backend    🟢 HEALTHY      Item count: 56
 PostgreSQL     🟢 Connected    DNS resolution working
 API Endpoints  🟢 Operational  Responding normally

📊 Error Summary (Last Hour)
 Metric                 Value
 ────────────────────────────────────────────────────
 Total Errors           5 (all historical)
 New Errors Since Then  ✅ None
```
