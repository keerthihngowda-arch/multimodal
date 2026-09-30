import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def load_data():
    orders_path = os.path.join(BASE_DIR, "data", "orders.json")
    policies_path = os.path.join(BASE_DIR, "data", "policies.json")

    with open(orders_path) as f:
        orders = json.load(f)

    with open(policies_path) as f:
        policies = json.load(f)

    docs = []

    # =========================
    # 📦 ORDERS (Natural Language)
    # =========================
    for o in orders:
        doc = f"""
        Order {o.get('order_id')} for {o.get('item')} is currently {o.get('status')}.
        """

        if o.get("expected_delivery"):
            doc += f" It is expected to be delivered by {o.get('expected_delivery')}."

        if o.get("delivery_date"):
            doc += f" It was delivered on {o.get('delivery_date')}."

        if o.get("current_location"):
            doc += f" Current location of the order is {o.get('current_location')}."

        if o.get("delay_reason"):
            doc += f" The order is delayed due to {o.get('delay_reason')}."

        if o.get("refund_status"):
            doc += f" Refund status is {o.get('refund_status')}."

        if o.get("return_status"):
            doc += f" Return status is {o.get('return_status')}."

        docs.append(doc.strip())

    # =========================
    # 🔄 RETURN POLICY
    # =========================
    returns = policies["returns"]
    docs.append(
        f"""
        Returns are {'allowed' if returns['allowed'] else 'not allowed'} within {returns['window_days']} days.
        Conditions include: {', '.join(returns['conditions'])}.
        Exceptions: {', '.join(returns.get('exceptions', []))}.
        """
    )

    # =========================
    # 💰 REFUND POLICY
    # =========================
    refunds = policies["refunds"]
    docs.append(
        f"""
        Refunds are processed via {refunds['method']} within {refunds['processing_time_days']} days.
        """
    )

    # =========================
    # ❌ CANCELLATION POLICY
    # =========================
    if "cancellations" in policies:
        cancel = policies["cancellations"]
        docs.append(
            f"""
            Orders can be cancelled {'only before shipping' if cancel['before_shipping_only'] else 'anytime'}.
            """
        )

    # =========================
    # 🚚 SHIPPING INFO
    # =========================
    if "shipping" in policies:
        ship = policies["shipping"]
        docs.append(
            f"""
            Standard delivery takes {ship['standard_delivery_days']}.
            Orders may be delayed due to: {', '.join(ship['delayed_conditions'])}.
            """
        )

    # =========================
    # ❓ FAQ (VERY IMPORTANT)
    # =========================
    if "faq" in policies:
        for faq in policies["faq"]:
            docs.append(
                f"Question: {faq['question']} Answer: {faq['answer']}"
            )

    return docs