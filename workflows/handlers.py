from typing import Dict, Any, List
from core.tools import ToolRegistry

class WorkflowHandlers:
    """Specialized handlers for routing intents."""

    @staticmethod
    def handle_inventory_mismatch(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates price difference and reorder suggestions for inventory alerts.
        Expected keys: sku, internal_price, vendor_price, current_stock, min_stock
        """
        internal_price = payload.get("internal_price", 0.0)
        vendor_price = payload.get("vendor_price", 0.0)
        current_stock = payload.get("current_stock", 0)
        min_stock = payload.get("min_stock", 0)

        price_diff = ToolRegistry.calculate_price_difference(internal_price, vendor_price)
        reorder_qty = ToolRegistry.calculate_reorder_quantity(current_stock, min_stock)

        return {
            "workflow": "Inventory Mismatch & Restock",
            "sku": payload.get("sku", "UNKNOWN"),
            "price_discrepancy_pct": price_diff,
            "reorder_quantity": reorder_qty,
            "needs_reorder": reorder_qty > 0,
            "status": "Processed"
        }

    @staticmethod
    def handle_order_tracking(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieves real-time status and delivery info for orders.
        Expected keys: identifier (order_id or email)
        """
        identifier = payload.get("identifier") or payload.get("order_id") or payload.get("customer_email")
        if not identifier:
            return {"error": "Missing order identifier (order_id or email)"}

        order_data = ToolRegistry.query_order_db(identifier)
        if not order_data:
            return {"status": "Not Found", "message": f"No order found for {identifier}"}

        return {
            "workflow": "Order Tracking",
            "order_details": order_data,
            "status": "Success"
        }

    @staticmethod
    def handle_task_allocation(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Matches task skill requirements to employee capabilities and current capacity.
        Expected keys: task_name, required_skills, estimated_hours
        """
        task_name = payload.get("task_name", "General Task")
        req_skills = payload.get("required_skills", [])
        est_hours = payload.get("estimated_hours", 0)

        employees = ToolRegistry.query_employee_db()
        candidates = []

        for emp in employees:
            available_hours = emp["max_capacity"] - emp["workload_hours"]
            if available_hours >= est_hours:
                matching_skills = set(req_skills).intersection(set(emp["skills"]))
                score = len(matching_skills) / max(len(req_skills), 1)
                candidates.append({
                    "employee_id": emp["id"],
                    "name": emp["name"],
                    "match_score": round(score, 2),
                    "remaining_capacity": available_hours
                })

        candidates.sort(key=lambda x: (x["match_score"], x["remaining_capacity"]), reverse=True)

        return {
            "workflow": "Task Allocation",
            "task": task_name,
            "recommended_assignee": candidates[0] if candidates else None,
            "all_candidates": candidates,
            "status": "Success" if candidates else "No Capacity"
        }
