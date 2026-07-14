from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)

@app.route('/api/transcript')
def get_transcript():
    url = request.args.get('url')
    if not url:
        return jsonify({"code": 400, "error": "请提供网址"})

    # 提取视频 ID
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    if not match:
        return jsonify({"code": 400, "error": "网址格式不对"})

    video_id = match.group(1)

    try:
        # 优先抓取中文，如果没有则抓取英文
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['zh-Hans', 'zh-Hant', 'en'])
        text = " ".join([t['text'] for t in transcript])
        return jsonify({"code": 200, "text": text})
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)})
