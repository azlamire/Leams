from bs4 import BeautifulSoup
from loguru import logger
from typing import List, Tuple, Literal, Dict
from playwright.async_api import async_playwright, Error as PlaywrightError
from pydantic import TypeAdapter
from pydantic_core import ValidationError
from urllib.error import URLError
from app.services.s3 import S3Client


async def parse(
    url: str,
    main: tuple[str, str],
    elements: List[Tuple[str, str, Literal["text", "src"], str]],
) -> Dict[str, str]:
    """
    This function was made for parsing from elements some info

    Args:
        url (str): Site's url
        main (tuple[str,str]): The main element where all elements are set
        elements (tuple[str,str]): What elements you'd like to be parserd
    Returns:
        str - parsed content from page.
    Raises:
        ValueError - Url must not to be null
        ValueError - Arg main must be tuple[str,str]
    Examples:
        >>> parse(
        ...    url="https://www.twitch.tv/",
        ...    main=(
        ...        "a",
        ...        "ScCoreLink-sc-16kq0mq-0 fytYW InjectLayout-sc-1i43xsx-0 cnzybN side-nav-card__link tw-link",
        ...    ),
        ... )
        [<a class="...">...</a>, ...]
    """
    try:
        TypeAdapter(tuple[str, str]).validate_python(main)
    except ValidationError:
        logger.error("arg main must be tuple[str,str]")
        raise ValueError("Arg main must be tuple[str,str]")
    tag, class_name = main[0], main[1]
    if not url or not isinstance(url, str):
        logger.error(f""" "Can't parse with url like {url} """)
        raise ValueError("Url is str type and must not be null ")

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        res = {}
        try:
            page = await browser.new_page()

            try:
                await page.goto(url, wait_until="load")
                for i in range(10):
                    await page.evaluate("""
                        document.querySelector(".scrollable-area.root-scrollable.root-scrollable__content").scrollTo(0, (document.querySelector(".scrollable-area.root-scrollable.root-scrollable__content").scrollHeight - 600))
                    """)
                    await page.wait_for_timeout(2000)
                await page.screenshot(path="screenshot.png")
            except PlaywrightError as exc:
                logger.error(
                    "Url is not valid" + "\n" + "Please check the example of this func"
                )
                raise URLError("Url is not valid") from exc

            content = BeautifulSoup(await page.content(), "html.parser")
            links = content.find_all(
                tag,
                {"class": class_name},
            )
            # IDK: Links is one huge str and still can be iterated many times

            count = 0
            for link in links:
                temp = dict()
                for num, need in enumerate(elements):
                    element = elements[num]
                    fasc = link.find(element[0], {"class": element[1]})
                    match element[2]:
                        case "text":
                            if fasc and fasc is not None:
                                fasc = fasc.text
                        case "src":
                            if fasc and fasc is not None and fasc.has_attr("src"):
                                fasc = fasc.get("src")
                    temp[element[3]] = fasc
                res[count] = list(temp.values())[0] if len(elements) == 1 else temp
                temp = dict()
                count += 1
        finally:
            await browser.close()
            return res
