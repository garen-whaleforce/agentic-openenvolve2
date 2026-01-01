
"""
calendar_utils.py

Trading-calendar helpers built on exchange_calendars.

We default to XNYS sessions, which is a practical approximation for US equities.

If you trade ADRs or non-US listings, you can parameterize the calendar name.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import pandas as pd

try:
    import exchange_calendars as ecals
except Exception as e:  # pragma: no cover
    ecals = None


class CalendarError(RuntimeError):
    pass


@dataclass(frozen=True)
class TradingCalendar:
    name: str = "XNYS"

    def _get_cal(self):
        if ecals is None:
            raise CalendarError("exchange_calendars is not installed. Install with: pip install exchange_calendars")
        try:
            return ecals.get_calendar(self.name)
        except Exception as e:
            raise CalendarError(f"Failed to load exchange calendar '{self.name}': {e}")

    def sessions_in_range(self, start: pd.Timestamp, end: pd.Timestamp) -> pd.DatetimeIndex:
        cal = self._get_cal()
        start = pd.Timestamp(start).normalize()
        end = pd.Timestamp(end).normalize()
        # sessions_in_range is inclusive
        return cal.sessions_in_range(start, end)

    def next_session(self, session: pd.Timestamp) -> pd.Timestamp:
        cal = self._get_cal()
        session = pd.Timestamp(session).normalize()
        nxt = cal.next_session(session)
        return pd.Timestamp(nxt).normalize()

    def add_sessions(self, session: pd.Timestamp, n: int) -> pd.Timestamp:
        """
        Add n trading sessions to 'session'.
        If n=0 returns the same session.
        """
        cal = self._get_cal()
        session = pd.Timestamp(session).normalize()
        if n == 0:
            return session
        # sessions_window gives a window inclusive of session
        try:
            # get_loc requires exact match; ensure session is a valid session
            sessions = cal.sessions_in_range(session, session)
            if len(sessions) == 0:
                raise CalendarError(f"{session.date()} is not a valid trading session in {self.name}")
        except Exception as e:
            raise CalendarError(str(e))

        # To add n sessions, we can step iteratively using next_session for robustness
        cur = session
        step = 1 if n > 0 else -1
        for _ in range(abs(n)):
            if step > 0:
                cur = pd.Timestamp(cal.next_session(cur)).normalize()
            else:
                cur = pd.Timestamp(cal.previous_session(cur)).normalize()
        return cur
