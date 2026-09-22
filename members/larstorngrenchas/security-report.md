# Säkerhetsrapport

## Executive Summary

Detta projekt har flera allvarliga säkerhetsbrister som tillsammans utgör en hög risk för konfidentialitet, integritet och autentisering. Den mest kritiska problemet är SQL-injection i login-flödet, följt av felaktig lösenordshantering, hårdkodade hemligheter, bristande auktorisation och exponering av känslig intern information i seed-data. Om systemet används i en verklig miljö med användardata eller produktionsdata kan detta leda till obehörig åtkomst, dataläckage och manipulation av användarkonton.

Det rekommenderas att projektet inte deployas eller användas med riktiga användare förrän de viktigaste sårbarheterna är åtgärdade. En genomgripande säkringsprocess krävs innan systemet kan anses vara säkert nog för produktion.

## Sammanfattning

Detta projekt innehåller flera tydliga och allvarliga säkerhetsbrister i autentisering, auktorisation, datalagring och konfiguration. Den största risken kommer från SQL-injection i login-flödet, felaktig lösenordshantering, hårdkodade hemligheter och brist på åtkomstkontroll i profil- och användardata. Projektet är inte säkert för produktion och bör betraktas som högrisk om det används i en verklig miljö.

## Scope

Granskningen omfattar den Flask-baserade webbapplikationen i projektet, inklusive:

- autentisering i [src/company_website/auth.py](src/company_website/auth.py)
- routings och profiloperationer i [src/company_website/routes.py](src/company_website/routes.py)
- konfiguration i [src/company_website/config.py](src/company_website/config.py)
- databasinitiering i [src/company_website/db.py](src/company_website/db.py)
- seed-data i [src/company_website/migrations/002_seed_data.sql](src/company_website/migrations/002_seed_data.sql) och [src/company_website/migrations/004_seed_user_profiles.sql](src/company_website/migrations/004_seed_user_profiles.sql)

## Metod

Granskningen baseras på genomgång av koden och manuell analys av autentiserings- och databasflöden, säkerhetskonfiguration och seed-data i projektet.

## Resultat

### 1. SQL-injection i login-funktionen

**Sårbarhet:** SQL injection  
**Källkod:** [src/company_website/auth.py](src/company_website/auth.py)  
**Risknivå:** Hög

I login-funktionen byggs SQL-frågan med en formatsträng och användarinmatning i SQL-kod:

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password_hash = '{password}'"
cursor.execute(query)
```

Detta gör att användaren kan injicera SQL-kod i `username` eller `password`, vilket kan förändra sökfrågan och ge tillgång till data man inte borde ha.

**Konsekvens:**
- Databasintrång
- Läsning av användardata
- Manipulation av användarkonton
- Potentiellt full kontroll över applikationens databas

**Rekommenderad åtgärd:**
- Använd parametriserade SQL-frågor utan f-string interpolation.
- Exempel:

```python
cursor.execute(
    "SELECT * FROM users WHERE username = ?",
    (username,)
)
```

---

### 2. Felaktig behandling av lösenord och hashes

**Sårbarhet:** Svag autentisering och felaktig lösenordshantering  
**Källkod:** [src/company_website/auth.py](src/company_website/auth.py)  
**Risknivå:** Hög

Koden använder inte ett korrekt lösenordsflöde. Istället för att verifiera lösenordet mot ett säkert hashvärde i databasen, jämförs `password_hash` direkt mot användarens inmatning i SQL-frågan. Den enda användningen av `check_password_hash()` är i ett sekundärt villkor, men huvudflödet för login är inte korrekt implementerat.

**Konsekvens:**
- Lösenord kan verifieras felaktigt eller undvikas
- Hashlogiken blir otillförlitlig
- Risk för autentiseringsbypass

**Rekommenderad åtgärd:**
- Hasha alla lösenord med ett starkt algoritm, exempelvis scrypt eller bcrypt.
- Verifiera med `check_password_hash()` eller equivalent säker metod.
- Använd en tydlig, korrekt autentiseringsmodell utan att lägga lösenord i SQL-frågor.

---

### 3. Hårdkodad hemlighet i konfiguration

**Sårbarhet:** Hårdkodad hemlighet/nyckel  
**Källkod:** [src/company_website/config.py](src/company_website/config.py)  
**Risknivå:** Hög

```python
SECRET_KEY = 'dev-secret-key'
```

Detta är inte lämpligt för produktionsmiljöer. Flask-sessioner och cookies är otillräckligt skyddade om `SECRET_KEY` är välkänd eller statisk i koden.

**Konsekvens:**
- Session hijacking
- Förfalskade cookies
- Känsliga autentiseringsuppgifter kan utnyttjas om nyckeln blir känd

**Rekommenderad åtgärd:**
- Lagra hemligheter i miljövariabler eller en betrodd säkerhetshanterare.
- Använd en lång, slumpmässig nyckel som inte finns i versionskontroll.
- Aktivera säkra cookie-flaggor i Flask.

---

### 4. Brist på auktorisation vid profilredigering

**Sårbarhet:** Insecure Direct Object Reference (IDOR)  
**Källkod:** [src/company_website/routes.py](src/company_website/routes.py)  
**Risknivå:** Hög

`edit_profile(id)` hämtar användarprofilen baserat på ett ID i URL:en utan att kontrollera om den inloggade användaren faktiskt har rätt att ändra den profilen.

**Exempel:**

```python
@main_bp.route('/profiles/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    ...
```

Det finns ingen check som verifierar `current_user.id == id`.

**Konsekvens:**
- En användare kan redigera andras profiler
- Läckage av interna uppgifter
- Manipulation av användardata

**Rekommenderad åtgärd:**
- Kontrollera att `current_user.id` matchar den begärda profilen.
- Begränsa redigering till den egna användaren om inte admin-rättigheter finns.
- Implementera rollbaserad åtkomstkontroll för känsliga operationer.

---

### 5. Exponering av känslig intern information

**Sårbarhet:** Informationsläcka  
**Källkod:** [src/company_website/migrations/004_seed_user_profiles.sql](src/company_website/migrations/004_seed_user_profiles.sql)  
**Risknivå:** Hög

Seed-data innehåller text som avslöjar:
- staging DB-lösenord
- sökvägar till backups
- interna projektkodnamn
- admin-panelens mockup-plats

Detta visar att känslig information lagras i versionerad kod och kan exponeras i produktion eller i testmiljöer.

**Konsekvens:**
- Läckage av systemhemligheter
- Förenklad attack mot miljöer
- Ökad risk för insider- och externa attacker

**Rekommenderad åtgärd:**
- Ta bort all intern information från versionerad kod.
- Använd separata miljövariabler/secret storage för hemligheter.
- Exponera aldrig känsliga uppgifter i databasseed-data.

---

### 6. Brist på CSRF-skydd

**Sårbarhet:** Cross-Site Request Forgery (CSRF)  
**Källkod:** [src/company_website/routes.py](src/company_website/routes.py)  
**Risknivå:** Hög

Profiluppdatering sker via `POST` utan CSRF-token eller skydd. Detta gör att en angripare kan försöka få en inloggad användare att skicka en skadlig förfrågan utan att veta det.

**Konsekvens:**
- Oautentiserade ändringar i användardata
- Förfalskade uppdateringar
- Potentiell manipulation av användarprofiler

**Rekommenderad åtgärd:**
- Använd Flask-WTF eller en likvärdig CSRF-skyddslösning.
- Inkludera CSRF-token i formulär och verifiera det server-side.

---

### 7. Otydligt session- och cookie-säkerhet

**Sårbarhet:** Svag sessionsäkerhet  
**Källkod:** [src/company_website/app.py](src/company_website/app.py), [src/company_website/config.py](src/company_website/config.py)  
**Risknivå:** Medium till hög

Det finns ingen tydlig konfiguration för säkra cookies, exempelvis:
- `SESSION_COOKIE_SECURE`
- `SESSION_COOKIE_HTTPONLY`
- `SESSION_COOKIE_SAMESITE`

Flask använder standardinställningar om inget specificeras, och det är inte tillräckligt för produktion.

**Konsekvens:**
- Session theft
- Cross-site scripting risker förvärras
- Cookies kan exfiltreras i osäkra miljöer

**Rekommenderad åtgärd:**
- Aktivera `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY` och `SESSION_COOKIE_SAMESITE='Lax'` eller strängare.
- Kontrollera HTTPS i produktion.

---

### 8. Databasdesign och datahantering är inte säkert för produktion

**Sårbarhet:** Otillräcklig produktionstillförlitlighet  
**Källkod:** [src/company_website/db.py](src/company_website/db.py)  
**Risknivå:** Medium

Projektet använder SQLite med en lokal fil i filsystemet. Det fungerar för demo eller små applikationer, men är inte ersättning för en databas som stöder säkerhet, åtkomstkontroll, säkra autentiseringsmekanismer och production-grade drift.

**Konsekvens:**
- Mindre säkert i produktionsmiljöer
- Mindre skalbarhet och kontroll
- Högre risk vid filsystemåtkomst

**Rekommenderad åtgärd:**
- Använd en säker databas för produktion, exempelvis PostgreSQL eller MySQL.
- Separera applikations- och databassekretess.
- Implementera säker körning, backup och åtkomstkontroll.

---

## Kritiska fynd

De mest allvarliga bristerna är:

1. SQL injection i login
2. felaktig lösenordshantering
3. hårdkodad `SECRET_KEY`
4. bristande åtkomstkontroll i profilredigering
5. exponering av hemligheter i seed-data

Dessa problem tillsammans gör att applikationen inte bör användas med riktiga användare eller känslig data.

## Riskbedömning

| Kategori | Bedömning |
| --- | --- |
| Konfidentialitet | Hög |
| Integritet | Hög |
| Tillgänglighet | Medium |
| Autentisering | Hög |
| Auktorisation | Hög |
| Sårbarhet mot webbförsvar | Hög |

## Rekommenderade nästa steg

1. Åtgärda SQL injection i login.
2. Implementera korrekt lösenordshashning och verifiering.
3. Flytta alla hemligheter till miljövariabler.
4. Lägg in strikt åtkomstkontroll i profilredigering.
5. Lägg till CSRF-skydd på alla state-changing formulär.
6. Ta bort känslig data från SQL-migrationer.
7. Använd en produktionstestad databas och säkra cookie-inställningar.
8. Gör en sekundär kodgranskning efter patchning.

## Slutsats

Projektet innehåller flera tydliga säkerhetsproblem som inte kan ignoreras. Den största riskgruppen är autentisering och auktorisation, men även dataläckage och hemlighetsförvaltning är allvarliga. Om systemet inte genomgår en genomgripande säkringsprocess är det inte lämpligt för produktionsanvändning.

## Dokumentinformation

- Version: 1.0
- Datum: 2026-09-22
- Status: Öppen – kräver omedelbar säkerhetsåtgärd
