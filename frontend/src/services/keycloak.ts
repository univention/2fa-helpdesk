import Keycloak from "keycloak-js";

const keycloakConfig = {
  url: "https://id.yschmidt-opendesk.univention.dev/",
  realm: "opendesk",
  clientId: "chrissytest",
};

const keycloak = new Keycloak(keycloakConfig);

export default keycloak;
