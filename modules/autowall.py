from modules.func_module import group_id, vk_polzovat, random, time


def create_post():
    while True:
        # Отправка фото в ВК:
        att = vk_polzovat.photos.search(q='Anime', count='1', offset=random.randint(0, 100000))
        while len(att['items']) == 0:
            att = vk_polzovat.photos.search(q='Anime', count='1', offset=random.randint(0, 100000))
        photo = att['items'][0]
        owner_id = photo['owner_id']
        photo_id = photo['id']
        attachment = f'photo{owner_id}_{photo_id}'
        vk_polzovat.wall.post(owner_id='-' + group_id, from_group='1', attachments=attachment,
                              message='Это вам, мои сладенькие!',
                              publish_date=str(int(time.time()) + 86400))
        time.sleep(3600)
