import cgi

form = b'''
<html>
    <head>
        <title>Hello User!</title>
    </head>
    <body>
        <form method="post">
            <label>First Name:</label>
            <input type="text" name="first_name">
            <br>
            <label>Last Name:</label>
            <input type="text" name="last_name">
            <br>
            <label>Gender</label>
            <input type="text" name="gender">
            <br>
            <label>Email:</label>
            <input type="text" name="email">
            <br>
            <input type="submit" value="Submit">
        </form>
    </body>
</html>
'''

def app(environ, start_response):
    html = form

    if environ['REQUEST_METHOD'] == 'POST':
        post_env = environ.copy()
        post_env['QUERY_STRING'] = ''
        post = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=post_env,
            keep_blank_values=True
        )
        html = b'Hello, ' + post['last_name'].value + ', ' + post['first_name'].value + '!'

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [html]

if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server
        httpd = make_server('', 8080, app)
        print('Serving on port 8080...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Goodbye.')
