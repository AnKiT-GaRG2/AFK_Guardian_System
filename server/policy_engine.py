import os


class DecisionPolicyEngine:
    PRODUCTIVE_WINDOW_KEYWORDS = [
        "visual studio code",
        "vscode",
        "code",
        "chrome",
        "google chrome",
        "jetbrains",
        "pycharm",
        "intellij",
        "terminal",
        "bash",
        "zsh",
    ]

    def __init__(self):
        self.mode = os.getenv("PAY_POLICY_MODE", "productivity_percent").strip().lower()
        if self.mode not in {"productive_time", "productivity_percent"}:
            self.mode = "productivity_percent"

        self.time_unit_seconds = int(os.getenv("PAY_TIME_UNIT_SECONDS", "30"))
        if self.time_unit_seconds <= 0:
            self.time_unit_seconds = 30

        self.pay_rate_per_unit = float(os.getenv("PAY_RATE_PER_UNIT", "1"))
        if self.pay_rate_per_unit < 0:
            self.pay_rate_per_unit = 0.0

    @staticmethod
    def _clamp(value, min_value, max_value):
        return min(max(value, min_value), max_value)

    @staticmethod
    def _safe_number(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def _calculate_productivity_percent(self, details):
        activity_summary = details.get("activity_summary", {})
        window_activity = details.get("window_activity", {})

        speaking_time = self._safe_number(activity_summary.get("SPEAKING", 0))
        not_speaking_time = self._safe_number(activity_summary.get("NOT SPEAKING", 0))
        eyes_open_time = self._safe_number(activity_summary.get("eyes_open_time", 0))
        eyes_closed_time = self._safe_number(activity_summary.get("eyes_closed_time", 0))
        eyes_not_detected_time = self._safe_number(activity_summary.get("eyes_not_detected_time", 0))

        eye_total = eyes_open_time + eyes_closed_time + eyes_not_detected_time
        voice_total = speaking_time + not_speaking_time

        eye_score = (
            self._clamp((eyes_open_time - 0.4 * eyes_closed_time - 0.9 * eyes_not_detected_time) / eye_total, 0, 1)
            if eye_total > 0
            else 0.5
        )

        voice_score = (
            self._clamp((not_speaking_time + 0.6 * speaking_time) / voice_total, 0, 1)
            if voice_total > 0
            else 0.5
        )

        total_keyboard = 0.0
        total_mouse_movement = 0.0
        total_mouse_clicks = 0.0
        total_mouse_scrolls = 0.0
        total_tracked_window_time = 0.0
        max_single_window_time = 0.0
        productive_window_time = 0.0

        for window_name, window_entry in window_activity.items():
            time_spent = self._safe_number(window_entry.get("time_spent", 0))
            activities = window_entry.get("activities", {})
            normalized_window_name = str(window_name or "").lower()
            is_productive_window = any(
                keyword in normalized_window_name for keyword in self.PRODUCTIVE_WINDOW_KEYWORDS
            )

            total_tracked_window_time += time_spent
            max_single_window_time = max(max_single_window_time, time_spent)
            if is_productive_window:
                productive_window_time += time_spent

            total_keyboard += self._safe_number(activities.get("keyboard_activity", {}).get("count", 0))
            total_mouse_movement += self._safe_number(activities.get("mouse_movement_distance", {}).get("count", 0))
            total_mouse_clicks += self._safe_number(activities.get("mouse_clicks", {}).get("count", 0))
            total_mouse_scrolls += self._safe_number(activities.get("mouse_scrolls", {}).get("count", 0))

        keyboard_signal = self._clamp(total_keyboard / 60, 0, 1)
        movement_signal = self._clamp(total_mouse_movement / 5000, 0, 1)
        click_signal = self._clamp(total_mouse_clicks / 12, 0, 1)
        scroll_signal = self._clamp(total_mouse_scrolls / 40, 0, 1)

        interaction_score = self._clamp(
            0.4 * keyboard_signal
            + 0.25 * movement_signal
            + 0.2 * click_signal
            + 0.15 * scroll_signal,
            0,
            1,
        )

        focus_score = (
            self._clamp(max_single_window_time / total_tracked_window_time, 0, 1)
            if total_tracked_window_time > 0
            else 0.5
        )

        productive_window_score = (
            self._clamp(productive_window_time / total_tracked_window_time, 0, 1)
            if total_tracked_window_time > 0
            else 0.5
        )

        weighted_score = self._clamp(
            0.3 * eye_score
            + 0.15 * voice_score
            + 0.3 * interaction_score
            + 0.1 * focus_score
            + 0.15 * productive_window_score,
            0,
            1,
        )

        return round(weighted_score * 100)

    def _calculate_tracked_seconds(self, details):
        window_activity = details.get("window_activity", {})
        tracked_seconds = 0.0
        productive_seconds = 0.0

        for window_name, window_entry in window_activity.items():
            time_spent = self._safe_number(window_entry.get("time_spent", 0))
            normalized_window_name = str(window_name or "").lower()
            is_productive_window = any(
                keyword in normalized_window_name for keyword in self.PRODUCTIVE_WINDOW_KEYWORDS
            )
            tracked_seconds += time_spent
            if is_productive_window:
                productive_seconds += time_spent

        return tracked_seconds, productive_seconds

    def evaluate_employee(self, employee_records):
        sorted_records = sorted(employee_records.items(), key=lambda item: item[0])

        accumulated_pay = 0.0
        total_productive_seconds = 0.0
        policy_records = []

        for timestamp, details in sorted_records:
            productivity_percent = self._calculate_productivity_percent(details)
            tracked_seconds, productive_seconds = self._calculate_tracked_seconds(details)
            total_productive_seconds += productive_seconds

            unit_fraction = tracked_seconds / self.time_unit_seconds if self.time_unit_seconds else 0

            # Guardrail: do not award pay when no productive time was observed.
            if productive_seconds <= 0:
                pay_earned = 0
            elif self.mode == "productive_time":
                pay_earned = self.pay_rate_per_unit * (productive_seconds / self.time_unit_seconds)
            else:
                pay_earned = self.pay_rate_per_unit * (productivity_percent / 100.0) * unit_fraction

            pay_earned = round(max(pay_earned, 0), 2)
            accumulated_pay = round(accumulated_pay + pay_earned, 2)

            policy_records.append(
                {
                    "timestamp": timestamp,
                    "productivity_percent": productivity_percent,
                    "tracked_seconds": round(tracked_seconds, 2),
                    "productive_seconds": round(productive_seconds, 2),
                    "pay_earned": pay_earned,
                    "accumulated_pay": accumulated_pay,
                }
            )

        return {
            "config": {
                "mode": self.mode,
                "time_unit_seconds": self.time_unit_seconds,
                "pay_rate_per_unit": round(self.pay_rate_per_unit, 2),
            },
            "accumulated_pay": round(accumulated_pay, 2),
            "total_productive_seconds": round(total_productive_seconds, 2),
            "records": policy_records,
        }
