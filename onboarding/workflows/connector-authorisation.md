# Connector authorisation workflow

## Goal

Connect only the services required for the selected first automation, using customer-controlled authorisation and minimum viable access.

## Flow

1. The default profile explains the business purpose in plain language.
2. The product strategist identifies the minimum data and action requirements.
3. The architect proposes the minimum required connector scopes and records exclusions.
4. The customer or authorised operator completes the provider’s approved OAuth or secret-store connection flow.
5. Store the connection metadata in the Integration Register; store credentials only in the approved secret store or provider connection manager.
6. The builder performs a safe read-only or draft-mode verification.
7. The quality guardian checks scope against the Customer Blueprint and Integration Register.

## Hard stops

Stop and ask for customer input when:

- Requested scope includes unrelated data or broad administrative access.
- A provider requires a password, API key, cookie, or token to be sent in chat or committed to a file.
- A connector cannot distinguish read access from send/write/delete access.
- The customer has not named an owner for the integration.

## Output

The Integration Register is updated with authorised services, scopes, owner, exclusions, and revocation procedure. It must contain no secret material.
