from sys import argv, exit

from keycloak import KeycloakOpenID

from classes.Config import config

usage_msg = '''usage: user password'''

keycloakOpenId = KeycloakOpenID(f"{config.KEYCLOAK_ISSUER}/auth",
                                config.KEYCLOAK_REALM_NAME or "",
                                config.KEYCLOAK_CLIENT_ID,
                                config.KEYCLOAK_CLIENT_SECRET)

#Validate usage
if(len(argv) != 3):
    print("Incorrect usage")
    print(usage_msg)
    exit()

[ user, password ] = argv[1:]

token = keycloakOpenId.token(user, password)
print(token['access_token'])
