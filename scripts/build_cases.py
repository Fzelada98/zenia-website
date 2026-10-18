#!/usr/bin/env python3
"""Fichas de caso premium de Zenia (25-sep-2026).

Genera, desde el contenido de abajo, las fichas EN y ES de cada caso y los
índices de casos (/cases/ y /es/casos.html). Una sola plantilla para que
todas se vean iguales; el color de acento es de cada cliente.

Reglas de contenido (no negociables):
  - Solo lo construido y cifras reales. Los resultados comerciales se añaden
    cuando existan, nunca se estiman.
  - Croian & Hein: al enólogo no se le nombra y no hay precios.
  - Cicero: ni precios, ni comisión, ni el piloto; su landing sigue en revisión
    y no se enlaza.

Uso: python3 scripts/build_cases.py   (desde la raíz del repo)
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://zeniapartners.com"
WA = "https://wa.me/34677612799?text="
CAL = "https://calendly.com/zeladauriartef/30min"
FECHA = "2026-09-25"

ZMARK = '<svg class="zmark" aria-hidden="true" viewBox="0 0 140 140" fill="none"><defs><linearGradient id="zg-b" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#2563EB"/><stop offset="100%" stop-color="#3B82F6"/></linearGradient><linearGradient id="zg-v" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#6366F1"/><stop offset="100%" stop-color="#7C3AED"/></linearGradient></defs><rect width="140" height="140" rx="28" fill="#0F172A"/><path d="M 70 18 Q 18 18 18 38 L 18 57 Q 18 63 24 63 L 88 63 Z" fill="url(#zg-b)"/><path d="M 70 122 Q 122 122 122 102 L 122 83 Q 122 77 116 77 L 52 77 Z" fill="url(#zg-v)"/></svg>'

CSS = """
:root{--bg:#0A0F1C;--bg2:#0C1220;--ink:#F1F5F9;--ink2:#C3CFDD;--mute:#8C9BB0;--line:rgba(148,163,184,.14);--blue:#3B82F6;--violet:#6366F1}
*{margin:0;padding:0;box-sizing:border-box}html{scroll-behavior:smooth;-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:100%}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--ink);line-height:1.6;overflow-x:hidden}
a{color:inherit;text-decoration:none}img{display:block;max-width:100%;height:auto}
h1,h2,h3{font-family:'Space Grotesk','Inter',sans-serif;font-weight:700;letter-spacing:-.03em;line-height:1.05}
.wrap{max-width:1200px;margin:0 auto;padding:0 40px}
.acc{background:linear-gradient(120deg,var(--a1),var(--a2));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.nav{position:sticky;top:0;z-index:50;background:rgba(10,15,28,.82);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;align-items:center;justify-content:space-between;height:68px}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;letter-spacing:-.02em;font-size:19px}
.zmark{width:30px;height:30px;flex-shrink:0}
.nav-r{display:flex;align-items:center;gap:28px;font-size:14px;color:var(--ink2)}
.nav-r a:hover{color:var(--ink)}
.nav-cta{padding:9px 18px;border-radius:999px;border:1px solid var(--line);color:var(--ink)!important}
.nav-cta:hover{border-color:rgba(255,255,255,.3)}
.hero{position:relative;padding:112px 0 72px;overflow:hidden}
.hero:before{content:'';position:absolute;top:-260px;left:50%;width:1100px;height:760px;transform:translateX(-50%);background:radial-gradient(closest-side,var(--glow),transparent);pointer-events:none}
.kicker{display:flex;flex-wrap:wrap;align-items:center;gap:12px;font-size:12px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);position:relative}
.kicker b{color:var(--a1);font-weight:600}.kicker i{width:4px;height:4px;border-radius:50%;background:var(--mute);opacity:.5}
.lockup{display:flex;align-items:center;gap:22px;margin:44px 0 36px;position:relative}
.lockup .zmark{width:46px;height:46px}.lockup .x{color:var(--mute);font-size:20px;font-weight:300}
.lockup img{height:54px;width:auto}.lockup .cn{font-family:'Space Grotesk',sans-serif;font-size:22px;letter-spacing:-.01em;color:var(--ink)}
.hero h1{font-size:clamp(2.5rem,6.2vw,5.2rem);max-width:15ch;position:relative}
.lede{font-size:clamp(1.08rem,1.6vw,1.3rem);line-height:1.7;color:var(--ink2);max-width:62ch;margin-top:32px;position:relative}
.facts{display:grid;grid-template-columns:repeat(5,1fr);margin-top:72px;border-top:1px solid var(--line);position:relative}
.facts div{padding:22px 24px 0 0}
.facts dt{font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);margin-bottom:8px}
.facts dd{font-size:15px;color:var(--ink);line-height:1.5}.facts dd a{border-bottom:1px solid var(--a1)}
.stage{position:relative;padding:24px 0 120px;overflow:hidden}
.stage:before{content:'';position:absolute;inset:10% 0 0;background:radial-gradient(60% 55% at 50% 45%,var(--glow),transparent 70%);pointer-events:none}
.dev{position:relative;max-width:1080px;margin:0 auto}
.browser{border-radius:14px;overflow:hidden;background:#0B0B0E;border:1px solid rgba(255,255,255,.1);box-shadow:0 60px 120px -30px rgba(0,0,0,.8),0 0 0 1px rgba(0,0,0,.4)}
.bar{display:flex;align-items:center;gap:7px;height:38px;padding:0 16px;background:#15171C;border-bottom:1px solid rgba(255,255,255,.06)}
.bar i{width:10px;height:10px;border-radius:50%;background:#2B2E35}
.bar span{margin:0 auto;padding:4px 18px;border-radius:7px;background:#0D0F13;color:#8C93A0;font-size:12px;letter-spacing:.02em;transform:translateX(-18px)}
.phone{position:absolute;right:-3%;bottom:-9%;width:23%;border-radius:34px;padding:9px;background:#08080A;border:1px solid rgba(255,255,255,.14);box-shadow:0 40px 90px -20px rgba(0,0,0,.9)}
.phone img{border-radius:26px}
.posters{display:grid;grid-template-columns:1fr 1fr;gap:32px;max-width:980px;margin:0 auto;position:relative}
.posters img{border-radius:14px;border:1px solid rgba(255,255,255,.08);box-shadow:0 50px 100px -30px rgba(0,0,0,.85)}
.nums{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.nums div{padding:48px 28px 44px;border-left:1px solid var(--line)}.nums div:first-child{border-left:0;padding-left:0}
.nums b{display:block;font-family:'Space Grotesk',sans-serif;font-size:clamp(2.6rem,5vw,4.2rem);line-height:1;letter-spacing:-.04em;margin-bottom:14px}
.nums span{font-size:14px;line-height:1.5;color:var(--ink2);display:block;max-width:22ch}
.nums-cap{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);font-weight:600;padding:0 0 18px}
.sec{padding:120px 0 0}
.row{display:grid;grid-template-columns:260px 1fr;gap:72px}
.lab{font-size:12px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--a1);padding-top:12px}
.row h2{font-size:clamp(2rem,3.8vw,3.2rem);max-width:18ch;margin-bottom:28px}
.row p{font-size:1.14rem;line-height:1.8;color:var(--ink2);max-width:64ch;margin-bottom:18px}
.row p strong{color:var(--ink);font-weight:600}
.rules{list-style:none;margin-top:30px;border-top:1px solid var(--line)}
.rules li{padding:16px 0;border-bottom:1px solid var(--line);color:var(--ink2);font-size:1.02rem;display:grid;grid-template-columns:28px 1fr}
.rules li:before{content:'—';color:var(--a1)}
.chs{margin-top:56px}
.ch{display:grid;grid-template-columns:260px 1fr 1.25fr;gap:72px;padding:52px 0;border-top:1px solid var(--line)}
.ch .n{font-family:'Space Grotesk',sans-serif;font-size:15px;color:var(--a1);letter-spacing:.06em}
.ch h3{font-size:clamp(1.45rem,2.3vw,1.9rem);letter-spacing:-.025em;line-height:1.15}
.ch p{font-size:1.04rem;line-height:1.8;color:var(--ink2)}
.shot{padding:8px 0 56px}.shot figcaption{font-size:13px;color:var(--mute);margin-top:16px;text-align:center}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.crest{display:flex;align-items:center;justify-content:center;gap:10%;padding:72px 0;border-radius:14px;background:radial-gradient(70% 90% at 50% 50%,#17120A,#07070A);border:1px solid rgba(255,255,255,.06)}
.crest img{height:300px;width:auto}.crest img+img{height:190px}
.pal{display:flex;gap:0;margin-top:0;border-radius:0 0 14px 14px;overflow:hidden}
.pal span{flex:1;height:56px;display:flex;align-items:flex-end;padding:8px 12px;font-size:11px;letter-spacing:.08em}
.flow{display:grid;grid-template-columns:repeat(6,1fr);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.flow div{padding:28px 20px 30px;border-left:1px solid var(--line);position:relative;background:linear-gradient(180deg,rgba(255,255,255,.02),transparent)}
.flow div:first-child{border-left:0}
.flow em{font-style:normal;font-family:'Space Grotesk',sans-serif;color:var(--a1);font-size:13px}
.flow b{display:block;font-family:'Space Grotesk',sans-serif;font-size:1.05rem;margin:10px 0 8px;letter-spacing:-.01em}
.flow span{font-size:13px;line-height:1.55;color:var(--mute);display:block}
.reels{display:grid;grid-template-columns:1fr 1fr;gap:40px;max-width:780px;margin:0 auto;position:relative}
.reel video{display:block;width:100%;height:auto;aspect-ratio:9/16;object-fit:cover;border-radius:22px;border:1px solid rgba(255,255,255,.12);background:#000;box-shadow:0 50px 100px -30px rgba(0,0,0,.85)}
.reel figcaption{margin-top:16px;font-size:14px;line-height:1.55;color:var(--ink2)}.reel figcaption b{display:block;color:var(--ink);font-weight:600;margin-bottom:4px}
.reels-cta{text-align:center;margin-top:48px;position:relative}
.cards a.feat{grid-column:1/-1}
@media(max-width:760px){.reels{grid-template-columns:1fr;max-width:400px;gap:48px}}
.qs{display:flex;flex-wrap:wrap;gap:10px;margin:8px 0 24px}
.qs span{font-family:'SFMono-Regular',ui-monospace,Menlo,monospace;font-size:14px;padding:9px 16px;border-radius:999px;border:1px solid var(--line);color:var(--ink)}
.qs span:before{content:'⌕ ';color:var(--a1)}
.dl{font-size:1rem;line-height:2.1;color:var(--ink2)}.dl span:after{content:'/';color:var(--mute);margin:0 14px;opacity:.6}.dl span:last-child:after{content:''}
.cta{text-align:center;padding:170px 0 120px;position:relative;overflow:hidden}
.cta:before{content:'';position:absolute;top:30%;left:50%;width:900px;height:600px;transform:translateX(-50%);background:radial-gradient(closest-side,var(--glow),transparent);pointer-events:none}
.cta h2{font-size:clamp(2.2rem,5vw,4rem);max-width:18ch;margin:0 auto 24px;position:relative}
.cta p{font-size:1.15rem;color:var(--ink2);max-width:56ch;margin:0 auto 44px;line-height:1.7;position:relative}
.btns{display:flex;justify-content:center;gap:14px;flex-wrap:wrap;position:relative}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;padding:17px 32px;border-radius:999px;font-weight:600;font-size:16px;transition:transform .2s,box-shadow .2s,background .2s}
.btn-p{background:linear-gradient(135deg,#2563EB,#6366F1);color:#fff;box-shadow:0 0 30px rgba(59,130,246,.3)}
.btn-p:hover{transform:translateY(-2px);box-shadow:0 0 44px rgba(99,102,241,.45)}
.btn-s{border:1px solid rgba(255,255,255,.16);color:var(--ink)}.btn-s:hover{background:rgba(255,255,255,.06)}
.next{display:grid;grid-template-columns:1fr auto;align-items:end;gap:24px;padding:56px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.next small{display:block;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);font-weight:600;margin-bottom:12px}
.next strong{font-family:'Space Grotesk',sans-serif;font-size:clamp(1.7rem,3.6vw,2.8rem);letter-spacing:-.03em;line-height:1.1}
.next .arr{font-size:clamp(1.8rem,3vw,2.6rem);color:var(--mute);transition:transform .25s,color .25s}
.next:hover .arr{transform:translateX(8px);color:var(--ink)}
.alt{text-align:center;padding:28px 0 0;font-size:14px;color:var(--mute)}.alt a{color:var(--ink2);border-bottom:1px solid var(--line)}
.foot{padding:56px 0 40px;margin-top:72px;border-top:1px solid var(--line);font-size:13px;color:var(--mute)}
.foot .wrap{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap}.foot nav{display:flex;gap:24px;flex-wrap:wrap}.foot a:hover{color:var(--ink)}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:72px}
.card-img{border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,.08);aspect-ratio:16/10;background:#0B0B0E}
.card-img img{width:100%;height:100%;object-fit:cover;object-position:top;transition:transform .6s}
.cards a:hover .card-img img{transform:scale(1.025)}
.cards .meta{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);font-weight:600;margin:24px 0 10px}
.cards h3{font-size:clamp(1.5rem,2.4vw,2rem);letter-spacing:-.025em;line-height:1.15;margin-bottom:12px}
.cards p{color:var(--ink2);font-size:1.02rem;line-height:1.7}
.cards .go{display:inline-block;margin-top:16px;font-weight:600;font-size:15px}
.list{margin-top:96px;border-top:1px solid var(--line)}
.list a{display:grid;grid-template-columns:260px 1fr auto;gap:40px;align-items:baseline;padding:30px 0;border-bottom:1px solid var(--line)}
.list small{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);font-weight:600}
.list strong{font-family:'Space Grotesk',sans-serif;font-size:1.35rem;letter-spacing:-.02em;font-weight:700}
.list em{font-style:normal;color:var(--mute);transition:transform .25s}.list a:hover em{transform:translateX(6px);color:var(--ink)}
@media(max-width:1024px){.facts{grid-template-columns:repeat(3,1fr)}.facts div{padding-bottom:18px}.row,.ch{grid-template-columns:1fr;gap:18px}.ch{padding:40px 0}.flow{grid-template-columns:repeat(3,1fr)}.flow div:nth-child(4){border-left:0}.flow div:nth-child(n+4){border-top:1px solid var(--line)}}
@media(max-width:760px){.wrap{padding:0 20px}.nav-r .hide{display:none}.nav-r{gap:16px}.hero{padding:72px 0 48px}.lockup{margin:32px 0 28px;gap:16px}.lockup img{height:42px}.lockup .zmark{width:36px;height:36px}
.facts{grid-template-columns:1fr 1fr;margin-top:48px}.facts div:last-child{grid-column:1/-1}
.stage{padding:8px 0 72px}.phone{width:34%;right:-2%;bottom:-12%;border-radius:22px;padding:5px}.phone img{border-radius:18px}.bar{height:28px}.bar span{font-size:10px}
.posters,.pair,.cards{grid-template-columns:1fr;gap:20px}.nums{grid-template-columns:1fr 1fr}.nums div{padding:32px 16px 30px}.nums div:nth-child(3){border-left:0;padding-left:0}.nums div:nth-child(n+3){border-top:1px solid var(--line)}
.sec{padding:84px 0 0}.crest{padding:44px 0;gap:8%}.crest img{height:170px}.crest img+img{height:110px}.pal span{height:44px;font-size:9px;padding:6px}
.flow{grid-template-columns:1fr 1fr}.flow div:nth-child(odd){border-left:0}.flow div:nth-child(4){border-left:1px solid var(--line)}.flow div:nth-child(n+3){border-top:1px solid var(--line)}
.cta{padding:110px 0 80px}.btn{width:100%}.list a{grid-template-columns:1fr auto;gap:8px 16px}.list small{grid-column:1/-1}}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">')

GA = ('<script async src="https://www.googletagmanager.com/gtag/js?id=G-HP0VQSEL68"></script>'
      "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-HP0VQSEL68');</script>")

# Botón flotante + beacon + formulario de cualificación: mismo marcado que el
# resto del sitio, para que el guard SEO los reconozca y no los duplique.
TAIL = ('<a href="{wa}" target="_blank" rel="noopener" aria-label="Contactar por WhatsApp" data-directo '
        'style="position:fixed;bottom:24px;right:24px;z-index:9998;background:#25D366;color:white;width:56px;height:56px;'
        'border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(37,211,102,0.4);">'
        '<svg viewBox="0 0 24 24" fill="currentColor" width="28" height="28" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg></a>\n'
        '<script>document.addEventListener("click",function(e){{var t=e.target,a=t.closest?t.closest(\'a[href*="wa.me"]\'):null;if(!a)return;'
        'try{{navigator.sendBeacon("https://gaia-relojes.onrender.com/gwb/lead",JSON.stringify({{site:"zenia",path:location.pathname+location.search,ref:document.referrer||""}}))}}catch(r){{}}}},true);</script>\n'
        '<script src="/assets/qualify.js?v=4" defer></script>\n'
        '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{{"token": "67e4803d7cd443a49b12c7d8a99365bf"}}\'></script>')

UI = {
    "en": {"cases": "Cases", "blog": "Blog", "talk": "Talk to us", "home": "/", "blog_url": "/blog/",
           "hub": "/cases/", "kicker": "Case study", "client": "Client", "sector": "Sector", "market": "Market",
           "scope": "Scope", "status": "Status", "next": "Next case", "all": "All cases",
           "wa_btn": "Message us on WhatsApp", "cal_btn": "Book a strategy call",
           "rights": "All rights reserved.", "about": "About", "about_url": "/about.html",
           "contact": "Contact", "delivered": "Deliverables"},
    "es": {"cases": "Casos", "blog": "Blog", "talk": "Hablemos", "home": "/es/", "blog_url": "/blog/",
           "hub": "/es/casos.html", "kicker": "Caso de éxito", "client": "Cliente", "sector": "Sector",
           "market": "Mercado", "scope": "Alcance", "status": "Estado", "next": "Siguiente caso",
           "all": "Todos los casos", "wa_btn": "Escríbenos por WhatsApp", "cal_btn": "Agenda una llamada",
           "rights": "Todos los derechos reservados.", "about": "Nosotros", "about_url": "/about.html",
           "contact": "Contacto", "delivered": "Entregables"},
}


def e(s):
    return html.escape(s, quote=True)


def wa(txt):
    from urllib.parse import quote
    return WA + quote(txt)


def head(lang, title, desc, url, og, alt_lang, alt_url, jsonld):
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{GA}
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{url}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="alternate" hreflang="{lang}" href="{SITE}{url}">
<link rel="alternate" hreflang="{alt_lang}" href="{SITE}{alt_url}">
<link rel="alternate" hreflang="x-default" href="{SITE}{url if lang == 'en' else alt_url}">
<link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
<meta property="og:type" content="article">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{url}">
<meta property="og:site_name" content="ZENIA">
<meta property="og:image" content="{SITE}{og}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}{og}">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
{FONTS}
<style>{CSS}</style>
</head>"""


def nav(lang):
    u = UI[lang]
    return f"""<nav class="nav"><div class="wrap">
<a class="brand" href="{u['home']}">{ZMARK}<span>ZENIA</span></a>
<div class="nav-r"><a class="hide" href="{u['hub']}">{u['cases']}</a><a class="hide" href="{u['blog_url']}">{u['blog']}</a>
<a class="nav-cta" href="{wa('Hola, vengo de los casos de Zenia' if lang == 'es' else 'Hi, I come from the Zenia case studies')}" target="_blank" rel="noopener">{u['talk']}</a></div>
</div></nav>"""


def foot(lang):
    u = UI[lang]
    return f"""<footer class="foot"><div class="wrap"><span>&copy; 2026 ZENIA. {u['rights']}</span>
<nav><a href="{u['home']}">Home</a><a href="{u['hub']}">{u['cases']}</a><a href="{u['about_url']}">{u['about']}</a><a href="{u['blog_url']}">Blog</a><a href="mailto:fabrizzio.zelada@zeniapartners.com">{u['contact']}</a></nav>
</div></footer>"""


def stage(c):
    if c["stage"]["type"] == "devices":
        s = c["stage"]
        return f"""<section class="stage"><div class="wrap"><div class="dev">
<figure class="browser"><div class="bar"><i></i><i></i><i></i><span>{s['domain']}</span></div><img src="{s['desk']}" alt="{e(s['alt'])}" width="1600" height="1000" fetchpriority="high"></figure>
<figure class="phone"><img src="{s['mob']}" alt="{e(s['alt_mob'])}" width="640" height="1385" loading="lazy"></figure>
</div></div></section>"""
    if c["stage"]["type"] == "videos":
        s = c["stage"]
        figs = "".join(
            f'<figure class="reel"><video controls playsinline preload="metadata" poster="{v["poster"]}" width="720" height="1280">'
            f'<source src="{v["src"]}" type="video/mp4"></video><figcaption><b>{v["label"]}</b>{v["note"]}</figcaption></figure>'
            for v in s["videos"])
        cta = (f'<div class="reels-cta"><a class="btn btn-p" href="{wa(s["cta_wa"])}" target="_blank" rel="noopener">{s["cta_btn"]}</a></div>'
               if s.get("cta_wa") else "")
        return f'<section class="stage"><div class="wrap"><div class="reels">{figs}</div>{cta}</div></section>'
    imgs = "".join(f'<img src="{i}" alt="{e(a)}" width="1080" height="1350" loading="lazy">' for i, a in c["stage"]["imgs"])
    return f'<section class="stage"><div class="wrap"><div class="posters">{imgs}</div></div></section>'


def browser(src, domain, alt, w=1400, h=875):
    return (f'<figure class="browser"><div class="bar"><i></i><i></i><i></i><span>{domain}</span></div>'
            f'<img src="{src}" alt="{e(alt)}" width="{w}" height="{h}" loading="lazy"></figure>')


def visual(v):
    t = v["type"]
    if t == "shot":
        return f'<div class="shot">{browser(v["src"], v["domain"], v["alt"])}<figcaption>{v["cap"]}</figcaption></div>'
    if t == "pair":
        a, b = v["items"]
        return (f'<div class="shot"><div class="pair">{browser(a[0], a[1], a[2])}{browser(b[0], b[1], b[2])}</div>'
                f'<figcaption>{v["cap"]}</figcaption></div>')
    if t == "crest":
        sw = "".join(f'<span style="background:{c};color:{fg}">{n}</span>' for c, fg, n in v["palette"])
        return (f'<div class="shot"><div class="crest" style="border-radius:14px 14px 0 0"><img src="{v["crest"]}" alt="{e(v["alt"])}" width="420" height="480" loading="lazy">'
                f'<img src="{v["mark"]}" alt="" width="131" height="200" loading="lazy"></div><div class="pal">{sw}</div>'
                f'<figcaption>{v["cap"]}</figcaption></div>')
    if t == "flow":
        cells = "".join(f'<div><em>{n}</em><b>{h}</b><span>{d}</span></div>' for n, h, d in v["steps"])
        return f'<div class="shot"><div class="flow">{cells}</div><figcaption>{v["cap"]}</figcaption></div>'
    return ""


def page(c, lang):
    u = UI[lang]
    t = c[lang]
    other = "es" if lang == "en" else "en"
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": t["title"], "description": t["desc"],
          "datePublished": FECHA, "dateModified": FECHA, "inLanguage": lang,
          "image": SITE + c["og"], "mainEntityOfPage": SITE + c["url"][lang],
          "author": {"@type": "Organization", "name": "ZENIA", "url": SITE},
          "publisher": {"@type": "Organization", "name": "ZENIA", "url": SITE,
                        "logo": {"@type": "ImageObject", "url": SITE + "/assets/icons/favicon.svg"}},
          "about": {"@type": "Organization", "name": c["client"], "url": c["client_url"]}}
    if c["stage"]["type"] == "videos":
        st = c["stage"] | t.get("stage_txt", {})
        ld["video"] = [{"@type": "VideoObject", "name": v["name"], "description": v["desc"],
                        "thumbnailUrl": SITE + v["poster"], "contentUrl": SITE + v["src"],
                        "uploadDate": v["date"], "duration": v["dur"], "inLanguage": v.get("lang", lang)}
                       for v in st["videos"]]
    out = [head(lang, t["title"], t["desc"], c["url"][lang], c["og"], other, c["url"][other], ld)]
    out.append(f'<body style="--a1:{c["a1"]};--a2:{c["a2"]};--glow:{c["glow"]}">')
    out.append(nav(lang))
    kick = "".join(f"<i></i><span>{k}</span>" for k in t["kicker"])
    facts = "".join(f"<div><dt>{u[k]}</dt><dd>{v}</dd></div>" for k, v in t["facts"])
    logo = (f'<img src="{c["logo"]}" alt="{e(c["client"])}" width="{c["logo_w"]}" height="54">'
            + (f'<span class="cn">{c["client"]}</span>' if c.get("logo_name") else ""))
    out.append(f"""<header class="hero"><div class="wrap">
<div class="kicker"><b>{u['kicker']}</b>{kick}</div>
<div class="lockup">{ZMARK}<span class="x">&times;</span>{logo}</div>
<h1>{t['h1']}</h1>
<p class="lede">{t['lede']}</p>
<dl class="facts">{facts}</dl>
</div></header>""")
    out.append(stage(c | {"stage": c["stage"] | t.get("stage_txt", {})}))
    out.append(f'<section><div class="wrap"><div class="nums-cap">{t["nums_cap"]}</div><div class="nums">'
               + "".join(f"<div><b class=\"acc\">{n}</b><span>{l}</span></div>" for n, l in t["nums"])
               + "</div></div></section>")
    brief = "".join(f"<p>{p}</p>" for p in t["brief"])
    rules = ("<ul class=\"rules\">" + "".join(f"<li>{r}</li>" for r in t["rules"]) + "</ul>") if t.get("rules") else ""
    out.append(f"""<section class="sec"><div class="wrap"><div class="row"><div class="lab">{t['brief_lab']}</div>
<div><h2>{t['brief_h']}</h2>{brief}{rules}</div></div></div></section>""")
    chs = []
    for i, ch in enumerate(t["chapters"], 1):
        chs.append(f'<div class="ch"><div class="n">{i:02d}</div><h3>{ch["h"]}</h3><p>{ch["p"]}</p></div>')
        if ch.get("v"):
            chs.append(visual(ch["v"]))
    out.append(f"""<section class="sec"><div class="wrap"><div class="row"><div class="lab">{t['built_lab']}</div>
<div><h2>{t['built_h']}</h2><p>{t['built_p']}</p></div></div><div class="chs">{''.join(chs)}</div></div></section>""")
    if t.get("nums2"):
        out.append(f'<section class="sec"><div class="wrap"><div class="nums-cap">{t["nums2_cap"]}</div><div class="nums">'
                   + "".join(f"<div><b class=\"acc\">{n}</b><span>{l}</span></div>" for n, l in t["nums2"])
                   + "</div></div></section>")
    qs = ('<div class="qs">' + "".join(f"<span>{q}</span>" for q in t["queries"]) + "</div>") if t.get("queries") else ""
    sig = "".join(f"<p>{p}</p>" for p in t["signals"])
    dl = '<div class="dl">' + "".join(f"<span>{d}</span>" for d in t["deliverables"]) + "</div>"
    out.append(f"""<section class="sec"><div class="wrap"><div class="row"><div class="lab">{t['sig_lab']}</div>
<div><h2>{t['sig_h']}</h2>{sig}{qs}</div></div></div></section>
<section class="sec"><div class="wrap"><div class="row"><div class="lab">{u['delivered']}</div><div>{dl}</div></div></div></section>""")
    out.append(f"""<section class="cta"><div class="wrap"><h2>{t['cta_h']}</h2><p>{t['cta_p']}</p>
<div class="btns"><a class="btn btn-p" href="{wa(t['cta_wa'])}" target="_blank" rel="noopener">{u['wa_btn']}</a>
<a class="btn btn-s" href="{CAL}" target="_blank" rel="noopener">{u['cal_btn']}</a></div></div></section>""")
    nx = CASES[c["next"]]
    out.append(f"""<section><div class="wrap"><a class="next" href="{nx['url'][lang]}"><div><small>{u['next']}</small><strong>{nx[lang]['card_h']}</strong></div><span class="arr">&rarr;</span></a>
<p class="alt">{t['alt_txt']} <a href="{c['url'][other]}">{t['alt_link']}</a> &middot; <a href="{u['hub']}">{u['all']}</a></p></div></section>""")
    out.append(foot(lang))
    out.append(TAIL.format(wa=wa(t["cta_wa"])))
    out.append("</body>\n</html>\n")
    return "\n".join(out)


# ---------------------------------------------------------------- contenido

CROIAN = {
    "client": "Croian & Hein", "client_url": "https://croianhein.com",
    "a1": "#D9C49A", "a2": "#B9A477", "glow": "rgba(122,24,44,.30)",
    "logo": "/cases/img/croian-mark.svg", "logo_w": 36, "logo_name": True,
    "og": "/cases/img/croian-og.jpg", "next": "cicero",
    "url": {"en": "/cases/croian-hein-private-cellar-switzerland.html", "es": "/es/caso-croian-hein.html"},
    "stage": {"type": "devices", "domain": "croianhein.com", "desk": "/cases/img/croian-home.webp",
              "mob": "/cases/img/croian-mobile.webp"},
    "card_img": "/cases/img/croian-home.webp",
    "en": {
        "title": "Croian & Hein: launching a private rare-wine house in Switzerland | ZENIA case study",
        "desc": "How ZENIA turned a private collection of 1,000+ rare wines into a luxury house for Swiss collectors: positioning, an engraved identity, a 430+ page digital cellar, AI visibility and the kit to sell in person.",
        "kicker": ["Luxury &amp; collectibles", "Switzerland"],
        "h1": 'Some bottles are never sold. <span class="acc">We built the house that entrusts them.</span>',
        "lede": "Croian &amp; Hein holds the Swiss exclusive of a private collection of more than 1,000 references, from 1815 to 2024, assembled over a lifetime by a renowned winemaker who prefers not to be named. ZENIA took it from a trade price list to a complete luxury house: positioning, identity, a digital home built for collectors, a search engine made of the cellar itself, and the kit to sell it in person.",
        "facts": [("client", "Croian &amp; Hein"), ("sector", "Rare wine &amp; collectibles"),
                  ("market", "Switzerland &middot; EN FR DE IT"), ("scope", "Brand, web, SEO, AI visibility, sales kit"),
                  ("status", 'Live at <a href="https://croianhein.com" target="_blank" rel="noopener">croianhein.com</a>')],
        "stage_txt": {"alt": "Croian & Hein home page on desktop", "alt_mob": "Croian & Hein home page on mobile"},
        "nums_cap": "In numbers",
        "nums": [("&lt;72 h", "from first brief to a live house"), ("430+", "pages generated from the real inventory"),
                 ("4", "languages for the Swiss market"), ("1,000+", "references catalogued, 1815 to 2024")],
        "brief_lab": "The brief",
        "brief_h": "The asset was extraordinary. The market had never heard of it.",
        "brief": ["The collection existed as a dealer's price list: trade abbreviations, no stories, no brand. Pétrus 1946, a complete Sassicaia vertical from 1968 to 2022, a Marsala from the year of Waterloo, the first rosé Roederer ever released. Many of them the last bottle left.",
                  "The people who buy this (collectors, family offices, sommeliers of the best tables in Bern, Geneva and Zürich) never buy from a list. They buy trust, provenance and discretion. And the founder was flying to Switzerland days later."],
        "rules": ["No public prices, anywhere. Every bottle is quoted on request.",
                  "The owner of the collection is never named.",
                  "It had to feel like a house that has always existed, not a start-up.",
                  "The name had to stay open to objects beyond wine."],
        "built_lab": "What we built",
        "built_h": "Not a website. A house, launched end to end.",
        "built_p": "Seven pieces, designed together and shipped as one launch.",
        "chapters": [
            {"h": "Positioning", "p": "A private cellar opened by appointment, built on three words: discretion, provenance, placement. One line carries it: <strong>Some bottles are never sold. They are entrusted.</strong> Everything else follows from it, including what the house refuses to say."},
            {"h": "An engraved identity", "p": "A heron crest drawn entirely in code: double pearled oval, a heron cut with burin hatching, knotted laurels and the motto <em>Silentio et fide</em>. Four colourways, a flat heron for small sizes, and a palette of ivory, universe black, bordeaux, wine green and champagne set in Cormorant Garamond and Jost.",
             "v": {"type": "crest", "crest": "/cases/img/croian-crest.svg", "mark": "/cases/img/croian-mark.svg",
                   "alt": "Croian & Hein engraved heron crest",
                   "palette": [("#F4EFE6", "#0B0A0C", "IVORY"), ("#0B0A0C", "#B9A477", "UNIVERSE"), ("#5A1020", "#F4EFE6", "BORDEAUX"),
                               ("#18352F", "#F4EFE6", "WINE GREEN"), ("#B9A477", "#0B0A0C", "CHAMPAGNE")],
                   "cap": "The crest, the heron and the house palette."}},
            {"h": "The digital house", "p": "A full-screen opening where an illustrated bottle, rendered in code, turns to the light to reveal its label. Then the house, the manifesto, six bottles that explain the cellar, the collection by region with a sheet for every wine, the founder, provenance and a private enquiry. No third-party scripts, strict security headers, fast on any phone.",
             "v": {"type": "pair", "items": [("/cases/img/croian-house.webp", "croianhein.com", "The house section"),
                                              ("/cases/img/croian-cellar.webp", "croianhein.com", "Six bottles that explain the cellar")],
                   "cap": "The house and six bottles that explain the cellar."}},
            {"h": "The cellar as a search engine", "p": "Collectors do not search for &ldquo;rare wine&rdquo;. They search for the exact bottle and vintage. We parsed the owner's list line by line and generated a page for every wine, a page for every vintage in stock and six complete verticals, each with format, bottles remaining and condition translated from trade shorthand. Four Swiss hubs (Switzerland, Geneva, Zürich, Lugano) cover delivery and customs in their own language.",
             "v": {"type": "pair", "items": [("/cases/img/croian-vintage.webp", "croianhein.com/cellar/petrus/1946", "Pétrus 1946 vintage page"),
                                              ("/cases/img/croian-vertical.webp", "croianhein.com/verticals", "Sassicaia vertical 1968 to 2022")],
                   "cap": "One page per vintage. Pétrus 1946 and the Sassicaia vertical, 1968 to 2022."}},
            {"h": "The Journal", "p": "Twenty-three long-form pieces, more than 16,000 words, on what Swiss collectors actually ask: importing wine into Switzerland, bonded storage, selling a cellar, fill levels, provenance. The practical guides also in French and German. A weekly agent now reads real search data and writes the next one.",
             "v": {"type": "shot", "src": "/cases/img/croian-journal.webp", "domain": "croianhein.com/journal",
                   "alt": "Journal article on importing wine into Switzerland", "cap": "What a bottle actually costs to land in Switzerland."}},
            {"h": "Readable by AI", "p": "The whole inventory is published in machine-readable form (a site map for language models, the full cellar in text and JSON, product data on roughly 400 pages) and 24 AI crawlers are explicitly welcome. When someone asks an assistant who holds a 1961 Latour in Switzerland, the answer exists."},
            {"h": "The kit for the room", "p": "Every page opens WhatsApp with the exact bottle already written, and tells the founder where the enquiry came from. Trade line sheets in four languages and two currencies, QR cards, a contact card, pages for sommeliers and a researched route of houses to visit in person."},
        ],
        "sig_lab": "Early signals",
        "sig_h": "The first searches arriving are the thesis, word for word.",
        "signals": ["The house went live on 12 September 2026 and Google is still indexing it. The first organic queries to find it were not generic. They were exact bottles and vintages:"],
        "queries": ["petrus 1946", "1985 sassicaia", "dom perignon 1960", "masseto 2023"],
        "deliverables": ["Positioning", "Naming rules", "Crest and heron", "Palette and type", "Website", "60 wine sheets",
                         "One page per vintage", "6 verticals", "Swiss city hubs", "Journal", "AI-readable inventory",
                         "WhatsApp with attribution", "Line sheets in 4 languages", "Sales route", "Weekly content agent"],
        "cta_h": "Selling something rare? It deserves a house, not a listing.",
        "cta_p": "Wine, watches, art or anything that is bought on trust: we build the brand, the digital house and the engine that brings the right buyers to it.",
        "cta_wa": "Hi, I read the Croian & Hein case and I'd like to talk about my project",
        "card_h": "Croian &amp; Hein: a private rare-wine house for Switzerland",
        "card_p": "From a trade price list to a luxury house in under 72 hours: identity, a 430+ page digital cellar, AI visibility and the kit to sell in person.",
        "card_meta": "Luxury &middot; Switzerland",
        "alt_txt": "Also in", "alt_link": "Spanish",
    },
    "es": {
        "title": "Croian & Hein: lanzamiento de una casa privada de vinos raros en Suiza | Caso ZENIA",
        "desc": "Cómo ZENIA convirtió una colección privada de más de 1.000 vinos raros en una casa de lujo para coleccionistas suizos: posicionamiento, identidad grabada, una bodega digital de más de 430 páginas, visibilidad en IA y el kit para vender en persona.",
        "kicker": ["Lujo y coleccionismo", "Suiza"],
        "h1": 'Hay botellas que nunca se venden. <span class="acc">Construimos la casa que las confía.</span>',
        "lede": "Croian &amp; Hein tiene la exclusiva para Suiza de una colección privada de más de 1.000 referencias, de 1815 a 2024, reunida durante toda una vida por un reputado enólogo que prefiere no ser nombrado. ZENIA la llevó de una lista de precios de gremio a una casa de lujo completa: posicionamiento, identidad, una casa digital pensada para coleccionistas, un buscador hecho con la propia bodega y el kit para venderla en persona.",
        "facts": [("client", "Croian &amp; Hein"), ("sector", "Vinos raros y coleccionismo"),
                  ("market", "Suiza &middot; EN FR DE IT"), ("scope", "Marca, web, SEO, visibilidad en IA, kit de venta"),
                  ("status", 'En vivo en <a href="https://croianhein.com" target="_blank" rel="noopener">croianhein.com</a>')],
        "stage_txt": {"alt": "Portada de Croian & Hein en escritorio", "alt_mob": "Portada de Croian & Hein en el móvil"},
        "nums_cap": "En cifras",
        "nums": [("&lt;72 h", "del primer briefing a la casa en vivo"), ("430+", "páginas generadas desde el inventario real"),
                 ("4", "idiomas para el mercado suizo"), ("1.000+", "referencias catalogadas, de 1815 a 2024")],
        "brief_lab": "El reto",
        "brief_h": "El activo era extraordinario. El mercado nunca había oído hablar de él.",
        "brief": ["La colección existía como una lista de precios de comerciante: abreviaturas de gremio, sin historias, sin marca. Pétrus 1946, una vertical completa de Sassicaia de 1968 a 2022, un Marsala del año de Waterloo, el primer rosado que sacó Roederer. Muchas de ellas, la última botella que queda.",
                  "Quien compra esto (coleccionistas, family offices, sumilleres de las mejores mesas de Berna, Ginebra y Zúrich) nunca compra de una lista. Compra confianza, procedencia y discreción. Y la fundadora volaba a Suiza pocos días después."],
        "rules": ["Sin precios públicos, en ningún sitio. Cada botella se cotiza a petición.",
                  "El propietario de la colección no se nombra nunca.",
                  "Tenía que parecer una casa de toda la vida, no una start-up.",
                  "El nombre debía quedar abierto a objetos más allá del vino."],
        "built_lab": "Lo que construimos",
        "built_h": "No una web. Una casa, lanzada de principio a fin.",
        "built_p": "Siete piezas diseñadas juntas y lanzadas como un solo lanzamiento.",
        "chapters": [
            {"h": "Posicionamiento", "p": "Una bodega privada que se abre con cita, sobre tres palabras: discreción, procedencia, colocación. Una frase lo sostiene todo: <strong>Hay botellas que nunca se venden. Se confían.</strong> Todo lo demás sale de ahí, incluido lo que la casa se niega a decir."},
            {"h": "Una identidad grabada", "p": "Un escudo con una garza dibujado íntegramente por código: óvalo doble perlado, garza rayada a buril, laureles anudados y el lema <em>Silentio et fide</em>. Cuatro combinaciones de color, una garza plana para tamaños pequeños y una paleta de marfil, negro universo, burdeos, verde vino y champán en Cormorant Garamond y Jost.",
             "v": {"type": "crest", "crest": "/cases/img/croian-crest.svg", "mark": "/cases/img/croian-mark.svg",
                   "alt": "Escudo grabado de Croian & Hein con la garza",
                   "palette": [("#F4EFE6", "#0B0A0C", "MARFIL"), ("#0B0A0C", "#B9A477", "UNIVERSO"), ("#5A1020", "#F4EFE6", "BURDEOS"),
                               ("#18352F", "#F4EFE6", "VERDE VINO"), ("#B9A477", "#0B0A0C", "CHAMPÁN")],
                   "cap": "El escudo, la garza y la paleta de la casa."}},
            {"h": "La casa digital", "p": "Una apertura a pantalla completa donde una botella ilustrada, dibujada por código, gira hacia la luz y revela su etiqueta. Después, la casa, el manifiesto, seis botellas que explican la bodega, la colección por regiones con una ficha para cada vino, la fundadora, la procedencia y una consulta privada. Sin scripts de terceros, cabeceras de seguridad estrictas y rápida en cualquier móvil.",
             "v": {"type": "pair", "items": [("/cases/img/croian-house.webp", "croianhein.com", "La sección de la casa"),
                                              ("/cases/img/croian-cellar.webp", "croianhein.com", "Seis botellas que explican la bodega")],
                   "cap": "La casa y seis botellas que explican la bodega."}},
            {"h": "La bodega como buscador", "p": "Un coleccionista no busca &laquo;vino raro&raquo;. Busca la botella y la añada exactas. Leímos la lista del propietario línea a línea y generamos una página por vino, una por cada añada en existencia y seis verticales completas, cada una con formato, botellas que quedan y estado traducido del argot del gremio. Cuatro portales suizos (Suiza, Ginebra, Zúrich, Lugano) resuelven entrega y aduana en su propio idioma.",
             "v": {"type": "pair", "items": [("/cases/img/croian-vintage.webp", "croianhein.com/cellar/petrus/1946", "Página de la añada Pétrus 1946"),
                                              ("/cases/img/croian-vertical.webp", "croianhein.com/verticals", "Vertical de Sassicaia de 1968 a 2022")],
                   "cap": "Una página por añada. Pétrus 1946 y la vertical de Sassicaia, de 1968 a 2022."}},
            {"h": "El Journal", "p": "Veintitrés artículos de fondo, más de 16.000 palabras, sobre lo que de verdad preguntan los coleccionistas en Suiza: importar vino, depósito aduanero, vender una bodega, niveles de llenado, procedencia. Las guías prácticas también en francés y alemán. Un agente semanal lee los datos reales de búsqueda y escribe el siguiente.",
             "v": {"type": "shot", "src": "/cases/img/croian-journal.webp", "domain": "croianhein.com/journal",
                   "alt": "Artículo del Journal sobre importar vino a Suiza", "cap": "Cuánto cuesta de verdad poner una botella en Suiza."}},
            {"h": "Legible por la IA", "p": "Todo el inventario está publicado en formato legible por máquinas (un mapa del sitio para modelos de lenguaje, la bodega completa en texto y JSON, datos de producto en unas 400 páginas) y 24 rastreadores de IA tienen la puerta abierta. Cuando alguien pregunta a un asistente quién tiene un Latour de 1961 en Suiza, la respuesta existe."},
            {"h": "El kit para la sala", "p": "Cada página abre WhatsApp con la botella exacta ya escrita y le dice a la fundadora de dónde viene la consulta. Hojas de oferta en cuatro idiomas y dos monedas, tarjetas con QR, tarjeta de contacto, páginas para sumilleres y una ruta investigada de casas para visitar en persona."},
        ],
        "sig_lab": "Primeras señales",
        "sig_h": "Las primeras búsquedas que llegan son la tesis, palabra por palabra.",
        "signals": ["La casa salió en vivo el 12 de septiembre de 2026 y Google todavía la está indexando. Las primeras búsquedas orgánicas que la encontraron no fueron genéricas. Fueron botellas y añadas exactas:"],
        "queries": ["petrus 1946", "1985 sassicaia", "dom perignon 1960", "masseto 2023"],
        "deliverables": ["Posicionamiento", "Reglas de nombre", "Escudo y garza", "Paleta y tipografía", "Web", "60 fichas de vino",
                         "Una página por añada", "6 verticales", "Portales por ciudad suiza", "Journal", "Inventario legible por IA",
                         "WhatsApp con atribución", "Hojas de oferta en 4 idiomas", "Ruta de venta", "Agente semanal de contenido"],
        "cta_h": "¿Vendes algo raro? Merece una casa, no un anuncio.",
        "cta_p": "Vino, relojes, arte o cualquier cosa que se compra por confianza: construimos la marca, la casa digital y el motor que le trae a los compradores correctos.",
        "cta_wa": "Hola, he leído el caso de Croian & Hein y quiero hablar de mi proyecto",
        "card_h": "Croian &amp; Hein: una casa privada de vinos raros para Suiza",
        "card_p": "De una lista de precios a una casa de lujo en menos de 72 horas: identidad, una bodega digital de más de 430 páginas, visibilidad en IA y el kit para vender en persona.",
        "card_meta": "Lujo &middot; Suiza",
        "alt_txt": "También en", "alt_link": "inglés",
    },
}

CICERO = {
    "client": "Cicero", "client_url": "https://thecicero.ai",
    "a1": "#E2C99A", "a2": "#C9A76B", "glow": "rgba(201,167,107,.13)",
    "logo": "/cases/img/cicero-mark.svg", "logo_w": 54, "logo_name": True,
    "og": "/cases/img/cicero-og.jpg", "next": "gwb",
    "url": {"en": "/cases/cicero-public-affairs-spain-italy.html", "es": "/es/caso-cicero.html"},
    "stage": {"type": "posters", "imgs": []},
    "card_img": "/cases/img/cicero-slide-1.webp",
    "en": {
        "title": "Cicero: taking an AI public-affairs platform to Spain and Italy | ZENIA case study",
        "desc": "ZENIA is Cicero's growth partner for Spain and Italy: market thesis, positioning per country, account intelligence, an outbound engine and a demo system for an AI regulatory-intelligence platform.",
        "kicker": ["Public affairs &amp; regulatory AI", "Spain &middot; Italy"],
        "h1": 'Anticipating a law is no longer a privilege of the largest firms. <span class="acc">We are taking that to Europe.</span>',
        "lede": "Cicero turns the work of a public-affairs firm into an AI engine with experts behind it: it tracks regulation, actors and risk, and delivers a daily brief with cited sources under the client's own brand. ZENIA is its growth partner for Spain and Italy. We design and run the full market entry, from the market thesis to booked demos.",
        "facts": [("client", '<a href="https://thecicero.ai" target="_blank" rel="noopener">Cicero</a>'),
                  ("sector", "Public affairs &amp; regulatory intelligence"), ("market", "Spain &middot; Italy"),
                  ("scope", "Positioning, account research, outbound, demo system"), ("status", "Phase 1 underway since September 2026")],
        "stage_txt": {"imgs": [("/cases/img/cicero-slide-1.webp", "Zenia and Cicero alliance announcement"),
                               ("/cases/img/cicero-slide-3.webp", "What Cicero brings to Europe")]},
        "nums_cap": "Week one",
        "nums": [("150", "accounts researched and scored"), ("75", "named decision-makers mapped"),
                 ("2", "markets localised end to end"), ("12", "objections mapped, each with its answer")],
        "brief_lab": "The brief",
        "brief_h": "A product that already works, entering two markets that don't know it yet.",
        "brief": ["Regulation in Europe moves on three levels at once: the Union, the state and the region. The firms that live from it (public-affairs consultancies, law firms, in-house regulatory teams, industry associations) buy on reputation and never from a cold pitch.",
                  "Cicero needed a partner on the ground who could open Spain and Italy with the right message for each, find the exact people who feel the problem, and do it without ever putting its own brand or domain at risk."],
        "rules": ["Every message that speaks for Cicero passes one approval round before the first campaign.",
                  "Outbound runs from a dedicated ZENIA domain, never from Cicero's.",
                  "Accounts Cicero already works are excluded before anyone is contacted."],
        "built_lab": "What we built",
        "built_h": "A market-entry engine, not a campaign.",
        "built_p": "Six modules, designed in the first week and run continuously from there.",
        "chapters": [
            {"h": "Market thesis &amp; ICP", "p": "Three buyer segments across Spain and Italy, qualification criteria, a precise definition of what counts as an originated client and an exclusions annex, so the engine never touches an account Cicero already works.",
             "v": {"type": "flow", "cap": "The engine, from market thesis to a booked demo.",
                   "steps": [("01", "Thesis", "Segments and exclusions per country"), ("02", "Message", "Positioning for the European regulatory frame"),
                             ("03", "Accounts", "Researched and scored, 150 at a time"), ("04", "Outbound", "Email and LinkedIn in four touches"),
                             ("05", "Demo", "Scripted, prepared 24 h before"), ("06", "Control", "Shared CRM and monthly report")]}},
            {"h": "Positioning per market", "p": "Messaging adapted to the European regulatory frame, one-pagers per segment and market pages in Spanish and Italian with attribution by channel."},
            {"h": "Account intelligence", "p": "150 accounts in the first week (consultancies, law firms, heads of public and regulatory affairs, associations) researched from lobbying registers, corporate sites, sector press and hiring signals, then scored and loaded into a shared CRM. 75 of them with a named decision-maker."},
            {"h": "Outbound engine", "p": "Four-touch sequences per segment in Spanish and Italian, by email and LinkedIn, with follow-ups at three, seven and fourteen days that stop the moment someone replies. Sent from a dedicated ZENIA domain."},
            {"h": "Demo system", "p": "A 30-minute demo script, answers to the twelve most frequent objections (price, &ldquo;we already have a firm&rdquo;, data, language, European sources) and a preparation sheet delivered 24 hours before every demo."},
            {"h": "Control", "p": "A shared CRM with the origin, channel and next step of every account, a monthly report by channel and country, and a review at day 45 and day 90. Next on the roadmap: an AI agent on WhatsApp and web that answers and qualifies in Spanish and Italian in under a minute."},
        ],
        "nums2_cap": "The platform we bring to Europe",
        "nums2": [("70+", "sources of evidence, monitored almost in real time"), ("900+", "actor profiles on a power and interest map"),
                  ("12", "regulatory sectors covered"), ("Daily", "regulatory brief with cited sources")],
        "sig_lab": "Status",
        "sig_h": "Phase 1 launched on 22 September 2026.",
        "signals": ["Week one is delivered: thesis, accounts, messages, market pages and the demo system. The first campaigns go live after Cicero's approval round.",
                    "Replies, demos and closed accounts will be published here as they happen. We don't publish estimates."],
        "deliverables": ["Market thesis", "ICP and exclusions", "Positioning ES and IT", "One-pagers per segment", "Market pages",
                         "150 scored accounts", "Shared CRM", "Outbound sequences", "Dedicated sending domain", "Demo script",
                         "12 objection answers", "Demo prep sheets", "Monthly reporting"],
        "cta_h": "Have a product that works? Let's open your next market.",
        "cta_p": "We act as the growth team on the ground: thesis, message, accounts, outbound and demos, run end to end in the market you want to enter.",
        "cta_wa": "Hi, I read the Cicero case and I'd like to talk about entering a new market",
        "card_h": "Cicero: taking an AI public-affairs platform to Spain and Italy",
        "card_p": "Growth partner on the ground: market thesis, 150 scored accounts in week one, outbound in two languages and a full demo system.",
        "card_meta": "Regulatory AI &middot; Spain &amp; Italy",
        "alt_txt": "Also in", "alt_link": "Spanish",
    },
    "es": {
        "title": "Cicero: llevar una plataforma de asuntos públicos con IA a España e Italia | Caso ZENIA",
        "desc": "ZENIA es el partner de crecimiento de Cicero para España e Italia: tesis de mercado, posicionamiento por país, inteligencia de cuentas, motor de outbound y sistema de demos para una plataforma de inteligencia regulatoria con IA.",
        "kicker": ["Asuntos públicos e IA regulatoria", "España &middot; Italia"],
        "h1": 'Anticiparse a una ley dejó de ser un privilegio de las grandes. <span class="acc">Lo estamos llevando a Europa.</span>',
        "lede": "Cicero convierte el trabajo de un despacho de asuntos públicos en un motor de IA con expertos detrás: sigue la regulación, a los actores y el riesgo, y entrega un reporte diario con fuentes citadas y la marca del cliente. ZENIA es su partner de crecimiento para España e Italia. Diseñamos y operamos la entrada al mercado completa, de la tesis a las demos agendadas.",
        "facts": [("client", '<a href="https://thecicero.ai" target="_blank" rel="noopener">Cicero</a>'),
                  ("sector", "Asuntos públicos e inteligencia regulatoria"), ("market", "España &middot; Italia"),
                  ("scope", "Posicionamiento, inteligencia de cuentas, outbound, sistema de demos"), ("status", "Fase 1 en marcha desde septiembre de 2026")],
        "stage_txt": {"imgs": [("/cases/img/cicero-slide-1.webp", "Anuncio de la alianza entre Zenia y Cicero"),
                               ("/cases/img/cicero-slide-3.webp", "Lo que llevamos a Europa con Cicero")]},
        "nums_cap": "Primera semana",
        "nums": [("150", "cuentas investigadas y puntuadas"), ("75", "decisores con nombre identificados"),
                 ("2", "mercados trabajados de principio a fin"), ("12", "objeciones mapeadas, cada una con su respuesta")],
        "brief_lab": "El reto",
        "brief_h": "Un producto que ya funciona, entrando en dos mercados que aún no lo conocen.",
        "brief": ["La regulación en Europa se mueve en tres niveles a la vez: la Unión, el Estado y la región. Quienes viven de ella (consultoras de asuntos públicos, despachos, equipos regulatorios internos, asociaciones sectoriales) compran por reputación y nunca por un mensaje en frío.",
                  "Cicero necesitaba un socio sobre el terreno capaz de abrir España e Italia con el mensaje justo para cada una, encontrar a las personas exactas que sienten el problema y hacerlo sin poner nunca en riesgo su marca ni su dominio."],
        "rules": ["Todo mensaje que habla en nombre de Cicero pasa una ronda de aprobación antes de la primera campaña.",
                  "El outbound sale de un dominio dedicado de ZENIA, nunca del de Cicero.",
                  "Las cuentas con las que Cicero ya trabaja se excluyen antes de contactar a nadie."],
        "built_lab": "Lo que construimos",
        "built_h": "Un motor de entrada al mercado, no una campaña.",
        "built_p": "Seis módulos, diseñados en la primera semana y operados de forma continua desde entonces.",
        "chapters": [
            {"h": "Tesis de mercado e ICP", "p": "Tres segmentos de comprador entre España e Italia, criterios de cualificación, una definición precisa de qué cuenta como cliente originado y un anexo de exclusiones, para que el motor nunca toque una cuenta con la que Cicero ya trabaja.",
             "v": {"type": "flow", "cap": "El motor, de la tesis de mercado a la demo agendada.",
                   "steps": [("01", "Tesis", "Segmentos y exclusiones por país"), ("02", "Mensaje", "Posicionamiento para el marco regulatorio europeo"),
                             ("03", "Cuentas", "Investigadas y puntuadas, de 150 en 150"), ("04", "Outbound", "Correo y LinkedIn en cuatro toques"),
                             ("05", "Demo", "Con guion y preparada 24 h antes"), ("06", "Control", "CRM compartido y reporte mensual")]}},
            {"h": "Posicionamiento por mercado", "p": "Mensajes adaptados al marco regulatorio europeo, one-pagers por segmento y páginas de mercado en español e italiano con atribución por canal."},
            {"h": "Inteligencia de cuentas", "p": "150 cuentas en la primera semana (consultoras, despachos, responsables de asuntos públicos y regulatorios, asociaciones) investigadas en registros de grupos de interés, webs corporativas, prensa sectorial y ofertas de empleo, puntuadas y cargadas en un CRM compartido. 75 de ellas con un decisor identificado por su nombre."},
            {"h": "Motor de outbound", "p": "Secuencias de cuatro toques por segmento en español e italiano, por correo y LinkedIn, con seguimientos a los tres, siete y catorce días que se detienen en cuanto alguien responde. Enviadas desde un dominio dedicado de ZENIA."},
            {"h": "Sistema de demos", "p": "Un guion de demo de 30 minutos, respuestas a las doce objeciones más frecuentes (precio, &laquo;ya tenemos despacho&raquo;, datos, idioma, fuentes europeas) y una ficha de preparación entregada 24 horas antes de cada demo."},
            {"h": "Control", "p": "Un CRM compartido con el origen, el canal y el siguiente paso de cada cuenta, un reporte mensual por canal y país y una revisión en el día 45 y en el día 90. Lo próximo en la hoja de ruta: un agente de IA en WhatsApp y web que responde y cualifica en español e italiano en menos de un minuto."},
        ],
        "nums2_cap": "La plataforma que llevamos a Europa",
        "nums2": [("70+", "fuentes de evidencia, monitorizadas casi en tiempo real"), ("900+", "perfiles de actor en un mapa de poder e interés"),
                  ("12", "sectores regulatorios cubiertos"), ("Diario", "reporte regulatorio con fuentes citadas")],
        "sig_lab": "Estado",
        "sig_h": "La Fase 1 arrancó el 22 de septiembre de 2026.",
        "signals": ["La primera semana está entregada: tesis, cuentas, mensajes, páginas de mercado y sistema de demos. Las primeras campañas salen tras la ronda de aprobación de Cicero.",
                    "Las respuestas, las demos y las cuentas cerradas se publicarán aquí a medida que ocurran. No publicamos estimaciones."],
        "deliverables": ["Tesis de mercado", "ICP y exclusiones", "Posicionamiento ES e IT", "One-pagers por segmento", "Páginas de mercado",
                         "150 cuentas puntuadas", "CRM compartido", "Secuencias de outbound", "Dominio de envío dedicado", "Guion de demo",
                         "Respuesta a 12 objeciones", "Fichas de preparación", "Reporte mensual"],
        "cta_h": "¿Tu producto ya funciona? Abramos tu siguiente mercado.",
        "cta_p": "Actuamos como tu equipo de crecimiento sobre el terreno: tesis, mensaje, cuentas, outbound y demos, operados de principio a fin en el mercado al que quieres entrar.",
        "cta_wa": "Hola, he leído el caso de Cicero y quiero hablar de entrar en un mercado nuevo",
        "card_h": "Cicero: llevar una plataforma de asuntos públicos con IA a España e Italia",
        "card_p": "Partner de crecimiento sobre el terreno: tesis de mercado, 150 cuentas puntuadas en la primera semana, outbound en dos idiomas y un sistema de demos completo.",
        "card_meta": "IA regulatoria &middot; España e Italia",
        "alt_txt": "También en", "alt_link": "inglés",
    },
}

VIDEO1 = {'src': '/cases/video/gwb-agente-247am.mp4', 'poster': '/cases/img/gwb-agente-poster.webp', 'date': '2026-09-04', 'dur': 'PT47S', 'lang': 'es'}
VIDEO2 = {'src': '/cases/video/gwb-network.mp4', 'poster': '/cases/img/gwb-network-poster.webp', 'date': '2026-09-26', 'dur': 'PT62S', 'lang': 'en'}

GWB = {
    "client": "Global Watch Buyers", "client_url": "https://globalwatchbuyers.com",
    "a1": "#EAD6A6", "a2": "#C4A15E", "glow": "rgba(196,161,94,.14)",
    "logo": "/cases/img/gwb-mark.svg", "logo_w": 54, "logo_name": True,
    "og": "/cases/img/gwb-og.jpg", "next": "ts",
    "url": {"en": "/cases/global-watch-buyers-ai-acquisition.html", "es": "/es/caso-global-watch-buyers.html"},
    "stage": {"type": "videos"},
    "card_img": "/cases/img/gwb-card.webp",
    "en": {
        "title": "Global Watch Buyers: luxury watch sellers from 33 countries, captured with AI | ZENIA case",
        "desc": "How ZENIA built the acquisition engine of Global Watch Buyers: sell pages by brand and city in 13 languages, WhatsApp with qualification, a lead panel by tier, ads that only bring sellers, ChatGPT visibility and GWB Network. With the videos of the case.",
        "kicker": ["Luxury watches", "33 countries", "Video"],
        "h1": 'Watch sellers from 33 countries. <span class="acc">Answered even at 2:47 a.m.</span>',
        "lede": "Global Watch Buyers buys luxury watches from private owners across Latin America, Europe and the United States. ZENIA built the whole system that brings those sellers in and sorts them: sell pages by brand and city, a direct line into WhatsApp with the watch already described, a panel that separates premium pieces from the rest and a private network to move watches by hand. Here are the videos and the numbers.",
        "facts": [("client", "Global Watch Buyers"), ("sector", "Luxury watch buying"),
                  ("market", "Latin America, Europe, US"), ("scope", "Website, WhatsApp acquisition, lead panel, Google Ads, AI visibility, GWB Network"),
                  ("status", 'Live at <a href="https://globalwatchbuyers.com" target="_blank" rel="noopener">globalwatchbuyers.com</a>')],
        "stage_txt": {"videos": [
            dict(VIDEO1, label="The flow, recreated: from a 2:47 a.m. message to a booked call",
                 note="The chat is a recreation (in Spanish). The figures at the end were the real ones on 4 September; today they are higher.",
                 name="2:47 a.m.: a watch seller answered while the team sleeps",
                 desc="Recreation of the WhatsApp acquisition flow ZENIA builds: a seller in London writes at 2:47 a.m., the piece is qualified and a call is booked."),
            dict(VIDEO2, label="Launch film of GWB Network, the private hand-carry network",
                 note="Membership by vouch, verified identity, a handover code on every run.",
                 name="GWB Network: know who is carrying your watch",
                 desc="Launch film of GWB Network, the private and verified hand-carry network for the watch trade built by ZENIA for Global Watch Buyers.")],
            "cta_wa": "Hi, I watched the Global Watch Buyers videos and want something like this for my business",
            "cta_btn": "I want this for my business"},
        "nums_cap": "In numbers (3 July to 18 October 2026)",
        "nums": [("831", "WhatsApp conversations started by sellers"), ("33", "countries they write from"),
                 ("10 of 12", "contacts from ads bring a premium watch"), ("$1.1", "per premium seller coming from ads")],
        "brief_lab": "The challenge",
        "brief_h": "The watches existed. The sellers did not know who to write to.",
        "brief": ["Someone who wants to sell a Rolex in Bogotá or a Cartier in Santiago is not looking for a brand. They want someone trustworthy who pays today, and they write when they can, often at night.",
                  "Global Watch Buyers needed to show up in exactly that search, in every city and in the seller's language, and turn each visit into a conversation with the piece already described, without wasting time on buyers or replicas."],
        "rules": ["We only buy: no ad may attract people who want to buy.", "Every contact measured end to end, from the search to the conversation.",
                  "The seller writes in their language, on the channel they already use: WhatsApp."],
        "built_lab": "What we built",
        "built_h": "A complete acquisition engine, not a website.",
        "built_p": "Six pieces that work together.",
        "chapters": [
            {"h": "Sell pages by brand and city", "p": "More than 2,900 pages in 13 languages: selling a Rolex in Bogotá, a Patek in Madrid or a Cartier in Lima, each with real market prices and a direct way into WhatsApp."},
            {"h": "WhatsApp with the watch already described", "p": "A direct button and a short form (model, year, condition, box and papers) that opens WhatsApp with the message already written. The buyer receives a qualified seller, not a bare &laquo;hi, info&raquo;."},
            {"h": "A lead panel by tier", "p": "Every conversation lands in a panel that separates premium watches (tier A) from the rest, alerts in real time and measures the ads: cost per seller, conversion and return."},
            {"h": "Ads that only bring sellers", "p": "Google Ads by premium brand in Bogotá, Santiago, Lima and Guayaquil, with an exclusion list that keeps out buyers and replica hunters. Result: 10 out of 12 contacts from ads bring a premium watch, at about $1.1 each."},
            {"h": "Visible in ChatGPT", "p": "Direct-answer guides, structured data and Bing indexing so AI search engines cite Global Watch Buyers. ChatGPT already sends visits every week and has brought real sellers."},
            {"h": "GWB Network", "p": "The trade's private network to move watches by hand: membership by vouch, verified identity, a handover code on every run and a permanent track record. We launched it with the film on this page."},
        ],
        "nums2_cap": "Reach",
        "nums2": [("2,900+", "sell pages and guides published"), ("13", "languages"), ("~20", "weekly visits coming from ChatGPT"), ("1,700+", "views of the GWB Network launch film")],
        "sig_lab": "What it means for you",
        "sig_h": "The same engine works for any business that lives on WhatsApp.",
        "signals": ["Workshops, clinics, real estate agencies or luxury stores: the problem is the same. The customer writes when they can and stays with whoever answers first.",
                    "On top of this engine we can add an AI agent that answers in seconds, qualifies and books, like in the recreated video. We design it for your business and connect it to the software you already use."],
        "deliverables": ["Website in 13 languages", "Pages by brand and city", "Qualification form", "WhatsApp with a written message", "Lead panel",
                         "Real-time alerts", "Google Ads", "Ad metrics", "AI visibility", "GWB Network", "Launch film", "Instagram content"],
        "cta_h": "Do your customers write at night? Make sure no one is left unanswered.",
        "cta_p": "In 30 minutes we show you what this engine would look like in your business, with your numbers.",
        "cta_wa": "Hi, I saw the Global Watch Buyers case and want something like this for my business",
        "card_h": "Global Watch Buyers: luxury watch sellers from 33 countries, captured with AI",
        "card_p": "831 WhatsApp conversations in three and a half months, pages in 13 languages, ads that only bring premium watches and GWB Network. With the videos of the case.",
        "card_meta": "Luxury watches &middot; 33 countries &middot; Video",
        "alt_txt": "Also in", "alt_link": "Spanish",
    },
    "es": {
        "title": "Global Watch Buyers: vendedores de relojes de lujo de 33 países, captados con IA | Caso ZENIA",
        "desc": "Cómo ZENIA construyó el motor de captación de Global Watch Buyers: páginas de venta por marca y ciudad en 13 idiomas, WhatsApp con cualificación, panel de leads por niveles, anuncios que solo traen vendedores, visibilidad en ChatGPT y GWB Network. Con los vídeos del caso.",
        "kicker": ["Relojes de lujo", "33 países", "Vídeo"],
        "h1": 'Vendedores de relojes de 33 países. <span class="acc">Atendidos aunque sean las 2:47 de la madrugada.</span>',
        "lede": "Global Watch Buyers compra relojes de lujo a particulares de Latinoamérica, Europa y Estados Unidos. ZENIA construyó todo el sistema que los trae y los ordena: páginas de venta por marca y ciudad, entrada directa a WhatsApp con el reloj ya descrito, un panel que separa las piezas premium del resto y una red privada para mover relojes en mano. Estos son los vídeos y las cifras.",
        "facts": [("client", "Global Watch Buyers"), ("sector", "Compra de relojes de lujo"),
                  ("market", "Latinoamérica, Europa y EE. UU."), ("scope", "Web, captación por WhatsApp, panel de leads, Google Ads, visibilidad en IA, GWB Network"),
                  ("status", 'En vivo en <a href="https://globalwatchbuyers.com" target="_blank" rel="noopener">globalwatchbuyers.com</a>')],
        "stage_txt": {"videos": [
            dict(VIDEO1, label="El flujo, recreado: de un mensaje a las 2:47 a la llamada agendada",
                 note="El chat es una recreación. Las cifras del final eran las reales del 4 de septiembre; hoy son más.",
                 name="Las 2:47 de la madrugada: un vendedor de relojes atendido mientras el equipo duerme",
                 desc="Recreación del flujo de captación por WhatsApp que construye ZENIA: un vendedor en Londres escribe a las 2:47, se cualifica la pieza y queda agendada la llamada."),
            dict(VIDEO2, label="Vídeo de lanzamiento de GWB Network, la red privada de transporte en mano",
                 note="Miembros por aval, identidad verificada y un código de entrega en cada transporte. En inglés.",
                 name="GWB Network: sabe quién lleva tu reloj",
                 desc="Vídeo de lanzamiento de GWB Network, la red privada y verificada de transporte en mano para el gremio de relojes, construida por ZENIA para Global Watch Buyers.")],
            "cta_wa": "Hola, he visto los vídeos de Global Watch Buyers y quiero algo así para mi negocio",
            "cta_btn": "Quiero esto para mi negocio"},
        "nums_cap": "En cifras (3 de julio a 18 de octubre de 2026)",
        "nums": [("831", "conversaciones de WhatsApp iniciadas por vendedores"), ("33", "países desde los que escriben"),
                 ("10 de 12", "contactos que llegan por anuncios traen un reloj premium"), ("1,1 $", "por cada vendedor premium que llega por anuncios")],
        "brief_lab": "El reto",
        "brief_h": "Los relojes existían. Los vendedores no sabían a quién escribir.",
        "brief": ["Quien quiere vender un Rolex en Bogotá o un Cartier en Santiago no busca una marca: busca a alguien de confianza que le pague hoy. Y escribe cuando puede, muchas veces de noche.",
                  "Global Watch Buyers necesitaba aparecer justo en esa búsqueda, en cada ciudad y en el idioma del vendedor, y convertir cada visita en una conversación con la pieza ya descrita, sin perder tiempo con compradores ni con réplicas."],
        "rules": ["Solo compramos: ningún anuncio puede atraer a quien quiere comprar.", "Cada contacto, medido de principio a fin: de la búsqueda a la conversación.",
                  "El vendedor escribe en su idioma y en el canal que ya usa: WhatsApp."],
        "built_lab": "Lo que construimos",
        "built_h": "Un motor de captación completo, no una web.",
        "built_p": "Seis piezas que trabajan juntas.",
        "chapters": [
            {"h": "Páginas de venta por marca y ciudad", "p": "Más de 2.900 páginas en 13 idiomas: vender un Rolex en Bogotá, un Patek en Madrid o un Cartier en Lima, cada una con precios de mercado reales y una salida directa a WhatsApp."},
            {"h": "WhatsApp con el reloj ya descrito", "p": "Un botón directo y un formulario corto (modelo, año, estado, caja y papeles) que abre WhatsApp con el mensaje ya escrito. Quien compra recibe al vendedor cualificado, no un &laquo;hola, info&raquo;."},
            {"h": "Panel de leads por niveles", "p": "Cada conversación entra en un panel que separa los relojes premium (Nivel A) del resto, avisa al momento y mide los anuncios: coste por vendedor, conversión y retorno."},
            {"h": "Anuncios que solo traen vendedores", "p": "Google Ads por marca premium en Bogotá, Santiago, Lima y Guayaquil, con una lista de exclusiones que deja fuera a quien busca comprar o réplicas. Resultado: 10 de cada 12 contactos de anuncios traen un reloj premium, a unos 1,1 $ cada uno."},
            {"h": "Visible en ChatGPT", "p": "Guías de respuesta directa, datos estructurados e indexación en Bing para que los buscadores de IA citen a Global Watch Buyers. ChatGPT ya envía visitas cada semana y ha traído vendedores reales."},
            {"h": "GWB Network", "p": "La red privada del gremio para mover relojes en mano: miembros por aval, identidad verificada, un código de entrega en cada transporte e historial permanente. La lanzamos con el vídeo de esta página."},
        ],
        "nums2_cap": "Alcance",
        "nums2": [("2.900+", "páginas de venta y guías publicadas"), ("13", "idiomas"), ("~20", "visitas a la semana que llegan desde ChatGPT"), ("1.700+", "reproducciones del vídeo de lanzamiento de GWB Network")],
        "sig_lab": "Qué significa para ti",
        "sig_h": "El mismo motor sirve para cualquier negocio que vive de WhatsApp.",
        "signals": ["Talleres, clínicas, inmobiliarias o tiendas de lujo: el problema es el mismo. El cliente escribe cuando puede y se queda con quien contesta primero.",
                    "Encima de este motor podemos poner un agente de IA que conteste en segundos, cualifique y agende, como en la recreación del vídeo. Lo diseñamos a la medida de tu negocio y lo conectamos al programa que ya usas."],
        "deliverables": ["Web en 13 idiomas", "Páginas por marca y ciudad", "Formulario de cualificación", "WhatsApp con mensaje redactado", "Panel de leads",
                         "Avisos en tiempo real", "Google Ads", "Métricas de anuncios", "Visibilidad en IA", "GWB Network", "Vídeo de lanzamiento", "Contenido para Instagram"],
        "cta_h": "¿Tus clientes escriben de noche? Que nadie se quede sin respuesta.",
        "cta_p": "En 30 minutos te enseñamos cómo quedaría este motor en tu negocio, con tus números.",
        "cta_wa": "Hola, he visto el caso de Global Watch Buyers y quiero algo así para mi negocio",
        "card_h": "Global Watch Buyers: vendedores de relojes de lujo de 33 países, captados con IA",
        "card_p": "831 conversaciones de WhatsApp en tres meses y medio, páginas en 13 idiomas, anuncios que solo traen relojes premium y GWB Network. Con los vídeos del caso.",
        "card_meta": "Relojes de lujo &middot; 33 países &middot; Vídeo",
        "alt_txt": "También en", "alt_link": "inglés",
    },
}

STEPS_ES = [('01', 'Referencia', 'El equipo la manda por WhatsApp'), ('02', 'Ficha', 'Variante, material y tamaño verificados'), ('03', 'Fotos', '8 fotos revisadas por visión artificial'), ('04', 'Precio', 'Calculado con las reglas de la casa'), ('05', 'Preview', 'Se corrige todo por chat'), ('06', 'eBay', 'Publicado tras el «sí» del equipo')]
STEPS_EN = [('01', 'Reference', 'The team sends it on WhatsApp'), ('02', 'Specs', 'Variant, material and size verified'), ('03', 'Photos', '8 photos checked by computer vision'), ('04', 'Price', 'Set by the house rules'), ('05', 'Preview', 'Everything fixed by chat'), ('06', 'eBay', 'Live after the team says yes')]

TS = {
    "client": "Throwin' Salt", "client_url": "https://throwinsalt.com",
    "a1": "#E8D9B5", "a2": "#BFA06A", "glow": "rgba(191,160,106,.13)",
    "logo": "/cases/img/ts-mark.png", "logo_w": 71, "logo_name": True,
    "og": "/cases/img/ts-og.jpg", "next": "croian",
    "url": {"en": "/cases/throwin-salt-gaia-ebay-whatsapp.html", "es": "/es/caso-throwin-salt-gaia.html"},
    "stage": {"type": "posters", "imgs": []},
    "card_img": "/cases/img/ts-card.webp",
    "en": {
        "title": "Throwin' Salt: 54 luxury watches listed on eBay from WhatsApp | ZENIA case",
        "desc": "Phase 1 of Gaia, the AI agent of Throwin' Salt: it replaced InkFrog and lists luxury watches on eBay from WhatsApp, with photos checked by computer vision, verified specs and a daily batch ready to approve.",
        "kicker": ["Luxury watches", "eBay", "Phase 1"],
        "h1": 'From a WhatsApp message to a live eBay listing. <span class="acc">Without opening a single dashboard.</span>',
        "lede": "Throwin' Salt sells high-end watches on eBay. Until August 2026 every listing was built by hand in InkFrog, a tool that was also shutting down. ZENIA built Gaia, an AI agent that lives in the team's WhatsApp: it prepares each listing with title, specs, photos and price, enforces the house rules and publishes on eBay when the team says &laquo;publish&raquo;. This is phase 1.",
        "facts": [("client", "Throwin' Salt"), ("sector", "Luxury watch retail"), ("market", "United States &middot; eBay"),
                  ("scope", "WhatsApp AI agent, eBay publishing, computer-vision photo checks, daily batch"),
                  ("status", "Phase 1 in production since August 2026")],
        "stage_txt": {"imgs": [("/cases/img/ts-gaia-chat.webp", "Recreation of the team's WhatsApp chat with Gaia"),
                               ("/cases/img/ts-gaia-lote.webp", "The daily batch: Full Set watches with 8 checked photos")]},
        "nums_cap": "Phase 1 in numbers (20 August to 17 September 2026)",
        "nums": [("54", "luxury watches listed on eBay from the chat"), ("23", "watches listed in a single day"),
                 ("$2M", "of inventory listed, about $38,000 on average"), ("8", "photos per listing, each one checked by computer vision")],
        "brief_lab": "The challenge",
        "brief_h": "Listing a $40,000 watch cannot depend on filling in forms by hand.",
        "brief": ["Every fine-watch listing needs the same things: the exact reference with its variant, the right material and size, eight photos in the house order and a price that is not off by a zero. Doing it by hand in InkFrog took hours, and a wrong spec meant deleting the listing.",
                  "On top of that, InkFrog was shutting down. Throwin' Salt needed a faster way to list, with fewer mistakes, without changing how the team already works: on WhatsApp."],
        "rules": ["Never a wrong reference: same variant, correct material and size.", "No hands or wrists in the photos, and always the brand's official box on Full Set listings.",
                  "Never list a reference twice.", "Nothing goes live without the team's yes."],
        "built_lab": "What we built",
        "built_h": "An agent that works inside the team's WhatsApp.",
        "built_p": "Five pieces, one conversation.",
        "chapters": [
            {"h": "Gaia, the WhatsApp agent", "p": "The team writes to it like a colleague: sends references or photos, asks for a price change or says &laquo;publish&raquo;. Gaia answers in seconds, shows a preview of each listing and fixes it by chat. It speaks Spanish and understands voice notes."},
            {"h": "From the chat to eBay, without InkFrog", "p": "Gaia builds each listing with an optimised title, full specs, condition, eight photos in the house order and a price, and publishes it on eBay. It also edits or ends live listings, from the same chat.",
             "v": {"type": "flow", "cap": "From the reference to the live listing, in one conversation.", "steps": STEPS_EN}},
            {"h": "Photos checked by computer vision", "p": "Every photo goes through a vision model before it reaches the listing: no hands or wrists, no boxes that are not the brand's, and Full Set confirmed by looking at the photos themselves. The team stopped hunting mistakes by eye."},
            {"h": "A daily batch ready to approve", "p": "Every morning Gaia proposes a batch of new watches, all Full Set, with the exact reference, eight photos and a calculated price, never repeating anything already listed. The team removes, corrects and publishes from the chat."},
            {"h": "Control of what is listed", "p": "A record of every listing (who asked for it, when, at what price) and a private panel of everything listed, to follow the business and the accounts."},
        ],
        "sig_lab": "Next phase",
        "sig_h": "Phase 1 solved listing. Phase 2 is about selling more.",
        "signals": ["With listing solved, the focus moves to a wider catalogue of available references, tiered pricing and taking the same agent to Instagram and Facebook.",
                    "The same pattern works for any business with a catalogue: an agent in the team's WhatsApp that turns messages into live listings, without touching a dashboard."],
        "deliverables": ["WhatsApp AI agent", "eBay publishing", "Edit and end by chat", "Preview of every listing", "Computer-vision photo checks",
                         "Automated house rules", "Daily batch", "Listing record", "Private panel", "Team manual"],
        "cta_h": "Is your team still listing by hand? Let an agent do it.",
        "cta_p": "In 30 minutes we show you what an agent like this would look like for your catalogue, on eBay, your website or any marketplace.",
        "cta_wa": "Hi, I saw the Throwin' Salt case and want an agent like this for my business",
        "card_h": "Throwin' Salt: luxury watches listed on eBay from WhatsApp",
        "card_p": "Phase 1 of Gaia: 54 watches listed in four weeks, up to 23 in one day, with photos checked by computer vision and no dashboards.",
        "card_meta": "Luxury watches &middot; eBay &middot; Phase 1",
        "alt_txt": "Also in", "alt_link": "Spanish",
    },
    "es": {
        "title": "Throwin' Salt: 54 relojes de lujo publicados en eBay desde WhatsApp | Caso ZENIA",
        "desc": "Fase 1 de Gaia, el agente de IA de Throwin' Salt: sustituyó a InkFrog y publica relojes de lujo en eBay desde WhatsApp, con fotos revisadas por visión artificial, specs verificadas y un lote diario listo para aprobar.",
        "kicker": ["Relojes de lujo", "eBay", "Fase 1"],
        "h1": 'De un mensaje de WhatsApp a un anuncio en eBay. <span class="acc">Sin abrir ningún panel.</span>',
        "lede": "Throwin' Salt vende relojes de alta gama en eBay. Hasta agosto de 2026, cada anuncio se montaba a mano en InkFrog, una herramienta que además cerraba. ZENIA construyó Gaia, un agente de IA que vive en el WhatsApp del equipo: prepara cada anuncio con título, especificaciones, fotos y precio, aplica las reglas de la casa y lo publica en eBay cuando el equipo dice &laquo;publica&raquo;. Esta es la fase 1.",
        "facts": [("client", "Throwin' Salt"), ("sector", "Venta de relojes de lujo"), ("market", "Estados Unidos &middot; eBay"),
                  ("scope", "Agente de IA en WhatsApp, publicación en eBay, revisión de fotos con visión artificial, lote diario"),
                  ("status", "Fase 1 en producción desde agosto de 2026")],
        "stage_txt": {"imgs": [("/cases/img/ts-gaia-chat.webp", "Recreación del chat del equipo con Gaia en WhatsApp"),
                               ("/cases/img/ts-gaia-lote.webp", "El lote diario: relojes Full Set con 8 fotos revisadas")]},
        "nums_cap": "La fase 1 en cifras (20 de agosto a 17 de septiembre de 2026)",
        "nums": [("54", "relojes de lujo publicados en eBay desde el chat"), ("23", "relojes publicados en un solo día"),
                 ("2 M$", "de inventario publicado, a unos 38.000 $ de media"), ("8", "fotos por anuncio, revisadas una a una por visión artificial")],
        "brief_lab": "El reto",
        "brief_h": "Publicar un reloj de 40.000 $ no puede depender de rellenar formularios a mano.",
        "brief": ["Cada anuncio de alta relojería exige lo mismo: la referencia exacta con su variante, el material y el tamaño correctos, ocho fotos en el orden de la casa y un precio que no se equivoque por un cero. Hacerlo a mano en InkFrog llevaba horas, y un error en las specs obligaba a borrar el anuncio.",
                  "Además, InkFrog cerraba. Throwin' Salt necesitaba otra forma de publicar, más rápida y con menos errores, sin cambiar la manera en que el equipo ya trabaja: por WhatsApp."],
        "rules": ["Nunca un error de referencia: misma variante, con material y tamaño correctos.", "Nada de manos ni muñecas en las fotos, y siempre la caja oficial de la marca en los Full Set.",
                  "Nunca repetir una referencia ya publicada.", "Nada sale en vivo sin el «sí» del equipo."],
        "built_lab": "Lo que construimos",
        "built_h": "Un agente que trabaja dentro del WhatsApp del equipo.",
        "built_p": "Cinco piezas, una sola conversación.",
        "chapters": [
            {"h": "Gaia, el agente de WhatsApp", "p": "El equipo le escribe como a un compañero: manda referencias o fotos, pide un cambio de precio o dice &laquo;publica&raquo;. Gaia contesta en segundos, enseña un preview de cada anuncio y lo corrige por chat. Habla en español y entiende audios."},
            {"h": "Del chat a eBay, sin InkFrog", "p": "Gaia monta cada anuncio con título optimizado, especificaciones completas, condición, ocho fotos en el orden de la casa y precio, y lo publica en eBay. También edita o retira lo que ya está en vivo, desde el mismo chat.",
             "v": {"type": "flow", "cap": "De la referencia al anuncio en vivo, en una sola conversación.", "steps": STEPS_ES}},
            {"h": "Fotos revisadas por visión artificial", "p": "Cada foto pasa por un modelo de visión antes de llegar al anuncio: fuera manos y muñecas, fuera cajas que no son de la marca y el Full Set confirmado mirando las propias fotos. El equipo dejó de cazar errores a ojo."},
            {"h": "Un lote diario listo para aprobar", "p": "Cada mañana Gaia propone un lote de relojes nuevos, todos Full Set, con la referencia exacta, ocho fotos y el precio calculado, sin repetir nada de lo ya publicado. El equipo quita, corrige y publica desde el chat."},
            {"h": "Control de lo publicado", "p": "Un registro de cada anuncio (quién lo pidió, cuándo y a qué precio) y un panel privado de todo lo publicado, para seguir el negocio y las cuentas."},
        ],
        "sig_lab": "Siguiente fase",
        "sig_h": "La fase 1 resolvió publicar. La fase 2 va a por vender más.",
        "signals": ["Con la publicación resuelta, el foco pasa a ampliar el catálogo de referencias disponibles, afinar los precios por tramos y llevar el mismo agente a Instagram y Facebook.",
                    "El mismo patrón sirve para cualquier negocio con catálogo: un agente en el WhatsApp del equipo que convierte mensajes en anuncios publicados, sin tocar ningún panel."],
        "deliverables": ["Agente de IA en WhatsApp", "Publicación en eBay", "Edición y retirada por chat", "Preview de cada anuncio", "Revisión de fotos con visión artificial",
                         "Reglas de la casa automatizadas", "Lote diario", "Registro de publicaciones", "Panel privado", "Manual del equipo"],
        "cta_h": "¿Tu equipo sigue publicando a mano? Que lo haga un agente.",
        "cta_p": "En 30 minutos te enseñamos cómo quedaría un agente así para tu catálogo, sea en eBay, en tu web o en cualquier marketplace.",
        "cta_wa": "Hola, he visto el caso de Throwin' Salt y quiero un agente así para mi negocio",
        "card_h": "Throwin' Salt: relojes de lujo publicados en eBay desde WhatsApp",
        "card_p": "Fase 1 de Gaia: 54 relojes publicados en cuatro semanas, hasta 23 en un día, con fotos revisadas por visión artificial y sin abrir ningún panel.",
        "card_meta": "Relojes de lujo &middot; eBay &middot; Fase 1",
        "alt_txt": "También en", "alt_link": "inglés",
    },
}

CASES = {"croian": CROIAN, "cicero": CICERO, "gwb": GWB, "ts": TS}

# Casos anteriores que se listan en los índices (solo los verificados).
OLDER = {
    "en": [("/cases/boutique-law-firm-latam.html", "Legal &middot; Spain &harr; LATAM", "AI acquisition system for a boutique law firm"),
           ("/cases/whatsapp-bookkeeping-importer.html", "Trade &middot; United States", "WhatsApp-native bookkeeping AI for an importer"),
           ("/cases/ecommerce-usa.html", "Luxury ecommerce &middot; United States", "AI customer agent for a US luxury ecommerce brand"),
           ("/cases/personal-brand-content.html", "Personal brand &middot; United States", "AI content engine for a personal brand")],
    "es": [("/es/caso-despacho-boutique.html", "Legal &middot; España &harr; LATAM", "Sistema de captación con IA para un despacho boutique"),
           ],
}

HUB = {
    "en": {"url": "/cases/", "file": "cases/index.html", "alt": "/es/casos.html",
           "title": "Case studies: what ZENIA has built | ZENIA",
           "desc": "Selected work by ZENIA: brands, digital houses, acquisition systems and market-entry engines built with AI for companies in Europe and the Americas.",
           "kick": "Selected work", "h1": 'What we build, <span class="acc">shown in full.</span>',
           "lede": "Every case here is real and every number is measured. We show what we built, how it works and, when they exist, the results.",
           "more": "More work"},
    "es": {"url": "/es/casos.html", "file": "es/casos.html", "alt": "/cases/",
           "title": "Casos de éxito: lo que ha construido ZENIA | ZENIA",
           "desc": "Trabajos seleccionados de ZENIA: marcas, casas digitales, sistemas de captación y motores de entrada al mercado construidos con IA para empresas de Europa y América.",
           "kick": "Trabajos seleccionados", "h1": 'Lo que construimos, <span class="acc">enseñado entero.</span>',
           "lede": "Cada caso es real y cada cifra está medida. Enseñamos lo que construimos, cómo funciona y, cuando existen, los resultados.",
           "more": "Más trabajos"},
}


def hub(lang):
    h = HUB[lang]
    u = UI[lang]
    other = "es" if lang == "en" else "en"
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": h["title"], "description": h["desc"],
          "url": SITE + h["url"], "inLanguage": lang}
    out = [head(lang, h["title"], h["desc"], h["url"], CROIAN["og"], other, h["alt"], ld)]
    out.append('<body style="--a1:#8FB4FF;--a2:#8B5CF6;--glow:rgba(59,130,246,.10)">')
    out.append(nav(lang))
    cards = ""
    for k in ("gwb", "ts", "croian", "cicero"):
        c = CASES[k]
        t = c[lang]
        feat = ' class="feat"' if k in ("gwb", "ts") else ""
        cards += (f'<a href="{c["url"][lang]}"{feat}><div class="card-img"><img src="{c["card_img"]}" alt="{e(c["client"])}" loading="lazy"></div>'
                  f'<div class="meta">{t["card_meta"]}</div><h3>{t["card_h"]}</h3><p>{t["card_p"]}</p>'
                  f'<span class="go" style="color:{c["a1"]}">{"Read the case" if lang == "en" else "Leer el caso"} &rarr;</span></a>')
    rows = "".join(f'<a href="{href}"><small>{meta}</small><strong>{title}</strong><em>&rarr;</em></a>' for href, meta, title in OLDER[lang])
    out.append(f"""<header class="hero"><div class="wrap"><div class="kicker"><b>{h['kick']}</b></div>
<h1 style="margin-top:36px">{h['h1']}</h1><p class="lede">{h['lede']}</p>
<div class="cards">{cards}</div>
<div class="list">{rows}</div></div></header>""")
    out.append(f"""<section class="cta"><div class="wrap"><h2>{"Your company could be the next case." if lang == "en" else "Tu empresa puede ser el próximo caso."}</h2>
<div class="btns"><a class="btn btn-p" href="{wa('Hi, I saw your case studies and want to talk' if lang == 'en' else 'Hola, he visto vuestros casos y quiero hablar')}" target="_blank" rel="noopener">{u['wa_btn']}</a>
<a class="btn btn-s" href="{CAL}" target="_blank" rel="noopener">{u['cal_btn']}</a></div></div></section>""")
    out.append(foot(lang))
    out.append(TAIL.format(wa=wa("Hola, he visto vuestros casos" if lang == "es" else "Hi, I saw your case studies")))
    out.append("</body>\n</html>\n")
    return "\n".join(out)


def main():
    escritos = []
    for c in CASES.values():
        for lang in ("en", "es"):
            ruta = os.path.join(ROOT, c["url"][lang].lstrip("/"))
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(page(c, lang))
            escritos.append(c["url"][lang])
    for lang in ("en", "es"):
        with open(os.path.join(ROOT, HUB[lang]["file"]), "w", encoding="utf-8") as f:
            f.write(hub(lang))
        escritos.append(HUB[lang]["url"])
    print("\n".join(escritos))


if __name__ == "__main__":
    main()
