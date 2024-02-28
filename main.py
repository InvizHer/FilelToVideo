# main.py

from pyrogram import Client, filters
import math, time, os, asyncio, logging
from typing import Tuple
import shlex

logger = logging.getLogger(__name__)

api_id = 10098309
api_hash = "aaacac243dddc9f0433c89cab8efe323"
bot_token = "5181191526:AAHhsUwMaopLJj0xYSsYVXThPRowuX02gv8"
app = Client("video_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Define status variable
status = False

# Helper functions

async def execute(cmnd: str) -> Tuple[str, str, int, int]:
    cmnds = shlex.split(cmnd)
    process = await asyncio.create_subprocess_exec(
        *cmnds,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (stdout.decode('utf-8', 'replace').strip(),
            stderr.decode('utf-8', 'replace').strip(),
            process.returncode,
            process.pid)

async def clean_up(input1, input2=None):
    try:
        os.remove(input1)
        logger.info(f"Deleted: {input1}")
    except:
        logger.info(f"Delete Failed: {input1}")
        pass
    try:
        if input2:
            os.remove(input2)
            logger.info(f"Deleted: {input2}")
    except:
        if input2:
            logger.info(f"Delete Failed: {input2}")
        pass

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \n".format(
            ''.join(["●" for i in range(math.floor(percentage / 5))]),
            ''.join(["○" for i in range(20 - math.floor(percentage / 5))])
        )

        tmp = progress + Config2.PROGRESS.format(
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text="**{}**\n\n {}".format(
                    ud_type,
                    tmp
                ),
                parse_mode='markdown'
            )
        except:
            pass

def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
          ((str(hours) + "h, ") if hours else "") + \
          ((str(minutes) + "m, ") if minutes else "") + \
          ((str(seconds) + "s, ") if seconds else "") + \
          ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

# Main bot logic

@app.on_message(filters.document | filters.video)
async def convert_to_video(bot, message):
    global status
    
    if status:
        await message.reply_text(text="Please wait until the last process finishes, then try again.")
        return
    
    if not message.document and not message.video:
        await message.reply_text(text="Please reply with a document or video file.")
        return
    
    status = True
    
    try:
        # Download the file
        msg = await message.reply_text(text="⬇️ Downloading the file...")
        # Add your logic to download the file using download_from_url.py or any other method
        
        # Generate thumbnail
        await msg.edit(text="🌄 Generating thumbnail...")
        # Add your logic to generate thumbnail using thumbnail_video.py or any other method
        
        # Send the video
        await msg.edit(text="⬆️ Uploading as video...")
        # Add your logic to upload the video using Pyrogram
        
        await msg.delete()
        # Clean up temporary files
        # Add your logic to clean up using tools.py or any other method
        
        status = False
    except Exception as e:
        status = False
        await msg.edit(text=f"❌ Failed to convert the file to video.\nError: {str(e)}")

app.run()
