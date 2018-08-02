# import sys
# import os
# import shutil
# import tempfile
# import sqlite3
#
#
# TMPDIR = tempfile.mkdtemp()
# DATABASE = os.path.join(TMPDIR, "db.sqlite")
#
#
# class Connection(object):
#     """
#     context manager to establish database connection, providing access to
#     connection and cursor
#     """
#
#     def __init__(self, db_path=DATABASE, commit=False, **kwargs):
#         print "INIT", db_path, commit, kwargs
#         self.db = db_path
#         self.commit = commit
#
#     def __enter__(self, *args, **kwargs):
#         print "ENTER", args, kwargs
#         self.conn = sqlite3.connect(self.db)
#         return self.conn, self.conn.cursor()
#
#     def __exit__(self, *args, **kwargs):
#         print "EXIT", self.commit, args, kwargs
#         if self.commit:
#             self.conn.commit()
#         self.conn.close()
#
#
# def main(args):
#     from wsgiref.simple_server import make_server
#
#     initialize_db()
#
#     try:
#         srv = make_server("localhost", 8080, respond)
#         srv.serve_forever()
#     finally:
#         shutil.rmtree(TMPDIR)
#
#     return True
#
#
# def respond(environ, start_response):
#     start_response("200 OK", [("Content-Type", "text/html")])
#     with Connection() as (conn, cursor):
#         tags = cursor.execute("SELECT name FROM tags")
#         for row in tags:
#             print "yielding", row
#             yield row[0].encode("utf-8")
#
#
# def initialize_db():
#     with Connection(commit=True) as (conn, cursor):
#         cursor.execute("CREATE TABLE tags " +
#                 "(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
#         for tag in ["foo", "bar", "baz"]:
#             cursor.execute("INSERT INTO tags VALUES (?, ?)", (None, tag))
#
#
# if __name__ == "__main__":
#     status = not main(sys.argv)
#     sys.exit(status)


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