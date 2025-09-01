from fastapi import APIRouter, HTTPException
from app.services.haru_course import get_syllabus, get_lesson

router = APIRouter()

@router.get("/course/{level}/syllabus")
def syllabus(level: str):
    try:
        return get_syllabus(level)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/course/{level}/lesson/{lesson_id}")
def lesson(level: str, lesson_id: str):
    data = get_lesson(level, lesson_id)
    if not data:
        raise HTTPException(status_code=404, detail="Leccion no encontrada")
    return data
