# 📱 WhatsApp Automation Setup Guide

To automate WhatsApp messages, you need an API provider. Since the official WhatsApp Cloud API is complex to set up, many users prefer **UltraMsg** or similar services for quick integration.

### Option 1: UltraMsg (Recommended for Fast Setup)
1. Go to [UltraMsg.com](https://ultramsg.com/) and create a free trial account.
2. Scan the QR code with your WhatsApp.
3. You will get an **Instance ID** and a **Token**.
4. **Copy these.**

### Option 2: Official WhatsApp Cloud API (Free Tier)
1. Use the same [Facebook Developer App](https://developers.facebook.com/) you created for the Page.
2. Add the **WhatsApp** product.
3. Follow the "Quickstart" to get a **Temporary Access Token** and a **Phone Number ID**.
4. *Note: This requires a verified Business account for long-term use.*

### Update Autoflock Configuration
Paste your credentials into `/data/data/com.termux/files/home/projects/media/autoflock/config/social.json`:

```json
{
  "whatsapp_instance": "instance12345",
  "whatsapp_token": "your_token_here",
  "whatsapp_number": "1234567890" 
}
```
*Note: `whatsapp_number` is the destination (your group or your own number).*

### Implementation Status
I have updated `sheep10/social_poster.py` to use a real API request instead of a simulator.
