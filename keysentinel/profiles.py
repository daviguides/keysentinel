"""Profile management for predefined and custom token templates.

This module defines default token profiles for popular services
(e.g., AWS, GitHub, OpenAI) and allows loading user-defined custom
profiles from a local JSON file.
"""

import json
import os

# --- Default Token Profiles ---

TOKEN_PROFILES = {
    "aws": {
        "description": "AWS Credentials (access + secret keys)",
        "fields": ["aws_access_key_id", "aws_secret_access_key"],
    },
    "github": {
        "description": "GitHub Personal Access Token",
        "fields": ["github_token"],
    },
    "gitlab": {
        "description": "GitLab Personal Access Token",
        "fields": ["gitlab_token"],
    },
    "openai": {
        "description": "OpenAI API Key",
        "fields": ["openai_api_key"],
    },
    "azure": {
        "description": "Azure Service Principal Credentials",
        "fields": [
            "azure_client_id",
            "azure_client_secret",
            "azure_tenant_id",
            "azure_subscription_id",
        ],
    },
    "gcp": {
        "description": "Google Cloud Platform Service Account",
        "fields": [
            "gcp_client_email",
            "gcp_private_key",
            "gcp_project_id",
        ],
    },
    "google_calendar_oauth": {
        "description": "Google Calendar OAuth Client for Local Script",
        "fields": [
            "gcal_client_id",
            "gcal_client_secret",
            "gcal_project_id",
        ],
    },
    "digitalocean": {
        "description": "DigitalOcean API Token",
        "fields": ["do_token"],
    },
    "linode": {
        "description": "Linode Personal Access Token",
        "fields": ["linode_token"],
    },
    "vercel": {
        "description": "Vercel API Token",
        "fields": ["vercel_token"],
    },
    "netlify": {
        "description": "Netlify Personal Access Token",
        "fields": ["netlify_token"],
    },
    "cloudflare": {
        "description": "Cloudflare API Token",
        "fields": ["cloudflare_api_token"],
    },
    "slack": {
        "description": "Slack Bot/User OAuth Token",
        "fields": ["slack_token"],
    },
    "discord": {
        "description": "Discord Bot Token",
        "fields": ["discord_bot_token"],
    },
    "twilio": {
        "description": "Twilio Account Credentials",
        "fields": ["twilio_account_sid", "twilio_auth_token"],
    },
    "sendgrid": {
        "description": "SendGrid API Key",
        "fields": ["sendgrid_api_key"],
    },
    "stripe": {
        "description": "Stripe Secret API Key",
        "fields": ["stripe_secret_key"],
    },
    "paypal": {
        "description": "PayPal REST API Credentials",
        "fields": ["paypal_client_id", "paypal_client_secret"],
    },
    "mongoatlas": {
        "description": "MongoDB Atlas API Key",
        "fields": ["mongo_public_key", "mongo_private_key"],
    },
    "algolia": {
        "description": "Algolia Search API Credentials",
        "fields": ["algolia_app_id", "algolia_admin_api_key"],
    },
    "firebase": {
        "description": "Firebase Admin SDK Credentials",
        "fields": [
            "firebase_project_id",
            "firebase_private_key",
            "firebase_client_email",
        ],
    },
    "notion": {
        "description": "Notion Integration Secret",
        "fields": ["notion_integration_token"],
    },
    "asana": {
        "description": "Asana Personal Access Token",
        "fields": ["asana_token"],
    },
    "trello": {
        "description": "Trello API Credentials",
        "fields": ["trello_key", "trello_token"],
    },
    "jira": {
        "description": "Jira API Token",
        "fields": ["jira_email", "jira_api_token"],
    },
    "zendesk": {
        "description": "Zendesk API Token",
        "fields": ["zendesk_email", "zendesk_api_token"],
    },
    "bitbucket": {
        "description": "Bitbucket App Password",
        "fields": ["bitbucket_username", "bitbucket_app_password"],
    },
    "sentry": {
        "description": "Sentry Auth Token",
        "fields": ["sentry_auth_token"],
    },
    "dockerhub": {
        "description": "DockerHub Access Credentials",
        "fields": ["dockerhub_username", "dockerhub_password"],
    },
    "heroku": {
        "description": "Heroku API Key",
        "fields": ["heroku_api_key"],
    },
    "supabase": {
        "description": "Supabase API Credentials",
        "fields": ["supabase_url", "supabase_anon_key", "supabase_service_role_key"],
    },
    "huggingface": {
        "description": "Hugging Face API Token",
        "fields": ["hf_token"],
    },
}

# Path to load custom profiles from user environment.
DEFAULT_CUSTOM_PROFILES_PATH = os.getenv(
    "KEYSENTINEL_CUSTOM_PROFILES_PATH", "~/.keysentinel_profiles.json"
)


def load_custom_profiles_from_json(filepath: str | None = None) -> dict:
    """Load custom token profiles from a local JSON file.

    Args:
        filepath (str | None): Path to a custom profiles JSON file.
            Defaults to `DEFAULT_CUSTOM_PROFILES_PATH`.

    Returns:
        dict: Dictionary with custom profile definitions, or an empty dict if not found or invalid.
    """
    if filepath is None:
        filepath = DEFAULT_CUSTOM_PROFILES_PATH
    filepath = os.path.expanduser(filepath)

    if not os.path.exists(filepath):
        return {}

    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def get_token_profiles(custom_profiles: dict | None = None) -> dict[str, dict]:
    """Return the combined dictionary of default and custom token profiles.

    Args:
        custom_profiles (dict | None): Optional dictionary of custom profiles
            to merge with the defaults. If None, attempts to load from JSON file.

    Returns:
        dict[str, dict]: Merged dictionary of token profiles.
    """
    profiles = TOKEN_PROFILES.copy()

    if custom_profiles is None:
        custom_profiles = load_custom_profiles_from_json()

    if custom_profiles:
        profiles.update(custom_profiles)

    return profiles


# --- Example structure for documentation purposes ---

EXAMPLE_CUSTOM_PROFILES_JSON = """
{
  "huggingface": {
    "description": "Hugging Face API Token",
    "fields": ["hf_token"]
  },
  "figma": {
    "description": "Figma Personal Access Token",
    "fields": ["figma_token"]
  }
}
"""

# Users can create a file ~/.keysentinel_profiles.json with this structure to extend profiles automatically.
