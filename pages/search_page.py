from pages.base_page import BasePage



class SearchPage(BasePage):
    search_box={'type':'id','value':'key'}
    search_button={'type':'css','value':'#search > div > div.form.hotWords > button'}


    def search(self,text):
        self.input_element(self.search_box['type'],self.search_box['value'],text)
        self.click_element(self.search_button['type'],self.search_button['value'])
