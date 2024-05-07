import logging
import re
import uuid
from typing import (
    Annotated,
    Optional,
    Final,
)

import pydantic
import sqlalchemy
import sqlmodel

logger = logging.getLogger(__name__)
_NAME_PATTERN: Final[str] = r"^[a-z][a-z0-9_]+$"


class ConfigurationParameterValue(sqlmodel.SQLModel, table=True):
    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["configuration_parameter_id",],
            ["configurationparameter.id",],
            onupdate="CASCADE",
            ondelete="CASCADE",  # i.e. delete param value if its related param gets deleted
        ),
    )
    id: uuid.UUID = sqlmodel.Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    name: str
    description: str
    configuration_parameter_id: uuid.UUID

    configuration_parameter: "ConfigurationParameter" = sqlmodel.Relationship(
        back_populates="allowed_values",
    )
    used_in_configurations: "ConfigurationParameterPossibleValue" = sqlmodel.Relationship(
        back_populates="configuration_parameter_value",
        sa_relationship_kwargs={
            "cascade": "all, delete, delete-orphan",
            "passive_deletes": True,
            "order_by": "ConfigurationParameterPossibleValue.configuration_parameter_value_id"
        }
    )


class ConfigurationParameter(sqlmodel.SQLModel, table=True):
    id: uuid.UUID = sqlmodel.Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    name: str = sqlmodel.Field(unique=True, index=True)
    description: str

    allowed_values: list[ConfigurationParameterValue] = sqlmodel.Relationship(
        back_populates="configuration_parameter",
        sa_relationship_kwargs={
            "cascade": "all, delete, delete-orphan",
            "passive_deletes": True,
            "order_by": "ConfigurationParameterValue.name",
        }
    )


class ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
    sqlmodel.SQLModel
):
    name: str
    description: str


class ConfigurationParameterCreate(sqlmodel.SQLModel):
    name: Annotated[
        str,
        pydantic.Field(
            pattern=_NAME_PATTERN,
            help=(
                "Parameter name. Only alphanumeric characters and the underscore are "
                "allowed. Example: my_param"
            )
        )
    ]
    # name: str
    description: str

    allowed_values: list[
        ConfigurationParameterValueCreateEmbeddedInConfigurationParameter
    ]


class ConfigurationParameterValueUpdateEmbeddedInConfigurationParameterEdit(sqlmodel.SQLModel):
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None


class ConfigurationParameterUpdate(sqlmodel.SQLModel):
    name: Annotated[
        Optional[str],
        pydantic.Field(pattern=_NAME_PATTERN)
    ] = None
    description: Optional[str] = None

    allowed_values: list[
        ConfigurationParameterValueUpdateEmbeddedInConfigurationParameterEdit
    ]


class CoverageConfiguration(sqlmodel.SQLModel, table=True):
    """Configuration for NetCDF datasets.

    Can refer to either model forecast data or historical data derived from
    observations.
    """
    id: uuid.UUID = sqlmodel.Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    name: str = sqlmodel.Field(unique=True, index=True)
    thredds_url_pattern: str
    unit: str = ""
    palette: str
    color_scale_min: float = 0.0
    color_scale_max: float = 1.0

    possible_values: list["ConfigurationParameterPossibleValue"] = sqlmodel.Relationship(
        back_populates="coverage_configuration",
        sa_relationship_kwargs={
            "cascade": "all, delete, delete-orphan",
            "passive_deletes": True,
        }
    )

    @pydantic.computed_field()
    @property
    def coverage_id_pattern(self) -> str:
        id_parts = ["{name}"]
        for match_obj in re.finditer(r"(\{\w+\})", self.thredds_url_pattern):
            id_parts.append(match_obj.group(1))
        return "-".join(id_parts)

    def get_thredds_url_fragment(self, coverage_identifier: str) -> str:
        used_values = self.retrieve_used_values(coverage_identifier)
        rendered = self.thredds_url_pattern
        for used_value in used_values:
            param_name = used_value.configuration_parameter_value.configuration_parameter.name
            rendered = rendered.replace(
                f"{{{param_name}}}", used_value.configuration_parameter_value.name)
        return rendered

    def retrieve_used_values(
            self,
            coverage_identifier: str
    ) -> list["ConfigurationParameterPossibleValue"]:
        parsed_parameters = self.retrieve_configuration_parameters(coverage_identifier)
        result = []
        for param_name, value in parsed_parameters.items():
            for pv in self.possible_values:
                matches_param_name = (
                    pv.configuration_parameter_value.configuration_parameter.name == param_name
                )
                matches_param_value = pv.configuration_parameter_value.name == value
                if matches_param_name and matches_param_value:
                    result.append(pv)
                    break
            else:
                raise ValueError(
                    f"Invalid parameter/value pair: {(param_name, value)}")
        return result

    def retrieve_configuration_parameters(self, coverage_identifier) -> dict[str, str]:
        pattern_parts = re.finditer(
            r"\{(\w+)\}",
            self.coverage_id_pattern.partition("-")[-1])
        id_parts = coverage_identifier.split("-")[1:]
        result = {}
        for index, pattern_match_obj in enumerate(pattern_parts):
            id_part = id_parts[index]
            configuration_parameter_name = pattern_match_obj.group(1)
            result[configuration_parameter_name] = id_part
        return result


class CoverageConfigurationCreate(sqlmodel.SQLModel):

    name: Annotated[
        str,
        pydantic.Field(
            pattern=_NAME_PATTERN,
            help=(
                "Coverage configuration name. Only alphanumeric characters and the "
                "underscore are allowed. Example: my_name"
            )
        )
    ]
    thredds_url_pattern: str
    unit: str
    palette: str
    color_scale_min: float
    color_scale_max: float
    possible_values: list["ConfigurationParameterPossibleValueCreate"]

    @pydantic.field_validator("thredds_url_pattern")
    @classmethod
    def validate_thredds_url_pattern(cls, v: str) -> str:
        for match_obj in re.finditer(r"(\{.*?\})", v):
            logger.debug(f"{match_obj.group(1)[1:-1]=}")
            if re.match(_NAME_PATTERN, match_obj.group(1)[1:-1]) is None:
                raise ValueError(f"configuration parameter {v!r} has invalid name")
        return v


class CoverageConfigurationUpdate(sqlmodel.SQLModel):
    name: Annotated[
        Optional[str],
        pydantic.Field(
            pattern=_NAME_PATTERN
        )
    ] = None
    thredds_url_pattern: Optional[str] = None
    unit: Optional[str] = None
    palette: Optional[str] = None
    color_scale_min: Optional[float] = None
    color_scale_max: Optional[float] = None
    possible_values: list["ConfigurationParameterPossibleValueUpdate"]

    @pydantic.field_validator("thredds_url_pattern")
    @classmethod
    def validate_thredds_url_pattern(cls, v: str) -> str:
        for match_obj in re.finditer(r"(\{.*?\})", v):
            logger.debug(f"{match_obj.group(1)[1:-1]=}")
            if re.match(_NAME_PATTERN, match_obj.group(1)[1:-1]) is None:
                raise ValueError(f"configuration parameter {v!r} has invalid name")
        return v


class ConfigurationParameterPossibleValue(sqlmodel.SQLModel, table=True):
    """Possible values for a parameter of a coverage configuration.

    This model mediates an association table that governs a many-to-many relationship
    between a coverage configuration and a configuration parameter value."""
    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["coverage_configuration_id",],
            ["coverageconfiguration.id",],
            onupdate="CASCADE",
            ondelete="CASCADE",  # i.e. delete all possible values if the related coverage configuration gets deleted
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["configuration_parameter_value_id", ],
            ["configurationparametervalue.id", ],
            onupdate="CASCADE",
            ondelete="CASCADE",  # i.e. delete all possible values if the related conf parameter value gets deleted
        ),
    )

    coverage_configuration_id: Optional[uuid.UUID] = sqlmodel.Field(
        # NOTE: foreign key already defined in __table_args__ in order to be able to
        # specify the ondelete behavior
        default=None,
        primary_key=True,
    )
    configuration_parameter_value_id: Optional[uuid.UUID] = sqlmodel.Field(
        # NOTE: foreign key already defined in __table_args__ in order to be able to
        # specify the ondelete behavior
        default=None,
        primary_key=True,
    )

    coverage_configuration: CoverageConfiguration = sqlmodel.Relationship(
        back_populates="possible_values")
    configuration_parameter_value: ConfigurationParameterValue = sqlmodel.Relationship(
        back_populates="used_in_configurations")


class ConfigurationParameterPossibleValueCreate(sqlmodel.SQLModel):
    configuration_parameter_value_id: uuid.UUID


class ConfigurationParameterPossibleValueUpdate(sqlmodel.SQLModel):
    configuration_parameter_value_id: uuid.UUID

# def _get_subclasses(cls):
#     for subclass in cls.__subclasses__():
#         yield from _get_subclasses(subclass)
#         yield subclass
#
#
# _models_dict = {cls.__name__: cls for cls in _get_subclasses(sqlmodel.SQLModel)}
#
# for cls in _models_dict.values():
#     cls.model_rebuild(_types_namespace=_models_dict)