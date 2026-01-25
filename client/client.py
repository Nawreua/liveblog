import cmd
import re
import logging
from argparse import ArgumentParser

import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)

class LiveblogClient(cmd.Cmd):
    intro = 'Welcome to the liveblog client. Type help or ? to list commands.\n'
    prompt = '(client) '
    base_url = ''
    user = 'user'
    keypass = ''

    _url_pattern = None

    def __init__(self, completekey = "tab", stdin = None, stdout = None, base_url='', keypass='', user=''):
        super().__init__(completekey, stdin, stdout)
        if base_url != '':
            self.do_setup_url(base_url)
        self.keypass = keypass
        self.user = user

    def do_setup_url(self, url):
        'Configure the URL used by the client: setup_url http://127.0.0.1:5000/'

        if self._url_pattern is None:
            # Using [Liberal Regex Pattern for Web URLs by @gruber](https://gist.github.com/gruber/8891611)
            # License: https://opensource.org/license/bsd-3-clause
            self._url_pattern = re.compile("""(?i)\\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\\s()<>{}\\[\\]]+|\\([^\\s()]*?\\([^\\s()]+\\)[^\\s()]*?\\)|\\([^\\s]+?\\))+(?:\\([^\\s()]*?\\([^\\s()]+\\)[^\\s()]*?\\)|\\([^\\s]+?\\)|[^\\s`!()\\[\\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\\b/?(?!@)))""")
        if self._url_pattern.fullmatch(url) is None:
            print(f'Erroneous base URL configured: {url}')
        else:
            self.base_url = url if url.endswith('/') else url + '/'
            logger.info(f'New URL is {self.base_url}')

    def do_setup_user(self, user):
        'Configure the user used by the client: setup_user Test'
        self.user = user

    def do_setup_keypass(self, keypass):
        'Configure the keypass used by the client: setup_keypass test_keypass'
        self.keypass = keypass
    
    def do_view_post(self, arg):
        'Request and output a blog post: view_post 1'
        try:
            id = parse(arg.split(), [int])
        except ValueError:
            return False
        
        if (response := self.request_get('view/' + str(id))) is not None:
            post = response.json()
            logger.info(post)
            pretty_print_post(post)

    def do_fetch_posts(self, arg):
        'Request and output multiple blog posts: fetch_posts 1 25'
        try:
            offset, limit = parse(arg.split(), [int, int])
        except ValueError:
            return False
        
        if (response := self.request_get('view/', payload={'offset': offset, 'limit': limit})) is not None:
            posts = response.json()
            logger.info(posts)
            for post in posts:
                pretty_print_post(post)

    def do_send_post(self, _):
        'Input the new post and send it to the server: send_post'
        try:
            logger.info('Asking for title')
            title = input('Title: ')
            if title == '':
                print('Title cannot be empty')
                return False
            logger.info('Asking for content')
            content = input('Content: ')
            while (line := input()) != '':
                content += '\n' + line
        except EOFError:
            print('Cancelling new post...')
            return False

        post_data = {
            'author': self.user,
            'title': title,
            'content': content
        }
        logger.info(post_data)

        if (response := self.request_post('save/', json=post_data)) is not None:
            new_post = response.json()
            logger.info(new_post)
            pretty_print_post(new_post)

    def do_exit(self, _):
        'Cleanup and exit the client: exit'
        return True
    
    def check_request(self, url):
        if self.base_url == '':
            print('No URL setup for the client, check setup_url')
            return False
        if self._url_pattern.fullmatch(url) is None:
            print(f'Erroneous URL requested: {url}')
            return False
        return True

    def check_response(self, response: requests.Response):
        if not response.ok:
            print(f'Response error with code: {response.status_code}')
            return False
        return True
    
    def request_post(self, url, payload={}, json=None):
        complete_url = self.base_url + url
        if not self.check_request(complete_url):
            return None
        logger.info(f'Requesting {complete_url} with POST')
        response = requests.post(complete_url, auth=HTTPBasicAuth(self.user, self.keypass), params=payload, json=json)
        if self.check_response(response):
            return response
        return None
    
    def request_get(self, url, payload={}):
        complete_url = self.base_url + url
        if not self.check_request(complete_url):
            return None
        logger.info(f'Requesting {complete_url} with GET')
        response = requests.get(complete_url, auth=HTTPBasicAuth(self.user, self.keypass), params=payload)
        if self.check_response(response):
            return response
        return None

def pretty_print_post(post):
    print(post['title'])
    print(f'By {post['author']}')
    print(f'\x1B[3m{post['date']}\x1B[0m')
    print('-' * len(post['title']))
    if post['content'] is not None:
        print(post['content'])
    print()

def parse(args, converter):
    converted = []
    if len(args) != len(converter):
        print(f'Excepted {len(converter)} arguments, received only {len(args)}')
        raise ValueError
    for x, convert in zip(args, converter):
        try:
            converted += [convert(x)]
        except ValueError:
            print(f'Excepted value type {convert}, incompatible with {x}')
            raise ValueError
    if len(converted) == 1:
        return converted[0]
    return tuple(converted)

if __name__ == "__main__":
    parser = ArgumentParser(prog='liveblog client',
                            description='A simple REPL client for liveblog usage')
    parser.add_argument('--url', help='Setup the base URL used by the client', default='')
    parser.add_argument('--user', help='Setup the user name', default='user')
    parser.add_argument('--keypass', help='Setup the keypass used by the client', default='')
    parser.add_argument('-l', '--log', help='Enable info log', action='store_true')
    args = parser.parse_args()

    if args.log:
        logger.setLevel(logging.INFO)

    LiveblogClient(base_url=args.url, keypass=args.keypass, user=args.user).cmdloop()
