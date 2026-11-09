"""Add the AI-generated questions to questions.json.

Run from the repository root:  python3 content/build_ai_questions.py

- 160 practice questions (20 per topic) with set = "bank": they join the practice pools and mixed exams.
- 50 mock-exam questions with set = "mock-exam": only used by the "AI mock exam" source in exam mode.
Every question has aiGenerated = true. Re-running replaces the previous AI questions, so the script is idempotent.
Each module checks its own arithmetic against a separate formula before anything is written.
"""
import json, sys
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ai_fr, ai_cs, ai_audit, ai_ma, ai_bud, ai_var, ai_cap, ai_cpm, ai_mock  # noqa: E402,F401  (import order = question order)
from ai_common import QUESTIONS  # noqa: E402

BANK_VERSION = '2026-11-09.2'

def main():
 path = HERE / 'questions.json'
 bank = json.loads(path.read_text())
 kept = [q for q in bank['questions'] if not q.get('aiGenerated')]
 ids = {q['id'] for q in kept}
 clash = [q['id'] for q in QUESTIONS if q['id'] in ids]
 assert not clash, clash
 bank['questions'] = kept + QUESTIONS
 bank['bankVersion'] = BANK_VERSION
 path.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n')
 per = Counter((q['set'], q['topic']) for q in QUESTIONS)
 print(f'Wrote {len(bank["questions"])} questions ({len(kept)} existing + {len(QUESTIONS)} AI-generated).')
 for (s, t), c in sorted(per.items()): print(f'  {s:9} {t}: {c}')

if __name__ == '__main__':
 main()
