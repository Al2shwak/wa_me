#!/usr/bin/env python

import logging
import traceback
import sys
from typing import Any, Dict, Type

from .context import Ctx
from .core.client import Client

__all__ = ("Bot",)

_log = logging.getLogger(__name__)

CTX = Type[Ctx]


class Bot(Client):
    """Represents a Whatsapp bot."""

    async def handle(self, data: Dict[str, Any], *, cls_ctx: CTX = Ctx) -> None:
        try:
            _log.debug(f"Received event {data}")
            ctx = cls_ctx(self, data)
            await self.before_event(ctx)
            if ctx.error:
                await self.on_event_error(ctx)
            elif ctx.message:
                await self.before_event_message(ctx)
                if ctx.message.context:
                    await self.on_event_message_context(ctx)
                if ctx.message.referral:
                    await self.on_event_message_referral(ctx)
                if ctx.message.errors:
                    await self.on_event_message_error(ctx)
                else:
                    await getattr(self, f"on_event_message_{ctx.message.type.value}")(ctx)
                await self.after_event_message(ctx)
            elif ctx.status:
                await self.before_event_status(ctx)
                if ctx.status.errors:
                    await self.on_event_status_error(ctx)
                else:
                    await getattr(self, f"on_event_status_{ctx.status.status.value}")(ctx)
                await self.after_event_status(ctx)
            await self.after_event(ctx)
        except Exception as e:
            await self.on_exception(ctx, e)

    async def on_exception(self, ctx: Ctx, e: Exception) -> None:
        """The default error handler provided by the handler."""
        traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)

    async def before_event(self, ctx: Ctx) -> None:
        ...

    async def after_event(self, ctx: Ctx) -> None:
        ...

    async def before_event_message(self, ctx: Ctx) -> None:
        ...

    async def after_event_message(self, ctx: Ctx) -> None:
        ...

    async def before_event_status(self, ctx: Ctx) -> None:
        ...

    async def after_event_status(self, ctx: Ctx) -> None:
        ...

    async def on_event_error(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_audio(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_button(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_contacts(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_context(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_document(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_error(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_image(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_interactive(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_location(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_order(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_reaction(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_referral(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_sticker(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_system(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_template(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_text(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_unknown(self, ctx: Ctx) -> None:
        ...

    async def on_event_message_video(self, ctx: Ctx) -> None:
        ...

    async def on_event_status_deleted(self, ctx: Ctx) -> None:
        ...

    async def on_event_status_delivered(self, ctx: Ctx) -> None:
        ...

    async def on_event_status_error(self, ctx: Ctx) -> None:
        ...

    async def on_event_status_failed(self, ctx: Ctx) -> None:
        ...

    async def on_event_status_read(self, ctx: Ctx) -> None:
        ...

    async def on_event_status_sent(self, ctx: Ctx) -> None:
        ...
