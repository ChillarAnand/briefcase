import pytest

from briefcase.commands import UpdateCommand
from briefcase.config import AppConfig


class DummyUpdateCommand(UpdateCommand):
    """
    A dummy update command that doesn't actually do anything.
    It only serves to track which actions would be performend.
    """
    def __init__(self, *args, apps, **kwargs):
        super().__init__(*args, platform='tester', output_format='dummy', apps=apps, **kwargs)

        self.actions = []

    def bundle_path(self, app):
        return self.platform_path / '{app.name}.dummy'.format(app=app)

    def binary_path(self, app):
        return self.platform_path / '{app.name}.dummy.bin'.format(app=app)

    def verify_tools(self):
        self.actions.append(('verify'))

    # Override all the body methods of a UpdateCommand
    # with versions that we can use to track actions performed.
    def install_app_dependencies(self, app):
        self.actions.append(('dependencies', app))
        with open(self.bundle_path(app) / 'dependencies', 'w') as f:
            f.write("first app dependencies")

    def install_app_code(self, app):
        self.actions.append(('code', app))
        with open(self.bundle_path(app) / 'code.py', 'w') as f:
            f.write("print('first app')")

    def install_app_extras(self, app):
        self.actions.append(('extras', app))
        with open(self.bundle_path(app) / 'extras', 'w') as f:
            f.write("first app extras")


@pytest.fixture
def update_command(tmp_path):
    return DummyUpdateCommand(
        base_path=tmp_path,
        apps={
            'first': AppConfig(
                name='first',
                bundle='com.example',
                version='0.0.1',
                description='The first simple app',
            ),
            'second': AppConfig(
                name='second',
                bundle='com.example',
                version='0.0.2',
                description='The second simple app',
            ),
        }
    )


@pytest.fixture
def first_app(tmp_path):
    "Populate skeleton app content for the first app"
    bundle_dir = tmp_path / "tester" / "first.dummy"
    bundle_dir.mkdir(parents=True)
    with open(bundle_dir / 'Content', 'w') as f:
        f.write("first app.bundle")


@pytest.fixture
def second_app(tmp_path):
    "Populate skeleton app content for the second app"
    bundle_dir = tmp_path / "tester" / "second.dummy"
    bundle_dir.mkdir(parents=True)
    with open(bundle_dir / 'Content', 'w') as f:
        f.write("second app.bundle")
