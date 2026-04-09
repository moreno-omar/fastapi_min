"""Payment routes for Polar.sh integration."""
import json
from fastapi import APIRouter, Depends, HTTPException, Request, Header
from app.users import current_active_user
from app.db import User
from app.polar import (
    get_checkout_url,
    verify_webhook_signature,
    send_event_to_polar,
)

router = APIRouter(prefix="/payments", tags=["payments"])
webhook_router = APIRouter(tags=["webhooks"])

# In-memory user state for tracking payments
user_payments = {}


@router.post("/checkout")
async def checkout(
    packet_id: str,
    user: User = Depends(current_active_user),
):
    """
    Generate Polar checkout URL for a packet.
    
    Args:
        packet_id: The packet ID to purchase
        user: Current authenticated user
        
    Returns:
        Checkout URL to redirect user to
    """
    checkout_url = await get_checkout_url(packet_id)
    
    # Store checkout intent in memory
    user_payments[str(user.id)] = {
        "packet_id": packet_id,
        "status": "pending",
    }
    
    return {
        "checkout_url": checkout_url,
        "user_id": str(user.id),
        "packet_id": packet_id,
    }


@webhook_router.post("/webhooks/polar")
async def polar_webhook(
    request: Request,
    x_webhook_signature: str = Header(None),
):
    """
    Webhook endpoint for Polar.sh payment events.
    
    Args:
        request: The webhook request
        x_webhook_signature: Webhook signature header
        
    Returns:
        Acknowledgment of webhook receipt
    """
    # Get raw body for signature verification
    raw_body = await request.body()
    
    # Verify webhook signature
    if not verify_webhook_signature(raw_body, x_webhook_signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    # Parse body
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # Handle payment completion event
    event_type = payload.get("type")
    
    if event_type == "order.completed":
        order_data = payload.get("data", {})
        customer_email = order_data.get("customer", {}).get("email")
        product_id = order_data.get("product_id")
        order_id = order_data.get("id")
        
        # In a real app, look up user by email and update database
        # For now, log to memory and mark as verified
        print(f"✓ Payment received: {order_id} for {customer_email}")
        print(f"  Product: {product_id}")
        
        # Store successful payment (in production: update DB)
        user_payments[customer_email] = {
            "order_id": order_id,
            "product_id": product_id,
            "status": "completed",
        }
    
    elif event_type == "order.created":
        order_data = payload.get("data", {})
        print(f"Order created: {order_data.get('id')}")
    
    # Acknowledge webhook receipt
    return {"status": "received"}


@router.post("/test-event")
async def test_event(
    event_data: dict,
    user: User = Depends(current_active_user),
):
    """
    Test endpoint for sending events to Polar.sh API.
    Used to verify integration is working.
    
    Args:
        event_data: Event data to send
        user: Current authenticated user
        
    Returns:
        Polar API response
    """
    # Add user context to event
    event_with_user = {
        **event_data,
        "user_id": str(user.id),
        "email": user.email,
    }
    
    # Send to Polar API
    result = await send_event_to_polar(event_with_user)
    
    return {
        "sent_to_polar": True,
        "user_id": str(user.id),
        "polar_response": result,
    }
