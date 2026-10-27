
from typing import List
from langchain.tools import tool
from utils.expense_calculator import Calculator


class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Set up all expense calculator tools."""

        @tool
        def estimate_total_hotel_cost(
            price_per_night: float,
            total_days: int
        ) -> float:
            """Calculate total hotel cost.
            price_per_night: Numeric price per night, without currency symbols.
            total_days: Number of nights.
            """
            return self.calculator.multiply(
                float(price_per_night),
                int(total_days)
            )

        @tool
        def calculate_total_expense(costs: List[float]) -> float:
            """Calculate total trip expenses.
            costs: A list of numeric expenses, such as [150.0, 200.0, 50.0].
            Do not include currency symbols in the values.
            """
            numeric_costs = [float(cost) for cost in costs]
            return self.calculator.calculate_total(*numeric_costs)

        @tool
        def calculate_daily_expense_budget(
            total_cost: float,
            days: int
        ) -> float:
            """Calculate the daily expense budget.
            total_cost: Total numeric cost of the trip.
            days: Number of days.
            """
            return self.calculator.calculate_daily_budget(
                float(total_cost),
                int(days)
            )

        return [
            estimate_total_hotel_cost,
            calculate_total_expense,
            calculate_daily_expense_budget
        ]
