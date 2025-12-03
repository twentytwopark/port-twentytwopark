"""
Port MCP Authentication Wrapper for GitHub Copilot
Supports individual user credentials via GitHub Environments

This script:
1. Reads credentials from environment variables (set by GitHub Actions)
2. Exchanges client credentials for an access token
3. Connects to Port MCP Server using the token
"""

import os
import sys
import subprocess
import requests
import json

def get_access_token():
    """Exchange client credentials for access token"""
    # Get credentials from environment variables
    # These are set by GitHub Actions based on the environment
    client_id = os.environ.get("PORT_CLIENT_ID")
    client_secret = os.environ.get("PORT_CLIENT_SECRET")
    auth_base_url = os.environ.get("PORT_AUTH_BASE_URL", "https://api.getport.io")
    
    # Debug information (without exposing secrets)
    github_actor = os.environ.get("GITHUB_ACTOR", "unknown")
    github_env = os.environ.get("GITHUB_ENV_NAME", "default")
    
    if not client_id or not client_secret:
        print(f"Error: PORT_CLIENT_ID and PORT_CLIENT_SECRET must be set", file=sys.stderr)
        print(f"Debug: User={github_actor}, Environment={github_env}", file=sys.stderr)
        print(f"Debug: PORT_CLIENT_ID is {'set' if client_id else 'NOT SET'}", file=sys.stderr)
        print(f"Debug: PORT_CLIENT_SECRET is {'set' if client_secret else 'NOT SET'}", file=sys.stderr)
        print(f"Debug: PORT_AUTH_BASE_URL = {auth_base_url}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Exchange credentials for access token
        response = requests.post(
            f"{auth_base_url}/v1/auth/access_token",
            json={"clientId": client_id, "clientSecret": client_secret},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data.get("accessToken")
        
        if not access_token:
            print(f"Error: No access token in response", file=sys.stderr)
            print(f"Response: {token_data}", file=sys.stderr)
            sys.exit(1)
        
        print(f"Successfully authenticated for user: {github_actor}", file=sys.stderr)
        return access_token
        
    except requests.exceptions.RequestException as e:
        print(f"Error authenticating with Port: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                print(f"Error details: {error_detail}", file=sys.stderr)
            except:
                print(f"Response text: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except KeyError:
        print("Error: Invalid response from Port API", file=sys.stderr)
        sys.exit(1)

def main():
    """Main entry point - fetches token and launches mcp-remote"""
    # Get access token
    token = get_access_token()
    
    # Get MCP URL from environment (defaults to US region)
    mcp_url = os.environ.get("PORT_MCP_URL", "https://mcp.us.port.io/v1")
    
    # Execute mcp-remote with token
    cmd = [
        "npx", "mcp-remote",
        mcp_url,
        "--header",
        f"Authorization: Bearer {token}"
    ]
    
    # Pass through any additional arguments
    if len(sys.argv) > 1:
        cmd.extend(sys.argv[1:])
    
    # Execute and replace this process
    # This connects to Port MCP Server with the authenticated token
    os.execvp("npx", cmd)

if __name__ == "__main__":
    main()