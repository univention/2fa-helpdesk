# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from abc import ABC, abstractmethod
from .auth import AuthPort


class APIPort(ABC):
    @property
    @abstractmethod
    def auth(self) -> AuthPort:
        ...

    @abstractmethod
    def reset_own_token(self, username: str) -> None:
        ...

    @abstractmethod
    def reset_user_tokens(self, usernames: list[str]) -> None:
        ...

    @abstractmethod
    def list_users(self, query: str) -> list[dict]:
        ...
