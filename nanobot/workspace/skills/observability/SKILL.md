# Observability Skill

You have access to VictoriaLogs for querying structured logs and error counts.

## Available Tools

| Tool | Purpose | Parameters |
|------|---------|------------|
| `logs_search` | Search logs using LogsQL queries | `query` (LogsQL query, default "*"), `limit` (max results, default 20) |
| `logs_error_count` | Count errors per service over a time window | `service` (optional filter), `hours` (time window, default 1) |

## When to Use These Tools

### User asks "What went wrong?" or "Check system health"

This is a **multi-step investigation**. Follow this flow:

1. **Check for recent errors** — Call `logs_error_count` with `hours=1` (or last 15 minutes if specified)
2. **If errors found** — Call `logs_search` with query for recent errors to get details
3. **Extract trace ID** — From the error logs, find any `trace_id` field
4. **Fetch trace details** — If you have trace tools available, fetch the full trace
5. **Summarize findings** — Present a coherent investigation summary:
   - What failed (endpoint, operation)
   - Root cause (error message, exception type)
   - When it happened
   - Affected service
   - Trace ID for debugging

**Do NOT dump raw JSON.** Synthesize the information into a clear narrative.

### User asks about errors or issues
If the user asks "Any errors?", "What's broken?", "Show me errors", or similar:
1. Call `logs_error_count` with `hours=1` (or the specified time window)
2. Present the results clearly: "Found X errors in the last Y hours"
3. Break down by service if multiple services have errors

### User asks to search for specific events
If the user asks "Find logs about X", "Search for Y", or mentions a specific error:
1. Call `logs_search` with an appropriate LogsQL query
2. For service-specific searches, use: `service.name="Service Name" AND keyword`
3. Present results concisely — summarize, don't dump raw JSON

### User asks about a specific service
If the user asks "Is backend working?", "Any issues with X service?":
1. Call `logs_error_count` with `service="Service Name"`
2. If errors found, call `logs_search` to get details

## LogsQL Query Examples

- All logs: `*`
- Errors only: `level:error OR severity:error OR event:unhandled_exception`
- Service-specific: `service.name="Learning Management Service"`
- Service errors: `_stream:{service.name="Learning Management Service"} AND (level:error OR event:unhandled_exception)`
- By trace ID: `trace_id=abc123`

## Formatting Results

- **Error counts**: "Found **X errors** in the last **Y hours**" followed by a breakdown table
- **Log search**: Summarize key findings, mention trace IDs if relevant
- **Keep it concise**: Lead with the answer, offer more details if needed

## Example Interactions

**User:** "Any errors in the last hour?"
**You:** [Calls `logs_error_count` with `hours=1`] "Found 3 errors in the last hour, all from Learning Management Service. Would you like to see the details?"

**User:** "Show me errors from the backend"
**You:** [Calls `logs_error_count` with `service="Learning Management Service"`] "The Learning Management Service has 2 errors. Here are the details: [summary]"

**User:** "Search for database connection errors"
**You:** [Calls `logs_search` with `query="database OR db_query AND error"`] "Found 5 logs matching your query. The most recent shows: [brief summary]"

## When No Errors Found

If `logs_error_count` returns zero errors:
- "No errors found in the last X hours. The system appears healthy."
- Offer to check a different time window: "Would you like me to check a longer period?"

## When VictoriaLogs is Unavailable

If the tools return connection errors:
- "I'm unable to connect to VictoriaLogs right now. The observability system may be experiencing issues."
- Suggest alternatives: "You can check the VictoriaLogs UI directly at http://localhost:42002/utils/victorialogs/select/vmui"
