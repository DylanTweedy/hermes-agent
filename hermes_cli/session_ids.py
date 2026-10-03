"""Session identity helpers shared by interactive CLI launch surfaces."""

from __future__ import annotations

import os
import re
import uuid
from datetime import datetime


def new_cli_session_id(session_start: datetime) -> str:
    """Create a fresh session ID scoped to an optional launcher namespace.

    HERMES_HOME remains the shared profile/config/memory root. A launcher can
    set HERMES_SESSION_NAMESPACE to keep independent surfaces from sharing a
    transcript lease. The CLI calls this for startup and /new rotation.
    """
    timestamp = session_start.strftime("%Y%m%d_%H%M%S")
    suffix = uuid.uuid4().hex[:6]
    namespace = os.environ.get("HERMES_SESSION_NAMESPACE", "").strip()
    if namespace:
        namespace = re.sub(r"[^A-Za-z0-9_.-]+", "-", namespace).strip("-_.")[:48]
        if namespace:
            return f"{timestamp}_{namespace}_{suffix}"
    return f"{timestamp}_{suffix}"
