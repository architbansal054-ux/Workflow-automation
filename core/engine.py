import re
from typing import Dict, Any
from workflows.handlers import WorkflowHandlers

class WorkflowOrchestrator:
    """Scalable orchestrator mapping user requests to workflow handlers."""

    CATALOG = {
        "WF001": {"name": "Inventory Restock Check", "handler": WorkflowHandlers.handle_inventory_mismatch, "keywords": ["restock", "inventory", "stock"]},
        "WF005": {"name": "Customer Order Status", "handler": WorkflowHandlers.handle_order_tracking, "keywords": ["order", "ord-", "tracking", "where is"]},
        "WF009": {"name": "Employee Task Assignment", "handler": WorkflowHandlers.handle_task_allocation, "keywords": ["assign", "task", "developer"]}
    }

    def route(self, request_text: str) -> str:
        req = request_text.lower()
        for wf_id, item in self.CATALOG.items():
            if any(k in req for k in item["keywords"]):
                return wf_id
        return "WF001"

    def execute(self, request_text: str, custom_inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        wf_id = self.route(request_text)
        wf_meta = self.CATALOG[wf_id]
        inputs = custom_inputs or {}

        if wf_id == "WF005":
            match = re.search(r'ORD-\d+', request_text, re.IGNORECASE)
            inputs["identifier"] = match.group(0).upper() if match else "ORD-1001"
            
        elif wf_id == "WF009":
            inputs.setdefault("required_skills", ["Python", "AI"])
            inputs.setdefault("estimated_hours", 2)

        result = wf_meta["handler"](inputs)
        return {
            "selected_workflow": f"{wf_id}: {wf_meta['name']}",
            "result": result
        }
