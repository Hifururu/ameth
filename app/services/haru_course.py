import json, os

DATA_DIR = os.path.join("data", "haru")

def _path_for_level(level: str) -> str:
    return os.path.join(DATA_DIR, f"course_{level.lower()}.json")

def load_course(level: str) -> dict:
    fp = _path_for_level(level)
    if not os.path.exists(fp):
        raise FileNotFoundError(f"No existe curso para {level}")
    with open(fp, "r", encoding="utf-8") as f:
        return json.load(f)

def get_syllabus(level: str):
    data = load_course(level)
    lessons = [{"lesson_id": l["lesson_id"], "title": l["title"]} for l in data.get("syllabus", [])]
    return {"level": data.get("level", level.upper()), "lessons": lessons}

def get_lesson(level: str, lesson_id: str):
    data = load_course(level)
    for l in data.get("syllabus", []):
        if l.get("lesson_id") == lesson_id:
            return {"level": data.get("level", level.upper()), **l}
    return None
