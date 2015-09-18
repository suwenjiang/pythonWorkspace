#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Droopy (http://stackp.online.fr/droopy)
# Copyright 2008-2013 (c) Pierre Duquesne <stackp@online.fr>
# Licensed under the New BSD License.

# Changelog
#   20131121 * Update HTML/CSS for mobile devices
#            * Add HTTPS support
#            * Add HTTP basic authentication
#            * Add option to change uploaded file permissions
#            * Add support for HTML5 multiple file upload
#   20120108 * Taiwanese translation by Li-cheng Hsu.
#   20110928 * Correctly save message with --save-config. Fix by Sven Radde.
#   20110708 * Polish translation by Jacek Politowski.
#   20110625 * Fix bug regarding filesystem name encoding.
#            * Save the --dl option when --save-config is passed.
#   20110501 * Add the --dl option to let clients download files.
#            * CSS speech bubble.
#   20101130 * CSS and HTML update. Switch to the new BSD License.
#   20100523 * Simplified Chinese translation by Ye Wei.
#   20100521 * Hungarian translation by Csaba SzigetvÃ¡ri.
#            * Russian translation by muromec.
#            * Use %APPDATA% Windows environment variable -- fix by Maik.
#   20091229 * Brazilian Portuguese translation by
#              Carlos Eduardo Moreira dos Santos and Toony Poony.
#            * IE layout fix by Carlos Eduardo Moreira dos Santos.
#            * Galician translation by Miguel Anxo Bouzada.
#   20090721 * Indonesian translation by Kemas.
#   20090205 * Japanese translation by Satoru Matsumoto.
#            * Slovak translation by CyberBoBaK.
#   20090203 * Norwegian translation by Preben Olav Pedersen.
#   20090202 * Korean translation by xissy.
#            * Fix for unicode filenames by xissy.
#            * Relies on 127.0.0.1 instead of "localhost" hostname.
#   20090129 * Serbian translation by kotnik.
#   20090125 * Danish translation by jan.
#   20081210 * Greek translation by n2j3.
#   20081128 * Slovene translation by david.
#            * Romanian translation by Licaon.
#   20081022 * Swedish translation by David Eurenius.
#   20081001 * Droopy gets pretty (css and html rework).
#            * Finnish translation by ipppe.
#   20080926 * Configuration saving and loading.
#   20080906 * Extract the file base name (some browsers send the full path).
#   20080905 * File is uploaded directly into the specified directory.
#   20080904 * Arabic translation by Djalel Chefrour.
#            * Italian translation by fabius and d1s4st3r.
#            * Dutch translation by Tonio Voerman.
#            * Portuguese translation by Pedro Palma.
#            * Turkish translation by Heartsmagic.
#   20080727 * Spanish translation by Federico Kereki.
#   20080624 * Option -d or --directory to specify the upload directory.
#   20080622 * File numbering to avoid overwriting.
#   20080620 * Czech translation by JiÅ™Ã­.
#            * German translation by Michael.
#   20080408 * First release.

import BaseHTTPServer
import SocketServer
import cgi
import os
import posixpath
import macpath
import ntpath
import sys
import getopt
import mimetypes
import copy
import shutil
import tempfile
import socket
import locale
import urllib
import base64

LOGO = '''\
 _____
|     \.----.-----.-----.-----.--.--.
|  --  |   _|  _  |  _  |  _  |  |  |
|_____/|__| |_____|_____|   __|___  |
                        |__|  |_____|
'''

USAGE='''\
Usage: droopy [options] [PORT]

Options:
  -h, --help                            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY   set the directory to upload files to
  -m MESSAGE, --message MESSAGE         set the message
  -p PICTURE, --picture PICTURE         set the picture
  --dl                                  provide download links
  -a USER:PASS, --auth USER:PASS        set the authentication credentials
  --ssl PEMFILE                         set up https using the certificate file
  --chmod MODE                          set the file permissions (octal value)
  --save-config                         save options in a configuration file
  --delete-config                       delete the configuration file and exit

Example:
   droopy -m "Hi, this is Bob. You can send me a file." -p avatar.png
'''

picture = None
message = ""
port = 8000
directory = os.curdir
must_save_options = False
publish_files = False
auth = None
certfile = None
file_mode = None

# -- HTML templates

style = '''
<meta name="viewport"
      content="width=device-width,initial-scale=1,maximum-scale=1" />
<style type="text/css">
<!--
* {margin: 0; padding: 0;}
body {text-align: center; background-color: #eee; font-family: sans-serif;
      color:#777;}
div {word-wrap: break-word;}
img {max-width: 100%%;}
a {color: #4499cc; text-decoration: none;}
.container {max-width: 700px; margin: auto; background-color: #fff;}
.box {padding-top: 20px; padding-bottom: 20px;}
#linkurl {background-color: #333;}
#linkurl a {color: #ddd; text-decoration: none;}
#linkurl a:hover {color: #fff;}
#message {padding: 5px 0; font-size: 2em; font-weight: lighter;
          letter-spacing: -2px; line-height: 50px; color: #aaa;}
#sending {display: none; font-style: italic;}
#sending .text {padding-top: 10px; color: #bbb; font-size: 0.8em;}
#wrapform {height: 90px; padding-top:40px;}
#progress {display: inline;  border-collapse: separate; empty-cells: show;
           border-spacing: 24px 0; padding: 0; vertical-align: bottom;}
#progress td {height: 17px; width: 17px; background-color: #eee;
              padding: 0px; border-radius: 90px; box-shadow: 0 0 3px #bbb;}
#userinfo {padding-bottom: 20px;}
#files {
  margin: auto;
  padding: 13px 0;
  text-align: left;
  overflow: auto;
  margin-bottom: 20px;
}
#files a {text-decoration: none; display: block; padding: 10px 20px;}
#files a:nth-child(2n+1) {background-color: #F7F7F7;}
#files a:link {color: #4499cc}
#files a:visited {color: #a0c0e0}
#files a:hover {background-color:#f0f0f0}
--></style>'''

userinfo = '''
<div id="userinfo">
  %(message)s
  %(divpicture)s
</div>
'''

maintmpl = '''
<!doctype html>
<html>
<head>
<title>%(maintitle)s</title>
''' + style + '''
<script language="JavaScript">
function swap() {
   document.getElementById("form").style.display = "none";
   document.getElementById("sending").style.display = "block";
   pulse(0);
}

function pulse(i) {
    var NUMCELL = 5;
    var cell = document.getElementById("cell-" + (i %% NUMCELL));
    var prev = document.getElementById("cell-"+((i - 1 + NUMCELL) %% NUMCELL));
    cell.style.backgroundColor = "#7ac";
    prev.style.backgroundColor = "#eee";
    setTimeout(function() {pulse(i+1);}, 300);
}

function onunload() {
   document.getElementById("form").style.display = "block";
   document.getElementById("sending").style.display = "none";
}
</script></head>
<body>
%(linkurl)s
<div class="container">
<div id="wrapform">
  <div id="form" class="box">
    <form method="post" enctype="multipart/form-data" action="">
      <input name="upfile" type="file" multiple="yes">
      <input value="%(submit)s" onclick="swap()" type="submit">
    </form>
  </div>
  <div id="sending" class="box">
    <table id="progress">
      <tr>
        <td id="cell-0"/><td id="cell-1"/><td id="cell-2"/>
        <td id="cell-3"/><td id="cell-4"/>
      </tr>
    </table>
    <div class="text">%(sending)s</div>
  </div>
</div>
''' + userinfo + '''
%(files)s
</div>
</body>
</html>
'''

successtmpl = '''
<!doctype html>
<html>
<head><title> %(successtitle)s </title>
''' + style + '''
</head>
<body>
<div class="container">
<div id="wrapform">
  <div class="box">
    %(received)s
    <a href="/"> %(another)s </a>
  </div>
</div>
''' + userinfo + '''
</div>
</body>
</html>
'''

errortmpl = '''
<!doctype html>
<html>
<head><title> %(errortitle)s </title>
''' + style + '''
</head>
<body>
<div class="container">
<div id="wrapform">
  <div class="box">
    %(problem)s
    <a href="/"> %(retry)s </a>
  </div>
</div>
''' + userinfo + '''
</div>
</body>
</html>
'''

linkurltmpl = '''<div id="linkurl" class="box">
<a href="http://stackp.online.fr/droopy-ip.php?port=%(port)d&ssl=%(ssl)d"> %(discover)s
</a></div>'''


templates = {"main": maintmpl, "success": successtmpl, "error": errortmpl}

# -- Translations

ar = {"maintitle":       u"Ø¥Ø±Ø³Ø§Ù„ Ù…Ù„Ù",
      "submit":          u"Ø¥Ø±Ø³Ø§Ù„",
      "sending":         u"Ø§Ù„Ù…Ù„Ù Ù‚ÙŠØ¯ Ø§Ù„Ø¥Ø±Ø³Ø§Ù„",
      "successtitle":    u"ØªÙ… Ø§Ø³ØªÙ‚Ø¨Ø§Ù„ Ø§Ù„Ù…Ù„Ù",
      "received":        u"ØªÙ… Ø§Ø³ØªÙ‚Ø¨Ø§Ù„ Ø§Ù„Ù…Ù„Ù !",
      "another":         u"Ø¥Ø±Ø³Ø§Ù„ Ù…Ù„Ù Ø¢Ø®Ø±",
      "errortitle":      u"Ù…Ø´ÙƒÙ„Ø©",
      "problem":         u"Ø­Ø¯Ø«Øª Ù…Ø´ÙƒÙ„Ø© !",
      "retry":           u"Ø¥Ø¹Ø§Ø¯Ø© Ø§Ù„Ù…Ø­Ø§ÙˆÙ„Ø©",
      "discover":        u"Ø§ÙƒØªØ´Ø§Ù Ø¹Ù†ÙˆØ§Ù† Ù‡Ø°Ù‡ Ø§Ù„ØµÙØ­Ø©"}

cs = {"maintitle":       u"Poslat soubor",
      "submit":          u"Poslat",
      "sending":         u"PosÃ­lÃ¡m",
      "successtitle":    u"Soubor doruÄen",
      "received":        u"Soubor doruÄen !",
      "another":         u"Poslat dalÅ¡Ã­ soubor",
      "errortitle":      u"Chyba",
      "problem":         u"Stala se chyba !",
      "retry":           u"Zkusit znova.",
      "discover":        u"Zjistit adresu strÃ¡nky"}

da = {"maintitle":       u"Send en fil",
      "submit":          u"Send",
      "sending":         u"Sender",
      "successtitle":    u"Fil modtaget",
      "received":        u"Fil modtaget!",
      "another":         u"Send en fil til.",
      "errortitle":      u"Problem",
      "problem":         u"Det er opstÃ¥et en fejl!",
      "retry":           u"ForsÃ¸g igen.",
      "discover":        u"Find adressen til denne side"}

de = {"maintitle":       "Datei senden",
      "submit":          "Senden",
      "sending":         "Sendet",
      "successtitle":    "Datei empfangen",
      "received":        "Datei empfangen!",
      "another":         "Weitere Datei senden",
      "errortitle":      "Fehler",
      "problem":         "Ein Fehler ist aufgetreten!",
      "retry":           "Wiederholen",
      "discover":        "Internet-Adresse dieser Seite feststellen"}

el = {"maintitle":       u"Î£Ï„ÎµÎ¯Î»Îµ Î­Î½Î± Î±ÏÏ‡ÎµÎ¯Î¿",
      "submit":          u"Î‘Ï€Î¿ÏƒÏ„Î¿Î»Î®",
      "sending":         u"Î‘Ï€Î¿ÏƒÏ„Î­Î»Î»ÎµÏ„Î±Î¹...",
      "successtitle":    u"Î•Ï€Î¹Ï„Ï…Ï‡Î®Ï‚ Î»Î®ÏˆÎ· Î±ÏÏ‡ÎµÎ¯Î¿Ï… ",
      "received":        u"Î›Î®ÏˆÎ· Î±ÏÏ‡ÎµÎ¯Î¿Ï… Î¿Î»Î¿ÎºÎ»Î·ÏÏŽÎ¸Î·ÎºÎµ",
      "another":         u"Î£Ï„ÎµÎ¯Î»Îµ Î¬Î»Î»Î¿ Î­Î½Î± Î±ÏÏ‡ÎµÎ¯Î¿",
      "errortitle":      u"Î£Ï†Î¬Î»Î¼Î±",
      "problem":         u"Î Î±ÏÎ¿Ï…ÏƒÎ¹Î¬ÏƒÏ„Î·ÎºÎµ ÏƒÏ†Î¬Î»Î¼Î±",
      "retry":           u"Î•Ï€Î±Î½Î¬Î»Î·ÏˆÎ·",
      "discover":        u"Î’ÏÎµÏ‚ Ï„Î·Î½ Î´Î¹ÎµÏÎ¸Ï…Î½ÏƒÎ· Ï„Î·Ï‚ ÏƒÎµÎ»Î¯Î´Î±Ï‚"}

en = {"maintitle":       "Send a file",
      "submit":          "Send",
      "sending":         "Sending",
      "successtitle":    "File received",
      "received":        "File received!",
      "another":         "Send another file.",
      "errortitle":      "Problem",
      "problem":         "There has been a problem!",
      "retry":           "Retry.",
      "discover":        "Discover the address of this page"}

es = {"maintitle":       u"Enviar un archivo",
      "submit":          u"Enviar",
      "sending":         u"Enviando",
      "successtitle":    u"Archivo recibido",
      "received":        u"Â¡Archivo recibido!",
      "another":         u"Enviar otro archivo.",
      "errortitle":      u"Error",
      "problem":         u"Â¡Hubo un problema!",
      "retry":           u"Reintentar",
      "discover":        u"Descubrir la direcciÃ³n de esta pÃ¡gina"}

fi = {"maintitle":       u"LÃ¤hetÃ¤ tiedosto",
      "submit":          u"LÃ¤hetÃ¤",
      "sending":         u"LÃ¤hettÃ¤Ã¤",
      "successtitle":    u"Tiedosto vastaanotettu",
      "received":        u"Tiedosto vastaanotettu!",
      "another":         u"LÃ¤hetÃ¤ toinen tiedosto.",
      "errortitle":      u"Virhe",
      "problem":         u"Virhe lahetettÃ¤essÃ¤ tiedostoa!",
      "retry":           u"Uudelleen.",
      "discover":        u"NÃ¤ytÃ¤ tÃ¤mÃ¤n sivun osoite"}

fr = {"maintitle":       u"Envoyer un fichier",
      "submit":          u"Envoyer",
      "sending":         u"Envoi en cours",
      "successtitle":    u"Fichier reÃ§u",
      "received":        u"Fichier reÃ§u !",
      "another":         u"Envoyer un autre fichier.",
      "errortitle":      u"ProblÃ¨me",
      "problem":         u"Il y a eu un problÃ¨me !",
      "retry":           u"RÃ©essayer.",
      "discover":        u"DÃ©couvrir l'adresse de cette page"}

gl = {"maintitle":       u"Enviar un ficheiro",
      "submit":          u"Enviar",
      "sending":         u"Enviando",
      "successtitle":    u"Ficheiro recibido",
      "received":        u"Ficheiro recibido!",
      "another":         u"Enviar outro ficheiro.",
      "errortitle":      u"Erro",
      "problem":         u"XurdÃ­u un problema!",
      "retry":           u"Reintentar",
      "discover":        u"Descubrir o enderezo desta pÃ¡xina"}

hu = {"maintitle":       u"ÃllomÃ¡ny kÃ¼ldÃ©se",
      "submit":          u"KÃ¼ldÃ©s",
      "sending":         u"KÃ¼ldÃ©s folyamatban",
      "successtitle":    u"Az Ã¡llomÃ¡ny beÃ©rkezett",
      "received":        u"Az Ã¡llomÃ¡ny beÃ©rkezett!",
      "another":         u"TovÃ¡bbi Ã¡llomÃ¡nyok kÃ¼ldÃ©se",
      "errortitle":      u"Hiba",
      "problem":         u"Egy hiba lÃ©pett fel!",
      "retry":           u"MegismÃ©telni",
      "discover":        u"Az oldal Internet-cÃ­mÃ©nek megÃ¡llapÃ­tÃ¡sa"}

id = {"maintitle":       "Kirim sebuah berkas",
      "submit":          "Kirim",
      "sending":         "Mengirim",
      "successtitle":    "Berkas diterima",
      "received":        "Berkas diterima!",
      "another":         "Kirim berkas yang lain.",
      "errortitle":      "Permasalahan",
      "problem":         "Telah ditemukan sebuah kesalahan!",
      "retry":           "Coba kembali.",
      "discover":        "Kenali alamat IP dari halaman ini"}

it = {"maintitle":       u"Invia un file",
      "submit":          u"Invia",
      "sending":         u"Invio in corso",
      "successtitle":    u"File ricevuto",
      "received":        u"File ricevuto!",
      "another":         u"Invia un altro file.",
      "errortitle":      u"Errore",
      "problem":         u"Si Ã¨ verificato un errore!",
      "retry":           u"Riprova.",
      "discover":        u"Scopri lâ€™indirizzo di questa pagina"}

ja = {"maintitle":       u"ãƒ•ã‚¡ã‚¤ãƒ«é€ä¿¡",
      "submit":          u"é€ä¿¡",
      "sending":         u"é€ä¿¡ä¸­",
      "successtitle":    u"å—ä¿¡å®Œäº†",
      "received":        u"ãƒ•ã‚¡ã‚¤ãƒ«ã‚’å—ä¿¡ã—ã¾ã—ãŸï¼",
      "another":         u"ä»–ã®ãƒ•ã‚¡ã‚¤ãƒ«ã‚’é€ä¿¡ã™ã‚‹",
      "errortitle":      u"å•é¡Œç™ºç”Ÿ",
      "problem":         u"å•é¡ŒãŒç™ºç”Ÿã—ã¾ã—ãŸï¼",
      "retry":           u"ãƒªãƒˆãƒ©ã‚¤",
      "discover":        u"ã“ã®ãƒšãƒ¼ã‚¸ã®ã‚¢ãƒ‰ãƒ¬ã‚¹ã‚’ç¢ºèªã™ã‚‹"}

ko = {"maintitle":       u"íŒŒì¼ ë³´ë‚´ê¸°",
      "submit":          u"ë³´ë‚´ê¸°",
      "sending":         u"ë³´ë‚´ëŠ” ì¤‘",
      "successtitle":    u"íŒŒì¼ì´ ë°›ì•„ì¡ŒìŠµë‹ˆë‹¤",
      "received":        u"íŒŒì¼ì´ ë°›ì•„ì¡ŒìŠµë‹ˆë‹¤!",
      "another":         u"ë‹¤ë¥¸ íŒŒì¼ ë³´ë‚´ê¸°",
      "errortitle":      u"ë¬¸ì œê°€ ë°œìƒí–ˆìŠµë‹ˆë‹¤",
      "problem":         u"ë¬¸ì œê°€ ë°œìƒí–ˆìŠµë‹ˆë‹¤!",
      "retry":           u"ë‹¤ì‹œ ì‹œë„",
      "discover":        u"ì´ íŽ˜ì´ì§€ ì£¼ì†Œ ì•Œì•„ë³´ê¸°"}

nl = {"maintitle":       "Verstuur een bestand",
      "submit":          "Verstuur",
      "sending":         "Bezig met versturen",
      "successtitle":    "Bestand ontvangen",
      "received":        "Bestand ontvangen!",
      "another":         "Verstuur nog een bestand.",
      "errortitle":      "Fout",
      "problem":         "Er is een fout opgetreden!",
      "retry":           "Nog eens.",
      "discover":        "Vind het adres van deze pagina"}

no = {"maintitle":       u"Send en fil",
      "submit":          u"Send",
      "sending":         u"Sender",
      "successtitle":    u"Fil mottatt",
      "received":        u"Fil mottatt !",
      "another":         u"Send en ny fil.",
      "errortitle":      u"Feil",
      "problem":         u"Det har skjedd en feil !",
      "retry":           u"Send pÃ¥ nytt.",
      "discover":        u"Finn addressen til denne siden"}

pl = {"maintitle":       u"WyÅ›lij plik",
      "submit":          u"WyÅ›lij",
      "sending":         u"WysyÅ‚anie",
      "successtitle":    u"Plik wysÅ‚any",
      "received":        u"Plik wysÅ‚any!",
      "another":         u"WyÅ›lij kolejny plik.",
      "errortitle":      u"Problem",
      "problem":         u"WystÄ…piÅ‚ bÅ‚Ä…d!",
      "retry":           u"SprÃ³buj ponownie.",
      "discover":        u"ZnajdÅº adres tej strony"}

pt = {"maintitle":       u"Enviar um ficheiro",
      "submit":          u"Enviar",
      "sending":         u"A enviar",
      "successtitle":    u"Ficheiro recebido",
      "received":        u"Ficheiro recebido !",
      "another":         u"Enviar outro ficheiro.",
      "errortitle":      u"Erro",
      "problem":         u"Ocorreu um erro !",
      "retry":           u"Tentar novamente.",
      "discover":        u"Descobrir o endereÃ§o desta pÃ¡gina"}

pt_br = {
      "maintitle":       u"Enviar um arquivo",
      "submit":          u"Enviar",
      "sending":         u"Enviando",
      "successtitle":    u"Arquivo recebido",
      "received":        u"Arquivo recebido!",
      "another":         u"Enviar outro arquivo.",
      "errortitle":      u"Erro",
      "problem":         u"Ocorreu um erro!",
      "retry":           u"Tentar novamente.",
      "discover":        u"Descobrir o endereÃ§o desta pÃ¡gina"}

ro = {"maintitle":       u"Trimite un fiÅŸier",
      "submit":          u"Trimite",
      "sending":         u"Se trimite",
      "successtitle":    u"FiÅŸier recepÅ£ionat",
      "received":        u"FiÅŸier recepÅ£ionat !",
      "another":         u"Trimite un alt fiÅŸier.",
      "errortitle":      u"ProblemÄƒ",
      "problem":         u"A intervenit o problemÄƒ !",
      "retry":           u"ReÃ®ncearcÄƒ.",
      "discover":        u"DescoperÄƒ adresa acestei pagini"}

ru = {"maintitle":       u"ÐžÑ‚Ð¿Ñ€Ð°Ð²Ð¸Ñ‚ÑŒ Ñ„Ð°Ð¹Ð»",
      "submit":          u"ÐžÑ‚Ð¿Ñ€Ð°Ð²Ð¸Ñ‚ÑŒ",
      "sending":         u"ÐžÑ‚Ð¿Ñ€Ð°Ð²Ð»ÑÑŽ",
      "successtitle":    u"Ð¤Ð°Ð¹Ð» Ð¿Ð¾Ð»ÑƒÑ‡ÐµÐ½",
      "received":        u"Ð¤Ð°Ð¹Ð» Ð¿Ð¾Ð»ÑƒÑ‡ÐµÐ½ !",
      "another":         u"ÐžÑ‚Ð¿Ñ€Ð°Ð²Ð¸Ñ‚ÑŒ Ð´Ñ€ÑƒÐ³Ð¾Ð¹ Ñ„Ð°Ð¹Ð».",
      "errortitle":      u"ÐžÑˆÐ¸Ð±ÐºÐ°",
      "problem":         u"ÐŸÑ€Ð¾Ð¸Ð·Ð¾ÑˆÐ»Ð° Ð¾ÑˆÐ¸Ð±ÐºÐ° !",
      "retry":           u"ÐŸÐ¾Ð²Ñ‚Ð¾Ñ€Ð¸Ñ‚ÑŒ.",
      "discover":        u"ÐŸÐ¾ÑÐ¼Ð¾Ñ‚Ñ€ÐµÑ‚ÑŒ Ð°Ð´Ñ€ÐµÑ ÑÑ‚Ð¾Ð¹ ÑÑ‚Ñ€Ð°Ð½Ð¸Ñ†Ñ‹"}

sk = {"maintitle":       u"PoÅ¡li sÃºbor",
      "submit":          u"PoÅ¡li",
      "sending":         u"Posielam",
      "successtitle":    u"SÃºbor prijatÃ½",
      "received":        u"SÃºbor prijatÃ½ !",
      "another":         u"PoslaÅ¥ ÄalÅ¡Ã­ sÃºbor.",
      "errortitle":      u"Chyba",
      "problem":         u"Vyskytla sa chyba!",
      "retry":           u"SkÃºsiÅ¥ znova.",
      "discover":        u"Zisti adresu tejto strÃ¡nky"}

sl = {"maintitle":       u"PoÅ¡lji datoteko",
      "submit":          u"PoÅ¡lji",
      "sending":         u"PoÅ¡iljam",
      "successtitle":    u"Datoteka prejeta",
      "received":        u"Datoteka prejeta !",
      "another":         u"PoÅ¡lji novo datoteko.",
      "errortitle":      u"Napaka",
      "problem":         u"PriÅ¡lo je do napake !",
      "retry":           u"Poizkusi ponovno.",
      "discover":        u"PoiÅ¡Äi naslov na tej strani"}

sr = {"maintitle":       u"PoÅ¡alji fajl",
      "submit":          u"PoÅ¡alji",
      "sending":         u"Å aljem",
      "successtitle":    u"Fajl primljen",
      "received":        u"Fajl primljen !",
      "another":         u"PoÅ¡alji joÅ¡ jedan fajl.",
      "errortitle":      u"Problem",
      "problem":         u"Desio se problem !",
      "retry":           u"PokuÅ¡aj ponovo.",
      "discover":        u"Otkrij adresu ove stranice"}

sv = {"maintitle":       u"Skicka en fil",
      "submit":          u"Skicka",
      "sending":         u"Skickar...",
      "successtitle":    u"Fil mottagen",
      "received":        u"Fil mottagen !",
      "another":         u"Skicka en fil till.",
      "errortitle":      u"Fel",
      "problem":         u"Det har uppstÃ¥tt ett fel !",
      "retry":           u"FÃ¶rsÃ¶k igen.",
      "discover":        u"Ta reda pÃ¥ adressen till denna sida"}

tr = {"maintitle":       u"Dosya gÃ¶nder",
      "submit":          u"GÃ¶nder",
      "sending":         u"GÃ¶nderiliyor...",
      "successtitle":    u"GÃ¶nderildi",
      "received":        u"GÃ¶nderildi",
      "another":         u"BaÅŸka bir dosya gÃ¶nder.",
      "errortitle":      u"Problem.",
      "problem":         u"Bir problem oldu !",
      "retry":           u"Yeniden dene.",
      "discover":        u"Bu sayfanÄ±n adresini bul"}

zh_cn = {
      "maintitle":       u"å‘é€æ–‡ä»¶",
      "submit":          u"å‘é€",
      "sending":         u"å‘é€ä¸­",
      "successtitle":    u"æ–‡ä»¶å·²æ”¶åˆ°",
      "received":        u"æ–‡ä»¶å·²æ”¶åˆ°ï¼",
      "another":         u"å‘é€å¦ä¸€ä¸ªæ–‡ä»¶ã€‚",
      "errortitle":      u"é—®é¢˜",
      "problem":         u"å‡ºçŽ°é—®é¢˜ï¼",
      "retry":           u"é‡è¯•ã€‚",
      "discover":        u"æŸ¥çœ‹æœ¬é¡µé¢çš„åœ°å€"}

zh_tw = {
      "maintitle":       u"ä¸Šå‚³æª”æ¡ˆ",
      "submit":          u"ä¸Šå‚³",
      "sending":         u"å‚³é€ä¸­...",
      "successtitle":    u"å·²æ”¶åˆ°æª”æ¡ˆ",
      "received":        u"å·²æ”¶åˆ°æª”æ¡ˆï¼",
      "another":         u"ä¸Šå‚³å¦ä¸€å€‹æª”æ¡ˆã€‚",
      "errortitle":      u"éŒ¯èª¤",
      "problem":         u"å‡ºç¾éŒ¯èª¤ï¼",
      "retry":           u"é‡è©¦ã€‚",
      "discover":        u"æŸ¥é–±æœ¬ç¶²é çš„ç¶²å€"}

translations = {"ar": ar, "cs": cs, "da": da, "de": de, "el": el, "en": en,
                "es": es, "fi": fi, "fr": fr, "gl": gl, "hu": hu, "id": id,
                "it": it, "ja": ja, "ko": ko, "nl": nl, "no": no, "pl": pl,
                "pt": pt, "pt-br": pt_br, "ro": ro, "ru": ru, "sk": sk,
                "sl": sl, "sr": sr, "sv": sv, "tr": tr, "zh-cn": zh_cn,
                "zh-tw": zh_tw}


class DroopyFieldStorage(cgi.FieldStorage):
    """The file is created in the destination directory and its name is
    stored in the tmpfilename attribute.
    """

    TMPPREFIX = 'tmpdroopy'

    def make_file(self, binary=None):
        fd, name = tempfile.mkstemp(dir=directory, prefix=self.TMPPREFIX)
        self.tmpfile = os.fdopen(fd, 'w+b')
        self.tmpfilename = name
        return self.tmpfile


class HTTPUploadHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    protocol_version = 'HTTP/1.0'
    form_field = 'upfile'
    divpicture = '<div class="box"><img src="/__droopy/picture"/></div>'


    def html(self, page):
        """
        page can be "main", "success", or "error"
        returns an html page (in the appropriate language) as a string
        """

        # -- Parse accept-language header
        if not self.headers.has_key("accept-language"):
            a = []
        else:
            a = self.headers["accept-language"]
            a = a.split(',')
            a = [e.split(';q=') for e in  a]
            a = [(lambda x: len(x)==1 and (1, x[0]) or
                                           (float(x[1]), x[0])) (e) for e in a]
            a.sort()
            a.reverse()
            a = [x[1] for x in a]
        # now a is an ordered list of preferred languages

        # -- Choose the appropriate translation dictionary (default is english)
        lang = "en"
        for l in a:
            if translations.has_key(l):
                lang = l
                break
        dico = copy.copy(translations[lang])

        # -- Set message and picture
        if message:
            dico["message"] = ('<div id="message">%s</div>' %
                               message)
        else:
            dico["message"] = ""

        if picture != None:
            dico["divpicture"] = self.divpicture
        else:
            dico["divpicture"] = ""

        # -- Possibly provide download links
        links = ""
        names = self.published_files()
        if names:
            for name in names:
                links += '<a href="/%s">%s</a>' % (
                                urllib.quote(name.encode('utf-8')),
                                name)
            links = '<div id="files">' + links + '</div>'
        dico["files"] = links

        # -- Add a link to discover the url
        if self.client_address[0] == "127.0.0.1":
            dico["port"] = self.server.server_port
            dico["ssl"] = int(certfile is not None)
            dico["linkurl"] =  linkurltmpl % dico
        else:
            dico["linkurl"] = ""

        return templates[page] % dico

    def check_auth(method):
        def decorated(self, *args):
            if auth and self.headers.getheader('Authorization') != \
                                            'Basic ' + base64.b64encode(auth):
                self.send_response(401)
                self.send_header('WWW-Authenticate', 'Basic realm=\"Droopy\"')
                self.send_header('Content-type', 'text/html')
                self.end_headers()
            else:
                method(self, *args)
        return decorated

    @check_auth
    def do_GET(self):
        name = self.path.lstrip('/')
        name = urllib.unquote(name)
        name = name.decode('utf-8')

        if picture != None and self.path == '/__droopy/picture':
            # send the picture
            self.send_file(picture)

        elif name in self.published_files():
            localpath = os.path.join(directory, name)
            self.send_file(localpath)

        else:
            self.send_html(self.html("main"))


    @check_auth
    def do_POST(self):
        # Do some browsers /really/ use multipart ? maybe Opera ?
        try:
            self.log_message("Started file transfer")

            # -- Set up environment for cgi.FieldStorage
            env = {}
            env['REQUEST_METHOD'] = self.command
            if self.headers.typeheader is None:
                env['CONTENT_TYPE'] = self.headers.type
            else:
                env['CONTENT_TYPE'] = self.headers.typeheader

            # -- Save file (numbered to avoid overwriting, ex: foo-3.png)
            form = DroopyFieldStorage(fp = self.rfile, environ = env);
            file_items = form[self.form_field]

            #-- Handle multiple file upload
            if not isinstance(file_items, list):
                file_items = [file_items]

            for item in file_items:
                filename = self.basename(item.filename).decode('utf-8')
                if filename == "":
                    continue

                localpath = os.path.join(directory, filename).encode('utf-8')
                root, ext = os.path.splitext(localpath)
                i = 1

                # race condition, but hey...
                while (os.path.exists(localpath)):
                    localpath = "%s-%d%s" % (root, i, ext)
                    i = i + 1
                if hasattr(item, 'tmpfile'):
                    # DroopyFieldStorage.make_file() has been called
                    item.tmpfile.close()
                    shutil.move(item.tmpfilename, localpath)
                else:
                    # no temporary file, self.file is a StringIO()
                    # see cgi.FieldStorage.read_lines()
                    fout = file(localpath, 'wb')
                    shutil.copyfileobj(item.file, fout)
                    fout.close()

                if file_mode is not None:
                    os.chmod(localpath, file_mode)
                self.log_message("Received: %s", os.path.basename(localpath))

            # -- Reply
            if publish_files:
                # The file list gives a feedback for the upload
                # success
                self.send_response(301)
                self.send_header("Location", "/")
                self.end_headers()
            else:
                self.send_html(self.html("success"))

        except Exception, e:
            self.log_message(repr(e))
            self.send_html(self.html("error"))


    def send_html(self, htmlstr):
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(htmlstr.encode('utf-8'))

    def send_file(self, localpath):
        f = open(localpath, 'rb')
        self.send_response(200)
        self.send_header('Content-type',
                         mimetypes.guess_type(localpath)[0])
        self.send_header('Content-length', os.fstat(f.fileno())[6])
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)

    def basename(self, path):
        """Extract the file base name (some browsers send the full file path).
        """
        for mod in posixpath, macpath, ntpath:
            path = mod.basename(path)
        return path

    def published_files(self):
        """Returns the list of files that should appear as download links.

        The returned filenames are unicode strings.
        """
        if publish_files:
            # os.listdir() returns a list of unicode strings when the
            # directory is passed as an unicode string itself.
            names = [name for name in os.listdir(unicode(directory))
                     if os.path.isfile(os.path.join(directory, name))
                     and not name.startswith(DroopyFieldStorage.TMPPREFIX)]
            names.sort(key=lambda s: s.lower())
        else:
            names = []
        return names

    def handle(self):
        try:
            BaseHTTPServer.BaseHTTPRequestHandler.handle(self)
        except socket.error, e:
            self.log_message(str(e))
            raise Abort()


class Abort(Exception): pass


class ThreadedHTTPServer(SocketServer.ThreadingMixIn,
                         BaseHTTPServer.HTTPServer):

    def handle_error(self, request, client_address):
        # Override SocketServer.handle_error
        exctype = sys.exc_info()[0]
        if not exctype is Abort:
            BaseHTTPServer.HTTPServer.handle_error(self,request,client_address)


# -- Options

def fullpath(path):
    return os.path.abspath(os.path.expanduser(path))

def configfile():
    appname = 'droopy'
    # os.name is 'posix', 'nt', 'os2', 'mac', 'ce' or 'riscos'
    if os.name == 'posix':
        filename = "%s/.%s" % (os.environ["HOME"], appname)

    elif os.name == 'mac':
        filename = ("%s/Library/Application Support/%s" %
                    (os.environ["HOME"], appname))

    elif os.name == 'nt':
        filename = ("%s\%s" % (os.environ["APPDATA"], appname))

    else:
        filename = None

    return filename


def save_options():
    opt = []
    if message:
        opt.append('--message=%s' % message.replace('\n', '\\n'))
    if picture:
        opt.append('--picture=%s' % picture)
    if directory:
        opt.append('--directory=%s' % directory)
    if auth:
        opt.append('--auth=%s' % auth)
    if certfile:
        opt.append('--ssl=%s' % certfile)
    if file_mode:
        opt.append('--chmod=%s' % file_mode)
    if publish_files:
        opt.append('--dl')
    if port:
        opt.append('%d' % port)
    f = open(configfile(), 'w')
    f.write('\n'.join(opt).encode('utf8'))
    f.close()


def load_options():
    try:
        f = open(configfile())
        cmd = [line.strip().decode('utf8').replace('\\n', '\n')
               for line in f.readlines()]
        parse_args(cmd)
        f.close()
        return True
    except IOError, e:
        return False


def parse_args(cmd=None):
    """Parse command-line arguments.

    Parse sys.argv[1:] if no argument is passed.
    """
    global picture, message, port, directory, must_save_options, publish_files
    global auth, certfile, file_mode

    if cmd == None:
        cmd = sys.argv[1:]
        lang, encoding = locale.getdefaultlocale()
        if encoding != None:
            cmd = [a.decode(encoding) for a in cmd]

    opts, args = None, None
    try:
        opts, args = getopt.gnu_getopt(cmd, "p:m:d:a:h",
                                       ["picture=","message=", "directory=",
                                        "auth=", "ssl=", "chmod=", "help",
                                        "save-config", "delete-config", "dl"])
    except Exception, e:
        print e
        sys.exit(1)

    for o, a in opts:
        if o in ["-p", "--picture"]:
            if os.path.exists(a):
                picture = fullpath(a)
            else:
                print "Picture not found: '%s'" % a

        elif o in ["-m", "--message"]:
            message = a

        elif o in ['-d', '--directory']:
            directory = fullpath(a)

        elif o in ['--save-config']:
            must_save_options = True

        elif o in ['--delete-config']:
            try:
                filename = configfile()
                os.remove(filename)
                print 'Deleted ' + filename
            except Exception, e:
                print e
            sys.exit(0)

        elif o in ['--dl']:
            publish_files = True

        elif o in ['-a', '--auth']:
            if ':' not in a:
                print "Error: authentication credentials must be " \
                      "specified as USER:PASSWORD"
                sys.exit(1)
            auth = a

        elif o in ['--ssl']:
            if not os.path.isfile(a):
                print "PEM file not found: '%s'" % a
                sys.exit(1)
            certfile = fullpath(a)

        elif o in ['--chmod']:
            try:
                file_mode = int(a, 8)
            except ValueError:
                print "Invalid octal value passed to chmod option: '%s'" % a
                sys.exit(1)


        elif o in ['-h', '--help']:
            print USAGE
            sys.exit(0)

    # port number
    try:
        if args[0:]:
            port = int(args[0])
    except ValueError:
        print args[0], "is not a valid port number"
        sys.exit(1)


# --

def run():
    """Run the webserver."""
    socket.setdefaulttimeout(3*60)
    server_address = ('', port)
    httpd = ThreadedHTTPServer(server_address, HTTPUploadHandler)
    if certfile:
        try:
            import ssl
        except:
            print "Error: Could not import module 'ssl', exiting."
            sys.exit(2)
        httpd.socket = ssl.wrap_socket(httpd.socket, certfile=certfile,
                                       server_side=True)
    httpd.serve_forever()


if __name__ == '__main__':
    print LOGO

    config_found = load_options()
    parse_args()

    if config_found:
        print 'Configuration found in %s' % configfile()
    else:
        print "No configuration file found."

    if must_save_options:
        save_options()
        print "Options saved in %s" % configfile()

    proto = 'https' if certfile else 'http'
    print "Files will be uploaded to %s" % directory
    print
    print ("HTTP server running... Check it out at %s://localhost:%d"
           % (proto, port))
    try:
        run()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        # some threads may run until they terminate
