import requests
import logging

logger = logging.getLogger(__name__)

def submit_urls(urls):
    """
    提交 URL 列表到 IndexNow 进行批量收录推送。
    :param urls: List[str] 绝对 URL 字符串列表，例如 ["https://bearclicker.net/game1"]
    :return: bool 是否全部提交成功
    """
    if not urls:
        logger.warning("No URLs provided to IndexNow submitter.")
        return False
        
    data = {
        "host": "www.bearclicker.net",
        "key": "79b10f40ab4848b5a84b4d154927ed13",
        "keyLocation": "https://bearclicker.net/79b10f40ab4848b5a84b4d154927ed13.txt",
        "urlList": urls
    }

    try:
        response = requests.post(
            "https://api.indexnow.org/IndexNow",
            json=data,
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=10
        )
        
        if response.status_code in [200, 202]:
            logger.info(f"Successfully submitted {len(urls)} URLs to IndexNow. Status: {response.status_code}")
            return True
        else:
            logger.error(f"Failed to submit to IndexNow. Status code: {response.status_code}, Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"IndexNow submission error: {e}")
        return False

if __name__ == "__main__":
    # Test execution
    test_urls = ["https://bearclicker.net/cookie-clicker-game"]
    submit_urls(test_urls)