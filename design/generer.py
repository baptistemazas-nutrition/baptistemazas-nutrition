import pathlib, re
from playwright.sync_api import sync_playwright

ICI = pathlib.Path(__file__).resolve().parent
ASSETS = ICI.parent / "assets"
BUILD = ICI / "build"
CHROME = "/usr/bin/google-chrome"
NB, FINE = " ", " "


def ico(nom, taille=22, trait=1.8):
    s = re.sub(r"<!--.*?-->", "", (ICI / f"{nom}.svg").read_text(encoding="utf-8"), flags=re.S)
    s = s.replace('width="24"', f'width="{taille}"').replace('height="24"', f'height="{taille}"')
    return s.replace('stroke-width="2"', f'stroke-width="{trait}"')


def police(f):
    return (ICI / f).as_uri()


CSS = f"""
@font-face {{ font-family: Cormorant; src: url({police('cormorant-garamond-latin-600-normal.woff2')}); font-weight: 600; }}
@font-face {{ font-family: Cormorant; src: url({police('cormorant-garamond-latin-700-normal.woff2')}); font-weight: 700; }}
@font-face {{ font-family: Cormorant; src: url({police('cormorant-garamond-latin-500-italic.woff2')}); font-weight: 500; font-style: italic; }}
:root {{ --encre:#1B2333; --texte:#4A5363; --doux:#6F7785; --vert:#2E5A43; --vert2:#467F61; --or:#B88A4E; --ivoire:#FFFDF9;
        --bord:#EADFCF; --ciel:#DCE3EC; --peche:#F6E6D3; --vertpale:#E6EFE8; --titre:#1B2333; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ background:transparent; font-family:Inter, system-ui, sans-serif; -webkit-font-smoothing:antialiased; color:var(--encre); }}
#c {{ display:inline-block; }}
.marge {{ padding:20px; }}
.carte {{ position:relative; overflow:hidden; background:var(--ivoire); border:1px solid var(--bord); border-radius:22px;
          box-shadow:0 10px 18px -8px rgba(27,35,51,.16), 0 2px 6px rgba(27,35,51,.05); }}
.lueur {{ background:radial-gradient(380px 260px at 100% 0%, rgba(243,214,178,.62) 0%, rgba(243,214,178,0) 72%), var(--ivoire); }}
.badge {{ width:46px; height:46px; border-radius:15px; display:grid; place-items:center; color:#fff; flex:none;
          background:linear-gradient(140deg, var(--vert) 0%, var(--vert2) 100%); box-shadow:0 6px 14px rgba(46,90,67,.28); }}
.tag {{ font:600 11px/1 Inter; letter-spacing:.11em; text-transform:uppercase; color:var(--or); }}
.titre {{ font:700 36px/1.02 Cormorant; color:var(--encre); letter-spacing:.2px; }}
.accroche {{ font:italic 500 21px/1.28 Cormorant; color:var(--vert); }}
.desc {{ font:400 14px/1.55 Inter; color:var(--texte); }}
.puces {{ display:flex; flex-wrap:wrap; gap:7px; }}
.puce {{ display:inline-flex; align-items:center; gap:6px; padding:6px 11px; border-radius:999px; background:var(--vertpale);
         color:var(--vert); font:600 12px/1 Inter; white-space:nowrap; }}
.puce.or {{ background:var(--peche); color:#8A6332; }}
.puce svg {{ width:13px; height:13px; }}
.cta {{ display:inline-flex; align-items:center; gap:7px; font:600 14px/1 Inter; color:var(--vert); white-space:nowrap; }}
.cta.plein {{ background:var(--vert); color:#fff; padding:11px 18px; border-radius:999px; box-shadow:0 6px 14px rgba(46,90,67,.25); }}
.cta svg {{ width:16px; height:16px; }}
"""


def page(corps, extra=""):
    return f"<!doctype html><html lang='fr'><head><meta charset='utf-8'><style>{CSS}{extra}</style></head><body>{corps}</body></html>"


def carte_profil():
    b = (ICI / "banniere-linkedin.png").as_uri()
    css = """.profil img { display:block; width:100%; height:auto; }
    .identite { display:flex; justify-content:space-between; align-items:flex-start; padding:22px 30px 26px; }
    .nom { font:700 42px/1 Cormorant; } .filet { width:46px; height:2px; border-radius:2px; background:var(--or); margin:14px 0 13px; }
    .l1 { font:500 14.5px/1.5 Inter; color:var(--encre); } .l2 { font:400 13.5px/1.5 Inter; color:var(--texte); }"""
    corps = f"""<div id="c" class="marge"><div class="carte profil" style="width:880px">
      <img src="{b}">
      <div class="identite"><div>
        <div class="nom">Dr Baptiste Mazas</div><div class="filet"></div>
        <div class="l1">Médecin AP-HP · Diabétologie · Nutrition · Prévention cardiométabolique · Médecine du sport</div>
        <div class="l2">Chercheur NutriOmics (Inserm / Sorbonne Université) · Données de santé &amp; IA</div></div>
        <span class="puce" style="margin-top:6px">{ico('map-pin', 13, 2.2)}Paris</span></div></div></div>"""
    return page(corps, css)


def bouton(libelle, icone, externe):
    css = """.bt { display:inline-flex; align-items:center; gap:9px; height:42px; padding:0 18px 0 15px; border-radius:999px;
      background:var(--ivoire); border:1px solid var(--bord); box-shadow:0 4px 10px -4px rgba(27,35,51,.2); font:600 14.5px/1 Inter; }
      .bt .i { color:var(--vert); display:flex; } .bt .f { color:var(--or); display:flex; }"""
    fleche = f"<span class='f'>{ico('arrow-up-right', 15, 2.2)}</span>" if externe else ""
    return page(f"<div id='c' style='padding:10px'><div class='bt'><span class='i'>{ico(icone, 18, 2)}</span>{libelle}{fleche}</div></div>", css)


def titre(texte, icone, sombre):
    css = f""":root {{ --titre:{'#F1EBE2' if sombre else '#1B2333'}; }}
      .ts {{ display:flex; align-items:center; gap:15px; width:920px; padding:26px 20px 8px; }}
      .ts .badge {{ width:40px; height:40px; border-radius:13px; box-shadow:none; }}
      .ts .t {{ font:700 32px/1 Cormorant; color:var(--titre); white-space:nowrap; }}
      .ts .l {{ flex:1; height:1.5px; margin:6px 0 0 6px; background:linear-gradient(90deg, var(--or), rgba(184,138,78,0)); }}"""
    return page(f"<div id='c'><div class='ts'><div class='badge'>{ico(icone, 20, 1.9)}</div><div class='t'>{texte}</div><div class='l'></div></div></div>", css)


CSS_LARGE = """.large { display:flex; } .large .txt { flex:1; padding:28px 28px 26px 32px; display:flex; flex-direction:column; gap:11px; }
  .large .vis { width:300px; flex:none; position:relative;
    background:linear-gradient(170deg, #DCE3EC 0%, #EEE4D8 58%, #F6E2C9 100%); border-left:1px solid var(--bord); }
  .large .bas { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-top:auto; }
  .large .accroche { font-size:19.5px; }"""


def carte_veille():
    css = CSS_LARGE + """
  .mini { position:absolute; width:190px; padding:13px 14px; border-radius:14px; background:#fff; border:1px solid #E8E1D6;
          box-shadow:0 8px 18px rgba(27,35,51,.10); display:flex; gap:11px; align-items:center; }
  .note { width:30px; height:30px; border-radius:9px; display:grid; place-items:center; color:#fff; font:700 15px/1 Inter; flex:none; }
  .lg { flex:1; display:flex; flex-direction:column; gap:6px; } .lg i { display:block; height:6px; border-radius:4px; background:#E4E8EE; }
  .lg i.c { width:60%; } .lg i.t { background:#CFD6DF; width:85%; }"""
    vis = f"""<div class='vis'>
      <div class='mini' style='left:56px; top:34px; transform:rotate(-3deg)'><span class='note' style='background:#2E5A43'>A</span><div class='lg'><i class='t'></i><i></i><i class='c'></i></div></div>
      <div class='mini' style='left:78px; top:104px; transform:rotate(1.5deg)'><span class='note' style='background:#B88A4E'>B</span><div class='lg'><i class='t'></i><i></i><i class='c'></i></div></div>
      <div class='mini' style='left:48px; top:172px; transform:rotate(-1.5deg)'><span class='note' style='background:#6B88A6'>C</span><div class='lg'><i class='t'></i><i></i><i class='c'></i></div></div></div>"""
    corps = f"""<div id='c' class='marge'><div class='carte large lueur' style='width:880px; height:262px'>
      <div class='txt'><div class='tag'>Veille scientifique · Cofondateur</div>
        <div class='titre'>Veille Médicale</div>
        <div class='accroche'>Les nouvelles études de votre spécialité, résumées en français chaque jour.</div>
        <div class='desc'>Études et recommandations sélectionnées (PubMed, HAS, sociétés savantes, ClinicalTrials.gov), classées par spécialité, avec un niveau de preuve de A à C.</div>
        <div class='bas'><div class='puces'><span class='puce'>Gratuit</span><span class='puce or'>Web · mobile · e-mail · audio</span></div>
          <span class='cta plein'>veillemedicale.fr {ico('arrow-up-right', 16, 2.2)}</span></div></div>{vis}</div></div>"""
    return page(corps, css)


def carte_cotation():
    css = CSS_LARGE + """
  .ticket { position:absolute; left:38px; top:40px; width:224px; padding:18px; border-radius:16px; background:#fff;
            border:1px solid #E8E1D6; box-shadow:0 10px 22px rgba(27,35,51,.11); transform:rotate(-2deg); }
  .ticket .h { font:600 10.5px/1 Inter; letter-spacing:.1em; text-transform:uppercase; color:#8A93A1; margin-bottom:12px; }
  .codes { display:flex; gap:6px; align-items:center; flex-wrap:wrap; }
  .code { font:700 15px/1 'DejaVu Sans Mono', ui-monospace, monospace; color:var(--vert); background:var(--vertpale); padding:8px 9px; border-radius:8px; }
  .plus { font:600 14px/1 Inter; color:#9AA3AF; }
  .tl { margin-top:14px; display:flex; flex-direction:column; gap:6px; } .tl i { display:block; height:6px; border-radius:4px; background:#E4E8EE; } .tl i.c { width:55%; }"""
    vis = f"""<div class='vis'><div class='ticket'><div class='h'>Codes à saisir</div>
      <div class='codes'><span class='code'>CS</span><span class='plus'>+</span><span class='code'>MCS</span><span class='plus'>+</span><span class='code'>MCE</span></div>
      <div class='tl'><i></i><i class='c'></i></div></div></div>"""
    corps = f"""<div id='c' class='marge'><div class='carte large lueur' style='width:880px; height:246px'>
      <div class='txt'><div class='tag'>Outil en accès libre · Médecins spécialistes</div>
        <div class='titre'>Cotation</div>
        <div class='accroche'>La bonne cotation NGAP, en quelques secondes.</div>
        <div class='desc'>Codes à saisir, montant, mode de facturation et pièges à éviter, selon votre spécialité et votre secteur.</div>
        <div class='bas'><div class='puces'><span class='puce'>Ville et hôpital</span><span class='puce or'>Aucune donnée envoyée</span></div>
          <span class='cta plein'>Ouvrir l'outil {ico('arrow-up-right', 16, 2.2)}</span></div></div>{vis}</div></div>"""
    return page(corps, css)


def carte_radar():
    css = CSS_LARGE + """
  .onde { position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); border-radius:50%; border:1.5px solid rgba(46,90,67,.26); }
  .balayage { position:absolute; left:50%; top:50%; width:208px; height:208px; transform:translate(-50%,-50%); border-radius:50%;
              background:conic-gradient(from 300deg, rgba(184,138,78,0) 0deg, rgba(184,138,78,.34) 62deg, rgba(184,138,78,0) 63deg); }
  .centre { position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); width:46px; height:46px; border-radius:15px;
            display:grid; place-items:center; color:#fff; background:linear-gradient(140deg, var(--vert) 0%, var(--vert2) 100%);
            box-shadow:0 6px 14px rgba(46,90,67,.28); }
  .lieu { position:absolute; display:inline-flex; align-items:center; gap:5px; padding:6px 10px; border-radius:999px; background:#fff;
          border:1px solid #E8E1D6; box-shadow:0 6px 14px rgba(27,35,51,.10); font:600 12px/1 Inter; color:var(--vert); white-space:nowrap; }
  .lieu.or { color:#8A6332; background:#FFF8EF; } .lieu svg { width:13px; height:13px; }"""
    vis = f"""<div class='vis'>
      <div class='onde' style='width:208px; height:208px'></div><div class='onde' style='width:140px; height:140px'></div><div class='onde' style='width:74px; height:74px'></div>
      <div class='balayage'></div><div class='centre'>{ico('users', 22, 1.8)}</div>
      <span class='lieu' style='left:26px; top:34px'>{ico('map-pin', 13, 2.2)}Concert</span>
      <span class='lieu or' style='right:22px; top:66px'>Gratuit</span>
      <span class='lieu' style='left:20px; bottom:58px'>{ico('map-pin', 13, 2.2)}Atelier</span>
      <span class='lieu' style='right:30px; bottom:30px'>{ico('map-pin', 13, 2.2)}Expo</span></div>"""
    corps = f"""<div id='c' class='marge'><div class='carte large lueur' style='width:880px; height:262px'>
      <div class='txt'><div class='tag'>Prévention · Lien social</div>
        <div class='titre'>Le Radar — Paris</div>
        <div class='accroche'>Des sorties près de chez soi, chaque semaine, pour recréer du lien.</div>
        <div class='desc'>Concerts, expos, stand-up, ateliers et plein air{NB}: une sélection vérifiée, souvent gratuite, avec le lien pour réserver. Parce que le lien social est au cœur de la prévention.</div>
        <div class='bas'><div class='puces'><span class='puce'>Chaque semaine</span><span class='puce or'>Sorties gratuites</span></div>
          <span class='cta plein'>Voir le Radar {ico('arrow-up-right', 16, 2.2)}</span></div></div>{vis}</div></div>"""
    return page(corps, css)


def carte_outil(tag, nom, desc, cta, icone):
    css = """.o { width:420px; height:240px; padding:24px 26px 22px; display:flex; flex-direction:column; gap:10px; }
      .o .haut { display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; }
      .o .titre { font-size:31px; } .o .desc { flex:1; } """
    corps = f"""<div id='c' class='marge'><div class='carte lueur o'>
      <div class='haut'><div class='badge'>{ico(icone, 22, 1.8)}</div><span class='puce or'>{tag}</span></div>
      <div class='titre'>{nom}</div><div class='desc'>{desc}</div>
      <span class='cta'>{cta} {ico('arrow-up-right', 16, 2.2)}</span></div></div>"""
    return page(corps, css)


def carte_projet(nom, role, desc, puce, icone, cta, note=""):
    css = """.p { width:267px; height:340px; padding:24px 22px 22px; display:flex; flex-direction:column; gap:10px; }
      .p .titre { font-size:33px; margin-top:6px; } .p .role { font:600 10.5px/1.35 Inter; letter-spacing:.1em; text-transform:uppercase; color:var(--or); }
      .p .desc { flex:1; font-size:13.5px; } .p .note { font:400 11.5px/1.4 Inter; color:var(--doux); margin-top:-2px; }"""
    lien = f"<span class='cta'>{cta} {ico('arrow-up-right', 16, 2.2)}</span>" if cta else "<span class='cta' style='color:var(--doux)'>Bientôt en ligne</span>"
    corps = f"""<div id='c' class='marge'><div class='carte lueur p'>
      <div class='badge'>{ico(icone, 22, 1.8)}</div>
      <div class='titre'>{nom}</div><div class='role'>{role}</div><div class='desc'>{desc}</div>
      <div><span class='puce'>{puce}</span>{f"<div class='note' style='margin-top:7px'>{note}</div>" if note else ''}</div>
      {lien}</div></div>"""
    return page(corps, css)


def panneau(colonnes, elements, hauteur, vertical=False):
    css = f""".pn {{ width:880px; height:{hauteur}px; display:grid; grid-template-columns:repeat({colonnes}, 1fr); }}
      .el {{ padding:26px 26px 24px; display:flex; flex-direction:{'column' if vertical else 'row'}; gap:{14 if vertical else 15}px; align-items:flex-start; border-right:1px solid #EFE7DA; border-bottom:1px solid #EFE7DA; }}
      .el:nth-child({colonnes}n) {{ border-right:none; }} .el.dernier {{ border-bottom:none; }}
      .el .t {{ font:700 22px/1.12 Cormorant; color:var(--encre); margin:2px 0 7px; }} .el .desc {{ font-size:13.5px; }}"""
    n = len(elements)
    dern = set(range(n - colonnes, n)) if n % colonnes == 0 else set(range(n - n % colonnes, n))
    cases = "".join(f"<div class='el{' dernier' if i in dern else ''}'><div class='badge'>{ico(ic, 21, 1.8)}</div><div><div class='t'>{t}</div><div class='desc'>{d}</div></div></div>"
                    for i, (ic, t, d) in enumerate(elements))
    return page(f"<div id='c' class='marge'><div class='carte lueur pn'>{cases}</div></div>", css)


def carte_linkedin():
    css = """.li { width:880px; height:128px; display:flex; align-items:center; gap:20px; padding:0 30px; }
      .li .titre { font-size:30px; } .li .desc { margin-top:5px; } .li .m { flex:1; }"""
    corps = f"""<div id='c' class='marge'><div class='carte lueur li'><div class='badge'>{ico('users', 22, 1.8)}</div>
      <div class='m'><div class='titre'>Suivre mes partages</div><div class='desc'>Synthèses d'études et messages de prévention, régulièrement sur LinkedIn.</div></div>
      <span class='cta plein'>LinkedIn {ico('arrow-up-right', 16, 2.2)}</span></div></div>"""
    return page(corps, css)


def signature(sombre):
    css = f""".sg {{ width:920px; padding:30px 20px 18px; display:flex; align-items:center; gap:18px; }}
      .sg .l {{ flex:1; height:1.5px; }} .sg .l.g {{ background:linear-gradient(270deg, var(--or), rgba(184,138,78,0)); }}
      .sg .l.d {{ background:linear-gradient(90deg, var(--or), rgba(184,138,78,0)); }}
      .sg .m {{ display:flex; align-items:center; gap:12px; color:var(--or); }}
      .sg .t {{ font:italic 500 25px/1 Cormorant; color:{'#E9DCC8' if sombre else '#2E5A43'}; white-space:nowrap; }}"""
    return page(f"<div id='c'><div class='sg'><div class='l g'></div><div class='m'>{ico('sunrise', 22, 1.7)}<span class='t'>Remettre la prévention au cœur du soin</span></div><div class='l d'></div></div></div>", css)


def composants():
    yield "carte-profil", carte_profil()
    for nom, lib, ic, ext in [("bouton-veille", "Veille Médicale", "globe", True), ("bouton-linkedin", "LinkedIn", "users", True),
                              ("bouton-outils", "Outils", "wrench", False), ("bouton-projets", "Projets", "rocket", False),
                              ("bouton-recherche", "Recherche", "microscope", False)]:
        yield nom, bouton(lib, ic, ext)
    for cle, texte, ic in [("veille", "Veille scientifique", "newspaper"), ("outils", "Outils et ressources en accès libre", "wrench"),
                           ("projets", "Projets en santé numérique", "rocket"), ("recherche", "Recherche", "microscope"),
                           ("enseignement", "Enseignement et publications", "graduation-cap")]:
        yield f"titre-{cle}-clair", titre(texte, ic, False)
        yield f"titre-{cle}-sombre", titre(texte, ic, True)
    yield "carte-veille-medicale", carte_veille()
    yield "carte-cotation", carte_cotation()
    yield "carte-radar", carte_radar()
    yield "carte-sosie", carte_outil("Python · Mac", "Sosie", f"Travailler avec l'IA sur des bases de données de santé, sans jamais lui montrer les vraies{NB}: elle écrit ses scripts sur un sosie fictif.", "Site et démo", "shield-check")
    yield "carte-manuscript-agents", carte_outil("Plugin Claude", "Manuscript Agents", f"De la question de recherche à l'article publié{NB}: statistiques, EQUATOR, rédaction, relecture simulée et soumission.", "Installer", "feather")
    yield "carte-sous-titres", carte_outil("Application web", "Sous-titres", "Sous-titres en direct, traduits entre deux langues et attribués à chaque intervenant, pour suivre ou donner une intervention.", "Ouvrir", "captions")
    yield "carte-remboursement-glp1", carte_outil("Patients et soignants", "Remboursement GLP-1", "Savoir si l'on est concerné par le remboursement des traitements de l'obésité et trouver un centre spécialisé proche.", "Ouvrir", "badge-euro")
    yield "carte-activ", carte_projet("ACTIV", "Cofondateur", "Prescrire et orienter vers l'activité physique adaptée.", "Retenu par IMPULSE Healthcare", "footprints", "Découvrir", "AP-HP · Google.org · Bayes Impact")
    yield "carte-sano", carte_projet("Sano", "Fondateur", "Outil numérique de prévention en santé.", "En développement", "sprout", "Découvrir")
    yield "carte-boli", carte_projet("Boli", "Directeur scientifique et médical", "Accompagnement numérique des patients en situation d'obésité et de leurs soignants, entre les consultations.", f"DM classe{NB}I · marqué{NB}CE", "heart-pulse", "boli.care")
    yield "panneau-recherche", panneau(3, [
        ("brain-circuit", "Prédire la perte de poids sous sémaglutide", "Apprentissage automatique · Master 2 MODES (Université Paris Cité) · NutriOmics"),
        ("microscope", "Microbiote et maladies cardiométaboliques", f"Entérotype <i>Bacteroides{NB}2</i> dans la cohorte MetaCardis · thèse de médecine"),
        ("activity", "Activité physique adaptée", f"Profils d'adhésion dans une base de 2{FINE}500 patients (Hôtel-Dieu) · 6{NB}communications nationales")], 244, vertical=True)
    yield "panneau-enseignement", panneau(2, [
        ("graduation-cap", "Capacité de médecine du sport", "Obésité, diabète et activité physique adaptée"),
        ("book-open", "DU Obésité · Sorbonne Université", f"Activité physique{NB}: recommandations et prescription"),
        ("presentation", "DU Activité physique et santé", "Sorbonne Université · élaboration du programme"),
        ("sparkles", "Practico", "Outils d'IA et d'apprentissage pour les étudiants")], 236)
    yield "carte-linkedin", carte_linkedin()
    yield "signature-clair", signature(False)
    yield "signature-sombre", signature(True)


def main():
    BUILD.mkdir(exist_ok=True); ASSETS.mkdir(exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME if pathlib.Path(CHROME).exists() else None, args=["--allow-file-access-from-files"])
        pg = nav.new_page(viewport={"width": 1000, "height": 900}, device_scale_factor=2)
        for nom, html in composants():
            f = BUILD / f"{nom}.html"
            f.write_text(html, encoding="utf-8")
            pg.goto(f.as_uri())
            pg.evaluate("document.fonts.ready.then(() => true)")
            pg.wait_for_timeout(120)
            pg.locator("#c").screenshot(path=str(ASSETS / f"{nom}.png"), omit_background=True)
            print(nom)
        nav.close()
    try:
        import imagequant
        from PIL import Image
        for f in ASSETS.glob("*.png"):
            q = imagequant.quantize_pil_image(Image.open(f).convert("RGBA"), dithering_level=1.0, max_colors=256, min_quality=75, max_quality=96)
            q.save(f, optimize=True)
    except ImportError:
        print("imagequant absent : images non compressées")


if __name__ == "__main__":
    main()
