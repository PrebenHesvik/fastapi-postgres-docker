from fastapi import HTTPException, status

LEVEL_OF_IMPORTANCE = (
    "low",
    "medium",
    "high",
    "critical",
)


def validate_level_of_importance(cls, value: dict) -> dict:
    level = value.get("level")
    if level not in LEVEL_OF_IMPORTANCE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{level} is not a valid region.",
        )
    return value
