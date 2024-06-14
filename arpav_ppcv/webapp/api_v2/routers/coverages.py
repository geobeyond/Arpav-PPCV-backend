import logging
import math
import urllib.parse
import uuid
from xml.etree import ElementTree as et
from typing import (
    Annotated,
    Optional,
    Type,
)

import httpx
import pandas as pd
import pydantic
import shapely.io
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Request,
    Response,
    status,
)
from sqlmodel import Session

from .... import (
    database as db,
    exceptions,
    operations,
)
from ....config import ArpavPpcvSettings
from ....thredds import utils as thredds_utils
from ....schemas.base import (
    CoverageDataSmoothingStrategy,
    ObservationDataSmoothingStrategy,
    RELATED_TIME_SERIES_PATTERN,
    UNCERTAINTY_TIME_SERIES_PATTERN,
)
from ....schemas.coverages import CoverageInternal
from ... import dependencies
from ..schemas import coverages as coverage_schemas
from ..schemas.base import (
    TimeSeries,
    TimeSeriesItem,
    TimeSeriesList,
)


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/configuration-parameters",
    response_model=coverage_schemas.ConfigurationParameterList,
)
async def list_configuration_parameters(
    request: Request,
    db_session: Annotated[Session, Depends(dependencies.get_db_session)],
    list_params: Annotated[dependencies.CommonListFilterParameters, Depends()],
):
    """List configuration parameters."""
    config_params, filtered_total = db.list_configuration_parameters(
        db_session,
        limit=list_params.limit,
        offset=list_params.offset,
        include_total=True,
    )
    _, unfiltered_total = db.list_configuration_parameters(
        db_session, limit=1, offset=0, include_total=True
    )
    return coverage_schemas.ConfigurationParameterList.from_items(
        config_params,
        request,
        limit=list_params.limit,
        offset=list_params.offset,
        filtered_total=filtered_total,
        unfiltered_total=unfiltered_total,
    )


@router.get(
    "/coverage-configurations",
    response_model=coverage_schemas.CoverageConfigurationList,
)
async def list_coverage_configurations(
    request: Request,
    db_session: Annotated[Session, Depends(dependencies.get_db_session)],
    list_params: Annotated[dependencies.CommonListFilterParameters, Depends()],
):
    """### List coverage configurations.

    A coverage configuration represents a set of multiple NetCDF files that are
    available in the ARPAV THREDDS server.

    A coverage configuration can be used to generate *coverage identifiers* that
    refer to individual NetCDF files by constructing a string based on the
    `dataset_id_pattern` property. For example, If there is a coverage configuration
    with the following properties:

    ```yaml
    name: myds
    coverage_id_pattern: {name}-something-{scenario}-{year_period}
    possible_values:
      - configuration_parameter_name: scenario
        configuration_parameter_value: scen1
      - configuration_parameter_name: scenario
        configuration_parameter_value: scen2
      - configuration_parameter_name: year_period
        configuration_parameter_value: winter
      - configuration_parameter_name: year_period
        configuration_parameter_value: autumn
    ```

    Then the following would be valid coverage identifiers:

    - `myds-something-scen1-winter`
    - `myds-something-scen1-autumn`
    - `myds-something-scen2-winter`
    - `myds-something-scen2-autumn`

    Each of these coverage identifiers could further be used to gain access to the WMS
    endpoint.

    """
    coverage_configurations, filtered_total = db.list_coverage_configurations(
        db_session,
        limit=list_params.limit,
        offset=list_params.offset,
        include_total=True,
    )
    _, unfiltered_total = db.list_coverage_configurations(
        db_session, limit=1, offset=0, include_total=True
    )
    return coverage_schemas.CoverageConfigurationList.from_items(
        coverage_configurations,
        request,
        limit=list_params.limit,
        offset=list_params.offset,
        filtered_total=filtered_total,
        unfiltered_total=unfiltered_total,
    )


@router.get(
    "/coverage-configurations/{coverage_configuration_id}",
    response_model=coverage_schemas.CoverageConfigurationReadDetail,
)
def get_coverage_configuration(
    request: Request,
    db_session: Annotated[Session, Depends(dependencies.get_db_session)],
    coverage_configuration_id: pydantic.UUID4,
):
    db_coverage_configuration = db.get_coverage_configuration(
        db_session, coverage_configuration_id
    )
    allowed_coverage_identifiers = db.list_allowed_coverage_identifiers(
        db_session, coverage_configuration_id=db_coverage_configuration.id
    )
    return coverage_schemas.CoverageConfigurationReadDetail.from_db_instance(
        db_coverage_configuration, allowed_coverage_identifiers, request
    )


@router.get(
    "/coverage-identifiers",
    response_model=coverage_schemas.CoverageIdentifierList,
)
def list_coverage_identifiers(
    request: Request,
    settings: Annotated[ArpavPpcvSettings, Depends(dependencies.get_settings)],
    db_session: Annotated[Session, Depends(dependencies.get_db_session)],
    list_params: Annotated[dependencies.CommonListFilterParameters, Depends()],
    name_contains: Annotated[list[str], Query()] = None,
):
    cov_internals, filtered_total = db.list_coverage_identifiers(
        db_session,
        limit=list_params.limit,
        offset=list_params.offset,
        include_total=True,
        name_filter=name_contains,
    )
    _, unfiltered_total = db.list_coverage_identifiers(
        db_session, limit=1, offset=0, include_total=True
    )
    records = []
    for cov_internal in cov_internals:
        thredds_url_fragment = cov_internal.configuration.get_thredds_url_fragment(
            cov_internal.identifier
        )
        wms_base_url = "/".join(
            (
                settings.thredds_server.base_url,
                settings.thredds_server.wms_service_url_fragment,
                thredds_url_fragment,
            )
        )
        records.append(
            coverage_schemas.CoverageIdentifierReadListItem(
                identifier=cov_internal.identifier,
                wms_base_url=wms_base_url,
                wms_main_layer_name=cov_internal.configuration.wms_main_layer_name,
            )
        )

    return coverage_schemas.CoverageIdentifierList.from_items(
        records,
        request=request,
        limit=list_params.limit,
        offset=list_params.offset,
        filtered_total=filtered_total,
        unfiltered_total=unfiltered_total,
    )


@router.get("/wms/{coverage_identifier}")
async def wms_endpoint(
    request: Request,
    db_session: Annotated[Session, Depends(dependencies.get_db_session)],
    settings: Annotated[ArpavPpcvSettings, Depends(dependencies.get_settings)],
    http_client: Annotated[httpx.AsyncClient, Depends(dependencies.get_http_client)],
    coverage_identifier: str,
    version: str = "1.3.0",
):
    """### Serve coverage via OGC Web Map Service.

    Pass additional relevant WMS query parameters directly to this endpoint.
    """
    db_coverage_configuration = db.get_coverage_configuration_by_coverage_identifier(
        db_session, coverage_identifier
    )
    if db_coverage_configuration is not None:
        try:
            thredds_url_fragment = db_coverage_configuration.get_thredds_url_fragment(
                coverage_identifier
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid coverage_identifier")
        else:
            base_wms_url = "/".join(
                (
                    settings.thredds_server.base_url,
                    settings.thredds_server.wms_service_url_fragment,
                    thredds_url_fragment,
                )
            )
            parsed_url = urllib.parse.urlparse(base_wms_url)
            logger.info(f"{base_wms_url=}")
            query_params = {k.lower(): v for k, v in request.query_params.items()}
            logger.debug(f"original query params: {query_params=}")
            if query_params.get("request") in ("GetMap", "GetLegendGraphic"):
                query_params = thredds_utils.tweak_wms_get_map_request(
                    query_params,
                    ncwms_palette=db_coverage_configuration.palette,
                    ncwms_color_scale_range=(
                        db_coverage_configuration.color_scale_min,
                        db_coverage_configuration.color_scale_max,
                    ),
                    uncertainty_visualization_scale_range=(
                        settings.thredds_server.uncertainty_visualization_scale_range
                    ),
                )
            logger.debug(f"{query_params=}")
            wms_url = parsed_url._replace(
                query=urllib.parse.urlencode(
                    {
                        **query_params,
                        "service": "WMS",
                        "version": version,
                    }
                )
            ).geturl()
            logger.info(f"{wms_url=}")
            try:
                wms_response = await thredds_utils.proxy_request(wms_url, http_client)
            except httpx.HTTPStatusError as err:
                logger.exception(
                    msg=f"THREDDS server replied with an error: {err.response.text}"
                )
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY, detail=err.response.text
                )
            except httpx.HTTPError as err:
                logger.exception(msg="THREDDS server replied with an error")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                ) from err
            else:
                if query_params.get("request") == "GetCapabilities":
                    response_content = _modify_capabilities_response(
                        wms_response.text, str(request.url).partition("?")[0]
                    )
                else:
                    response_content = wms_response.content
                response = Response(
                    content=response_content,
                    status_code=wms_response.status_code,
                    headers=dict(wms_response.headers),
                )
            return response
    else:
        raise HTTPException(status_code=400, detail="Invalid coverage_identifier")


def _modify_capabilities_response(
    raw_response_content: str,
    wms_public_url: str,
) -> bytes:
    ns = {
        "wms": "http://www.opengis.net/wms",
        "xlink": "http://www.w3.org/1999/xlink",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "edal": "http://reading-escience-centre.github.io/edal-java/wms",
    }
    et.register_namespace("", ns["wms"])
    for prefix, uri in {k: v for k, v in ns.items() if k != "wms"}.items():
        et.register_namespace(prefix, uri)
    root = et.fromstring(raw_response_content)
    service_el = root.findall(f"{{{ns['wms']}}}Service")[0]

    # Remove the OnlineResource element, since we do not expose other
    # internal THREDDS server URLs
    for online_resource_el in service_el.findall(f"{{{ns['wms']}}}OnlineResource"):
        service_el.remove(online_resource_el)
    request_el = root.findall(f"{{{ns['wms']}}}Capability/{{{ns['wms']}}}Request")[0]

    # modify URLs for GetCapabilities, GetMap and GetFeatureInfo methods
    get_caps_el = request_el.findall(f"{{{ns['wms']}}}GetCapabilities")[0]
    get_map_el = request_el.findall(f"{{{ns['wms']}}}GetMap")[0]
    get_feature_info_el = request_el.findall(f"{{{ns['wms']}}}GetFeatureInfo")[0]
    for parent_el in (get_caps_el, get_map_el, get_feature_info_el):
        resource_el = parent_el.findall(
            f"{{{ns['wms']}}}DCPType/"
            f"{{{ns['wms']}}}HTTP/"
            f"{{{ns['wms']}}}Get/"
            f"{{{ns['wms']}}}OnlineResource"
        )[0]
        resource_el.set(f"{{{ns['xlink']}}}href", wms_public_url)
    # for each relevant layer, modify LegendURL and Style abstract
    for layer_el in root.findall(f".//{{{ns['wms']}}}Layer"):
        for legend_online_resource_el in layer_el.findall(
            f"./"
            f"{{{ns['wms']}}}Style/"
            f"{{{ns['wms']}}}LegendURL/"
            f"{{{ns['wms']}}}OnlineResource"
        ):
            attribute_name = f"{{{ns['xlink']}}}href"
            private_url = legend_online_resource_el.get(attribute_name)
            url_query = private_url.partition("?")[-1]
            new_url = "?".join((wms_public_url, url_query))
            legend_online_resource_el.set(f"{{{ns['xlink']}}}href", new_url)
        for abstract_el in layer_el.findall(
            f"./" f"{{{ns['wms']}}}Style/" f"{{{ns['wms']}}}Abstract"
        ):
            old_url_start = abstract_el.text.find("http")
            old_url = abstract_el.text[old_url_start:]
            query = old_url.partition("?")[-1]
            new_url = "?".join((wms_public_url, query))
            abstract_el.text = abstract_el.text[:old_url_start] + new_url
    return et.tostring(
        root,
        encoding="utf-8",
    )


@router.get("/time-series/{coverage_identifier}", response_model=TimeSeriesList)
def get_time_series(
    db_session: Annotated[Session, Depends(dependencies.get_db_session)],
    settings: Annotated[ArpavPpcvSettings, Depends(dependencies.get_settings)],
    http_client: Annotated[httpx.Client, Depends(dependencies.get_sync_http_client)],
    coverage_identifier: str,
    coords: str,
    datetime: Optional[str] = "../..",
    include_coverage_data: bool = True,
    include_observation_data: Annotated[
        bool,
        Query(
            description=(
                "Whether data from the nearest observation station (if any) "
                "should be included in the response."
            )
        ),
    ] = False,
    coverage_data_smoothing: Annotated[list[CoverageDataSmoothingStrategy], Query()] = [  # noqa
        ObservationDataSmoothingStrategy.NO_SMOOTHING
    ],
    observation_data_smoothing: Annotated[
        list[ObservationDataSmoothingStrategy], Query()
    ] = [ObservationDataSmoothingStrategy.NO_SMOOTHING],  # noqa
    include_coverage_uncertainty: bool = False,
    include_coverage_related_data: bool = False,
):
    """### Get forecast-related time series for a geographic location.

    Given that a `coverage_identifier` represents a dataset generated by running a
    forecast model, this endpoint will return a representation of the various temporal
    series of data related to this forecast.
    """
    if (
        db_cov_conf := db.get_coverage_configuration_by_coverage_identifier(
            db_session, coverage_identifier
        )
    ) is not None:
        allowed_cov_ids = db.list_allowed_coverage_identifiers(
            db_session, coverage_configuration_id=db_cov_conf.id
        )
        if coverage_identifier in allowed_cov_ids:
            coverage = CoverageInternal(
                configuration=db_cov_conf, identifier=coverage_identifier
            )
            # TODO: catch errors with invalid geom
            geom = shapely.io.from_wkt(coords)
            if geom.geom_type == "MultiPoint":
                logger.warning(
                    f"Expected coords parameter to be a WKT Point but "
                    f"got {geom.geom_type!r} instead - Using the first point"
                )
                point_geom = geom.geoms[0]
            elif geom.geom_type == "Point":
                point_geom = geom
            else:
                logger.warning(
                    f"Expected coords parameter to be a WKT Point but "
                    f"got {geom.geom_type!r} instead - Using the centroid instead"
                )
                point_geom = geom.centroid
            try:
                time_series = operations.get_coverage_time_series(
                    settings,
                    db_session,
                    http_client,
                    coverage,
                    point_geom,
                    datetime,
                    coverage_data_smoothing,
                    observation_data_smoothing,
                    include_coverage_data,
                    include_observation_data,
                    include_coverage_uncertainty,
                    include_coverage_related_data,
                )
            except exceptions.CoverageDataRetrievalError as err:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Could not retrieve data",
                ) from err
            else:
                series = []
                if include_coverage_data:
                    series.extend(
                        _serialize_dataframe(
                            time_series[coverage.identifier],
                            CoverageDataSmoothingStrategy.NO_SMOOTHING
                            in coverage_data_smoothing,
                            available_smoothing_strategies=CoverageDataSmoothingStrategy,
                            extra_info={"coverage_identifier": coverage.identifier},
                        )
                    )
                    if include_coverage_uncertainty:
                        uncertainty_time_series = {
                            k: v
                            for k, v in time_series.items()
                            if UNCERTAINTY_TIME_SERIES_PATTERN in k
                        }
                        for uncert_name, uncert_df in uncertainty_time_series.items():
                            series.extend(
                                _serialize_dataframe(
                                    uncert_df,
                                    CoverageDataSmoothingStrategy.NO_SMOOTHING
                                    in coverage_data_smoothing,
                                    available_smoothing_strategies=CoverageDataSmoothingStrategy,
                                )
                            )
                    if include_coverage_related_data:
                        related_time_series = {
                            k: v
                            for k, v in time_series.items()
                            if RELATED_TIME_SERIES_PATTERN in k
                        }
                        for related_name, related_df in related_time_series.items():
                            series.extend(
                                _serialize_dataframe(
                                    related_df,
                                    (
                                        CoverageDataSmoothingStrategy.NO_SMOOTHING
                                        in coverage_data_smoothing
                                    ),
                                    available_smoothing_strategies=CoverageDataSmoothingStrategy,
                                )
                            )
                if include_observation_data:
                    variable = coverage.configuration.related_observation_variable
                    for df_name, df in time_series.items():
                        if df_name.startswith("station_"):
                            station_id = uuid.UUID(df_name.split("_")[1])
                            db_station = db.get_station(db_session, station_id)
                            station_series = _serialize_dataframe(
                                df,
                                ObservationDataSmoothingStrategy.NO_SMOOTHING
                                in observation_data_smoothing,
                                available_smoothing_strategies=ObservationDataSmoothingStrategy,
                                extra_info={
                                    "station_id": str(db_station.id),
                                    "station_name": db_station.name,
                                    "variable_name": variable.name,
                                    "variable_description": variable.description,
                                },
                            )
                            series.extend(station_series)
                return TimeSeriesList(series=series)
        else:
            raise HTTPException(status_code=400, detail="Invalid coverage_identifier")
    else:
        raise HTTPException(status_code=400, detail="Invalid coverage_identifier")


def _serialize_dataframe(
    data_: pd.DataFrame,
    include_unsmoothed: bool,
    available_smoothing_strategies: Type[
        ObservationDataSmoothingStrategy | CoverageDataSmoothingStrategy
    ],
    extra_info: Optional[dict[str, str]] = None,
) -> list[TimeSeries]:
    series = []
    for series_name, series_measurements in data_.to_dict().items():
        name_prefix, smoothing_strategy = series_name.rpartition("__")[::2]
        smoothed_with = available_smoothing_strategies(smoothing_strategy)
        if (
            smoothed_with == available_smoothing_strategies.NO_SMOOTHING
            and not include_unsmoothed
        ):
            continue  # client did not ask for the NO_SMOOTHING strategy
        else:
            measurements = []
            for timestamp, value in series_measurements.items():
                if not math.isnan(value):
                    measurements.append(TimeSeriesItem(value=value, datetime=timestamp))
            series.append(
                TimeSeries(
                    name=series_name,
                    values=measurements,
                    info={
                        "smoothing": smoothing_strategy.lower(),
                        **(extra_info or {}),
                    },
                )
            )
    return series
