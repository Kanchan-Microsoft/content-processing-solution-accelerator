import unittest
from unittest.mock import patch, MagicMock
import os

# Import the module to test
from ..libs.base.application_main import AppMainBase

class TestAppMainBase(unittest.TestCase):
    
    @patch("libs.base.application_main.load_dotenv")
    @patch("libs.base.application_main.EnvConfiguration")
    @patch("libs.base.application_main.AppConfigurationHelper")
    @patch("libs.base.application_main.AppContext")
    @patch("libs.base.application_main.AppConfiguration")
    def test_init(self, MockAppConfiguration, MockAppContext, MockAppConfigHelper, MockEnvConfiguration, MockLoadDotenv):
        """
        Test the initialization of AppMainBase, ensuring environment variables are loaded
        and the context is set up correctly.
        """
        class DummyAppMain(AppMainBase):
            def run(self):
                pass  # Implement a dummy run method
        
        # Mock Env Configuration to avoid actual dependency calls
        MockEnvConfiguration().app_config_endpoint = "mock_endpoint"
        MockAppContextInstance = MockAppContext.return_value
        MockAppConfigurationInstance = MockAppConfiguration.return_value
        
        # Instantiate the DummyAppMain class
        app_main = DummyAppMain()
        
        # Ensure environment variables are loaded
        MockLoadDotenv.assert_called()
        MockAppConfigHelper.assert_called_with("mock_endpoint")
        MockAppConfigHelper().read_and_set_environmental_variables.assert_called()
        
        # Ensure application context is initialized correctly
        self.assertEqual(app_main.application_context, MockAppContextInstance)
        MockAppContextInstance.set_configuration.assert_called_with(MockAppConfigurationInstance)

    @patch("libs.base.application_main.load_dotenv")
    def test_load_env(self, MockLoadDotenv):
        """
        Test if _load_env method correctly loads the .env file from the expected location.
        """
        class DummyAppMain(AppMainBase):
            def run(self):
                pass
        
        app_main = DummyAppMain()
        env_path = app_main._load_env("/mock/path/.env")
        
        # Verify that load_dotenv was called with the correct path
        MockLoadDotenv.assert_called_with(dotenv_path="/mock/path/.env")
        self.assertEqual(env_path, "/mock/path/.env")

    def test_get_derived_class_location(self):
        """
        Test if _get_derived_class_location correctly returns the file path of the derived class.
        """
        class DummyAppMain(AppMainBase):
            def run(self):
                pass
        
        app_main = DummyAppMain()
        
        with patch("inspect.getfile", return_value="/mock/path/application_main.py"):
            derived_path = app_main._get_derived_class_location()
        
        self.assertEqual(derived_path, "/mock/path/application_main.py")

if __name__ == "__main__":
    unittest.main()
