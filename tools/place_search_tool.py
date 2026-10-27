
import os
from typing import List
from dotenv import load_dotenv
from langchain.tools import tool
from utils.place_info_search import (
    GooglePlaceSearchTool,
    TavilyPlaceSearchTool
)


class PlaceSearchTool:
    def __init__(self):
        load_dotenv()

        self.google_api_key = os.getenv("GPLACES_API_KEY")
        self.google_places_search = GooglePlaceSearchTool(
            self.google_api_key
        )
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools()

    def _search(self, city: str, search_type: str) -> str:
        """Search Google Places first and use Tavily as fallback."""

        google_methods = {
            "attractions": self.google_places_search.google_search_attractions,
            "restaurants": self.google_places_search.google_search_restaurants,
            "activities": self.google_places_search.google_search_activity,
            "transportation": self.google_places_search.google_search_transportation,
        }

        tavily_methods = {
            "attractions": self.tavily_search.tavily_search_attractions,
            "restaurants": self.tavily_search.tavily_search_restaurants,
            "activities": self.tavily_search.tavily_search_activity,
            "transportation": self.tavily_search.tavily_search_transportation,
        }

        try:
            result = google_methods[search_type](city)
            if result:
                return f"{search_type.title()} in {city}: {result}"
        except Exception as e:
            google_error = str(e)
        else:
            google_error = "Google Places returned no results."

        try:
            result = tavily_methods[search_type](city)
            if result:
                return f"{search_type.title()} in {city}: {result}"

            return f"No {search_type} results found for {city}."
        except Exception as e:
            return (
                f"Could not find {search_type} for {city}. "
                f"Google error: {google_error}. Tavily error: {e}"
            )

    def _setup_tools(self) -> List:
        """Register tools with explicit argument schemas."""

        @tool
        def search_attractions(city: str) -> str:
            """Find tourist attractions in a city.
            Input must be a JSON object with the key city.
            Example: {"city": "London"}.
            """
            return self._search(city, "attractions")

        @tool
        def search_restaurants(city: str) -> str:
            """Find restaurants in a city.
            Input must be a JSON object with the key city.
            Example: {"city": "London"}.
            """
            return self._search(city, "restaurants")

        @tool
        def search_activities(city: str) -> str:
            """Find activities in a city.
            Input must be a JSON object with the key city.
            Example: {"city": "London"}.
            """
            return self._search(city, "activities")

        @tool
        def search_transportation(city: str) -> str:
            """Find transportation options in a city.
            Input must be a JSON object with the key city.
            Example: {"city": "London"}.
            """
            return self._search(city, "transportation")

        return [
            search_attractions,
            search_restaurants,
            search_activities,
            search_transportation,
        ]
