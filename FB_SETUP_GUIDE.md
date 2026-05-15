# 📘 Facebook Page API Setup Guide

To automate posts to your Facebook Page, follow these steps to get your **Page ID** and a **Permanent Page Access Token**.

### 1. Create a Facebook Developer App
1. Go to [Facebook Developers](https://developers.facebook.com/).
2. Click **My Apps** > **Create App**.
3. Select **Other** > **Business** (or the type that fits your page).
4. Give it a name (e.g., "Autoflock Poster").

### 2. Add "Facebook Login for Business"
1. In your App Dashboard, find **Add a Product**.
2. Add **Facebook Login for Business**.

### 3. Generate a Long-Lived Token (The Fast Way)
1. Go to the [Graph API Explorer](https://developers.facebook.com/tools/explorer/).
2. **Meta App**: Select your "Autoflock Poster" app.
3. **User or Page**: Select your **Facebook Page** (it will ask you to login and grant permissions).
4. **Permissions**: Add these 3 specific permissions:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_show_list`
5. Click **Generate Access Token**.
6. **Important**: This is a short-lived token (1 hour). To make it permanent/long-lived:
   - Copy the token.
   - Go to the [Access Token Tool](https://developers.facebook.com/tools/accesstoken/).
   - Click **Debug** next to your token.
   - Click **Extend Access Token** at the bottom.
   - This gives you a 60-day token. Page tokens generated this way often become permanent if you don't change your password.

### 4. Get your Page ID
1. Go to your Facebook Page > **About** > **Page Transparency**.
2. Your **Page ID** is listed there.

### 5. Update Autoflock
Paste these values into `/data/data/com.termux/files/home/projects/media/autoflock/config/social.json`:
```json
{
  "facebook_page_id": "YOUR_PAGE_ID",
  "facebook_access_token": "YOUR_ACCESS_TOKEN"
}
```
