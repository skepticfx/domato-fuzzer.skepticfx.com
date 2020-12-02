import http.server
import socketserver
import io
import os
import sys

from grammar import Grammar
from generator import generate_new_sample

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        result = generate_new_sample(template, htmlgrammar, cssgrammar, jsgrammar)
        # print(result)
        # Construct a server response.
        self.send_response(200)
        self.send_header('Content-type',
                         'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(str.encode(result))
        return



# open all fds
grammar_dir = os.path.dirname(__file__)

f = open(os.path.join(grammar_dir, 'template.html'))
template = f.read()
f.close()

htmlgrammar = Grammar()
err = htmlgrammar.parse_from_file(os.path.join(grammar_dir, 'html.txt'))
# CheckGrammar(htmlgrammar)
if err > 0:
    print('There were errors parsing grammar')
    sys.exit()

cssgrammar = Grammar()
err = cssgrammar.parse_from_file(os.path.join(grammar_dir, 'css.txt'))
# CheckGrammar(cssgrammar)
if err > 0:
    print('There were errors parsing grammar')
    sys.exit()

jsgrammar = Grammar()
err = jsgrammar.parse_from_file(os.path.join(grammar_dir, 'js.txt'))
# CheckGrammar(jsgrammar)
if err > 0:
    print('There were errors parsing grammar')
    sys.exit()

# JS and HTML grammar need access to CSS grammar.
# Add it as import
htmlgrammar.add_import('cssgrammar', cssgrammar)
jsgrammar.add_import('cssgrammar', cssgrammar)



port = int(os.environ.get("PORT", 5000))

print('Server listening on port ' + str(port) + '...')
httpd = socketserver.TCPServer(('', port), Handler)
httpd.serve_forever()