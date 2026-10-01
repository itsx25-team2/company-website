# Säkerhetsrapport

## Sammanfattning

Detta är en komplettering till föregående säkerhets-rapport. Detta med anledning av att koden för company-website har uppdaterats med en funktion för email-signatur, som visat sig innehålla brister och särehetsproblem.

## Scope

Granskningen omfattar den Flask-baserade webbapplikationen i projektet, inklusive:

- routing och profiloperationer i [src/company_website/routes.py](src/company_website/routes.py)
- tester i [src/company_website/config.py](src/company_website/tests/test_app.py)

## Metod

Granskningen baseras på genomgång av koden.

## Resultat

Förhandsvisningen har en Jinja-injektionsrisk: användarens signatur skickas till render_template_string, medan en begränsad blocklista försökte stoppa farliga uttryck, till exempel {{ config.SECRET_KEY }}.

**Konsekvens:**
- Databasintrång
- Läsning av användardata

**Rekommenderad åtgärd:**
- Ta bort dynamisk Jinja-rendering i routes.py.
- Ersätt endast firstname, lastname, email, role och company.
- Endast förutbestämda variabler får skickas in. Själva ersättningen tolkar inte längre malltext som Jinja, och aktuell endpoint accepterar bara exakta variabelnamn. Övriga uttryck ska avvisas.


## Kritiska fynd

1. Jinja injection i förhandsvisning av email-signatur.

Detta problem gör att applikationen inte bör användas med riktiga användare eller känslig data.

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

Gör en sekundär kodgranskning efter patchning.

## Slutsats

Projektet innehåller flera tydliga säkerhetsproblem som inte kan ignoreras. Om systemet inte genomgår en genomgripande säkringsprocess är det inte lämpligt för produktionsanvändning.

## Dokumentinformation

- Version: 3.0
- Datum: 2026-09-24
- Status: Öppen – kräver omedelbar säkerhetsåtgärd
