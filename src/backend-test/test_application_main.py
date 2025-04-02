import os
import inspect
import logging
from unittest import mock
import pytest
from dotenv import load_dotenv
from libs.base.application_main import AppMainBase
from libs.application.application_context import AppContext
from libs.application.application_configuration import AppConfiguration
from libs.azure_helper.app_configuration import AppConfigurationHelper


class TestAppMainBase:
    @mock.patch.object(AppConfigurationHelper, "read_and_set_environmental_variables")
    @mock.patch.object(load_dotenv, "__call__", return_value=True)
    @mock.patch.object(AppContext, "set_configuration")
    def test_initialization(self, mock_set_config, mock_load_env, mock_app_config):
        """Test that the AppMainBase initializes correctly."""
        
        class TestAppMain(AppMainBase):
            def run(self):
                pass

        app = TestAppMain(env_file_path=".env")

        # Check if environment file was loaded
        mock_load_env.assert_called_with(dotenv_path=".env")

        # Check if environment variables were set
        mock_app_config.assert_called_once()

        # Check if app context was initialized
        assert isinstance(app.application_context, AppContext)

    @mock.patch.object(AppConfigurationHelper, "read_and_set_environmental_variables")
    @mock.patch.object(load_dotenv, "__call__", return_value=True)
    def test_load_env_with_provided_path(self, mock_load_env, mock_app_config):
        """Test that _load_env loads environment variables from the given file path."""

        class TestAppMain(AppMainBase):
            def run(self):
                pass

        app = TestAppMain(env_file_path="custom_env.env")

        mock_load_env.assert_called_with(dotenv_path="custom_env.env")

    @mock.patch("os.path.dirname", return_value="/mock/path")
    @mock.patch("os.path.join", return_value="/mock/path/.env")
    @mock.patch.object(load_dotenv, "__call__", return_value=True)
    def test_load_env_without_provided_path(self, mock_load_env, mock_join, mock_dirname):
        """Test _load_env when no env path is provided, it derives from class location."""
        
        class TestAppMain(AppMainBase):
            def run(self):
                pass

        app = TestAppMain()

        # Verify the derived path is used
        mock_load_env.assert_called_with(dotenv_path="/mock/path/.env")

    @mock.patch("inspect.getfile", return_value="/mock/path/application_main.py")
    def test_get_derived_class_location(self, mock_inspect):
        """Test that _get_derived_class_location returns the correct file path."""

        class TestAppMain(AppMainBase):
            def run(self):
                pass

        app = TestAppMain()
        derived_location = app._get_derived_class_location()

        assert derived_location == "/mock/path/application_main.py"

    @mock.patch("logging.basicConfig")
    @mock.patch.object(AppConfiguration, "app_logging_enable", new_callable=mock.PropertyMock, return_value=True)
    @mock.patch.object(AppConfiguration, "app_logging_level", new_callable=mock.PropertyMock, return_value="DEBUG")
    def test_logging_initialization(self, mock_log_level, mock_log_enable, mock_basic_config):
        """Test that logging is configured properly when enabled."""
        
        class TestAppMain(AppMainBase):
            def run(self):
                pass

        app = TestAppMain()
        mock_basic_config.assert_called_with(level=logging.DEBUG)
