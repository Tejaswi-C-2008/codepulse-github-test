from uuid import UUID
from datetime import date

from backend.models.ai_runs import AIRunCreate


test_data = AIRunCreate(
    user_id=UUID("00000000-0000-0000-0000-000000000001"),
    week=date(2026, 9, 7),
    prompt_version="v1",
    input_snapshot_hash="test-hash-123",
    output_text="Developer health analysis generated successfully.",
    eval_scores={
        "quality": 0.90,
        "relevance": 0.95
    }
)

print("AI Runs model verified successfully")
print(test_data)