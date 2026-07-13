from typing import Dict, List


class RecommendationConfig:
    """
    Controls:
    - Which categories should be fetched.
    - How many places should be fetched.
    - Adapts recommendations based on trip duration and interests.
    """

    # Categories always useful
    BASE_CATEGORIES = [
        "hotels",
        "restaurants",
        "cafes",
    ]

    # Interests -> categories
    INTEREST_CATEGORY_MAP = {

        "culture": [
            "museums",
            "parks",
        ],

        "history": [
            "museums",
        ],

        "nature": [
            "parks",
            "beaches",
        ],

        "beach": [
            "beaches",
        ],

        "shopping": [
            "shopping",
        ],

        "food": [
            "restaurants",
            "cafes",
        ],

        "family": [
            "parks",
            "entertainment",
        ],

        "kids": [
            "parks",
            "entertainment",
        ],

        "nightlife": [
            "entertainment",
        ],

        "adventure": [
            "entertainment",
        ],
    }

    @classmethod
    def get_categories(
        cls,
        interests: List[str] | None,
    ) -> List[str]:

        categories = set(cls.BASE_CATEGORIES)

        if interests:

            for interest in interests:

                interest = interest.lower().strip()

                categories.update(
                    cls.INTEREST_CATEGORY_MAP.get(
                        interest,
                        []
                    )
                )

        return sorted(categories)

    @classmethod
    def get_limits(
        cls,
        days: int,
        interests: List[str] | None = None,
        trip_type: str | None = None,
    ) -> Dict[str, int]:

        days = max(days, 1)

        limits = {

            "hotels": 5,

            "restaurants": min(3 + days, 8),

            "cafes": min(2 + days // 2, 5),

            "museums": min(1 + days // 2, 4),

            "parks": min(1 + days // 2, 4),

            "entertainment": min(1 + days // 2, 4),

            "shopping": min(1 + days // 3, 3),

            "beaches": min(days, 4),
        }

        interests = [
            i.lower().strip()
            for i in (interests or [])
        ]

        # -----------------------------
        # Interest-based adjustments
        # -----------------------------

        if "culture" in interests or "history" in interests:

            limits["museums"] += 2
            limits["parks"] += 1

            limits["shopping"] = max(
                1,
                limits["shopping"] - 1
            )

        if "beach" in interests:

            limits["beaches"] += 2

            limits["museums"] = max(
                1,
                limits["museums"] - 1
            )

        if "shopping" in interests:

            limits["shopping"] += 2

            limits["parks"] = max(
                1,
                limits["parks"] - 1
            )

        if "food" in interests:

            limits["restaurants"] += 2
            limits["cafes"] += 1

        if "family" in interests or "kids" in interests:

            limits["entertainment"] += 2
            limits["parks"] += 1

        if "nightlife" in interests:

            limits["entertainment"] += 2

        if "nature" in interests:

            limits["parks"] += 2
            limits["beaches"] += 1

        # -----------------------------
        # Trip type adjustments
        # -----------------------------

        if trip_type:

            trip_type = trip_type.lower()

            if trip_type == "business":

                limits["restaurants"] = min(
                    limits["restaurants"],
                    5
                )

                limits["cafes"] = min(
                    limits["cafes"],
                    3
                )

                limits["museums"] = 1
                limits["parks"] = 1
                limits["shopping"] = 1

            elif trip_type == "honeymoon":

                limits["cafes"] += 2
                limits["beaches"] += 1

            elif trip_type == "backpacking":

                limits["parks"] += 1
                limits["entertainment"] += 1

        # -----------------------------
        # Hard Caps
        # -----------------------------

        for category, cap in cls.get_hard_caps().items():

            limits[category] = min(
                limits[category],
                cap
            )

        return limits
    
    @classmethod
    def get_hard_caps(cls) -> Dict[str, int]:
        """
        Maximum number of places to fetch and cache
        for each category.
        """

        return {
            "hotels": 5,
            "restaurants": 8,
            "cafes": 5,
            "museums": 4,
            "parks": 4,
            "shopping": 3,
            "entertainment": 4,
            "beaches": 4,
        }