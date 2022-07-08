# AMBOSS Anki Add-on
#
# Copyright (C) 2019-2020 AMBOSS MD Inc. <https://www.amboss.com/us>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import json
from enum import Enum
from typing import NamedTuple, Optional

from urllib3.exceptions import HTTPError  # type: ignore[import]

from .network import HTTPClientFactory, RateLimit, RateLimitParser, TokenAuth


class GraphQLQueryMeta(NamedTuple):
    rate_limit: Optional[RateLimit] = None


class GraphQLQueryResponse(NamedTuple):
    data: dict
    meta: Optional[GraphQLQueryMeta] = None


class GraphQLException(Exception):
    """Generic GraphQL exception."""

    def __init__(self, message=None):
        """TODO: get rid of this and don't use it for control flow"""
        self.message = message

    def __repr__(self):
        return str(self.message)


class GraphQLNetworkException(GraphQLException):
    """Generic GraphQL client exception."""

    pass


class GraphQLClientException(GraphQLException):
    """Generic GraphQL client exception."""

    pass


class GraphQLErrorCode(Enum):
    wrong_credentials = "access_denied.credentials_are_wrong"
    not_authorized = "permission.user_is_not_authorized"


class GraphQLQueryResolver:
    def __init__(
        self,
        uri: str,
        token_auth: TokenAuth,
        http_client_factory: HTTPClientFactory,
        rate_limit_parser: RateLimitParser,
    ):
        self._token_auth = token_auth
        self._http_client = http_client_factory.create(uri)
        self._rate_limit_parser = rate_limit_parser

    def resolve(self, query: str) -> GraphQLQueryResponse:
        """
        Resolves query to unprocessed GraphQL response data dict.
        Injects request rate-limit metadata, if available.

        :raises GraphQLNetworkException: Networking error
        :raises GraphQLClientException:  Bad data or unexpected format
        """

        try:
            response = self._http_client.post(
                {"query": query}, self._token_auth.get_header()
            )
        except HTTPError as e:
            raise GraphQLNetworkException(str(e))
        try:
            data = json.loads(response.data.decode("utf-8"))
        except ValueError as e:
            raise GraphQLClientException(f"Response status {response.status}\n\n{e}")
        if not isinstance(data, dict):
            raise GraphQLClientException(data)
        if "data" not in data:
            raise GraphQLClientException(data)

        rate_limit = self._rate_limit_parser.parse(response.headers)

        return GraphQLQueryResponse(
            data=data,
            meta=GraphQLQueryMeta(rate_limit=rate_limit) if rate_limit else None,
        )
