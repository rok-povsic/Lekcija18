#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("chat.html")


class ProcesirajSporociloHandler(BaseHandler):
    def post(self):
        uporabnikovo_ime = self.request.get("ime")
        uporabnikovo_sporocilo = self.request.get("sporocilo")

        # izpis = "<b>" + uporabnikovo_ime + ":</b> " + uporabnikovo_sporocilo
        # self.write(izpis)

        view_vars = {
            'ime': uporabnikovo_ime,
            'sporocilo': uporabnikovo_sporocilo,
        }
        return self.render_template("prikazi.html", view_vars)


class ProcesirajSporociloHandler2(BaseHandler):
    sprocila = []

    def post(self):
        uporabnikovo_ime = self.request.get("ime")
        uporabnikovo_sporocilo = self.request.get("sporocilo")

        pair = (uporabnikovo_ime, uporabnikovo_sporocilo)
        self.sprocila.append(pair)

        view_vars = {
            'sporocila': self.sprocila
        }
        return self.render_template("prikazi2.html", view_vars)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    # webapp2.Route('/poslji-sporocilo', ProcesirajSporociloHandler),
    webapp2.Route('/poslji-sporocilo', ProcesirajSporociloHandler2),
], debug=True)
