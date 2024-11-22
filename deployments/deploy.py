"""Deployment script

This is used for managing semi-automated deployments of the system.
"""

# NOTE: IN ORDER TO SIMPLIFY DEPLOYMENT, THIS SCRIPT SHALL ONLY USE STUFF FROM THE
# PYTHON STANDARD LIBRARY

import argparse
import dataclasses
import configparser
import json
import logging
import os
import shlex
import shutil
import socket
import subprocess
import sys
import urllib.request
from pathlib import Path
from string import Template
from typing import Protocol
from urllib.error import HTTPError

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class DeploymentConfiguration:
    backend_image: str
    compose_project_name: str = dataclasses.field(init=False)
    db_image_tag: str
    db_name: str
    db_password: str
    db_user: str
    deployment_files_repo: str
    deployment_root: Path
    discord_notification_urls: list[str]
    executable_webapp_service_name: str = dataclasses.field(init=False)
    frontend_image: str
    git_repo_clone_destination: Path = dataclasses.field(init=False)
    martin_conf_path: Path = dataclasses.field(
        init=False
    )  # is copied to inside the deployment_root dir
    martin_env_database_url: str = dataclasses.field(init=False)
    martin_image_tag: str
    prefect_db_name: str
    prefect_db_password: str
    prefect_db_user: str
    prefect_server_env_allow_ephemeral_mode: bool = dataclasses.field(init=False)
    prefect_server_env_api_database_connection_url: str = dataclasses.field(init=False)
    prefect_server_env_api_host: str = dataclasses.field(init=False)
    prefect_server_env_api_port: int = dataclasses.field(init=False)
    prefect_server_env_api_url: str = dataclasses.field(init=False)
    prefect_server_env_cli_prompt: bool = dataclasses.field(init=False)
    prefect_server_env_csrf_protection_enabled: bool = dataclasses.field(init=False)
    prefect_server_env_debug_mode: bool = dataclasses.field(init=False)
    prefect_server_env_home: str = dataclasses.field(init=False)
    prefect_server_env_ui_api_url: str = dataclasses.field(init=False)
    prefect_server_env_ui_serve_base: str = dataclasses.field(init=False)
    prefect_server_env_ui_url: str = dataclasses.field(init=False)
    prefect_server_image_tag: str
    prefect_static_worker_env_arpav_ppcv_db_dsn: str = dataclasses.field(init=False)
    prefect_static_worker_env_arpav_ppcv_debug: bool = dataclasses.field(init=False)
    prefect_static_worker_env_prefect_api_url: str = dataclasses.field(init=False)
    prefect_static_worker_env_prefect_debug_mode: bool = dataclasses.field(init=False)
    reverse_proxy_image_tag: str
    tls_cert_path: Path
    tls_cert_key_path: Path
    tolgee_app_env_server_port: int = dataclasses.field(init=False)
    tolgee_app_env_server_spring_datasource_url: str = dataclasses.field(init=False)
    tolgee_app_env_spring_datasource_password: str = dataclasses.field(init=False)
    tolgee_app_env_spring_datasource_username: str = dataclasses.field(init=False)
    tolgee_app_env_tolgee_authentication_create_demo_for_initial_user: bool = (
        dataclasses.field(init=False)
    )
    tolgee_app_env_tolgee_authentication_enabled: bool = dataclasses.field(init=False)
    tolgee_app_env_tolgee_authentication_initial_password: str
    tolgee_app_env_tolgee_authentication_jwt_secret: str
    tolgee_app_env_tolgee_file_storage_fs_data_path: str = dataclasses.field(init=False)
    tolgee_app_env_tolgee_frontend_url: str
    tolgee_app_env_tolgee_postgres_autostart_enabled: bool = dataclasses.field(
        init=False
    )
    tolgee_app_env_tolgee_telemetry_enabled: bool = dataclasses.field(init=False)
    tolgee_app_image_tag: str
    tolgee_db_name: str
    tolgee_db_password: str
    tolgee_db_user: str
    traefik_conf_path: Path = dataclasses.field(
        init=False
    )  # is copied to inside the deployment_root dir
    traefik_users_file_path: Path
    webapp_env_admin_user_password: str
    webapp_env_admin_user_username: str
    webapp_env_allow_cors_credentials: bool = dataclasses.field(init=False)
    webapp_env_bind_host: str = dataclasses.field(init=False)
    webapp_env_bind_port: int = dataclasses.field(init=False)
    webapp_env_cors_methods: list[str] = dataclasses.field(init=False)
    webapp_env_cors_origins: list[str]
    webapp_env_db_dsn: str = dataclasses.field(init=False)
    webapp_env_debug: bool = dataclasses.field(init=False)
    webapp_env_num_uvicorn_worker_processes: int
    webapp_env_public_url: str
    webapp_env_session_secret_key: str
    webapp_env_thredds_server_base_url: str
    webapp_env_uvicorn_log_config_file: Path

    def __post_init__(self):
        _debug = False
        self.compose_project_name = "arpav-cline"
        self.executable_webapp_service_name = "arpav-cline-webapp-1"
        self.git_repo_clone_destination = Path("/tmp/arpav-cline")
        self.martin_conf_path = self.deployment_root / "martin-config.yaml"
        self.traefik_conf_path = self.deployment_root / "traefik-config.toml"
        self.martin_env_database_url = (
            f"postgresql://{self.db_user}:{self.db_password}@db:5432/{self.db_name}"
        )
        self.prefect_server_env_api_database_connection_url = (
            f"postgresql+asyncpg://{self.prefect_db_user}:{self.prefect_db_password}@"
            f"prefect_db/{self.prefect_db_name}"
        )
        self.prefect_server_env_api_host = "0.0.0.0"
        self.prefect_server_env_api_port = 4200
        self.prefect_server_env_allow_ephemeral_mode = False
        self.prefect_server_env_api_url = (
            f"http://{self.prefect_server_env_api_host}:"
            f"{self.prefect_server_env_api_port}/api"
        )
        self.prefect_server_env_cli_prompt = False
        self.prefect_server_env_csrf_protection_enabled = True
        self.prefect_server_env_debug_mode = _debug
        self.prefect_server_env_home = "/prefect_home"
        self.prefect_server_env_ui_api_url = f"{self.webapp_env_public_url}/prefect/api"
        self.prefect_server_env_ui_serve_base = "/prefect/ui"
        self.prefect_server_env_ui_url = (
            f"{self.webapp_env_public_url}{self.prefect_server_env_ui_serve_base}"
        )
        self.prefect_static_worker_env_arpav_ppcv_db_dsn = (
            f"postgresql://{self.db_user}:{self.db_password}@db:5432/{self.db_name}"
        )
        self.prefect_static_worker_env_arpav_ppcv_debug = _debug
        self.prefect_static_worker_env_prefect_api_url = (
            f"http://prefect-server:{self.prefect_server_env_api_port}/api"
        )
        self.prefect_static_worker_env_prefect_debug_mode = _debug
        self.tolgee_app_env_server_port = 8080
        self.tolgee_app_env_server_spring_datasource_url = (
            f"jdbc:postgresql://tolgee-db:5432/{self.tolgee_db_name}"
        )
        self.tolgee_app_env_spring_datasource_password = self.tolgee_db_password
        self.tolgee_app_env_spring_datasource_username = self.tolgee_db_user
        self.tolgee_app_env_tolgee_authentication_create_demo_for_initial_user = False
        self.tolgee_app_env_tolgee_authentication_enabled = True
        self.tolgee_app_env_tolgee_file_storage_fs_data_path = "/data"
        self.tolgee_app_env_tolgee_postgres_autostart_enabled = False
        self.tolgee_app_env_tolgee_telemetry_enabled = False
        self.webapp_env_allow_cors_credentials = True
        self.webapp_env_bind_host = "0.0.0.0"
        self.webapp_env_bind_port = 5001
        self.webapp_env_cors_methods = ["*"]
        self.webapp_env_db_dsn = (
            f"postgresql://{self.db_user}:{self.db_password}@db:5432/{self.db_name}"
        )
        self.webapp_env_debug = _debug

    @classmethod
    def from_config_parser(cls, config_parser: configparser.ConfigParser):
        return cls(
            backend_image=config_parser["main"]["backend_image"],
            db_image_tag=config_parser["main"]["db_image_tag"],
            db_name=config_parser["db"]["name"],
            db_password=config_parser["db"]["password"],
            db_user=config_parser["db"]["user"],
            deployment_files_repo=config_parser["main"]["deployment_files_repo"],
            deployment_root=Path(config_parser["main"]["deployment_root"]),
            discord_notification_urls=[
                i.strip()
                for i in config_parser["main"]["discord_notification_urls"].split(",")
            ],
            frontend_image=config_parser["main"]["frontend_image"],
            martin_image_tag=config_parser["main"]["martin_image_tag"],
            prefect_db_name=config_parser["prefect_db"]["name"],
            prefect_db_password=config_parser["prefect_db"]["password"],
            prefect_db_user=config_parser["prefect_db"]["user"],
            prefect_server_image_tag=config_parser["main"]["prefect_server_image_tag"],
            reverse_proxy_image_tag=config_parser["reverse_proxy"]["image_tag"],
            tls_cert_path=Path(config_parser["reverse_proxy"]["tls_cert_path"]),
            tls_cert_key_path=Path(config_parser["reverse_proxy"]["tls_cert_key_path"]),
            tolgee_app_env_tolgee_authentication_initial_password=config_parser[
                "tolgee_app"
            ]["env_tolgee_authentication_initial_password"],
            tolgee_app_env_tolgee_authentication_jwt_secret=config_parser["tolgee_app"][
                "env_tolgee_authentication_jwt_secret"
            ],
            tolgee_app_env_tolgee_frontend_url=config_parser["tolgee_app"][
                "env_tolgee_frontend_url"
            ],
            tolgee_app_image_tag=config_parser["tolgee_app"]["image_tag"],
            tolgee_db_name=config_parser["tolgee_db"]["name"],
            tolgee_db_password=config_parser["tolgee_db"]["password"],
            tolgee_db_user=config_parser["tolgee_db"]["user"],
            traefik_users_file_path=Path(
                config_parser["reverse_proxy"]["traefik_users_file_path"]
            ),
            webapp_env_admin_user_password=config_parser["webapp"][
                "env_admin_user_password"
            ],
            webapp_env_admin_user_username=config_parser["webapp"][
                "env_admin_user_username"
            ],
            webapp_env_cors_origins=[
                o.strip()
                for o in config_parser["webapp"]["env_cors_origins"].split(",")
            ],
            webapp_env_num_uvicorn_worker_processes=config_parser.getint(
                "webapp", "env_num_uvicorn_worker_processes"
            ),
            webapp_env_public_url=config_parser["webapp"]["env_public_url"],
            webapp_env_session_secret_key=config_parser["webapp"][
                "env_session_secret_key"
            ],
            webapp_env_thredds_server_base_url=config_parser["webapp"][
                "env_thredds_server_base_url"
            ],
            webapp_env_uvicorn_log_config_file=Path(
                config_parser["webapp"]["env_uvicorn_log_config_file"]
            ),
        )

    def ensure_paths_exist(self):
        paths_to_test = (
            self.deployment_root,
            self.tls_cert_path,
            self.tls_cert_key_path,
        )
        for path in paths_to_test:
            if not path.exists():
                raise RuntimeError(
                    f"Could not find referenced configuration file {path!r}"
                )


class DeployStepProtocol(Protocol):
    name: str
    config: DeploymentConfiguration

    def handle(self) -> None:
        ...


@dataclasses.dataclass
class _CloneRepo:
    config: DeploymentConfiguration
    name: str = "clone git repository to a temporary directory"

    def handle(self) -> None:
        print("Cloning repo...")
        if self.config.git_repo_clone_destination.exists():
            shutil.rmtree(self.config.git_repo_clone_destination)
        subprocess.run(
            shlex.split(
                f"git clone {self.config.deployment_files_repo} "
                f"{self.config.git_repo_clone_destination}"
            ),
            check=True,
        )


@dataclasses.dataclass
class _CopyRelevantRepoFiles:
    config: DeploymentConfiguration
    name: str = (
        "Copy files relevant to the deployment from temporary git clone "
        "to target location"
    )
    deployment_related_files = (
        "deployments/deploy.py",
        "docker/compose.yaml",
        "docker/compose.production.template.yaml",
    )
    martin_conf_file = "docker/martin/config.yaml"
    traefik_conf_file = "docker/traefik/production-config.toml"

    def handle(self) -> None:
        to_copy_martin_conf_file_path = (
            self.config.git_repo_clone_destination / self.martin_conf_file
        )
        to_copy_traefik_conf_file_path = (
            self.config.git_repo_clone_destination / self.traefik_conf_file
        )
        to_copy_deployment_related_file_paths = [
            self.config.git_repo_clone_destination / i
            for i in self.deployment_related_files
        ]
        all_files_to_copy = (
            *to_copy_deployment_related_file_paths,
            to_copy_martin_conf_file_path,
            to_copy_traefik_conf_file_path,
        )
        for to_copy_path in all_files_to_copy:
            if not to_copy_path.exists():
                raise RuntimeError(
                    f"Could not find expected file in the previously cloned "
                    f"git repo: {to_copy_path!r}"
                )
        for to_copy_path in to_copy_deployment_related_file_paths:
            shutil.copyfile(
                to_copy_path, self.config.deployment_root / to_copy_path.name
            )
        shutil.copyfile(to_copy_martin_conf_file_path, self.config.martin_conf_path)
        shutil.copyfile(to_copy_traefik_conf_file_path, self.config.traefik_conf_path)


@dataclasses.dataclass
class _RelaunchDeploymentScript:
    config: DeploymentConfiguration
    original_call_args: list[str]
    name: str = "Relaunch the updated deployment script"

    def handle(self) -> None:
        call_args = self.original_call_args[:]
        if (update_flag_index := args.index("--auto-update")) != -1:
            call_args.pop(update_flag_index)
        os.execv(sys.executable, call_args)


@dataclasses.dataclass
class _GenerateComposeFile:
    config: DeploymentConfiguration
    name: str = "generate docker compose file"

    def handle(self) -> None:
        compose_teplate_path = (
            self.config.deployment_root / "compose.production.template.yaml"
        )
        compose_template = Template(compose_teplate_path.read_text())
        rendered = compose_template.substitute(dataclasses.asdict(self.config))
        target_path = Path(
            self.config.deployment_root / "docker/compose.production.yaml"
        )
        target_path.write_text(rendered)
        compose_teplate_path.unlink(missing_ok=True)


@dataclasses.dataclass
class _ComposeCommandExecutor:
    config: DeploymentConfiguration
    environment: dict[str, str] | None = None

    def handle(self) -> None:
        raise NotImplementedError

    def _run_compose_command(self, suffix: str) -> subprocess.CompletedProcess:
        compose_files = [
            self.config.deployment_root / "compose.yaml",
            self.config.deployment_root / "compose.production.yaml",
        ]
        compose_files_fragment = " ".join(f"-f {p}" for p in compose_files)
        return subprocess.run(
            shlex.split(f"docker compose {compose_files_fragment} {suffix}"),
            cwd=self.config.deployment_root,
            env=self.environment or os.environ,
            check=True,
        )


class _StartCompose(_ComposeCommandExecutor):
    name: str = "start docker compose"

    def handle(self) -> None:
        print("Restarting the docker compose stack...")
        self._run_compose_command("up --detach --force-recreate")


class _StopCompose(_ComposeCommandExecutor):
    name: str = "stop docker compose"

    def handle(self) -> None:
        print("Stopping docker compose stack...")
        run_result = self._run_compose_command("down")
        if run_result.returncode == 14:
            logger.info("docker compose stack was not running, no need to stop")
        else:
            run_result.check_returncode()


@dataclasses.dataclass
class _PullImages(_ComposeCommandExecutor):
    name: str = "pull new docker images from their respective container registries"

    def handle(self) -> None:
        self._run_compose_command("pull")


@dataclasses.dataclass
class _CompileTranslations:
    config: DeploymentConfiguration
    name: str = "compile static translations"

    def handle(self) -> None:
        print("Compiling translations...")
        subprocess.run(
            shlex.split(
                f"docker exec {self.config.executable_webapp_service_name} poetry run "
                f"arpav-ppcv translations compile"
            ),
            check=True,
        )


@dataclasses.dataclass
class _RunMigrations:
    config: DeploymentConfiguration
    name: str = "run DB migrations"

    def handle(self) -> None:
        print("Upgrading database...")
        subprocess.run(
            shlex.split(
                f"docker exec {self.config.executable_webapp_service_name} poetry run "
                f"arpav-ppcv db upgrade"
            ),
            check=True,
        )


@dataclasses.dataclass
class _SendDiscordChannelNotification:
    config: DeploymentConfiguration
    content: str
    name: str = "send a notification to a discord channel"

    def handle(self) -> None:
        for webhook_url in self.config.discord_notification_urls:
            request = urllib.request.Request(webhook_url, method="POST")
            request.add_header("Content-Type", "application/json")

            # the discord server blocks the default user-agent sent by urllib, the
            # one sent by httpx works, so we just use that
            request.add_header("User-Agent", "python-httpx/0.27.0")
            try:
                print(f"Sending notification to {webhook_url!r}...")
                with urllib.request.urlopen(
                    request, data=json.dumps({"content": self.content}).encode("utf-8")
                ) as response:
                    if 200 <= response.status <= 299:
                        print("notification sent")
                    else:
                        print(
                            f"notification response was not successful: {response.status}"
                        )
            except HTTPError:
                print("sending notification failed")


def get_configuration(config_file: Path) -> DeploymentConfiguration:
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return DeploymentConfiguration.from_config_parser(config_parser)


def perform_deployment(
    *,
    configuration: DeploymentConfiguration,
    confirmed: bool = False,
):
    deployment_steps = [
        _CloneRepo(config=configuration),
        _CopyRelevantRepoFiles(config=configuration),
        _RelaunchDeploymentScript(config=configuration, original_call_args=sys.argv),
        _StopCompose(config=configuration),
        _GenerateComposeFile(config=configuration),
        _PullImages(config=configuration),
        _StartCompose(config=configuration),
        _RunMigrations(config=configuration),
        _CompileTranslations(config=configuration),
    ]
    this_host = socket.gethostname()
    if len(configuration.discord_notification_urls) > 0:
        deployment_steps.append(
            _SendDiscordChannelNotification(
                config=configuration,
                content=(
                    f"A new deployment of ARPAV-Cline to {this_host!r} has finished"
                ),
            )
        )
    if not confirmed:
        print("Performing a dry-run")
    for step in deployment_steps:
        print(f"Running step: {step.name!r}...")
        if confirmed:
            step.handle()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--config-file",
        default=Path.home() / "arpav-cline/production-deployment.cfg",
        help="Path to configuration file",
        type=Path,
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Turn on debug logging level",
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help=(
            "Perform the actual deployment. If this is not provided the script runs "
            "in dry-run mode, just showing what steps would be performed"
        ),
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING)
    config_file = args.config_file.resolve()
    logger.debug(f"{config_file=}")
    if config_file.exists():
        deployment_config = get_configuration(config_file)
        deployment_config.ensure_paths_exist()
        logger.debug("Configuration:")
        for k, v in dataclasses.asdict(deployment_config).items():
            logger.debug(f"{k}: {v}")
        try:
            perform_deployment(
                configuration=deployment_config,
                confirmed=args.confirm,
            )
        except RuntimeError as err:
            raise SystemExit(err) from err
    else:
        raise SystemExit(f"Configuration file {str(config_file)!r} not found")
