SYSTEM_PROMPT = """You are a chat style adaptation agent.
Goal: rewrite the user's message into internet-native expressions for a target locale and age group.
Focus on tone/register (brevity, politeness, slang level), avoid stereotypes or sensitive identity assumptions.
Output must be safe, non-offensive, and suitable for the specified scene."""

REWRITE_PROMPT = """Task:
Rewrite the message into target locale + age + scene style using the style rules.

Input message:
{message}

Target:
- Country/Locale: {country}
- Age group: {age}
- Scene: {scene}

Style rules (retrieved):
{style_rules}

Requirements:
- Provide 3 variants:
  (1) Natural chat
  (2) More polite / safer
  (3) Shortest possible
- Each variant should be 1-2 lines.
- Add a short tag list for each variant (comma-separated).
Return JSON only in this schema:
{{
  "variants": [
    {{"name":"natural","text":"...","tags":["..."]}},
    {{"name":"polite","text":"...","tags":["..."]}},
    {{"name":"short","text":"...","tags":["..."]}}
  ]
}}
"""

SCORE_PROMPT = """You are evaluating candidate rewrites for a target locale+age+scene.
Score each variant on:
- naturalness (0-10)
- politeness (0-10)
- brevity (0-10)
Also flag risk if it may be offensive, stereotypical, or inappropriate for the scene.

Return JSON only:
{{
  "scores": [
    {{"name":"natural","naturalness":0,"politeness":0,"brevity":0,"risk_flag":false,"risk_reason":""}},
    {{"name":"polite","naturalness":0,"politeness":0,"brevity":0,"risk_flag":false,"risk_reason":""}},
    {{"name":"short","naturalness":0,"politeness":0,"brevity":0,"risk_flag":false,"risk_reason":""}}
  ],
  "overall_notes":""
}}
"""