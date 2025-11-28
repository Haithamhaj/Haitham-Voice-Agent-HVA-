CLASSIFY_MEMORY_PROMPT = """
Analyze the following content and classify it for a personal knowledge management system.

Content:
"{content}"

Context (if any):
{context}

Return a JSON object with the following fields:
- project: The most relevant project (e.g., "Mind-Q", "AI Coach", "Personal", "Health", "Business", "General"). Infer from content.
- topic: A specific topic or subject (2-5 words).
- type: One of ["idea", "decision", "question", "task", "note", "issue", "reflection", "reminder", "insight"].
- tags: List of 3-7 relevant keywords/tags.
- sentiment: "positive", "neutral", or "negative".
- importance: Integer 1-5 (1=low, 5=critical).
- confidence: Float 0.0-1.0 (how confident are you in this classification).

JSON:
"""

SUMMARIZE_MEMORY_PROMPT = """
Generate a multi-level summary for the following content.

Content:
"{content}"

Return a JSON object with:
- ultra_brief: A single sentence summary (max 20 words).
- executive_summary: A list of 3-5 bullet points covering key details.
- detailed_summary: A comprehensive paragraph (or two) capturing all important information.
- key_insights: List of any specific insights or realizations.
- decisions: List of any decisions made.
- action_items: List of any tasks or next steps.
- open_questions: List of unresolved questions.
- people_mentioned: List of names mentioned.
- projects_mentioned: List of project names mentioned.

JSON:
"""
