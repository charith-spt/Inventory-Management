import pytest
from flask import Flask
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class TestApp(LiveServerTestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 5000
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.get_server_url())

    def tearDown(self):
        self.driver.quit()

    def test_home_page(self):
        assert "Welcome to the Inventory Management App" in self.driver.page_source

    def test_add_product_page(self):
        self.driver.find_element_by_link_text("New Product").click()
        assert "Add Product to Inventory" in self.driver.page_source

    def test_add_product(self):
        self.driver.find_element_by_link_text("New Product").click()
        self.driver.find_element_by_name("product_name").send_keys("TestProduct")
        self.driver.find_element_by_name("price").send_keys("10.99")
        self.driver.find_element_by_name("quantity").send_keys("50")
        self.driver.find_element_by_css_selector("input[type='submit']").click()
        assert "Product added successfully!" in self.driver.page_source

    def test_edit_product(self):
        # Assuming there is a product already in the list
        self.driver.find_element_by_name("edit").click()
        self.driver.find_element_by_name("name").clear()
        self.driver.find_element_by_name("name").send_keys("EditedProduct")
        self.driver.find_element_by_name("cost").clear()
        self.driver.find_element_by_name("cost").send_keys("15.99")
        self.driver.find_element_by_name("stocks").clear()
        self.driver.find_element_by_name("stocks").send_keys("75")
        self.driver.find_element_by_css_selector("input[type='submit']").click()
        assert "Product details updated successfully!" in self.driver.page_source

if __name__ == '__main__':
    pytest.main()
