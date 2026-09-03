from flask import Blueprint, current_app

from exceptions.CustomExceptions import ErrIncompleteData
from routes.spec import spec
from routes.v1.schemas.autoinfracao import (
    InfracaoCheckResponseDTO,
    InfracaoCheckUploadDTO,
    InfracaoCsvUploadDTO,
    InfracaoListResponseDTO,
    InfracaoMessageResponseDTO,
    InfracaoQueryDTO,
    InfracaoXlsQueryDTO,
    InfracaoXlsUploadDTO,
)
from routes.v1.schemas.common import create_api_response

AutoInfracaoBlueprint = Blueprint("infracao", __name__)


def _get_service():
    factory = current_app.extensions.get("service_factory")
    if not factory:
        raise ErrIncompleteData("ServiceFactory not configured", 500)
    return factory.get_autoinfracao_service()


@AutoInfracaoBlueprint.route("/infracao/csv", methods=["POST"])
@spec.validate(
    form=InfracaoCsvUploadDTO,
    resp=create_api_response(InfracaoMessageResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Autos de Infração"],
)
def post_csv(form: InfracaoCsvUploadDTO):
    service = _get_service()
    metrics = service.extract_csv(form.file.stream, ignore=True)
    return (
        InfracaoMessageResponseDTO(
            message=f"{metrics.get('inserted', 0)} autos de infração importados"
        ),
        200,
    )


@AutoInfracaoBlueprint.route("/infracao/xls", methods=["POST"])
@spec.validate(
    query=InfracaoXlsQueryDTO,
    form=InfracaoXlsUploadDTO,
    resp=create_api_response(InfracaoMessageResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Autos de Infração"],
)
def post_xls(query: InfracaoXlsQueryDTO, form: InfracaoXlsUploadDTO):
    insert_ignore = query.insert_ignore if query.insert_ignore is not None else True
    service = _get_service()
    metrics = service.extract_xls(form.file.stream, ignore=insert_ignore)
    return (
        InfracaoMessageResponseDTO(
            message=f"{metrics.get('inserted', 0)} autos inseridos com sucesso"
        ),
        200,
    )


@AutoInfracaoBlueprint.route("/infracao", methods=["GET"])
@spec.validate(
    query=InfracaoQueryDTO,
    resp=create_api_response(InfracaoListResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Autos de Infração"],
)
def get_infracoes(query: InfracaoQueryDTO):
    service = _get_service()
    return (
        InfracaoListResponseDTO(autos=service.get_infracoes(query.date, query.ai)),
        200,
    )


@AutoInfracaoBlueprint.route("/infracao/check", methods=["POST"])
@spec.validate(
    form=InfracaoCheckUploadDTO,
    resp=create_api_response(InfracaoCheckResponseDTO, success_code=200),
    security={"BearerAuth": []},
    tags=["Autos de Infração"],
)
def check_infracoes(form: InfracaoCheckUploadDTO):
    service = _get_service()
    db_rows, file_rows, rows_not_present = service.check_infracoes(form.file)
    return (
        InfracaoCheckResponseDTO(
            db_rows=f"{db_rows} Entries found in Database",
            file_rows=f"{file_rows} Rows present in File",
            Not_Present=f"{rows_not_present}",
        ),
        200,
    )
