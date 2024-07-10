import werkzeug


def missing_field_exception(missing_fields):
    ret = ""

    for field in missing_fields:
        ret += "Missing field: " + field + "\n"

    return werkzeug.exceptions.UnprocessableEntity(description=ret)


def verify_fields(data, fields):
    missing_fields = [field for field in fields if field not in data]

    if len(missing_fields) > 0:
        raise missing_field_exception(missing_fields)
