import datetime
import allure
import pytest
import allure_commons.types
from unittest import TestCase
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy as By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located as loc

"""
@Author: Petrov Roman
@Date: 2022-08-06
@Description: This script is a test script for appium automation framework. The script covers most of the 
functionalities of 'WEHAGO' application.

Test names describe the functionality covered by test. Next functionalities 
were not covered by the script: CONTACT SETTINGS -> import\export, link etc... , CONTACT MOVE/COPY. The reason is the
specifics of a blackbox testing.

Tests are ordered and should run in specified order.(pytest-order plugin). All plugins are included into pyproject.toml
file.

Tests store test result data into Allure folder. This is done by parametrizing the run configuration.  
"""
class RegisterContact(TestCase):
    dc = {}
    options = UiAutomator2Options()
    testName = 'RegisterContact'
    driver = None

    _fname = 'John'
    _lname = 'Smith'
    _phone = '010-123-45678'
    _email = 'workmail@company.com'
    _cname = 'Company LTD'
    _org = 'Sales'
    _rank = 'Sales manager'
    _task = 'Selling the product'
    _group = 'new'
    _hp = 'url.com'
    _memo = 'memo'
    _tag = 'sales'
    _workaddr: str
    _homeaddr: str

    @classmethod
    def setUpClass(cls):
        cls.dc['testName'] = cls.testName
        cls.dc['udid'] = 'emulator-5554'
        cls.dc['appPackage'] = 'com.duzon.android.lulubizpotal'
        cls.dc['appActivity'] = '.intro.SplashActivity'
        cls.dc['noReset'] = 'true'
        cls.dc['platformName'] = 'android'
        cls.dc['dontStopAppOnReset'] = 'true'
        cls.dc['autoGrantPermissions'] = 'true'
        cls.driver = webdriver.Remote('http://localhost:4723/wd/hub', options=cls.options.load_capabilities(caps=cls.dc))

    @pytest.mark.order(1)
    def test_Contacts(self):
        # enter contacts menu
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'cl_main_screen')))
        self.driver.find_element(By.ID, 'servicelist_recyclerview').find_elements(
            By.CLASS_NAME, 'android.widget.LinearLayout')[6].click()
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'tv_main_toolbar_title')))
        assert self.driver.find_element(By.ID, 'tv_main_toolbar_title').text == 'Contact'

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

    @pytest.mark.order(2)
    def test_Groups(self):
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'tv_dz_DropDownSelectBar_contact_left')))
        self.driver.find_element(By.ID, 'tv_dz_DropDownSelectBar_contact_left').click()
        assert self.driver.find_element(By.XPATH,
                                        '//android.widget.LinearLayout[5]/android.widget.LinearLayout/'
                                        'android.widget.LinearLayout[1]/android.widget.TextView').text == self.__class__._group

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot2.1',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        # delition test
        self.driver.find_element(By.ID, 'expandable_group_right_add').click()
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'et_security_pw')))
        self.driver.find_element(By.ID, 'et_security_pw').send_keys('delete')
        self.driver.find_element(By.ID, 'tv_ok').click()

        WebDriverWait(self.driver, 30).until(loc((By.ID, 'expandable_group_right_add')))
        self.driver.find_element(By.XPATH,
                                 '//android.widget.LinearLayout[6]/android.widget.LinearLayout/'
                                 'android.widget.LinearLayout[2]/android.widget.ImageView[2]').click()
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'tv_ok')))
        self.driver.find_element(By.ID, 'tv_ok').click()
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'expandable_group_right_add')))

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot2.2',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        self.driver.back()

    '''After registering a new contact the information disappears from the contact, except for number and name,
    all the other fields are left blank'''
    @pytest.mark.order(3)
    def test_RegisterContact(self):
        # contact add
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'fab_expand_menu_button')))
        self.driver.find_element(By.ID, 'fab_expand_menu_button').click()
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'fab_expand_menu_button')))
        self.driver.find_element(By.ID, 'fab_contact_list_direct').click()
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'tv_mainTitle')))
        assert self.driver.find_element(By.ID, 'tv_mainTitle').text == 'Register Contacts'

        # add contact info
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'ev_contact_add_last_name')))

        fname = self.driver.find_element(By.ID, 'ev_contact_add_first_name').send_keys(self.__class__._fname)
        assert fname.text == self.__class__._fname

        lname = self.driver.find_element(By.ID, 'ev_contact_add_last_name').send_keys(self.__class__._lname)
        assert lname.text == self.__class__._lname

        phone = self.driver.find_element(By.ID, 'ev_contact_add_contents').send_keys(self.__class__._phone)
        assert phone.text == self.__class__._phone

        # add phone number test
        self.driver.find_element(By.ID, 'btn_contact_layout_add').click()
        assert len(self.driver.find_element(By.ID, 'la_contact_basic_phone').find_elements(
            By.CLASS_NAME, 'android.widget.LinearLayout')) > 1
        self.driver.find_element(By.ID, 'btn_contact_layout_delete').click()

        # phone type test
        phonetype = self.driver.find_element(By.ID, 'tv_contact_add_spinner')
        phonetype.click()
        WebDriverWait(self.driver, 30).until(loc((By.XPATH, '//*[@text="Phone"]')))
        self.driver.find_element(By.XPATH, '//android.widget.ListView/android.widget.LinearLayout[1]').click()
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'tv_contact_add_spinner')))
        assert phonetype.text == 'Phone'

        email = self.driver.find_element(By.ID, 'ev_email_add_contents').send_keys(self.__class__._email)
        assert email.text == self.__class__._email

        # add email test
        self.driver.find_element(By.ID, 'btn_email_layout_add').click()
        assert len(self.driver.find_element(By.ID, 'la_contact_basic_email').find_elements(
            By.CLASS_NAME,'android.widget.LinearLayout')) > 1
        self.driver.find_element(By.ID, 'btn_email_layout_delete').click()

        # email type test
        emailtype = self.driver.find_element(By.ID, 'tv_email_add_spinner')
        emailtype.click()
        WebDriverWait(self.driver, 30).until(loc((By.XPATH, '//*[@text="Work Place"]')))
        self.driver.find_element(By.XPATH, '//android.widget.ListView/android.widget.LinearLayout[2]').click()
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'iv_contact_add_group')))
        assert emailtype.text == 'Work Place'

        self.driver.find_element(By.ID, 'iv_contact_add_group').click()
        self.driver.implicitly_wait(0.5)
        self.driver.find_element(By.ID, 'android:id/text1').click()
        self.driver.find_element(By.ID, 'com.duzon.android.lulubizpotal:id/tv_ok').click()

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot3.1',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        # work information
        self.driver.find_element(By.ACCESSIBILITY_ID, 'Work information').click()
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'ev_contact_mod_company_name')))

        cname = self.driver.find_element(By.ID, 'ev_contact_mod_company_name').send_keys(self.__class__._cname)
        assert cname.text == self.__class__._cname

        org = self.driver.find_element(By.ID, 'ev_contact_mod_organization').send_keys(self.__class__._org)
        assert org.text == self.__class__._org

        rank = self.driver.find_element(By.ID, 'ev_contact_mod_rank').send_keys(self.__class__._rank)
        assert rank.text == self.__class__._rank

        task = self.driver.find_element(By.ID, 'ev_contact_mod_task').send_keys(self.__class__._task)
        assert task.text == self.__class__._task

        self.driver.swipe(524, 1500, 600, 877, 292)

        # add work address
        self.driver.find_element(By.ID, 'btn_contact_mod_addr_search').click()
        WebDriverWait(self.driver, 10).until(loc((By.CLASS_NAME, 'android.widget.EditText')))
        self.driver.find_element(By.CLASS_NAME, 'android.widget.EditText').send_keys('seoul')
        self.driver.find_element(By.CLASS_NAME, 'android.widget.Button').click()
        self.driver.implicitly_wait(1)
        self.driver.find_element(
            By.XPATH,'//android.view.View[1]/android.widget.ListView/android.view.View[2]/android.widget.Button').click()
        WebDriverWait(self.driver, 2).until(loc((By.ID, 'ev_contact_mod_address1')))
        self.__class__._workaddr = self.driver.find_element(By.ID, 'ev_contact_mod_address1').text

        addr2 = self.driver.find_element(By.ID, 'ev_contact_mod_address2').send_keys('101')
        assert addr2.text == '101'

        # add company info button test
        self.driver.find_element(By.ID, 'btn_add_company').click()
        assert self.driver.find_element(By.ID, 'tv_contact_company_list_item_header').text == 'Work Place 2'
        self.driver.find_element(By.ID, 'btn_company_mod_delete').click()

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot3.2',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        # other information
        self.driver.find_element(By.ACCESSIBILITY_ID, 'Other information').click()
        WebDriverWait(self.driver, 1).until(loc((By.XPATH, '//*[@text="Search Address"]')))

        # home address add test
        self.driver.find_element(By.ID, 'btn_contact_search_address1').click()
        WebDriverWait(self.driver, 10).until(loc((By.CLASS_NAME, 'android.widget.EditText')))
        self.driver.find_element(By.CLASS_NAME, 'android.widget.EditText').send_keys('seoul')
        self.driver.find_element(By.CLASS_NAME, 'android.widget.Button').click()
        self.driver.implicitly_wait(1)
        self.driver.find_element(
            By.XPATH,'//android.view.View[1]/android.widget.ListView/android.view.View[2]/android.widget.Button').click()
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'ev_contact_add_address1')))

        addr2 = self.driver.find_element(By.ID, 'ev_contact_add_address2').send_keys('301')
        assert addr2.text == '301'

        self.__class__._homeaddr = self.driver.find_element(By.ID, 'ev_contact_add_address1').text + ' ' + addr2.text

        # address type test
        self.driver.find_element(By.ID, 'sp_contact_add_address2').click()
        WebDriverWait(self.driver, 1).until(loc((By.XPATH, '//*[@text="Individual"]')))
        self.driver.find_element(By.XPATH, '//android.widget.ListView/android.widget.LinearLayout[1]').click()
        WebDriverWait(self.driver, 1).until(loc((By.ID, 'ev_contact_add_homepage')))
        assert self.driver.find_element(By.ID, 'sp_contact_add_address2').text == 'Individual'

        # homepage test
        hp = self.driver.find_element(By.ID, 'ev_contact_add_homepage').send_keys(self.__class__._hp)
        assert hp.text == self.__class__._hp

        # birthday test
        bd = self.driver.find_element(By.ID, 'ev_contact_add_birthday')
        bd.click()
        self.driver.find_element(By.ID, 'android:id/button1').click()
        WebDriverWait(self.driver, 1).until(loc((By.XPATH, "//*[@text='Solar calendar']")))

        assert bd.text == datetime.date.today().strftime("%Y.%m.%d")

        self.driver.swipe(524, 1500, 600, 877, 292)
        WebDriverWait(self.driver, 1).until(loc((By.ID, 'sp_contact_birthday')))

        # calendar type check
        calendar = self.driver.find_element(By.ID, 'sp_contact_birthday')
        calendar.click()
        WebDriverWait(self.driver, 1).until(loc((By.XPATH, "//*[@text='Solar calendar']")))
        self.driver.find_element(By.XPATH, '//android.widget.ListView/android.widget.LinearLayout[2]').click()
        WebDriverWait(self.driver, 1).until(loc((By.ID, 'ev_contact_add_memo')))
        assert calendar.text == 'Solar calendar'

        # memo test
        memo = self.driver.find_element(By.ID, 'ev_contact_add_memo').send_keys(self.__class__._memo)
        assert memo.text == self.__class__._memo

        # tag test

        tag = self.driver.find_element(By.ID, 'ev_contact_add_tag')
        tag.click()
        tag.send_keys(self.__class__._tag)
        # noinspection JSUnresolvedVariable,UnnecessaryLabelJS
        self.driver.execute_script("mobile: performEditorAction", {'action': 'done'})
        self.driver.implicitly_wait(1.5)
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()

        # photo test
        WebDriverWait(self.driver, 1).until(loc((By.ID, 'btn_contact_add_photo_edit')))
        self.driver.find_element(By.ID, 'btn_contact_add_photo_edit').click()
        WebDriverWait(self.driver, 1).until(loc((By.XPATH, '//*[@text="Take Photos"]')))
        self.driver.find_element(By.XPATH, "//*[@text='Take Photos']").click()
        WebDriverWait(self.driver, 10).until(loc((By.ACCESSIBILITY_ID, 'Shutter')))
        self.driver.find_element(By.ACCESSIBILITY_ID, 'Shutter').click()
        WebDriverWait(self.driver, 2).until(loc((By.ACCESSIBILITY_ID, 'Done')))
        self.driver.find_element(By.ACCESSIBILITY_ID, 'Done').click()
        WebDriverWait(self.driver, 2).until(loc((By.ID, 'cl_crop_btn_done')))
        self.driver.find_element(By.ID, 'cl_crop_btn_done').click()
        WebDriverWait(self.driver, 5).until(loc((By.ID, 'btn_right1')))

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot3.3',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        self.driver.find_element(By.ID, 'btn_right1').click()

    @pytest.mark.order(4)
    def test_Favorites(self):
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'lv_contact_name_list')))
        plist = self.driver.find_element(By.ID, 'lv_contact_name_list').find_elements(By.CLASS_NAME,
                                                                                      'android.widget.LinearLayout')
        plist[-1].find_element(By.ID, 'layout_contact_list_item').click()
        WebDriverWait(self.driver, 1).until(loc((By.ID, 'btn_favo')))
        self.driver.find_element(By.ID, 'btn_favo').click()

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot5.1',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        self.driver.back()
        WebDriverWait(self.driver, 2).until(loc((By.ID, 'tv_dz_DropDownSelectBar_contact_left')))
        self.driver.find_element(By.ID, 'tv_dz_DropDownSelectBar_contact_left').click()

        assert self.driver.find_element(
            By.XPATH,'//android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.TextView[2]').text == '(1)'

        self.driver.back()

    @pytest.mark.order(5)
    @allure.description('''
    AFTER CANCELING SEARCH COMMAND THE CONTACT LIST SHOWS ARTIFACTS OF EXISTING CONTACTS.(SCREENSHOT)
    ''')
    def test_Search(self):
        #mock contacts #1
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'lv_contact_name_list')))
        self.driver.find_element(By.ID, 'fab_expand_menu_button').click()
        WebDriverWait(self.driver, 5).until(loc((By.ID, 'fab_expand_menu_button')))
        self.driver.find_element(By.ID, 'fab_contact_list_direct').click()
        WebDriverWait(self.driver, 2).until(loc((By.ID, 'tv_mainTitle')))
        WebDriverWait(self.driver, 2).until(loc((By.ID, 'ev_contact_add_last_name')))

        self.driver.find_element(By.ID, 'ev_contact_add_first_name').send_keys('mock1')
        self.driver.find_element(By.ID, 'btn_right1').click()

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot6.1',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        #mock contacts #2
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'lv_contact_name_list')))
        self.driver.find_element(By.ID, 'fab_expand_menu_button').click()
        WebDriverWait(self.driver, 5).until(loc((By.ID, 'fab_expand_menu_button')))
        self.driver.find_element(By.ID, 'fab_contact_list_direct').click()
        WebDriverWait(self.driver, 2).until(loc((By.ID, 'tv_mainTitle')))
        WebDriverWait(self.driver, 2).until(loc((By.ID, 'ev_contact_add_last_name')))

        self.driver.find_element(By.ID, 'ev_contact_add_first_name').send_keys('mock2')
        self.driver.find_element(By.ID, 'btn_right1').click()

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot6.2',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        WebDriverWait(self.driver, 30).until(loc((By.ID, 'lv_contact_name_list')))
        self.driver.find_element(By.ID, 'll_common_before_search').click()
        self.driver.find_element(By.ID, 'ev_common_search').send_keys(self.__class__._fname + self.__class__._lname)
        self.driver.hide_keyboard()

        WebDriverWait(self.driver, 1).until(loc((By.ID, 'lv_contact_name_list')))
        plist = self.driver.find_element(By.ID, 'lv_contact_name_list').find_elements(
            By.XPATH, '//*[contains(@resource-id,"layout_contact_list_item")]')
        assert plist[-1].find_element(By.ID, 'tv_contact_list_name').text == self.__class__._fname+self.__class__._lname

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot6.3',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

        self.driver.find_element(By.ID, 'bnt_common_search_cancel').click()

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot6.3',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

    @pytest.mark.order(6)
    def test_Sort(self):
        WebDriverWait(self.driver, 30).until(loc((By.ID, 'lv_contact_name_list')))
        self.driver.find_element(By.ID, 'iv_dz_DropDownSelectBar_contact_icon_filter').click()
        self.driver.find_element(By.XPATH, '//*[contains(@text,"Descending")]').click()
        self.driver.implicitly_wait(1)
        self.driver.find_element(By.ID, 'iv_dz_DropDownSelectBar_contact_icon_filter').click()
        self.driver.find_element(By.XPATH, '//*[contains(@text,"Ascending")]').click()

    @pytest.mark.order(7)
    def test_ModifyContact(self):
        plist = self.driver.find_element(By.ID, 'lv_contact_name_list').find_elements(
            By.CLASS_NAME, 'android.widget.LinearLayout')
        plist[-1].find_element(By.ID, 'layout_contact_list_item').click()
        WebDriverWait(self.driver, 1).until(loc((By.ID, 'tv_contact_detail_name')))
        self.driver.find_element(By.ID, 'btn_right').click()
        self.driver.find_element(
            By.XPATH, '//android.widget.ListView/android.widget.LinearLayout[1]/android.widget.TextView').click()

        WebDriverWait(self.driver, 30).until(loc((By.ID, 'ev_contact_mod_first_name')))
        assert self.driver.find_element(By.ID, 'ev_contact_mod_first_name').get_attribute('clickable') == 'true'

        self.driver.find_element(By.ID, 'btn_right1').click()
        WebDriverWait(self.driver, 30).until(loc((By.ACCESSIBILITY_ID, 'Navigate up')))
        self.driver.find_element(By.ACCESSIBILITY_ID, 'Navigate up').click()

    @pytest.mark.order(8)
    @allure.description("""THIS TEST IS EXPECTED TO FAIL.
        ASSERTION ERROR RAISES BECAUSE OF THE APP BUG >> THE CONTACT INFO DISAPPEARS AFTER SOME TIME.""")
    def test_ContactDetail(self):
        # find the last added contact
        WebDriverWait(self.driver, 10).until(loc((By.ID, 'lv_contact_name_list')))
        plist = self.driver.find_element(By.ID, 'lv_contact_name_list').find_elements(
            By.XPATH, '//*[contains(@resource-id,"layout_contact_list_item")]')
        plist[1].click()
        WebDriverWait(self.driver, 10).until(loc((By.ID, 'tv_contact_detail_name')))

        try:
            assert self.driver.find_element(
                By.ID, 'tv_contact_detail_name').text == self.__class__._fname + self.__class__._lname
            assert self.driver.find_element(
                By.ID, 'tv_contact_detail_full_path').text == self.__class__._cname + '>' + self.__class__._org
            assert self.driver.find_element(By.ID, 'tv_contact_detail_phone').text == self.__class__._phone
            assert self.driver.find_element(By.ID, 'tv_contact_detail_email').text == self.__class__._email
            assert self.driver.find_element(By.ID, 'tv_contact_detail_group').text == self.__class__._group

            allure.attach(self.driver.get_screenshot_as_png(), name='screenshot4.1',
                          attachment_type=allure_commons.types.AttachmentType.PNG)

            self.driver.find_element(By.ACCESSIBILITY_ID, 'Work information').click()

            assert self.driver.find_element(By.ID, 'tv_contact_detail_company_name').text == self.__class__._cname
            assert self.driver.find_element(By.ID, 'tv_contact_detail_organization').text == self.__class__._org
            assert self.driver.find_element(By.ID, 'tv_contact_detail_rank').text == self.__class__._rank
            assert self.driver.find_element(By.ID, 'tv_contact_detail_task').text == self.__class__._task
            assert self.driver.find_element(
                By.ID, 'tv_contact_detail_address1').text.replace('  ', ' ') == self.__class__._workaddr

            allure.attach(self.driver.get_screenshot_as_png(), name='screenshot4.2',
                          attachment_type=allure_commons.types.AttachmentType.PNG)

            self.driver.find_element(By.ACCESSIBILITY_ID, 'Other information').click()

            assert self.driver.find_element(
                By.ID, 'tv_contact_detail_zip').text.replace('  ', ' ') == self.__class__._homeaddr
            assert self.driver.find_element(By.ID, 'tv_contact_detail_homepage').text == f'https://{self.__class__._hp}'
            assert self.driver.find_element(
                By.ID, 'tv_contact_detail_birthday').text == datetime.date.today().strftime(
                '(Solar)%Yyear %mmonth %dday')
            assert self.driver.find_element(By.ID, 'tv_contact_detail_memo').text == self.__class__._memo
            assert self.driver.find_element(By.ID, 'tv_contact_detail_tag').text == self.__class__._tag

            allure.attach(self.driver.get_screenshot_as_png(), name='screenshot4.3',
                          attachment_type=allure_commons.types.AttachmentType.PNG)
        except AssertionError:
            allure.attach(self.driver.get_screenshot_as_png(), name='screenshot4.3',
                          attachment_type=allure_commons.types.AttachmentType.PNG)
            raise
        finally:
            self.driver.find_element(By.ACCESSIBILITY_ID, 'Navigate up').click()
    @pytest.mark.order(9)
    def test_DeleteContacts(self):
        WebDriverWait(self.driver, 10).until(loc((By.ID, 'iv_dz_DropDownSelectBar_contact_icon_mod')))
        self.driver.find_element(By.ID, 'iv_dz_DropDownSelectBar_contact_icon_mod').click()
        WebDriverWait(self.driver, 10).until(loc((By.ID, 'rv_contact_mod_name_list')))
        plist = self.driver.find_element(By.ID, 'rv_contact_mod_name_list')
        plist = plist.find_elements(By.XPATH, '//*[contains(@resource-id,"layout_contact_list_item")]')
        length = len(plist)
        plist[-1].click()
        plist[-2].click()

        WebDriverWait(self.driver, 10).until(loc((By.ID, 'la_contact_mod_delete_click')))
        self.driver.find_element(By.ID, 'la_contact_mod_delete_click').click()

        assert len(self.driver.find_element(By.ID, 'rv_contact_mod_name_list').find_elements(
            By.XPATH, '//*[contains(@resource-id,"layout_contact_list_item")]')) < length

        self.driver.back()

        allure.attach(self.driver.get_screenshot_as_png(), name='screenshot7.1',
                      attachment_type=allure_commons.types.AttachmentType.PNG)

    @classmethod
    def tearDownClass(cls):
        WebDriverWait(cls.driver, 10).until(loc((By.ID, 'lv_contact_name_list')))
        cls.driver.find_element(By.ID, 'lv_contact_name_list').find_elements(
            By.XPATH, '//*[contains(@resource-id,"layout_contact_list_item")]')[-1].click()
        WebDriverWait(cls.driver, 10).until(loc((By.ID, 'btn_right')))
        cls.driver.find_element(By.ID, 'btn_right').click()
        cls.driver.find_element(
            By.XPATH, '//android.widget.ListView/android.widget.LinearLayout[2]/android.widget.TextView').click()
        WebDriverWait(cls.driver, 10).until(loc((By.ID, 'tv_ok')))
        cls.driver.find_element(By.ID, 'tv_ok').click()
        cls.driver.terminate_app('com.duzon.android.lulubizpotal')
        cls.driver.quit()

    if __name__ == '__main__':
        pytest.main()
