import uuid
import typing

import pydantic
from fastapi import Request

from .base import WebResourceList
from ....schemas import coverages as app_models


class ConfigurationParameterValueEmbeddedInConfigurationParameter(pydantic.BaseModel):
    name: str
    description: str


class ConfigurationParameterReadListItem(pydantic.BaseModel):
    name: str
    description: str
    allowed_values: list[ConfigurationParameterValueEmbeddedInConfigurationParameter]

    @classmethod
    def from_db_instance(
        cls,
        instance: app_models.ConfigurationParameter,
        request: Request,
    ):
        return cls(
            **instance.model_dump(),
            allowed_values=[
                ConfigurationParameterValueEmbeddedInConfigurationParameter(
                    **pv.model_dump()
                )
                for pv in instance.allowed_values
            ],
        )


class ConfigurationParameterPossibleValueRead(pydantic.BaseModel):
    configuration_parameter_name: str
    configuration_parameter_value: str


class CoverageConfigurationReadListItem(pydantic.BaseModel):
    url: pydantic.AnyHttpUrl
    id: uuid.UUID
    name: str
    wms_main_layer_name: str | None
    coverage_id_pattern: str
    possible_values: list[ConfigurationParameterPossibleValueRead]

    @classmethod
    def from_db_instance(
        cls,
        instance: app_models.CoverageConfiguration,
        request: Request,
    ) -> "CoverageConfigurationReadListItem":
        url = request.url_for(
            "get_coverage_configuration", **{"coverage_configuration_id": instance.id}
        )
        return cls(
            **instance.model_dump(),
            url=str(url),
            possible_values=[
                ConfigurationParameterPossibleValueRead(
                    configuration_parameter_name=pv.configuration_parameter_value.configuration_parameter.name,
                    configuration_parameter_value=pv.configuration_parameter_value.name,
                )
                for pv in instance.possible_values
            ],
        )


class CoverageConfigurationReadDetail(CoverageConfigurationReadListItem):
    url: pydantic.AnyHttpUrl
    unit: str
    palette: str
    color_scale_min: float
    color_scale_max: float
    allowed_coverage_identifiers: list[str]

    @classmethod
    def from_db_instance(
        cls,
        instance: app_models.CoverageConfiguration,
        allowed_coverage_identifiers: list[str],
        request: Request,
    ) -> "CoverageConfigurationReadDetail":
        url = request.url_for(
            "get_coverage_configuration", **{"coverage_configuration_id": instance.id}
        )
        return cls(
            **instance.model_dump(),
            url=str(url),
            possible_values=[
                ConfigurationParameterPossibleValueRead(
                    configuration_parameter_name=pv.configuration_parameter_value.configuration_parameter.name,
                    configuration_parameter_value=pv.configuration_parameter_value.name,
                )
                for pv in instance.possible_values
            ],
            allowed_coverage_identifiers=allowed_coverage_identifiers,
        )


class CoverageConfigurationList(WebResourceList):
    items: list[CoverageConfigurationReadListItem]
    list_item_type = CoverageConfigurationReadListItem
    path_operation_name = "list_coverage_configurations"


class CoverageIdentifierReadListItem(pydantic.BaseModel):
    identifier: str
    wms_base_url: str
    wms_main_layer_name: str | None = None


class CoverageIdentifierList(WebResourceList):
    items: list[CoverageIdentifierReadListItem]
    path_operation_name = "list_coverage_identifiers"

    @classmethod
    def from_items(
        cls,
        items: typing.Sequence[str],
        request: Request,
        *,
        limit: int,
        offset: int,
        filtered_total: int,
        unfiltered_total: int,
    ):
        return cls(
            meta=cls._get_meta(len(items), unfiltered_total, filtered_total),
            links=cls._get_list_links(
                request, limit, offset, filtered_total, len(items)
            ),
            items=[i for i in items],
        )


class ConfigurationParameterList(WebResourceList):
    items: list[ConfigurationParameterReadListItem]
    list_item_type = ConfigurationParameterReadListItem
    path_operation_name = "list_configuration_parameters"
