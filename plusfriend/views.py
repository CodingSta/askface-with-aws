from requests.exceptions import HTTPError
from .decorators import before


@before
def on_init(request):
    return {
        'type': 'buttons',
        'buttons': ['안녕하세요. :)'],
    }


@before
def on_message(request):
    message_type = request.JSON['type']        # text, photo, audio(m4a), video(mp4)
    content = request.JSON['content']  # photo 타입일 경우에는 이미지 URL

    speech = 'ECHO : {}'.format(content)

    return {
        'message': {
            'text': speech,
        }
    }


@before
def on_added(request):
    pass


@before
def on_block(request, user_key):
    pass


@before
def on_leave(request, user_key):
    pass

