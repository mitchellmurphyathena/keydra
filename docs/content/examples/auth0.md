---
title: "Auth0 Client Secret Rotation"
date: 2024-01-15T10:00:00+11:00
draft: false
---

Example to rotate Auth0 client secrets daily, distributing the new credentials to Secrets Manager.

```yaml
auth0_client:
  key: auth0-dev
  description: Auth0 client secret for web application
  custodians: auth_team
  provider: auth0
  rotate: nightly
  distribute:
    - key: auth0/auth0/auth0-management-api-creds
      provider: secretsmanager
      source: secret
      envs:
        - dev
```

The Auth0 Management API credentials stored in `auth0/auth0/auth0-management-api-creds` should contain:

```json
{
  "clientId": "your-management-api-client-id",
  "clientSecret": "your-management-api-client-secret",
  "domain": "your-tenant.auth0.com",
  "audience": "https://your-tenant.auth0.com/api/v2/"
}
```
