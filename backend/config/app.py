from dataclasses import dataclass, asdict, field
from os import getenv
from typing import List


@dataclass
class Server:
    url: str
    description: str

    def dict(self):
        return asdict(self)


@dataclass
class ContactInfo:
    name: str
    email: str

    def dict(self):
        return asdict(self)


@dataclass
class AppConfiguration:
    servers: List[Server]
    description: str = "Deposit calculation system"
    title: str = "Deposit calculation system"
    debug: bool = False
    contact: ContactInfo = field(
        default_factory=lambda: ContactInfo(
            name="Anatoly Ploshchadnyy", email="anatoly.ploshchadnyy@gmail.com"
        )
    )

    def dict(self):
        return asdict(self)


def dev_config() -> AppConfiguration:
    return AppConfiguration(
        servers=[
            Server(
                url="http://localhost:5000",
                description="Local deployment of the service",
            )
        ],
        debug=False,
    )


def deployment_config() -> AppConfiguration:
    return AppConfiguration(
        servers=[
            Server(
                url="https://something.com",
                description="Prod deployment of the service",
            )
        ],
        debug=False,
    )


def get_config() -> AppConfiguration:
    return (
        deployment_config() if getenv("ENV_NAME", "local") == "deploy" else dev_config()
    )
