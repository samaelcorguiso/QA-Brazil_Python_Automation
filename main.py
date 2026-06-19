from time import time

import helpers
import data

from selenium import webdriver
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # Habilita os logs de performance — necessário para recuperar o código de confirmação do telefone
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)

        # Verifica se o servidor Urban Routes está acessível antes de iniciar os testes
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não é possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução")


    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_route_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)

        assert routes_page.get_from_field_text() == data.ADDRESS_FROM
        assert routes_page.get_to_field_text() == data.ADDRESS_TO


    def test_select_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_call_a_taxi_button()

        routes_page.click_comfort_option()

        assert routes_page.get_selected_tariff_option() == "Comfort"


    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_call_a_taxi_button()

        routes_page.set_phone(data.PHONE_NUMBER)

        assert routes_page.get_inserted_phone_number() == data.PHONE_NUMBER


    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_call_a_taxi_button()

        routes_page.set_card(data.CARD_NUMBER, data.CARD_CODE)

        assert routes_page.get_current_payment_method() == 'Cartão'


    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_call_a_taxi_button()

        routes_page.set_message_for_driver(data.MESSAGE_FOR_DRIVER)

        assert routes_page.get_message_for_driver() == data.MESSAGE_FOR_DRIVER


    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_call_a_taxi_button()
        routes_page.click_comfort_option()

        routes_page.click_blanket_and_handkerchiefs_option()

        assert routes_page.is_blanket_and_handkerchiefs_option_checked()


    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_call_a_taxi_button()
        routes_page.click_comfort_option()

        # Define a quantidade desejada e adiciona os sorvetes
        desired_icecream_amount = 2
