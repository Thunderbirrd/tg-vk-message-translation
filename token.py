import vk_api


def generate_token(login, password):
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth()
    return dict(vk_session.token).get('access_token')
