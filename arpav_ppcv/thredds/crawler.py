import fnmatch
import functools
import logging
import traceback
import typing
from itertools import islice
from pathlib import Path
from xml.etree import ElementTree as etree

import anyio
import exceptiongroup
import httpx

from ..schemas import coverages
from .. import database

logger = logging.getLogger(__name__)

FNMATCH_SPECIAL_CHARS = ("*", "?", "[", "]", "[!")

_NAMESPACES: typing.Final = {
    "thredds": "http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0",
    "xlink": "http://www.w3.org/1999/xlink",
}

_THREDDS_FILE_SERVER_URL_FRAGMENT = "fileServer"


@functools.cache
def find_thredds_dataset_url_fragment(
    rendered_url_fragment: str,
    base_thredds_url: str,
) -> typing.Optional[str]:
    """Contact remote THREDDS server and discover concrete dataset URL.

    Some coverages may use fnmatch-style patterns, in order to indicate
    that the exact name of the THREDDS dataset is not known by the
    configuration. This function lists the available datasets at the
    THREDDS server and then keeps the first one whose name matches
    the fnmatch pattern.
    """
    logger.debug(
        "contacting THREDDS server in order to look for dataset URL fragment..."
    )
    catalog_fragment, name_fragment = rendered_url_fragment.rpartition("/")[::2]
    catalog_url = f"{base_thredds_url}/catalog/{catalog_fragment}/catalog.xml"
    response = httpx.get(catalog_url)
    result = None
    if response.status_code == httpx.codes.OK:
        try:
            root = etree.fromstring(response.content)
        except etree.ParseError:
            logger.error(
                f"Could not parse THREDDS server response as XML: {response.content}"
            )
        else:
            found_names = fnmatch.filter(
                (
                    ds_el.get("name", "")
                    for ds_el in root.findall(f".//{{{_NAMESPACES['thredds']}}}dataset")
                ),
                name_fragment,
            )
            if (num_names := len(found_names)) > 0:
                if num_names > 1:
                    logger.warning(
                        f"Found multiple possible thredds dataset URLs {found_names!r}, "
                        f"kept the first one and ignored the others"
                    )
                keeper = found_names[0]
                result = "/".join((catalog_fragment, keeper))
            else:
                logger.warning(
                    f"did not find any datasets with a name that matches the input "
                    f"fnmatch pattern: {name_fragment!r}"
                )
    else:
        logger.error(
            f"Request for {catalog_url!r} received invalid response from THREDDS "
            f"catalog service {response.status_code!r} - {response.content!r}"
        )
    return result


def get_coverage_configuration_urls(
    base_thredds_url: str,
    coverage_configuration: coverages.CoverageConfiguration,
) -> list[str]:
    coverage_identifiers = database.generate_coverage_identifiers(
        coverage_configuration=coverage_configuration
    )
    result = []
    for cov_identifier in coverage_identifiers:
        possible_fragment = coverage_configuration.get_thredds_url_fragment(
            cov_identifier
        )
        if any(c in possible_fragment for c in FNMATCH_SPECIAL_CHARS):
            logger.debug(
                f"THREDDS dataset url ({possible_fragment}) is an "
                f"fnmatch pattern, retrieving the actual URL from the server..."
            )
            ds_fragment = find_thredds_dataset_url_fragment(
                possible_fragment, base_thredds_url
            )
        else:
            ds_fragment = coverage_configuration.get_thredds_url_fragment(
                cov_identifier
            )
        result.append(
            "/".join(
                (
                    base_thredds_url,
                    _THREDDS_FILE_SERVER_URL_FRAGMENT,
                    ds_fragment,
                )
            )
        )
    return result


async def download_datasets(
    dataset_urls: list[str],
    base_thredds_url: str,
    output_base_directory: Path,
    force_download: bool = False,
) -> None:
    client = httpx.AsyncClient()
    logger.debug(f"There are {len(dataset_urls)} URLS to process in total")
    for batch in _batched(dataset_urls, 10):
        with exceptiongroup.catch({Exception: handle_thredds_download_exception}):
            async with anyio.create_task_group() as tg:
                for dataset_url in batch:
                    output_path = Path(
                        dataset_url.replace(
                            f"{base_thredds_url}/{_THREDDS_FILE_SERVER_URL_FRAGMENT}",
                            str(output_base_directory),
                        )
                    )
                    tg.start_soon(
                        download_individual_dataset,
                        client,
                        output_path,
                        dataset_url,
                        force_download,
                    )


def handle_thredds_download_exception(excgroup: exceptiongroup.ExceptionGroup):
    for exc in excgroup.exceptions:
        logger.warning("\n".join(traceback.format_exception(exc)))


async def download_individual_dataset(
    http_client: httpx.AsyncClient,
    output_path: Path,
    dataset_url: str,
    force_download: bool = False,
) -> None:
    if (not output_path.exists()) or force_download:
        async with http_client.stream("GET", dataset_url) as response:
            try:
                # we catch the exception here because anyio task groups seem
                # to cancel all tasks as soon as one of them raises an exception
                response.raise_for_status()
            except httpx.HTTPStatusError:
                logger.exception(f"Could not download dataset: {dataset_url}")
            else:
                logger.info(f"Downloading {dataset_url!r}...")
                output_dir = output_path.parent
                output_dir.mkdir(parents=True, exist_ok=True)
                with output_path.open("wb") as fh:
                    async for chunk in response.aiter_bytes():
                        fh.write(chunk)
    else:
        logger.info(f"dataset {output_path!r} already exists locally, skipping...")


def _batched(iterable, n):
    """Custom implementation of `itertools.batched()`.

    This is a custom implementation of `itertools.batched()`, which is only available
    on Python 3.12+. This is copied verbatim from the python docs at:

    https://docs.python.org/3/library/itertools.html#itertools.batched

    """
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch
