
import re


class Calculator:
    @staticmethod
    def _to_number(value) -> float:
        """Convert a numeric value or currency-formatted string to float."""
        if isinstance(value, (int, float)):
            return float(value)

        if not isinstance(value, str):
            raise ValueError(f"Expected a number, received {value!r}")

        value = value.strip()
        value = re.sub(r"[£$€₹,\s]", "", value)

        try:
            return float(value)
        except ValueError as e:
            raise ValueError(
                f"Invalid numeric value: {value!r}"
            ) from e

    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiply two numeric values."""
        return Calculator._to_number(a) * Calculator._to_number(b)

    @staticmethod
    def calculate_total(*x: float) -> float:
        """Calculate the sum of the given numbers."""
        return sum(Calculator._to_number(value) for value in x)

    @staticmethod
    def calculate_daily_budget(total: float, days: int) -> float:
        """Calculate the daily budget."""
        total = Calculator._to_number(total)
        days = int(Calculator._to_number(days))

        return total / days if days > 0 else 0.0
