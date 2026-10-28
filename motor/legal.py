"""pagina-wow · textos legales base (privacidad, términos, cookies) por país.

Son plantillas para negocios pequeños, no asesoría legal. Cada función devuelve
una lista de (titulo, [parrafos]). Los párrafos aceptan **negrita**.

Países: CO (Colombia), US (Estados Unidos), EU (Unión Europea / España), OTRO.
Datos que usan (de sitio.json → legal): responsable, id, email, direccion, pais,
datos_sensibles, edad_minima. Y lo que la página realmente usa (formulario,
analítica, cookies), que el generador pasa en `usa`.
"""

LEYES = {
    "CO": {"es": "la Ley 1581 de 2012, el Decreto 1377 de 2013 (compilado en el Decreto 1074 de 2015) y demás normas de protección de datos de Colombia",
           "en": "Colombian Law 1581 of 2012, Decree 1377 of 2013 (compiled in Decree 1074 of 2015) and related Colombian data protection rules"},
    "US": {"es": "las leyes aplicables de Estados Unidos, incluida la ley de privacidad en línea de California (CalOPPA) y, cuando aplique, la CCPA/CPRA",
           "en": "applicable United States law, including the California Online Privacy Protection Act (CalOPPA) and, where applicable, the CCPA/CPRA"},
    "EU": {"es": "el Reglamento General de Protección de Datos (Reglamento (UE) 2016/679, RGPD) y la normativa nacional aplicable",
           "en": "the General Data Protection Regulation (Regulation (EU) 2016/679, GDPR) and applicable national law"},
    "OTRO": {"es": "la normativa de protección de datos aplicable en el país del responsable",
             "en": "the data protection law applicable in the owner's country"},
}

AUTORIDAD = {
    "CO": {"es": "la Superintendencia de Industria y Comercio (SIC)", "en": "the Superintendence of Industry and Commerce (SIC)"},
    "EU": {"es": "la autoridad de control de tu país (en España, la Agencia Española de Protección de Datos)", "en": "your local supervisory authority"},
}

PROVEEDORES = {
    "vercel": ("Vercel Inc.", {"es": "alojamiento de la página (Estados Unidos)", "en": "website hosting (United States)"}),
    "fuentes": ("Google Fonts", {"es": "tipografías; tu navegador se conecta a servidores de Google", "en": "fonts; your browser connects to Google servers"}),
    "web3forms": ("Web3Forms", {"es": "envío del formulario de contacto al correo del responsable", "en": "delivers the contact form to the owner's email"}),
    "resend": ("Resend", {"es": "envío de correos del formulario de contacto (Estados Unidos)", "en": "sends contact form emails (United States)"}),
    "supabase": ("Supabase", {"es": "almacenamiento de los mensajes del formulario", "en": "stores contact form messages"}),
    "posthog": ("PostHog", {"es": "estadísticas de visitas", "en": "visit analytics"}),
    "vercel_analytics": ("Vercel Web Analytics", {"es": "estadísticas de visitas sin cookies", "en": "cookieless visit analytics"}),
    "whatsapp": ("WhatsApp (Meta)", {"es": "solo si decides escribir por WhatsApp; aplica la política de WhatsApp", "en": "only if you choose to message on WhatsApp; WhatsApp's policy applies"}),
}


def _quien(L, lang):
    r = L.get("responsable", "")
    ident = f" ({L['id']})" if L.get("id") else ""
    dire = f", con domicilio en {L['direccion']}" if L.get("direccion") and lang == "es" else (f", located at {L['direccion']}" if L.get("direccion") else "")
    return f"**{r}**{ident}{dire}"


def privacidad(L, usa, lang="es"):
    p = L.get("pais", "OTRO").upper()
    p = p if p in LEYES else "OTRO"
    q, mail = _quien(L, lang), L.get("email", "")
    prov = [k for k in ("vercel", "fuentes", "web3forms", "resend", "supabase", "posthog", "vercel_analytics", "whatsapp") if usa.get(k)]
    if lang == "en":
        S = [("Who is responsible", [f"{q} is responsible for the personal data collected through this website. Contact: **{mail}**.",
                                     f"This policy follows {LEYES[p]['en']}."])]
        datos = []
        if usa.get("formulario"): datos.append("**Contact form:** name, email and the message you write, to answer you.")
        if usa.get("whatsapp"): datos.append("**WhatsApp or email:** if you write to us, we receive your number or email and your message, only to answer you.")
        if usa.get("analitica"): datos.append("**Visit analytics:** pages viewed, approximate country, device and browser, in aggregate, to improve the site." + ("" if usa.get("cookies") else " No cookies are used for this."))
        datos.append("**Technical logs:** the hosting provider records IP addresses and technical data for security for a limited time.")
        S.append(("What data we collect and why", datos))
        if L.get("datos_sensibles"):
            S.append(("Sensitive information", ["To book an appointment, your name, a contact and the general reason for your visit are enough (for example, \"knee pain\"). Please do not send medical records, diagnoses or test results through the form or messages: we handle that information during your visit or through a private channel, with your explicit consent."]))
        S.append(("Who we share it with", ["We do not sell or rent your data. We only use these providers to run the site:"] + [f"**{PROVEEDORES[k][0]}:** {PROVEEDORES[k][1]['en']}." for k in prov]
                  + ["Some of these providers are located outside your country. They apply their own security measures and contractual safeguards."]))
        S.append(("How long we keep it", ["Messages are kept while we are in contact and up to 24 months afterwards, unless you ask us to delete them earlier or the law requires otherwise."]))
        der = ["You can request access to, correction of or deletion of your data, and withdraw your consent, by writing to **" + mail + "**. We reply within 30 days."]
        if p == "US": der += ["If you are a California resident, you have the rights granted by the CCPA/CPRA where they apply. We do not sell or share personal information for cross-context behavioral advertising.",
                              "Do Not Track: this site does not change its behavior based on Do Not Track signals; it does not track you across other websites."]
        if p == "EU": der += ["You also have the right to object, to restrict processing and to data portability, and to lodge a complaint with " + AUTORIDAD['EU']['en'] + ".",
                              "Legal basis: your consent (form and, if applicable, analytics cookies) and our legitimate interest in keeping the site secure."]
        S.append(("Your rights", der))
        S.append(("Children", [f"This site is not directed to people under {L.get('edad_minima', 13 if p == 'US' else 16)}. We do not knowingly collect their data."]))
        S.append(("Changes", ["If we change this policy we will publish the new version on this page with its date."]))
        return S

    S = [("Quién es el responsable", [f"{q} es responsable del tratamiento de los datos personales que se recogen en esta página. Contacto: **{mail}**.",
                                      f"Esta política sigue {LEYES[p]['es']}."])]
    datos = []
    if usa.get("formulario"): datos.append("**Formulario de contacto:** nombre, correo y el mensaje que escribas, para responderte.")
    if usa.get("whatsapp"): datos.append("**WhatsApp o correo:** si nos escribes, recibimos tu número o correo y tu mensaje, solo para responderte.")
    if usa.get("analitica"): datos.append("**Estadísticas de visitas:** páginas vistas, país aproximado, dispositivo y navegador, de forma agregada, para mejorar la página." + ("" if usa.get("cookies") else " Para esto no se usan cookies."))
    datos.append("**Registros técnicos:** el proveedor de alojamiento guarda direcciones IP y datos técnicos por seguridad, durante un tiempo limitado.")
    S.append(("Qué datos recogemos y para qué", datos))
    if p == "CO":
        S.append(("Autorización", ["Al enviar el formulario, marcar la casilla de aceptación o escribirnos, nos das tu **autorización previa, expresa e informada** para tratar tus datos con las finalidades descritas aquí.",
                                   "Responder preguntas sobre datos sensibles o de menores de edad es opcional."]))
    if L.get("datos_sensibles"):
        S.append(("Datos sensibles", ["Para pedir una cita basta con tu nombre, un contacto y el motivo de consulta en términos generales (por ejemplo, \"dolor de rodilla\"). No envíes por el formulario o los mensajes tu historia clínica, diagnósticos ni exámenes: esos datos los tratamos en la consulta o por un canal privado, con tu autorización expresa."]))
    S.append(("Con quién los compartimos", ["No vendemos ni alquilamos tus datos. Solo usamos estos proveedores para que la página funcione:"] + [f"**{PROVEEDORES[k][0]}:** {PROVEEDORES[k][1]['es']}." for k in prov]
              + ["Algunos de estos proveedores están fuera de tu país, por lo que puede haber **transferencia internacional de datos**. Ellos aplican sus propias medidas de seguridad y garantías contractuales."]))
    S.append(("Cuánto tiempo los guardamos", ["Guardamos los mensajes mientras estemos en contacto y hasta 24 meses después, salvo que pidas borrarlos antes o la ley exija otra cosa."]))
    if p == "CO":
        der = ["Como titular puedes **conocer, actualizar y rectificar** tus datos, pedir prueba de la autorización, ser informado del uso que les damos, **revocar la autorización o pedir que se supriman**, y presentar quejas ante " + AUTORIDAD['CO']['es'] + ".",
               f"Para ejercerlos escribe a **{mail}**. Las consultas se responden en máximo 10 días hábiles y los reclamos en máximo 15 días hábiles, según la ley."]
    elif p == "EU":
        der = [f"Puedes ejercer tus derechos de **acceso, rectificación, supresión, oposición, limitación y portabilidad** escribiendo a **{mail}**. Respondemos en un mes.",
               "Base legal: tu consentimiento (formulario y, si aplica, cookies de estadística) y nuestro interés legítimo en mantener la página segura.",
               "Si crees que no atendimos bien tu solicitud, puedes reclamar ante " + AUTORIDAD['EU']['es'] + "."]
    else:
        der = [f"Puedes pedir acceso, corrección o eliminación de tus datos, y retirar tu consentimiento, escribiendo a **{mail}**. Respondemos en máximo 30 días."]
        if p == "US": der += ["Si resides en California, tienes los derechos de la CCPA/CPRA cuando apliquen. No vendemos ni compartimos información personal para publicidad.",
                              "Señales Do Not Track: la página no cambia su comportamiento con esa señal, porque no te rastrea en otros sitios."]
    S.append(("Tus derechos", der))
    S.append(("Menores de edad", [f"Esta página no está dirigida a menores de {L.get('edad_minima', 13 if p == 'US' else 18 if p == 'CO' else 16)} años. No recogemos sus datos a sabiendas."]))
    S.append(("Cambios", ["Si cambiamos esta política, publicaremos la nueva versión en esta misma página con su fecha."]))
    return S


def terminos(L, usa, lang="es"):
    p = L.get("pais", "OTRO").upper()
    jur = {"CO": ("las leyes de Colombia", "the laws of Colombia"), "US": ("las leyes del estado donde opera el responsable, en Estados Unidos", "the laws of the state where the owner operates, in the United States"),
           "EU": ("las leyes del país de la Unión Europea donde está el responsable", "the laws of the EU country where the owner is established")}.get(p, ("las leyes del país del responsable", "the laws of the owner's country"))
    q, mail = _quien(L, lang), L.get("email", "")
    if lang == "en":
        return [("About these terms", [f"This website belongs to {q}. By using it you accept these terms."]),
                ("Information on the site", ["Content is for general information. It is not professional advice for your specific case until we agree on a service.",
                                             "Prices and availability can change. The final conditions of each service are the ones agreed in writing or by message before starting."]),
                ("Intellectual property", ["Texts, photos, logos and design belong to the owner or are used with permission. Do not copy them for commercial use without written authorization."]),
                ("External links", ["Links to WhatsApp, social networks or other sites are governed by their own terms and policies."]),
                ("Liability", ["We work to keep the site available and accurate, but we cannot guarantee it will always be error free or uninterrupted. To the extent allowed by law, we are not liable for indirect damages arising from its use."]),
                ("Applicable law", [f"These terms are governed by {jur[1]}. Questions: **{mail}**."])]
    S = [("Sobre estos términos", [f"Esta página pertenece a {q}. Al usarla aceptas estos términos."]),
         ("La información de la página", ["El contenido es informativo. No reemplaza una asesoría profesional para tu caso hasta que acordemos un servicio.",
                                          "Los precios y la disponibilidad pueden cambiar. Las condiciones finales de cada servicio son las que acordemos por escrito o por mensaje antes de empezar."]),
         ("Propiedad intelectual", ["Los textos, fotos, logos y diseño son del responsable o se usan con permiso. No los copies para uso comercial sin autorización escrita."]),
         ("Enlaces externos", ["Los enlaces a WhatsApp, redes sociales u otros sitios se rigen por sus propios términos y políticas."]),
         ("Responsabilidad", ["Trabajamos para que la página esté disponible y sea correcta, pero no podemos garantizar que nunca tenga errores o interrupciones. En lo que permita la ley, no respondemos por daños indirectos derivados de su uso."])]
    if p == "CO":
        S.append(("Derechos del consumidor", ["Si compras un producto o servicio, tienes los derechos del Estatuto del Consumidor (Ley 1480 de 2011), incluido el derecho de retracto cuando aplique a ventas a distancia."]))
    if p == "EU":
        S.append(("Derechos del consumidor", ["Si contratas a distancia como consumidor, tienes el derecho de desistimiento de 14 días naturales cuando aplique, salvo las excepciones legales (por ejemplo, servicios ya prestados por completo con tu consentimiento)."]))
    S.append(("Ley aplicable", [f"Estos términos se rigen por {jur[0]}. Dudas: **{mail}**."]))
    return S


def cookies(L, usa, lang="es"):
    mail = L.get("email", "")
    filas = [("pw_consent", "localStorage", "Guarda si aceptaste o rechazaste las cookies de estadística." if lang == "es" else "Stores whether you accepted or rejected analytics cookies.", "1 año" if lang == "es" else "1 year")] if usa.get("cookies") else []
    if usa.get("cookies"): filas.append(("ph_*_posthog", "cookie", "Estadísticas de visitas de PostHog. Solo si aceptas." if lang == "es" else "PostHog visit analytics. Only if you accept.", "1 año" if lang == "es" else "1 year"))
    if lang == "en":
        S = [("What cookies are", ["Cookies are small files a site saves in your browser. Some are necessary for it to work and others measure visits."])]
        if not usa.get("cookies"):
            S.append(("Cookies on this site", ["This site **does not use advertising or tracking cookies**." + (" Visit statistics are measured without cookies and without identifying you." if usa.get("analitica") else ""),
                                               "That is why you do not see a cookie banner."]))
        else:
            S.append(("Cookies on this site", ["Analytics cookies are only activated if you accept them in the banner. You can change your choice at any time with the **Cookie preferences** link in the footer."]))
        S.append(("How to delete them", ["You can delete or block cookies from your browser settings. Questions: **" + mail + "**."]))
        return S, filas
    S = [("Qué son las cookies", ["Las cookies son pequeños archivos que una página guarda en tu navegador. Algunas son necesarias para que funcione y otras sirven para medir visitas."])]
    if not usa.get("cookies"):
        S.append(("Cookies en esta página", ["Esta página **no usa cookies de publicidad ni de rastreo**." + (" Las estadísticas de visitas se miden sin cookies y sin identificarte." if usa.get("analitica") else ""),
                                             "Por eso no ves un aviso de cookies."]))
    else:
        S.append(("Cookies en esta página", ["Las cookies de estadística solo se activan si las aceptas en el aviso. Puedes cambiar tu decisión cuando quieras con el enlace **Preferencias de cookies** del pie de página."]))
    S.append(("Cómo borrarlas", ["Puedes borrar o bloquear las cookies desde la configuración de tu navegador. Dudas: **" + mail + "**."]))
    return S, filas
