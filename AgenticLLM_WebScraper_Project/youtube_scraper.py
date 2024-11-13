import logging
import agentql
from termcolor import colored
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
URL = "https://www.youtube.com"

with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
    page = agentql.wrap(browser.new_page())
    page.goto(URL)
    
    SRC = """
    {
        src_input
        src_btn
    }
    """
    
    VIDEO_QUERY = """
    {
        videos[]{
            video_title
            video_link
        }
    }
    """
    
    VIDEO_EXPAND_CONTROL_QUERY = """
    {
        description_btn
    }
    """
    
    DESCRIPTION = """
    {
        description_text
    }
    """
    
    COMMENT_QUERY = """
    {
        comments[] {
            channel_name
            comment_text
        }
    }
    """
    
    try:
        response = page.query_elements(SRC)
        
        response.src_input.type("James Bond and The Queen London 2012 Performance", delay=20)
        response.src_btn.click()
        
        response = page.query_elements(VIDEO_QUERY)
        
        video_title = response.videos[0].video_title.text_content()
        log.debug(colored(f"\n選取視頻的標題是: \n{video_title}", "cyan"))
        
        response.videos[0].video_link.click()
        
        description_response = page.query_elements(VIDEO_EXPAND_CONTROL_QUERY)
        
        description_response.description_btn.click()
        
        description_text_response = page.query_elements(DESCRIPTION)
        
        description_text = description_text_response.description_text.text_content()
        log.debug(colored(f"\n捕捉到的視頻描述: \n{description_text}", "cyan"))
        
        for i in range(10):
            page.keyboard.press("PageDown")
            page.wait_for_page_ready_state()
            
        comment_response = page.query_elements(COMMENT_QUERY)
        log.debug(colored(f"\n一共有{len(comment_response.comments)}個留言信息", "cyan"))
        
        for comment in comment_response.comments:
            print(colored(f"\n捕捉到的留言信息: \n用戶名稱: {comment.channel_name.text_content()}\n用戶留言: {comment.comment_text.text_content()}", "cyan"))
    
    except Exception as error:
        log.error(colored(f"錯誤: {error}", "red"))
        raise error
    
    page.wait_for_timeout(10000)