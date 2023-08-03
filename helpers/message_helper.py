import re
from typing import Union


def get_linkedin_jobpost_url(message: str) -> Union[str, None]:
    regex = r"https:\/\/www\.linkedin\.com\/jobs\/view\/\d+"
    match = re.search(regex, message)
    if match:
        return match.group(0)
    else:
        return None