# Customer email: self-host usage tracking and limits

Subject: Per-user usage tracking and spend limits are ready

Hi [Name],

Per-user LLM usage tracking and spend limits are now available for self-hosted
camelAI. You need selfhost-v0.1.14 or later. A normal upgrade generates the
admin API key used to manage the feature.

There is no UI for this. As with the rest of self-hosting, point your coding
agent at the docs and tell it what you want. For example, "Read
https://docs.camelai.dev/self-hosting/spend-limits and set a rolling 24-hour
limit of $5 for <user>." The endpoints are documented on the same pages if you
prefer to script them directly:

https://docs.camelai.dev/self-hosting/usage-tracking
https://docs.camelai.dev/self-hosting/spend-limits

Two details are worth knowing before you set limits:

- A limit denies the next LLM pull after spend reaches the cap. A pull already
  in progress finishes, and concurrent pulls can settle afterward, so spend can
  slightly exceed the limit.
- Limits fail closed if usage cannot be priced. Built-in models are priced
  automatically. If you use custom model IDs, add exact pricing overrides before
  enabling limits.

If you would like help choosing limits for your team, reply here and we can work
through it with you.

Best,

The camelAI team
