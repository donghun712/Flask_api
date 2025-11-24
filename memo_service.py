from typing import Dict, List, Tuple, Optional

MEMOS: Dict[int, Dict] = {}
NEXT_ID: int = 1


def _get_next_id() -> int:
    global NEXT_ID
    memo_id = NEXT_ID
    NEXT_ID += 1
    return memo_id


def create_memo(title: str, content: str) -> Tuple[Dict, int]:
    """단일 메모 생성 → (memo, 201)"""
    memo_id = _get_next_id()
    memo = {
        "id": memo_id,
        "title": title,
        "content": content,
    }
    MEMOS[memo_id] = memo
    return memo, 201


def create_memos_bulk(memos_list: List[Dict]) -> Tuple[Dict, int]:
    """
    여러 메모를 한 번에 생성.
    성공/실패를 함께 리턴 → (result, 207 Multi-Status 비슷한 의미)
    """
    created = []
    errors = []

    for idx, item in enumerate(memos_list):
        title = item.get("title")
        content = item.get("content", "")
        if not isinstance(title, str) or not title:
            errors.append(
                {
                    "index": idx,
                    "reason": "Invalid 'title'. Must be non-empty string.",
                }
            )
            continue

        memo, _ = create_memo(title, content)
        created.append(memo)

    result = {
        "created": created,
        "errors": errors,
    }

    if errors and created:
        status_code = 207
    elif errors and not created:
        status_code = 400
    else:
        status_code = 201
    return result, status_code


def get_all_memos() -> Tuple[List[Dict], int]:
    """전체 메모 조회 → (list, 200)"""
    return list(MEMOS.values()), 200


def get_memo(memo_id: int) -> Tuple[Optional[Dict], int]:
    """단일 메모 조회 → (memo or None, 200/404)"""
    memo = MEMOS.get(memo_id)
    if memo is None:
        return None, 404
    return memo, 200


def update_memo(memo_id: int, title: str, content: str) -> Tuple[Optional[Dict], int]:
    """메모 전체 수정 → (memo or None, 200/404)"""
    memo = MEMOS.get(memo_id)
    if memo is None:
        return None, 404

    memo["title"] = title
    memo["content"] = content
    return memo, 200


def update_memo_title(memo_id: int, title: str) -> Tuple[Optional[Dict], int]:
    """제목만 수정 → (memo or None, 200/404)"""
    memo = MEMOS.get(memo_id)
    if memo is None:
        return None, 404

    memo["title"] = title
    return memo, 200


def delete_memo(memo_id: int) -> Tuple[bool, int]:
    """단일 메모 삭제 → (deleted?, 200/404)"""
    if memo_id not in MEMOS:
        return False, 404

    del MEMOS[memo_id]
    return True, 200


def delete_all_memos() -> Tuple[None, int]:
    """전체 메모 삭제 → (None, 204)"""
    MEMOS.clear()
    return None, 204
