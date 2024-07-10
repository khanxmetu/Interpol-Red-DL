import os

class Config:
    def __init__(
        self,
        base_url=None,
        red_list_path=None,
        result_per_page=None,
        max_pages=None,
        api_rate_limit_delay_ms=None,
        headers_file_path=None,
        queue_name=None
    ) -> None:
        self.BASE_URL: str = base_url or "https://ws-public.interpol.int"
        self.RED_LIST_PATH: str = red_list_path or "/notices/v1/red"
        self.RESULT_PER_PAGE: int = result_per_page or 160
        self.MAX_PAGES: int = max_pages or 1
        self.API_RATE_LIMIT_DELAY_MS: int = api_rate_limit_delay_ms or 0
        self.HEADERS_FILE_PATH: str = headers_file_path or "headers.json"
        self.QUEUE_NAME = queue_name or "fetched_notices"

    @classmethod
    def load_from_env(cls):
        return cls(
            base_url=os.getenv("BASE_URL"),
            red_list_path=os.getenv("RED_LIST_PATH"),
            result_per_page=int(os.getenv("RESULT_PER_PAGE")),
            max_pages=int(os.getenv("MAX_PAGES")),
            api_rate_limit_delay_ms=int(os.getenv("API_RATE_LIMIT_DELAY_MS")),
            queue_name=os.getenv("QUEUE_NAME")
        )
