from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from memo_service import (
    create_memo,
    create_memos_bulk,
    get_all_memos,
    get_memo,
    update_memo,
    update_memo_title,
    delete_memo,
    delete_all_memos,
)

app = Flask(__name__)


# ---------------------------
# 공통 응답 포맷 헬퍼
# ---------------------------
def make_response_body(status: str, data=None, message: str | None = None):
    body = {"status": status}
    if data is not None:
        body["data"] = data
    if message is not None:
        body["message"] = message
    return body


# ---------------------------
# 미들웨어 (요청/응답 로그)
# ---------------------------
@app.before_request
def log_request():
    print(
        f"[REQUEST] {request.method} {request.path} "
        f"body={request.get_json(silent=True)}"
    )


@app.after_request
def log_response(response):
    print(f"[RESPONSE] status={response.status_code} path={request.path}")
    return response


# ---------------------------
# 에러 핸들링 (4xx, 5xx)
# ---------------------------
@app.errorhandler(HTTPException)
def handle_http_exception(e: HTTPException):
    # Flask 기본 404, 405 등
    response = jsonify(
        make_response_body(
            status="error",
            message=e.description,
        )
    )
    response.status_code = e.code
    return response


@app.errorhandler(Exception)
def handle_unexpected_exception(e: Exception):
    # 예기치 못한 서버 오류 → 500
    print(f"[ERROR] {e}")
    response = jsonify(
        make_response_body(
            status="error",
            message="Internal server error",
        )
    )
    response.status_code = 500
    return response


# ---------------------------
# POST APIs (2개)
# ---------------------------
@app.route("/memos", methods=["POST"])
def create_memo_route():
    body = request.get_json(silent=True) or {}
    title = body.get("title")
    content = body.get("content")

    if not title or not isinstance(title, str):
        # 잘못된 요청 → 400
        resp = jsonify(
            make_response_body(
                status="error",
                message="Field 'title' is required and must be a string.",
            )
        )
        resp.status_code = 400
        return resp

    memo, status_code = create_memo(title, content or "")
    resp = jsonify(make_response_body(status="success", data=memo))
    resp.status_code = status_code  # 201
    return resp


@app.route("/memos/bulk", methods=["POST"])
def create_memos_bulk_route():
    body = request.get_json(silent=True) or {}
    memos_list = body.get("memos")

    if not isinstance(memos_list, list):
        resp = jsonify(
            make_response_body(
                status="error",
                message="Field 'memos' must be a list.",
            )
        )
        resp.status_code = 400
        return resp

    result, status_code = create_memos_bulk(memos_list)
    resp = jsonify(make_response_body(status="success", data=result))
    resp.status_code = status_code  # 예: 207 Multi-Status
    return resp


# ---------------------------
# GET APIs (2개)
# ---------------------------
@app.route("/memos", methods=["GET"])
def get_all_memos_route():
    memos, status_code = get_all_memos()
    resp = jsonify(make_response_body(status="success", data=memos))
    resp.status_code = status_code  # 200
    return resp


@app.route("/memos/<int:memo_id>", methods=["GET"])
def get_memo_route(memo_id: int):
    memo, status_code = get_memo(memo_id)
    if memo is None:
        resp = jsonify(
            make_response_body(
                status="error",
                message=f"Memo {memo_id} not found.",
            )
        )
        resp.status_code = status_code  # 404
        return resp

    resp = jsonify(make_response_body(status="success", data=memo))
    resp.status_code = status_code  # 200
    return resp


# ---------------------------
# PUT APIs (2개)
# ---------------------------
@app.route("/memos/<int:memo_id>", methods=["PUT"])
def update_memo_route(memo_id: int):
    body = request.get_json(silent=True) or {}
    title = body.get("title")
    content = body.get("content")

    if not isinstance(title, str) or not isinstance(content, str):
        resp = jsonify(
            make_response_body(
                status="error",
                message="'title' and 'content' must be strings.",
            )
        )
        resp.status_code = 400
        return resp

    memo, status_code = update_memo(memo_id, title, content)
    if memo is None:
        resp = jsonify(
            make_response_body(
                status="error",
                message=f"Memo {memo_id} not found.",
            )
        )
        resp.status_code = status_code  # 404
        return resp

    resp = jsonify(make_response_body(status="success", data=memo))
    resp.status_code = status_code  # 200
    return resp


@app.route("/memos/<int:memo_id>/title", methods=["PUT"])
def update_memo_title_route(memo_id: int):
    body = request.get_json(silent=True) or {}
    title = body.get("title")

    if not isinstance(title, str) or not title:
        resp = jsonify(
            make_response_body(
                status="error",
                message="'title' is required and must be non-empty string.",
            )
        )
        resp.status_code = 400
        return resp

    memo, status_code = update_memo_title(memo_id, title)
    if memo is None:
        resp = jsonify(
            make_response_body(
                status="error",
                message=f"Memo {memo_id} not found.",
            )
        )
        resp.status_code = status_code  # 404
        return resp

    resp = jsonify(make_response_body(status="success", data=memo))
    resp.status_code = status_code  # 200
    return resp


# ---------------------------
# DELETE APIs (2개)
# ---------------------------
@app.route("/memos/<int:memo_id>", methods=["DELETE"])
def delete_memo_route(memo_id: int):
    deleted, status_code = delete_memo(memo_id)
    if not deleted:
        resp = jsonify(
            make_response_body(
                status="error",
                message=f"Memo {memo_id} not found.",
            )
        )
        resp.status_code = status_code  # 404
        return resp

    resp = jsonify(
        make_response_body(
            status="success",
            data={"id": memo_id},
            message="Memo deleted.",
        )
    )
    resp.status_code = status_code  # 200
    return resp


@app.route("/memos", methods=["DELETE"])
def delete_all_memos_route():
    _, status_code = delete_all_memos()
    # 204는 보통 body 없이 보내지만, 과제에서 포맷 통일을 위해 간단한 메세지 포함
    resp = jsonify(
        make_response_body(
            status="success",
            message="All memos deleted.",
        )
    )
    resp.status_code = status_code  # 204
    return resp


if __name__ == "__main__":
    app.run(debug=True)