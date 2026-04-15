import discord
import aiohttp
import asyncio
import json
from utils.logger import Logger
from utils.config import Config

# =========================================================
# محرك الأمان (Exponential Backoff Engine) - V3.0
# =========================================================
async def safe_execute(func, *args, _name="", _action="", _delay=0.5, **kwargs):
    retries = 0
    base_wait = Config.BASE_DELAY
    while retries < Config.MAX_RETRIES:
        try:
            res = await func(*args, **kwargs)
            if "Deleted" in _action:
                Logger.delete(f"{_action}: {_name}")
            else:
                Logger.add(f"{_action}: {_name}")
            
            await asyncio.sleep(_delay) # وقت راحة يسحب من الإعدادات
            return res
            
        except discord.HTTPException as e:
            if e.status == 429: # Rate Limit
                wait_time = base_wait * (2 ** retries) 
                try:
                    if hasattr(e, 'text') and e.text:
                        data = json.loads(e.text)
                        api_wait = float(data.get('retry_after', 0))
                        if api_wait > wait_time:
                            wait_time = api_wait + 1.0
                except: pass
                
                Logger.warning(f"Rate Limit [429]! Auto-Paused for {wait_time:.1f}s before retrying '{_name}'... (Attempt {retries+1}/{Config.MAX_RETRIES})")
                await asyncio.sleep(wait_time)
                retries += 1
            else:
                Logger.error(f"Failed {_action}: {_name} | API Error: {e.status}")
                break
        except discord.Forbidden:
            Logger.error(f"Missing Permissions to {_action}: {_name}")
            break
        except Exception as e:
            err_msg = str(e).lower()
            if '429' in err_msg or 'too many requests' in err_msg:
                wait_time = base_wait * (2 ** retries)
                Logger.warning(f"Rate Limit Hit! Auto-Paused for {wait_time:.1f}s before retrying '{_name}'... (Attempt {retries+1}/{Config.MAX_RETRIES})")
                await asyncio.sleep(wait_time)
                retries += 1
            else:
                Logger.error(f"Unexpected Error on '{_name}': {e}")
                break
    
    if retries >= Config.MAX_RETRIES:
        Logger.error(f"Skipped '{_name}' after {Config.MAX_RETRIES} failed rate-limit retries.")
    return None

class CloneEngine:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
        for role in guild_to.roles:
            if role.name != "@everyone":
                await safe_execute(role.delete, _name=role.name, _action="Deleted Role", _delay=Config.DELAY_DELETE)

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = [r for r in guild_from.roles if r.name != "@everyone"][::-1]
        for role in roles:
            await safe_execute(
                guild_to.create_role,
                name=role.name, permissions=role.permissions,
                colour=role.colour, hoist=role.hoist, mentionable=role.mentionable,
                _name=role.name, _action="Created Role", _delay=Config.DELAY_ROLE
            )

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            await safe_execute(channel.delete, _name=channel.name, _action="Deleted Channel/Category", _delay=Config.DELAY_DELETE)

    @staticmethod
    async def categories_delete_only(guild_to: discord.Guild):
        for category in guild_to.categories:
            await safe_execute(category.delete, _name=category.name, _action="Deleted Category", _delay=Config.DELAY_DELETE)

    @staticmethod
    async def channels_delete_only(guild_to: discord.Guild):
        for channel in guild_to.channels:
            if not isinstance(channel, discord.CategoryChannel):
                await safe_execute(channel.delete, _name=channel.name, _action="Deleted Channel", _delay=Config.DELAY_DELETE)

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for channel in guild_from.categories:
            overwrites_to = {}
            for key, value in channel.overwrites.items():
                if isinstance(key, discord.Role):
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    if role: overwrites_to[role] = value
            
            async def create_cat():
                try:
                    return await guild_to.create_category(name=channel.name, overwrites=overwrites_to)
                except AttributeError:
                    return await guild_to.create_category(name=channel.name)

            await safe_execute(create_cat, _name=channel.name, _action="Created Category", _delay=Config.DELAY_CATEGORY)

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for channel_text in guild_from.text_channels:
            category = discord.utils.get(guild_to.categories, name=channel_text.category.name) if channel_text.category else None
            overwrites_to = {}
            for key, value in channel_text.overwrites.items():
                if isinstance(key, discord.Role):
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    if role: overwrites_to[role] = value
                    
            async def create_txt():
                try:
                    return await guild_to.create_text_channel(
                        name=channel_text.name, overwrites=overwrites_to,
                        position=channel_text.position, topic=channel_text.topic,
                        slowmode_delay=channel_text.slowmode_delay, nsfw=channel_text.nsfw, category=category
                    )
                except AttributeError:
                    return await guild_to.create_text_channel(name=channel_text.name, category=category)

            await safe_execute(create_txt, _name=channel_text.name, _action="Created Text Channel", _delay=Config.DELAY_CHANNEL)

        for channel_voice in guild_from.voice_channels:
            category = discord.utils.get(guild_to.categories, name=channel_voice.category.name) if channel_voice.category else None
            overwrites_to = {}
            for key, value in channel_voice.overwrites.items():
                if isinstance(key, discord.Role):
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    if role: overwrites_to[role] = value
                    
            async def create_vc():
                try:
                    return await guild_to.create_voice_channel(
                        name=channel_voice.name, overwrites=overwrites_to,
                        position=channel_voice.position, bitrate=channel_voice.bitrate,
                        user_limit=channel_voice.user_limit, category=category
                    )
                except AttributeError:
                    return await guild_to.create_voice_channel(name=channel_voice.name, category=category)

            await safe_execute(create_vc, _name=channel_voice.name, _action="Created Voice Channel", _delay=Config.DELAY_CHANNEL)

    @staticmethod
    async def emojis_delete(guild_to: discord.Guild):
        for emoji in guild_to.emojis:
            await safe_execute(emoji.delete, _name=emoji.name, _action="Deleted Emoji", _delay=Config.DELAY_DELETE)

    @staticmethod
    async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
        limit = guild_to.emoji_limit
        created_count = len(guild_to.emojis)
        
        for emoji in guild_from.emojis:
            if created_count >= limit:
                Logger.warning(f"Server Emoji limit ({limit}) reached. Skipping remaining emojis...")
                return
            try:
                emoji_image = await emoji.url.read()
                res = await safe_execute(
                    guild_to.create_custom_emoji,
                    name=emoji.name, image=emoji_image,
                    _name=emoji.name, _action="Created Emoji", _delay=Config.DELAY_EMOJI
                )
                if res: created_count += 1
            except Exception as e:
                Logger.error(f"Failed to fetch image for Emoji '{emoji.name}': {e}")

    # =========================================================
    # استخدام aiohttp لاستنساخ الاستيكرات (Asynchronous HTTP)
    # =========================================================
    @staticmethod
    async def stickers_delete(guild_to: discord.Guild, token: str):
        headers = {"Authorization": str(token)}
        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                async with session.get(f"https://discord.com/api/v9/guilds/{guild_to.id}/stickers") as res:
                    if res.status == 200:
                        stickers = await res.json()
                        for st in stickers:
                            retries = 0
                            base_wait = Config.BASE_DELAY
                            while retries < Config.MAX_RETRIES:
                                async with session.delete(f"https://discord.com/api/v9/guilds/{guild_to.id}/stickers/{st['id']}") as del_res:
                                    if del_res.status == 429:
                                        del_data = await del_res.json()
                                        wait_time = base_wait * (2 ** retries)
                                        try: wait_time = max(wait_time, float(del_data.get('retry_after', 0)) + 1)
                                        except: pass
                                        Logger.warning(f"Rate Limit [429]! Auto-Paused for {wait_time:.1f}s before deleting sticker... (Attempt {retries+1}/{Config.MAX_RETRIES})")
                                        await asyncio.sleep(wait_time)
                                        retries += 1
                                    else:
                                        Logger.delete(f"Deleted Sticker: {st['name']}")
                                        await asyncio.sleep(Config.DELAY_DELETE)
                                        break
            except Exception as e:
                Logger.error(f"Error fetching stickers for deletion: {e}")

    @staticmethod
    async def stickers_create(guild_to: discord.Guild, guild_from: discord.Guild, token: str):
        boosts = getattr(guild_to, 'premium_subscription_count', 0)
        limit = 60 if boosts >= 14 else 30 if boosts >= 7 else 15 if boosts >= 2 else 5
        headers = {"Authorization": str(token)}
        
        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                async with session.get(f"https://discord.com/api/v9/guilds/{guild_from.id}/stickers") as res_from:
                    if res_from.status != 200: return
                    source_stickers = await res_from.json()
            except: return

            try:
                async with session.get(f"https://discord.com/api/v9/guilds/{guild_to.id}/stickers") as res_to:
                    created_count = len(await res_to.json()) if res_to.status == 200 else 0
            except: created_count = 0

            for st in source_stickers:
                if created_count >= limit:
                    Logger.warning(f"Server Sticker limit reached. Skipping remaining stickers...")
                    return
                if st.get('format_type') == 3: continue # Lottie (Animation) غير مدعوم برمجياً غالباً
                    
                retries = 0
                base_wait = Config.BASE_DELAY
                while retries < Config.MAX_RETRIES:
                    try:
                        ext = "gif" if st.get('format_type') == 4 else "png"
                        st_url = f"https://cdn.discordapp.com/stickers/{st['id']}.{ext}"
                        
                        # تحميل الصورة باستخدام aiohttp
                        async with session.get(st_url) as img_res:
                            if img_res.status != 200: break
                            img_data = await img_res.read()
                            
                        # تجهيز البيانات كـ FormData
                        form = aiohttp.FormData()
                        form.add_field('name', st['name'])
                        form.add_field('tags', st['tags'])
                        form.add_field('description', st.get("description", "cloned by nomix"))
                        form.add_field('file', img_data, filename=f"sticker.{ext}", content_type=f"image/{ext}")
                        
                        # رفع الاستيكر باستخدام aiohttp
                        async with session.post(f"https://discord.com/api/v9/guilds/{guild_to.id}/stickers", data=form) as post_res:
                            if post_res.status in [200, 201]:
                                Logger.add(f"Created Sticker: {st['name']}")
                                created_count += 1
                                await asyncio.sleep(Config.DELAY_STICKER) 
                                break
                            elif post_res.status == 429:
                                post_data = await post_res.json()
                                wait_time = base_wait * (2 ** retries)
                                try: wait_time = max(wait_time, float(post_data.get('retry_after', 0)) + 1)
                                except: pass
                                Logger.warning(f"Rate Limit [429]! Auto-Paused for {wait_time:.1f}s before creating sticker... (Attempt {retries+1}/{Config.MAX_RETRIES})")
                                await asyncio.sleep(wait_time)
                                retries += 1
                            else:
                                break
                    except Exception as e:
                        Logger.error(f"Error raising sticker {st['name']}: {e}")
                        break

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            icon_image = await guild_from.icon_url.read() if guild_from.icon_url else None
            await safe_execute(guild_to.edit, name=f'{guild_from.name}', _name="Server Name", _action="Updated", _delay=1)
            if icon_image:
                await safe_execute(guild_to.edit, icon=icon_image, _name="Server Icon", _action="Updated", _delay=1)
        except: pass