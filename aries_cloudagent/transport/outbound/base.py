"""Base outbound transport."""

import asyncio
from abc import ABC, abstractmethod
from typing import Union

from ...utils.stats import Collector
from ...config.injection_context import InjectionContext

from ..error import TransportError
from ..wire_format import BaseWireFormat


class BaseOutboundTransport(ABC):
    """Base outbound transport class."""

    def __init__(self, wire_format: BaseWireFormat = None) -> None:
        """Initialize a `BaseOutboundTransport` instance."""
        self._collector = None
        self._wire_format = wire_format
        self._context = None

    @property
    def context(self) -> InjectionContext:
        """Accessor for InjectionContext for any context injection purposes."""
        return self._context

    @context.setter
    def context(self, conn: InjectionContext):
        """Assign a new InjectionContext to instance."""
        self._context = conn

    @property
    def collector(self) -> Collector:
        """Accessor for the stats collector instance."""
        return self._collector

    @collector.setter
    def collector(self, coll: Collector):
        """Assign a new stats collector instance."""
        self._collector = coll

    async def __aenter__(self):
        """Async context manager enter."""
        await self.start()

    async def __aexit__(self, err_type, err_value, err_t):
        """Async context manager exit."""
        if err_type and err_type != asyncio.CancelledError:
            self.logger.exception("Exception in outbound transport")
        await self.stop()

    @abstractmethod
    async def start(self):
        """Start the transport."""

    @abstractmethod
    async def stop(self):
        """Shut down the transport."""

    @property
    def wire_format(self) -> BaseWireFormat:
        """Accessor for a custom wire format for the transport."""
        return self._wire_format

    @wire_format.setter
    def wire_format(self, format: BaseWireFormat):
        """Setter for a custom wire format for the transport."""
        self._wire_format = format

    @abstractmethod
    async def handle_message(self, payload: Union[str, bytes], endpoint: str):
        """
        Handle message from queue.

        Args:
            payload: message payload in string or byte format
            endpoint: URI endpoint for delivery
        """


class OutboundTransportError(TransportError):
    """Generic outbound transport error."""


class OutboundTransportRegistrationError(OutboundTransportError):
    """Outbound transport registration error."""


class OutboundDeliveryError(OutboundTransportError):
    """Base exception when a message cannot be delivered via an outbound transport."""
