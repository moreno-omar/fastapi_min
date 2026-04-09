"""Polar.sh SDK integration and helpers."""
import os
from dotenv import load_dotenv
import httpx
import json
from typing import Any
from polar_sdk.webhooks import validate_event, WebhookVerificationError

load_dotenv()

POLAR_TOKEN = os.getenv("POLAR_TOKEN")
POLAR_WEBHOOK_SECRET = os.getenv("POLAR_WEBHOOK_SECRET")
POLAR_PRODUCT_URL = os.getenv("POLAR_PRODUCT")
POLAR_WEBHOOK_URL = os.getenv("POLAR_WEBHOOK_URL")

# Polar API base URL (sandbox)
POLAR_API_BASE = "https://sandbox-api.polar.sh"

# Create Polar API client
polar_client = httpx.AsyncClient(
    base_url=POLAR_API_BASE,
    headers={
        "Authorization": f"Bearer {POLAR_TOKEN}",
        "Content-Type": "application/json",
    },
    timeout=10.0,
)


def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """
    Verify Polar webhook signature using polar_sdk.
    
    Args:
        payload: Raw request body
        signature: X-Webhook-Signature header value
        
    Returns:
        True if signature is valid, False otherwise
        
    Raises:
        WebhookVerificationError: If signature verification fails
    """
    if not POLAR_WEBHOOK_SECRET or not signature:
        return False
    
    try:
        validate_event(payload.decode(), signature, POLAR_WEBHOOK_SECRET)
        return True
    except WebhookVerificationError:
        return False


async def get_checkout_url(packet_id: str) -> str:
    """
    Get checkout URL for a packet.
    
    Args:
        packet_id: The packet/product ID
        
    Returns:
        Polar checkout URL
    """
    # For now, return the product URL directly
    # In production, you'd generate a unique checkout link per request
    return POLAR_PRODUCT_URL


async def send_event_to_polar(event_data: dict) -> dict[str, Any]:
    """
    Send an event to Polar.sh API.
    
    Args:
        event_data: Event data to send
        
    Returns:
        Polar API response
    """
    try:
        response = await polar_client.post(
            "/v1/events",
            json=event_data,
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        return {"error": str(e), "status": getattr(e.response, "status_code", None)}
