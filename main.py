from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

hash = "<insert_secret_here>"

def output(self, string):
    self.response.out.write(string)

def error(self):
    output(self, "error")

def deny(self):
    output(self, "denied")

class Message(db.Model):
    text = db.StringProperty()
    timestamp = db.DateTimeProperty(auto_now_add=True)

class DeleteMessage(webapp.RequestHandler):
    global hash

    def get(self):
        try:
            self.response.headers['Content-Type'] = 'text/plain'
            given_hash = self.request.get('h')

            if given_hash == hash:
                messages = Message.gql("ORDER BY timestamp DESC LIMIT 1")
                db.delete(messages)
            else:
                deny(self)

        except:
            error(self)

class NewMessage(webapp.RequestHandler):
    global hash

    def get(self):
        try:
            self.response.headers['Content-Type'] = 'text/plain'
            given_hash = self.request.get('h')

            if given_hash == hash:
                newmessage = self.request.get('m')

                if len(newmessage) > 0:
                    message = Message()
                    message.text = newmessage
                    message.put()
                else:
                    error(self)
            else:
                deny(self)

        except:
            error(self)

class GetMessage(webapp.RequestHandler):
    global hash

    def get(self):
        try:
            self.response.headers['Content-Type'] = 'text/plain'
            given_hash = self.request.get('h')

            if given_hash == hash:
                try:
                    messages = Message.gql("ORDER BY timestamp DESC LIMIT 1")
                    oldmessage = messages.get()

                    if oldmessage != None:
                        output(self, oldmessage.text)

                except:
                    error(self)
            else:
                deny(self)

        except:
            error(self)

app = webapp.WSGIApplication([('/', GetMessage), ('/n', NewMessage), ('/d', DeleteMessage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
