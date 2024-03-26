import logging
import typing
import urllib.parse
from itertools import islice
from pathlib import Path
from xml.etree import ElementTree as et

import anyio
import httpx

from . import models

logger = logging.getLogger(__name__)


_NAMESPACES: typing.Final = {
    "thredds": "http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0",
    "xlink": "http://www.w3.org/1999/xlink",
}


def discover_catalog_contents(
        catalog_reference_url: str,
        http_client: httpx.Client,
) -> models.ThreddsClientCatalog:
    """
    catalog_reference_url:
        https://thredds.arpa.veneto.it/thredds/catalog/ensembletwbc/clipped
    """

    response = http_client.get(catalog_reference_url)
    response.raise_for_status()
    raw_catalog_description = response.content
    parsed_services, parsed_dataset = _parse_catalog_client_description(
        raw_catalog_description)
    return models.ThreddsClientCatalog(
        url=urllib.parse.urlparse(catalog_reference_url),
        services={service.service_type: service for service in parsed_services},
        dataset=parsed_dataset
    )


async def download_datasets(
        output_base_directory: Path,
        catalog_contents: models.ThreddsClientCatalog,
        dataset_wildcard_filter: str = "*",
        force_download: bool = False
) -> None:
    client = httpx.AsyncClient()
    relevant_datasets = catalog_contents.get_public_datasets(
        dataset_wildcard_filter)
    for batch in _batched(relevant_datasets.values(), 10):
        logger.info(f"processing new batch")
        async with anyio.create_task_group() as tg:
            for public_dataset in batch:
                logger.info(f"processing dataset {public_dataset.id!r}...")
                tg.start_soon(
                    download_individual_dataset,
                    public_dataset.id,
                    catalog_contents,
                    output_base_directory,
                    force_download,
                    client,
                )


async def download_individual_dataset(
        dataset_id: str,
        catalog_contents: models.ThreddsClientCatalog,
        output_base_directory: Path,
        force_download: bool,
        http_client: httpx.AsyncClient,
) -> None:
    url = catalog_contents.build_dataset_download_url(dataset_id)
    output_path = output_base_directory / dataset_id
    if (not output_path.exists()) or force_download:
        async with http_client.stream("GET", url) as response:
            response.raise_for_status()
            output_dir = output_path.parent
            output_dir.mkdir(parents=True, exist_ok=True)
            with output_path.open("wb") as fh:
                async for chunk in response.aiter_bytes():
                    fh.write(chunk)
    else:
        logger.info(f"dataset {dataset_id!r} alread exists locally, skipping...")


def _parse_catalog_client_description(
        catalog_description: bytes
) -> tuple[list[models.ThreddsClientService], models.ThreddsClientDataset]:
    root_element = et.fromstring(catalog_description)
    service_qn = et.QName(_NAMESPACES["thredds"], "service")
    dataset_qn = et.QName(_NAMESPACES["thredds"], "dataset")
    services = []
    for service_element in root_element.findall(f"./{service_qn}/"):
        service = _parse_service_element(service_element)
        services.append(service)
    dataset = _parse_dataset_element(
        root_element.findall(f"./{dataset_qn}")[0])
    return services, dataset


def _parse_service_element(service_el: et.Element) -> models.ThreddsClientService:
    return models.ThreddsClientService(
        name=service_el.get("name", default=""),
        service_type=service_el.get("serviceType", default=""),
        base=service_el.get("base", default="")
    )


def _parse_dataset_element(dataset_el: et.Element) -> models.ThreddsClientDataset:
    prop_qname = et.QName(_NAMESPACES["thredds"], "property")
    meta_qname = et.QName(_NAMESPACES["thredds"], "metadata")
    ds_qname = et.QName(_NAMESPACES["thredds"], "dataset")
    cat_ref_qname = et.QName(_NAMESPACES["thredds"], "catalogRef")
    properties = {}
    metadata = {}
    public_datasets = {}
    catalog_references = {}
    for element in dataset_el.findall("./"):
        match element.tag:
            case prop_qname.text:
                properties[element.get("name")] = element.get("value")
            case meta_qname.text:
                for metadata_element in element.findall("./"):
                    key = metadata_element.tag.replace(
                        f"{{{_NAMESPACES['thredds']}}}", "")
                    metadata[key] = metadata_element.text
            case ds_qname.text:
                public_ds = models.ThreddsClientPublicDataset(
                    name=element.get("name", ""),
                    id=element.get("ID", ""),
                    url_path=element.get("urlPath", ""),
                )
                public_datasets[public_ds.id] = public_ds
            case cat_ref_qname.text:
                title_qname = et.QName(_NAMESPACES["xlink"], "title")
                href_qname = et.QName(_NAMESPACES["xlink"], "href")
                catalog_ref = models.ThreddsClientCatalogRef(
                    title=element.get(title_qname.text, ""),
                    id=element.get("ID", ""),
                    name=element.get("name", ""),
                    href=element.get(href_qname.text, ""),
                )
                catalog_references[catalog_ref.id] = catalog_ref
    return models.ThreddsClientDataset(
        name=dataset_el.get("name", default=""),
        properties=properties,
        metadata=metadata,
        public_datasets=public_datasets,
        catalog_refs=catalog_references,
    )


def _batched(iterable, n):
    """Custom implementation of `itertools.batched()`.

    This is a custom implementation of `itertools.batched()`, which is only availble
    on Python 3.12+. This is copied verbatim from the python docs at:

    https://docs.python.org/3/library/itertools.html#itertools.batched

    """
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch