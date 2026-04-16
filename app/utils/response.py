from app.utils.converters import convert_dict_keys_to_camel


def success_response(data=None, message="Success"):
    return{
        "success": True,
        "statusCode": 200,
        "message": message,
        "error": None,
        "data": convert_dict_keys_to_camel(data) if data else None

    }


def error_response(message="Error", error=None, status_code=400):
    return {
        "success" : False,
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": None
    }
