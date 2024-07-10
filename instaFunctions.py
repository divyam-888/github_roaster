from instagrapi import Client

cl = Client()
ACCOUNT_USERNAME = 'shakti_power9547'
ACCOUNT_PASSWORD = '@shakti_power7459'
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

user_id = cl.user_id_from_username(ACCOUNT_USERNAME)
medias = cl.user_medias(user_id, 20)

print(medias)
print("user_id: ", user_id)