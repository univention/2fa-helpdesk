
# Nubus deployment with the 2FA Helpdesk extension

To configure this extension in your new or existing Nubus deployment, add the following values to your
stackData `templateContext` of your Nubus deployment.

This will configure the extension, that creates the tiles for the 2FA Helpdesk.

If you already have a Nubus deployment, you can just simply add the values to the `values.yaml` and rerun your helm
upgrade with the new values.

```
nubusStackDataUms:
  templateContext:
    portalTwoFaLinkBase: 'https://{{ .Values.global.subDomains.twofaHelpdesk }}.{{ .Values.global.domain }}'
    twofaSelfserviceTileCategory: "domain-service"
    twofaAdminTileCategory: "domain-admin"
    portalTwoFaAllowedGroups:
      - "Domain Admins"
    twofaActivated: true

```
