---
title: "Auth0 Email Provider Configuration"
date: 2024-01-15T10:00:00+11:00
draft: false
---

Example to rotate an AWS IAM user's credentials and distribute them to Auth0's email provider configuration.
`source` is used to map IAM user's credentials into the Auth0 email provider fields.

```yaml
auth0_email:
  key: keydra_auth0_email
  description: Auth0 email provider credentials
  custodians: auth_team
  provider: iam
  rotate: nightly
  config:
    groups:
      - Auth0EmailSenderGroup
  distribute:
    - key: auth0-email-config
      provider: auth0_email_provider
      provider_secret_key: auth0-management-api-creds
      source:
        accessKeyId: key
        secretAccessKey: secret
      envs:
        - dev
```

The Auth0 Management API credentials stored in `keydra/auth0/auth0-management-api-creds` should contain:

```json
{
  "clientId": "your-management-api-client-id",
  "clientSecret": "your-management-api-client-secret",
  "domain": "your-tenant.auth0.com",
  "audience": "https://your-tenant.auth0.com/api/v2/"
}
```

The Management API application must have the `update:email_provider` permissions.

The rotated IAM credentials will be distributed as the SMTP or email service configuration that Auth0 requires for sending emails.
