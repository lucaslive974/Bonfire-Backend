from flask import Request, jsonify
from flask import Response as FlaskResponse
from pydantic import ValidationError
from spectree import SecurityScheme, SpecTree

bearer_scheme = SecurityScheme(
    name="BearerAuth",
    data={
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    },
)


def spectree_before_handler(
    req: Request,
    resp: FlaskResponse,
    err: ValidationError | None,
    instance,
) -> None:
    """Formats validation errors consistently with the API ErrorResponseDTO."""
    if err:
        errors = err.errors(include_context=False)
        if errors:
            first = errors[0]
            err_type = first.get("type", "")
            msg = first.get("msg", "Validation error")
            if msg.startswith("Value error, "):
                msg = msg[len("Value error, ") :]

            if (
                err_type == "incomplete_data"
                or "não está presente na requisição" in msg
            ):
                error_label = "Incomplete Data"
                status_code = 400
            else:
                loc = ".".join(str(item) for item in first.get("loc", []))
                msg = f"{loc}: {msg}" if loc else msg
                error_label = "ValidationError"
                status_code = 422
        else:
            error_label = "ValidationError"
            msg = "Dados da requisição inválidos."
            status_code = 422

        resp.set_data(
            jsonify(
                {
                    "error": error_label,
                    "message": msg,
                }
            ).get_data()
        )
        resp.status_code = status_code
        resp.headers["Content-Type"] = "application/json"


spec = SpecTree(
    "flask",
    title="Bonfire Backend API",
    version="1.0.0",
    path="apidoc",
    security_schemes=[bearer_scheme],
    before=spectree_before_handler,
)
