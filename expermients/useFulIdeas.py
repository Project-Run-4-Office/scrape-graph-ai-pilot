import re
import urllib.parse
import requests
import asyncio
from typing import List 

def minify_html(html):
    """
    minify_html function 
    """
    # Combine multiple regex operations into one for better performance
    patterns = [
        (r'<!--.*?-->', '', re.DOTALL),
        (r'>\s+<', '><', 0),
        (r'\s+>', '>', 0), 
        (r'<\s+', '<', 0),
        (r'\s+', ' ', 0),
        (r'\s*=\s*', '=', 0)
    ]
    
    for pattern, repl, flags in patterns:
        html = re.sub(pattern, repl, html, flags=flags)

    return html.strip()

def scrape_do_fetch(token, target_url, use_proxy=False, geoCode=None, super_proxy=False):
  """
  Fetches the IP address of the machine associated with the given URL using Scrape.do.

  Args:
      token (str): The API token for Scrape.do service.
      target_url (str): A valid web page URL to fetch its associated IP address.
      use_proxy (bool): Whether to use Scrape.do proxy mode. Default is False.
      geoCode (str, optional): Specify the country code for 
      geolocation-based proxies. Default is None.
      super_proxy (bool): If True, use Residential & Mobile Proxy Networks. Default is False.

  Returns:
      str: The raw response from the target URL.
  """
  encoded_url = urllib.parse.quote(target_url)
  if use_proxy:
      proxy_mode_url = f"http://{token}:@proxy.scrape.do:8080"
      proxies = {
          "http": proxy_mode_url,
          "https": proxy_mode_url,
      }
      params = {"geoCode": geoCode, "super": str(super_proxy).lower()} if geoCode else {}
      response = requests.get(target_url, proxies=proxies, verify=False, params=params)
  else:
      url = f"http://api.scrape.do?token={token}&url={encoded_url}"
      response = requests.get(url)

  return response.tex

"""
browserbase integration module 
"""
import asyncio
from typing import List

def browser_base_fetch(api_key: str, project_id: str, link: List[str],
                       text_content: bool = True, async_mode: bool = False) -> List[str]:
    """
    BrowserBase Fetch

    This module provides an interface to the BrowserBase API.

    The `browser_base_fetch` function takes three arguments:
    - `api_key`: The API key provided by BrowserBase.
    - `project_id`: The ID of the project on BrowserBase where you want to fetch data from.
    - `link`: The URL or link that you want to fetch data from.
    - `text_content`: A boolean flag to specify whether to return only the 
        text content (True) or the full HTML (False).
    - `async_mode`: A boolean flag that determines whether the function runs asynchronously 
        (True) or synchronously (False, default).

    It initializes a Browserbase object with the given API key and project ID, 
    then uses this object to load the specified link. 
    It returns the result of the loading operation.

    Example usage:

    ```
    from browser_base_fetch import browser_base_fetch

    result = browser_base_fetch(api_key="your_api_key", 
    project_id="your_project_id", link="https://example.com")
    print(result)
    ```

    Please note that you need to replace "your_api_key" and "your_project_id" 
    with your actual BrowserBase API key and project ID.

    Args:
        api_key (str): The API key provided by BrowserBase.
        project_id (str): The ID of the project on BrowserBase where you want to fetch data from.
        link (str): The URL or link that you want to fetch data from.
        text_content (bool): Whether to return only the text content 
        (True) or the full HTML (False). Defaults to True.
        async_mode (bool): Whether to run the function asynchronously 
        (True) or synchronously (False). Defaults to False.

    Returns:
        object: The result of the loading operation.
    """

    try:
        from browserbase import Browserbase
    except ImportError:
        raise ImportError(f"""The browserbase module is not installed. 
                          Please install it using `pip install browserbase`.""")


    browserbase = Browserbase(api_key=api_key, project_id=project_id)

    result = []
    async def _async_fetch_link(l):
        return await asyncio.to_thread(browserbase.load, l, text_content=text_content)

    if async_mode:
        async def _async_browser_base_fetch():
            for l in link:
                result.append(await _async_fetch_link(l))
            return result

        result = asyncio.run(_async_browser_base_fetch())
    else:
        for l in link:
            result.append(browserbase.load(l, text_content=text_content))


    return result
