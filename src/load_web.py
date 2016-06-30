import cookielib
import mechanize
import urllib

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.open('https://www.bbdc.sg/bbweb/default.aspx')
for form in br.forms():
    print "Form name:", form.name
    print form
br.select_form(nr=0)
#br.form['mail'] = 'xxxx@xxx.com'
#br.form['password'] = 'xxxxxxx'
#br.submit()
