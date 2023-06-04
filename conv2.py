import json
from datetime import datetime
import dateutil
from dateutil import parser



def generate_html(post):
    html = f'''
    <div class="post">
        <div class="post-header">
            <div class="author">{post['id']}</div>
            <div class="time">{format_time(post['creation_time'])}</div>
        </div>
        <div class="blockpost">
        <div class="title">
        <h2>{post['title']}</h2>
        </div>
        </div>
        <div class="contentbox">
        <div class="content">{post['content']}</div>
        </div>
        <div class="attachment">{process_attachment(post['attachment'])}</div>
        <div class="likes">{process_likes(post['likes'])}</div>
        <div class="comments">{process_comments(post['comments'])}</div>
    </div>
    </br>
    </br>
    </br>
    '''
    return html

def format_time(timestamp):
    datetime_obj = timestamp
    return dateutil.parser.parse(datetime_obj)




def process_attachment(attachment):
    if 'reshared_post' in attachment:
        return f'<div class="reshared-post">{attachment["reshared_post"]}</div>'
    elif 'media_attachment' in attachment:
        media = ''.join([f'<img src="{path}" alt="Image">' for path in attachment['media_attachment']['media']])
        return f'<div class="media-attachment">{media}</div>'
    elif 'link' in attachment:
        link = attachment['link']
        return f'<div class="link"><a href="{link["url"]}"><img src="{link["image_url"]}" alt="Link Image">{link["title"]}</a></div>'
    elif 'poll' in attachment:
        poll = attachment['poll']
        choices = ''.join([f'<li>{choice["description"]}</li>' for choice in poll['choices']])
        return f'''
        <div class="poll">
            <ul>{choices}</ul>
            <p>Total Votes: {poll["total_votes"]}</p>
            <p>User Choice: {poll["user_choice"]}</p>
        </div>
        '''
    elif 'community' in attachment:
        return f'<div class="community">{attachment["community"]}</div>'
    else:
        return ''

def process_likes(likes):
    return f'<div class="likes-count"><i class="fa fa-thumbs-o-up" aria-hidden="true"></i> {len(likes)} </div>'

def process_comments(comments):
    comments_html = ''
    for comment in comments:
        comments_html += f'''
        <div class="comment">
            <div class="author">{comment['author']}</div>
            <div class="content">{comment['content']}</div>
            <div class="attachment">{process_attachment(comment.get('attachment', {}))}</div>
            <div class="likes">{process_likes(comment.get('likes', []))}</div>
        </div>
        '''
    return comments_html

def convert_jsonl_to_html(input_file, output_file):
    with open(input_file, 'r') as file:
        posts = [json.loads(line) for line in file]

    html = '''
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="styles.css">
        <script src="https://kit.fontawesome.com/55e37cba71.js" crossorigin="anonymous"></script>
        <script src="script.js"></script>
    </head>
    <body>
    '''

    for post in posts:
        html += generate_html(post)

    html += '''
    </body>
    </html>
    '''

    with open(output_file, 'w') as file:
        file.write(html)

# Usage example
convert_jsonl_to_html('export.jsonl', 'output.html')