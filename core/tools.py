import re
from typing import Dict, Any, List

class ToolRegistry:
    """Atomic tools used by workflows."""

    @staticmethod
    def calculate_price_difference(internal_price: float, vendor_price: float) -> float:
        if internal_price == 0:
            return 0.0
        return round(abs(internal_price - vendor_price) / internal_price * 100, 2)

    @staticmethod
    def calculate_reorder_quantity(current_stock: int, min_stock: int, buffer_multiplier: float = 1.5) -> int:
        if current_stock >= min_stock:
            return 0
        return int((min_stock * buffer_multiplier) - current_stock)

    @staticmethod
    def query_order_db(identifier: str) -> Dict[str, Any]:
        orders_db = {
            "ORD-1001": {
                "order_id": "ORD-1001",
                "customer_email": "john@example.com",
                "status": "In Transit",
                "items": ["Wireless Ergonomic Mouse", "USB-C Hub"],
                "carrier": "FedEx",
                "tracking_number": "TRK94820194",
                "estimated_delivery": "2026-10-18"
            },
            "ORD-1002": {
                "order_id": "ORD-1002",
                "customer_email": "jane@example.com",
                "status": "Delivered",
                "items": ["Noise Cancelling Headphones"],
                "carrier": "BlueDart",
                "tracking_number": "BD1189423",
                "estimated_delivery": "2026-10-14"
            }
        }
        for k, v in orders_db.items():
            if k.lower() == identifier.lower() or v["customer_email"].lower() == identifier.lower():
                return v
        return None

    @staticmethod
    def query_employee_db() -> List[Dict[str, Any]]:
        return [
            {"id": "EMP01", "name": "Alice Johnson", "skills": ["Python", "Backend", "FastAPI"], "workload_hours": 34, "max_capacity": 40},
            {"id": "EMP02", "name": "Bob Smith", "skills": ["Python", "AI", "LangChain", "LLM"], "workload_hours": 22, "max_capacity": 40},
            {"id": "EMP03", "name": "Carol Lee", "skills": ["Frontend", "React", "UI/UX"], "workload_hours": 15, "max_capacity": 40},
            {"id": "EMP04", "name": "David Kumar", "skills": ["DevOps", "Kubernetes", "AWS"], "workload_hours": 39, "max_capacity": 40}
        ]

    @staticmethod
    def compute_jaccard_similarity(str1: str, str2: str) -> float:
        set1 = set(re.findall(r'\w+', str1.lower()))
        set2 = set(re.findall(r'\w+', str2.lower()))
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return round(intersection / union, 2) if union > 0 else 0.0
