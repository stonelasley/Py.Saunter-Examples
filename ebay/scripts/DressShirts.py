# Copyright 2011 Element 34
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from saunter.testcase.webdriver import SaunterTestCase

from pages.shirts import ShirtPage
from harpy.har import Har
import pytest
import saunter.web_element

class TestEbayExample(SaunterTestCase):    
    # @pytest.marks('shallow', 'ebay', 'shirts')
    @pytest.mark.shirts
    def test_collar_style(self):
        s = ShirtPage(self.driver).open().wait_until_loaded()
        self.take_numbered_screenshot()
        self.take_named_screenshot('monkey')
        # s.change_collar_style("Banded (Collarless)")
        # assert(s.is_collar_selected("Banded (Collarless)"))

    @pytest.marks('deep', 'ebay', 'meta')
    def test_meta(self):
        s = ShirtPage(self.driver)
        s.open()
        metas = s.get_meta_elements()
        assert(len(metas) == 7)
        
        keywords = s.get_meta_element("keywords")
        assert(keywords.get_attribute("Content") == "Dress Shirts")

        description = s.get_meta_element("description")
        assert(description.get_attribute("Content") == "Shop eBay Fashion for the most dynamic selection of affordable, new  Dress Shirts Items. Find the best deals on new and used fashion.  Learn more about eBay Buyer Protection.")

    @pytest.marks('shallow', 'ebay', 'blacklist')
    def test_blacklist(self):
        self.client.blacklist("http://www\\.ebay\\.com/.*", 306)
        self.client.blacklist("http://www\\.facebook\\.com/.*", 306)
        s = ShirtPage(self.driver)
        s.open()
        s.change_collar_style("Banded (Collarless)")
        assert(s.is_collar_selected("Banded (Collarless)"))
        
    @pytest.marks('shallow', 'ebay', 'har')
    def test_har_retrieval(self):
        self.client.blacklist("http://www\\.facebook\\.com/.*", 306)
        self.client.blacklist("http://static\\.ak\\.fbcdn\\.com/.*", 306)
        self.client.new_har("shirts")
        s = ShirtPage(self.driver)
        s.open()
        h = self.client.har
        har = Har(h)
        four_oh_fours = [e for e in har.entries if e.response.status == 404]
        assert(len(four_oh_fours) == 1)

    @pytest.marks('shallow', 'ebay', 'chain')
    def test_har_retrieval(self):
        s = ShirtPage(self.driver)
        s.open()
        table = self.driver.find_element_by_locator("id=v4-p225")
        row = table.find_element_by_locator("css=tr")
        assert(isinstance(row, saunter.web_element.WebElement))
        
    @pytest.marks('shallow', 'ebay', 'attributes')
    def test_har_retrieval(self):
        s = ShirtPage(self.driver)
        s.open()
        assert(s.result_count_class == 'rsltCnt')