# Server outage and recovery — 2026-11-24

The owner reported “Failed to fetch” followed by “The local error log could not be saved.” The shared browser retained failed attempts at the original crew-selection question and the explicit diagnostic question. Browser events reported connection refusal. A separate local connection check confirmed no listener on port 8765. The cause of the process termination was not established.

This was an application availability failure before retrieval could run. Because the browser sends diagnostic events to the same server, the outage prevented those events from being persisted. Existing log entries do not document these failed attempts. This note records the owner report and direct inspection; it is not a retrospective automatic log entry. No failed event was silently marked as saved or inserted as a synthetic production diagnostic.

## Recovery

Started the existing `mars-rag serve` command as a detached local process, with a new session, stdin disconnected and stdout/stderr redirected to ignored `logs/server.log`. Its PID is recorded in ignored `logs/server.pid`. This removes the immediate dependency on a foreground tool command remaining attached. A later tool invocation must still confirm availability; detachment is not a guarantee against every host lifecycle policy.

Retried the diagnostic question in the existing browser without reloading or clearing its thread. It returned five passages, led by DRA 5.0 PDF p. 81. No owner review was submitted or changed. No retrieval configuration, application code or source collection changed.

This does not install a login/startup service, restart automatically after a crash or survive a reboot by design. Offline diagnostic queueing remains unimplemented. A user-owned terminal running `.venv/bin/mars-rag serve` remains a supported way to keep the local app available while working; do not start a second server while port 8765 is occupied.

## Lesson

A failed search can be an availability failure or an evidence-relevance failure. Check reachability before drawing conclusions about retrieval quality. A server-side logger cannot capture requests that never reach it; a browser save-failure message must be treated as an actual diagnostics gap.
