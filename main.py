# main.py

from pyrogram import Client, filters
import asyncio
import os
import shlex
import logging

logger = logging.getLogger(__name__)

api_id = 10098309
api_hash = "aaacac243dddc9f0433c89cab8efe323"
bot_token = "5181191526:AAHhsUwMaopLJj0xYSsYVXThPRowuX02gv8"
app = Client("video_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Define status variable
status = False

# Helper functions

async def execute(cmnd: str) -> tuple:
    cmnds = shlex.split(cmnd)
    process = await asyncio.create_subprocess_exec(
        *cmnds,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode('utf-8', 'replace').strip(),
        stderr.decode('utf-8', 'replace').strip(),
        process.returncode,
        process.pid
    )

async def clean_up(input1, input2=None):
    try:
        os.remove(input1)
        logger.info(f"Deleted: {input1}")
    except Exception as e:
        logger.info(f"Delete Failed: {input1} - {e}")

    if input2:
        try:
            os.remove(input2)
            logger.info(f"Deleted: {input2}")
        except Exception as e:
            logger.info(f"Delete Failed: {input2} - {e}")

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
        file_path = await bot.download_media(message)
        await msg.edit_text(text="✅ File downloaded")
        
        # Generate thumbnail
        await msg.edit_text(text="🌄 Generating thumbnail...")
        thumbnail_path = f"{file_path}.jpg"
        cmd = f"ffmpeg -i {file_path} -vframes 1 -an -s 640x360 -ss 5 {thumbnail_path}"
        await execute(cmd)
        await msg.edit_text(text="✅ Thumbnail generated")
        
        # Convert file to video
        await msg.edit_text(text="🔄 Converting file to video...")
        output_path = f"{file_path}.mp4"
        cmd = f"ffmpeg -i {file_path} -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 192k -ac 2 {output_path}"
        await execute(cmd)
        await msg.edit_text(text="✅ File converted to video")
        
        # Send the video
        await msg.edit_text(text="⬆️ Uploading as video...")
        await message.reply_video(video=output_path, thumb=thumbnail_path)
        await msg.delete()
        
        # Clean up temporary files
        await clean_up(file_path)
        await clean_up(thumbnail_path)
        
        status = False
    except Exception as e:
        status = False
        await msg.edit_text(text=f"❌ Failed to convert the file to video.\nError: {str(e)}")

app.run()
