from typing import Optional
from urllib.request import Request, urlopen
from http.client import HTTPResponse
from urllib.error import HTTPError

from minio import Minio

from notice_saver.exceptions import (
    ImageDownloadException,
    InterpolServerRequestException,
    NotAnImageException,
)


class ImageHTTPHeaderListParser:
    def __init__(self, headers_list: list[str, str]):
        self._headers_list = headers_list

    def get_value(self, target_header_name: str) -> Optional[str | int]:
        for header_name, header_value in self._headers_list:
            if header_name == target_header_name:
                try:
                    return int(header_value)
                except ValueError:
                    return header_value
        return None

    def get_image_file_type(self, default: str = "jpg") -> Optional[str]:
        content_type = self.get_content_type()
        if not content_type:
            return default
        else:
            if not content_type.startswith("image/"):
                raise NotAnImageException(
                    "expected image type but received {content_type} instead"
                )
            else:
                return content_type.split("/")[1].lower()

    def get_content_type(self) -> Optional[str]:
        return self.get_value("Content-Type")

    def get_content_length(self) -> Optional[int]:
        return self.get_value("Content-Length")


class ImageDownloader:
    def __init__(
        self,
        bucket_name: str,
        request_headers: dict[str, str],
        public_base_url: str,
        minio_client: Minio,
    ):
        self._minio_client = minio_client
        self._bucket_name = bucket_name
        self._bucket_registered = False
        self._request_headers = request_headers
        self._public_base_url = public_base_url

    def _ensure_bucket_exists(self) -> None:
        if self._bucket_registered:
            return
        if not self._minio_client.bucket_exists(self._bucket_name):
            self._minio_client.make_bucket(self._bucket_name)
        self._bucket_registered = True

    def _get_response(self, request: Request):
        try:
            response: HTTPResponse = urlopen(request)
        except HTTPError as e:
            raise InterpolServerRequestException(e)
        return response

    def download_and_get_public_url(
        self, source_url: str, destination_directory: str, file_name: str
    ) -> str:
        self._ensure_bucket_exists()
        request = Request(source_url, headers=self._request_headers)
        try:
            response = self._get_response(request)
        except InterpolServerRequestException as e:
            raise ImageDownloadException(
                f"unable to fetch response. error: {e}"
            )

        header_list_parser = ImageHTTPHeaderListParser(response.getheaders())
        dst_path = f"{destination_directory}/{file_name}.{header_list_parser.get_image_file_type()}"
        length = header_list_parser.get_content_length() or -1
        part_size = 10 * 1024 * 1024

        self._minio_client.put_object(
            bucket_name=self._bucket_name,
            object_name=dst_path,
            data=response,
            length=length,
            content_type=header_list_parser.get_content_type(),
            part_size=part_size,
        )
        public_url = f"{self._public_base_url}/{self._bucket_name}/{dst_path}"
        return public_url
