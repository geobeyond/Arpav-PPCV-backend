import logging

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException
from starlette_admin.contrib.sqlmodel import Admin
from starlette_admin.views import Link

from ...import (
    config,
    database,
)
from ...schemas import coverages
from . import (
    auth,
    views,
)
from .middlewares import SqlModelDbSessionMiddleware

logger = logging.getLogger(__name__)


class ArpavPpcvAdmin(Admin):

    def mount_to(
            self, app: Starlette, settings: config.ArpavPpcvSettings) -> None:
        """Reimplemented in order to pass settings to the admin app."""
        admin_app = Starlette(
            routes=self.routes,
            middleware=self.middlewares,
            debug=self.debug,
            exception_handlers={HTTPException: self._render_error},
        )
        admin_app.state.ROUTE_NAME = self.route_name
        admin_app.state.settings = settings
        app.mount(
            self.base_url,
            app=admin_app,
            name=self.route_name,
        )


def create_admin(settings: config.ArpavPpcvSettings) -> ArpavPpcvAdmin:
    engine = database.get_engine(settings)
    admin = ArpavPpcvAdmin(
        engine,
        debug=settings.debug,
        templates_dir=str(settings.templates_dir / 'admin'),
        auth_provider=auth.UsernameAndPasswordProvider(),
        middlewares=[
            Middleware(SessionMiddleware, secret_key=settings.session_secret_key),
            Middleware(SqlModelDbSessionMiddleware, engine=engine)
        ],
    )
    admin.add_view(
        views.ConfigurationParameterView(coverages.ConfigurationParameter))
    admin.add_view(
        views.CoverageConfigurationView(coverages.CoverageConfiguration))
    admin.add_view(
        Link(
            "V2 API docs",
            icon="fa fa-link",
            url=f"{settings.public_url}{settings.v2_api_mount_prefix}/docs",
            target="blank_"
        )
    )
    return admin