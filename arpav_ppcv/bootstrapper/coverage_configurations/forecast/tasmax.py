from ....schemas.base import (
    CoreConfParamName,
    ObservationAggregationType,
)
from ....schemas.coverages import (
    CoverageConfigurationCreate,
    ConfigurationParameterPossibleValueCreate,
)

_DISPLAY_NAME_ENGLISH = "Maximum temperature"
_DISPLAY_NAME_ITALIAN = "Temperatura massima"
_DESCRIPTION_ENGLISH = "Maximum daily air temperature near the ground"
_DESCRIPTION_ITALIAN = "Temperatura massima giornaliera dell'aria vicino al suolo"
_DATA_PRECISION = 1


def generate_configurations(
    conf_param_values, variables
) -> list[CoverageConfigurationCreate]:
    return [
        CoverageConfigurationCreate(
            name="tasmax_seasonal_absolute_model_ensemble",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="ensymbc/clipped/tasmax_avg_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-3,
            color_scale_max=32,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_MODEL.value, "model_ensemble")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.YEAR_PERIOD.value, "winter")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.YEAR_PERIOD.value, "spring")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.YEAR_PERIOD.value, "summer")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.YEAR_PERIOD.value, "autumn")
                    ].id
                ),
            ],
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmax_annual_absolute_model_ensemble",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="ensymbc/clipped/tasmax_avg_{scenario}_ts19762100_ls_VFVG.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-3,
            color_scale_max=32,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_MODEL.value, "model_ensemble")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.YEAR_PERIOD.value, "all_year")
                    ].id
                ),
            ],
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmax_seasonal_absolute_model_ec_earth_cclm4_8_17",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ymbc/clipped/tasmax_EC-EARTH_CCLM4-8-17_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-3,
            color_scale_max=32,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (
                            CoreConfParamName.CLIMATOLOGICAL_MODEL.value,
                            "ec_earth_cclm_4_8_17",
                        )
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.YEAR_PERIOD.value, "winter")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.YEAR_PERIOD.value, "spring")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.YEAR_PERIOD.value, "summer")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.YEAR_PERIOD.value, "autumn")
                    ].id
                ),
            ],
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmax_annual_absolute_model_ec_earth_cclm4_8_17",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ymbc/clipped/tasmax_EC-EARTH_CCLM4-8-17_{scenario}_ts19762100_ls_VFVG.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (
                            CoreConfParamName.CLIMATOLOGICAL_MODEL.value,
                            "ec_earth_cclm_4_8_17",
                        )
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.YEAR_PERIOD.value, "all_year")
                    ].id
                ),
            ],
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmax_seasonal_absolute_model_ec_earth_racmo22e",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="EC-EARTH_RACMO22Eymbc/clipped/tasmax_EC-EARTH_RACMO22E_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-3,
            color_scale_max=32,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (
                            CoreConfParamName.CLIMATOLOGICAL_MODEL.value,
                            "ec_earth_racmo22e",
                        )
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "winter")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "spring")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "summer")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "autumn")
                    ].id
                ),
            ],
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmax_annual_absolute_model_ec_earth_racmo22e",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="EC-EARTH_RACMO22Eymbc/clipped/tasmax_EC-EARTH_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (
                            CoreConfParamName.CLIMATOLOGICAL_MODEL.value,
                            "ec_earth_racmo22e",
                        )
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "all_year")
                    ].id
                ),
            ],
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmax_seasonal_absolute_model_ec_earth_rca4",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="EC-EARTH_RCA4ymbc/clipped/tasmax_EC-EARTH_RCA4_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-3,
            color_scale_max=32,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_MODEL.value, "ec_earth_rca4")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "winter")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "spring")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "summer")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "autumn")
                    ].id
                ),
            ],
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmax_annual_absolute_model_ec_earth_rca4",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="EC-EARTH_RCA4ymbc/clipped/tasmax_EC-EARTH_RCA4_{scenario}_ts19762100_ls_VFVG.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_MODEL.value, "ec_earth_rca4")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "all_year")
                    ].id
                ),
            ],
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmax_seasonal_absolute_model_hadgem2_es_racmo22e",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eymbc/clipped/tasmax_HadGEM2-ES_RACMO22E_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-3,
            color_scale_max=32,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (
                            CoreConfParamName.CLIMATOLOGICAL_MODEL.value,
                            "hadgem2_racmo22e",
                        )
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "winter")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "spring")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "summer")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "autumn")
                    ].id
                ),
            ],
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmax_annual_absolute_model_hadgem2_es_racmo22e",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eymbc/clipped/tasmax_HadGEM2-ES_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (
                            CoreConfParamName.CLIMATOLOGICAL_MODEL.value,
                            "hadgem2_racmo22e",
                        )
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "all_year")
                    ].id
                ),
            ],
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmax_seasonal_absolute_model_mpi_esm_lr_remo2009",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ymbc/clipped/tasmax_MPI-ESM-LR_REMO2009_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-3,
            color_scale_max=32,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (
                            CoreConfParamName.CLIMATOLOGICAL_MODEL.value,
                            "mpi_esm_lr_remo2009",
                        )
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "winter")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "spring")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "summer")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "autumn")
                    ].id
                ),
            ],
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmax_annual_absolute_model_mpi_esm_lr_remo2009",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ymbc/clipped/tasmax_MPI-ESM-LR_REMO2009_{scenario}_ts19762100_ls_VFVG.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (
                            CoreConfParamName.CLIMATOLOGICAL_MODEL.value,
                            "mpi_esm_lr_remo2009",
                        )
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "all_year")
                    ].id
                ),
            ],
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmax_seasonal_absolute_model_ensemble_upper_uncertainty",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax_stdup",
            wms_main_layer_name="tasmax_stdup",
            thredds_url_pattern="ensymbc/std/clipped/tasmax_stdup_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_MODEL.value, "model_ensemble")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.UNCERTAINTY_TYPE.value, "upper_bound")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "winter")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "spring")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "summer")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "autumn")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="tasmax_seasonal_absolute_model_ensemble_lower_uncertainty",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax_stddown",
            wms_main_layer_name="tasmax_stddown",
            thredds_url_pattern="ensymbc/std/clipped/tasmax_stddown_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_MODEL.value, "model_ensemble")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.UNCERTAINTY_TYPE.value, "lower_bound")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "winter")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "spring")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "summer")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "autumn")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="tasmax_annual_absolute_model_ensemble_upper_uncertainty",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax_stdup",
            wms_main_layer_name="tasmax_stdup",
            thredds_url_pattern="ensymbc/std/clipped/tasmax_stdup_{scenario}_ts19762100_ls_VFVG.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_MODEL.value, "model_ensemble")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.UNCERTAINTY_TYPE.value, "upper_bound")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "all_year")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="tasmax_annual_absolute_model_ensemble_lower_uncertainty",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax_stddown",
            wms_main_layer_name="tasmax_stddown",
            thredds_url_pattern="ensymbc/std/clipped/tasmax_stddown_{scenario}_ts19762100_ls_VFVG.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_MODEL.value, "model_ensemble")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.UNCERTAINTY_TYPE.value, "lower_bound")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "all_year")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="tasmax_30yr_anomaly_seasonal_agree_model_ensemble",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax-uncertainty_group",
            wms_secondary_layer_name="tasmax",
            thredds_url_pattern="ensembletwbc/std/clipped/tasmax_avgagree_anom_{time_window}_{scenario}_{year_period}_VFVGTAA.nc",
            unit_english="ºC",
            palette="uncert-stippled/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "30yr")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "anomaly")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_MODEL.value, "model_ensemble")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw1")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw2")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "winter")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "spring")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "summer")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "autumn")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="tasmax_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="taspr5rcm/clipped/tasmax_EC-EARTH_CCLM4-8-17_{scenario}_seas_{time_window}{year_period}_VFVGTAA.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "30yr")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "anomaly")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (
                            CoreConfParamName.CLIMATOLOGICAL_MODEL.value,
                            "ec_earth_cclm_4_8_17",
                        )
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw1")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw2")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "winter")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "spring")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "summer")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "autumn")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="tasmax_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="taspr5rcm/clipped/tasmax_EC-EARTH_RACMO22E_{scenario}_seas_{time_window}{year_period}_VFVGTAA.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "30yr")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "anomaly")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (
                            CoreConfParamName.CLIMATOLOGICAL_MODEL.value,
                            "ec_earth_racmo22e",
                        )
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw1")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw2")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "winter")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "spring")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "summer")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "autumn")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="tasmax_30yr_anomaly_seasonal_model_ec_earth_rca4",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="taspr5rcm/clipped/tasmax_EC-EARTH_RCA4_{scenario}_seas_{time_window}{year_period}_VFVGTAA.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "30yr")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "anomaly")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_MODEL.value, "ec_earth_rca4")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw1")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw2")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "winter")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "spring")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "summer")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "autumn")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="tasmax_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="taspr5rcm/clipped/tasmax_HadGEM2-ES_RACMO22E_{scenario}_seas_{time_window}{year_period}_VFVGTAA.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "30yr")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "anomaly")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (
                            CoreConfParamName.CLIMATOLOGICAL_MODEL.value,
                            "hadgem2_racmo22e",
                        )
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw1")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw2")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "winter")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "spring")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "summer")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "autumn")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="tasmax_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tasmax",
            wms_main_layer_name="tasmax",
            thredds_url_pattern="taspr5rcm/clipped/tasmax_MPI-ESM-LR_REMO2009_{scenario}_seas_{time_window}{year_period}_VFVGTAA.nc",
            unit_english="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
            data_precision=_DATA_PRECISION,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.ARCHIVE.value, "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.CLIMATOLOGICAL_VARIABLE.value, "tasmax")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.AGGREGATION_PERIOD.value, "30yr")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.MEASURE.value, "anomaly")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (
                            CoreConfParamName.CLIMATOLOGICAL_MODEL.value,
                            "mpi_esm_lr_remo2009",
                        )
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw1")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw2")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        (CoreConfParamName.SCENARIO.value, "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "winter")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "spring")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "summer")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "autumn")
                    ].id
                ),
            ],
        ),
    ]


def get_related_map() -> dict[str, list[str]]:
    return {
        "tasmax_seasonal_absolute_model_ensemble": [
            "tasmax_seasonal_absolute_model_ec_earth_cclm4_8_17",
            "tasmax_seasonal_absolute_model_ec_earth_racmo22e",
            "tasmax_seasonal_absolute_model_ec_earth_rca4",
            "tasmax_seasonal_absolute_model_hadgem2_es_racmo22e",
            "tasmax_seasonal_absolute_model_mpi_esm_lr_remo2009",
        ],
        "tasmax_seasonal_absolute_model_ec_earth_cclm4_8_17": [
            "tasmax_seasonal_absolute_model_ensemble",
            "tasmax_seasonal_absolute_model_ec_earth_racmo22e",
            "tasmax_seasonal_absolute_model_ec_earth_rca4",
            "tasmax_seasonal_absolute_model_hadgem2_es_racmo22e",
            "tasmax_seasonal_absolute_model_mpi_esm_lr_remo2009",
        ],
        "tasmax_seasonal_absolute_model_ec_earth_racmo22e": [
            "tasmax_seasonal_absolute_model_ensemble",
            "tasmax_seasonal_absolute_model_ec_earth_cclm4_8_17",
            "tasmax_seasonal_absolute_model_ec_earth_rca4",
            "tasmax_seasonal_absolute_model_hadgem2_es_racmo22e",
            "tasmax_seasonal_absolute_model_mpi_esm_lr_remo2009",
        ],
        "tasmax_seasonal_absolute_model_ec_earth_rca4": [
            "tasmax_seasonal_absolute_model_ensemble",
            "tasmax_seasonal_absolute_model_ec_earth_cclm4_8_17",
            "tasmax_seasonal_absolute_model_ec_earth_racmo22e",
            "tasmax_seasonal_absolute_model_hadgem2_es_racmo22e",
            "tasmax_seasonal_absolute_model_mpi_esm_lr_remo2009",
        ],
        "tasmax_seasonal_absolute_model_hadgem2_es_racmo22e": [
            "tasmax_seasonal_absolute_model_ensemble",
            "tasmax_seasonal_absolute_model_ec_earth_cclm4_8_17",
            "tasmax_seasonal_absolute_model_ec_earth_racmo22e",
            "tasmax_seasonal_absolute_model_ec_earth_rca4",
            "tasmax_seasonal_absolute_model_mpi_esm_lr_remo2009",
        ],
        "tasmax_seasonal_absolute_model_mpi_esm_lr_remo2009": [
            "tasmax_seasonal_absolute_model_ensemble",
            "tasmax_seasonal_absolute_model_ec_earth_cclm4_8_17",
            "tasmax_seasonal_absolute_model_ec_earth_racmo22e",
            "tasmax_seasonal_absolute_model_ec_earth_rca4",
            "tasmax_seasonal_absolute_model_hadgem2_es_racmo22e",
        ],
        "tasmax_annual_absolute_model_ensemble": [
            "tasmax_annual_absolute_model_ec_earth_cclm4_8_17",
            "tasmax_annual_absolute_model_ec_earth_racmo22e",
            "tasmax_annual_absolute_model_ec_earth_rca4",
            "tasmax_annual_absolute_model_hadgem2_es_racmo22e",
            "tasmax_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "tasmax_annual_absolute_model_ec_earth_cclm4_8_17": [
            "tasmax_annual_absolute_model_ensemble",
            "tasmax_annual_absolute_model_ec_earth_racmo22e",
            "tasmax_annual_absolute_model_ec_earth_rca4",
            "tasmax_annual_absolute_model_hadgem2_es_racmo22e",
            "tasmax_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "tasmax_annual_absolute_model_ec_earth_racmo22e": [
            "tasmax_annual_absolute_model_ensemble",
            "tasmax_annual_absolute_model_ec_earth_cclm4_8_17",
            "tasmax_annual_absolute_model_ec_earth_rca4",
            "tasmax_annual_absolute_model_hadgem2_es_racmo22e",
            "tasmax_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "tasmax_annual_absolute_model_ec_earth_rca4": [
            "tasmax_annual_absolute_model_ensemble",
            "tasmax_annual_absolute_model_ec_earth_cclm4_8_17",
            "tasmax_annual_absolute_model_ec_earth_racmo22e",
            "tasmax_annual_absolute_model_hadgem2_es_racmo22e",
            "tasmax_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "tasmax_annual_absolute_model_hadgem2_es_racmo22e": [
            "tasmax_annual_absolute_model_ensemble",
            "tasmax_annual_absolute_model_ec_earth_cclm4_8_17",
            "tasmax_annual_absolute_model_ec_earth_racmo22e",
            "tasmax_annual_absolute_model_ec_earth_rca4",
            "tasmax_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "tasmax_annual_absolute_model_mpi_esm_lr_remo2009": [
            "tasmax_annual_absolute_model_ensemble",
            "tasmax_annual_absolute_model_ec_earth_cclm4_8_17",
            "tasmax_annual_absolute_model_ec_earth_racmo22e",
            "tasmax_annual_absolute_model_ec_earth_rca4",
            "tasmax_annual_absolute_model_hadgem2_es_racmo22e",
        ],
        "tasmax_30yr_anomaly_seasonal_agree_model_ensemble": [
            "tasmax_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            "tasmax_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            "tasmax_30yr_anomaly_seasonal_model_ec_earth_rca4",
            "tasmax_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
            "tasmax_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
        ],
        "tasmax_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17": [
            "tasmax_30yr_anomaly_seasonal_agree_model_ensemble",
            "tasmax_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            "tasmax_30yr_anomaly_seasonal_model_ec_earth_rca4",
            "tasmax_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
            "tasmax_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
        ],
        "tasmax_30yr_anomaly_seasonal_model_ec_earth_racmo22e": [
            "tasmax_30yr_anomaly_seasonal_agree_model_ensemble",
            "tasmax_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            "tasmax_30yr_anomaly_seasonal_model_ec_earth_rca4",
            "tasmax_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
            "tasmax_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
        ],
        "tasmax_30yr_anomaly_seasonal_model_ec_earth_rca4": [
            "tasmax_30yr_anomaly_seasonal_agree_model_ensemble",
            "tasmax_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            "tasmax_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            "tasmax_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
            "tasmax_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
        ],
        "tasmax_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e": [
            "tasmax_30yr_anomaly_seasonal_agree_model_ensemble",
            "tasmax_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            "tasmax_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            "tasmax_30yr_anomaly_seasonal_model_ec_earth_rca4",
            "tasmax_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
        ],
        "tasmax_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009": [
            "tasmax_30yr_anomaly_seasonal_agree_model_ensemble",
            "tasmax_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            "tasmax_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            "tasmax_30yr_anomaly_seasonal_model_ec_earth_rca4",
            "tasmax_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
        ],
    }


def get_uncertainty_map() -> dict[str, tuple[str, str]]:
    return {
        "tasmax_seasonal_absolute_model_ensemble": (
            "tasmax_seasonal_absolute_model_ensemble_lower_uncertainty",
            "tasmax_seasonal_absolute_model_ensemble_upper_uncertainty",
        ),
        "tasmax_annual_absolute_model_ensemble": (
            "tasmax_annual_absolute_model_ensemble_lower_uncertainty",
            "tasmax_annual_absolute_model_ensemble_upper_uncertainty",
        ),
    }
