from flask import jsonify


def success_res(data=None) -> dict:
    return jsonify({
        'status': 'ok',
        'data': data
    })


def error_res(msg: str) -> dict:
    return jsonify({
        'status': 'error',
        'message': msg
    })

