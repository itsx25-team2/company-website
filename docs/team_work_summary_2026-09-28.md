# Team 2 - arbetssammanfattning 2026-09-28

## Närvaro

- Närvarande: Jonny Nguyen, Fajk Zhupa, Tim Rundquist, Lars Torngren och Wilibroad Ngebi.
- Frånvarande: Amin Mahamoud.

## Dagens mål

Teamet påbörjade Workshop 4 med fokus på Software Bill of Materials (SBOM),
supply chain-spårbarhet och säker integrering av utbildarens senaste
applikationsversion. Arbetet genomfördes på `workshop4/instructor-sync` så
att `main` och den aktiva miljön inte påverkades under testningen.

## Integrering

Utbildarens senaste kända ändringar integrerades manuellt. De omfattar legacy-
autentisering, image-taggar och digest, Kubernetes Ingress, CycloneDX-SBOM,
Cosign-attestering och förhandsvisning av e-postsignaturer.

Team 2:s fungerande Headscale-, WIF-, K3s-, RBAC- och Ingress-konfiguration
bevarades. Utbildaren har meddelat att upstream-versionen inte ändras vidare,
vilket minskar risken för framtida mergekonflikter.

## Säkerhetsåtgärder

- Legacy-SQL använder parametrar och lösenord verifieras som hashvärden.
- E-postsignaturer använder begränsad variabelersättning utan Jinja-exekvering.
- Flask-WTF skyddar POST-formulär mot CSRF.
- Logout använder POST.
- Användare kan endast redigera sin egen profil.
- Interna anteckningar visas endast för profilens ägare.
- Avstängda konton kan inte fortsätta genom gamla sessioner.
- Flask kräver en extern `SECRET_KEY`.
- Produktionscookies använder `Secure`, `HttpOnly` och `SameSite=Lax`.
- Python-beroenden uppdaterades efter `pip-audit`.
- `pip` tas bort ur runtime-imagen för mindre attackyta.

## Kubernetes Secret

Jonny verifierade på `team2-primary` att hans OS Login-identitet får skapa
Secrets i namespace `default`. `company-website-secrets` skapades därefter
med datanyckeln `secret-key`. Endast namn och längd verifierades; värdet
visades inte, dokumenterades inte och lades inte i Git. Detta är Flasks
sessionsnyckel och inte en GCP Service Account Key.

## Tester

- 19 Pytest-tester passerade.
- `pip check` rapporterade inga konflikter.
- `pip-audit` rapporterade inga kända sårbarheter i deklarerade Python-paket.
- Bandit rapporterade inga kodfynd.
- YAML, Docker Compose och renderat Kubernetes-manifest validerades.
- Applikationen stoppades utan `SECRET_KEY` och startade med en testnyckel.
- `/healthz` rapporterade `healthy` med ansluten databas.
- CycloneDX 1.5 genererades från den lokala imagen.
- Imagen minskades från 158 till 139 identifierade komponenter.

Docker Scout minskade från sju High-fynd till två. De återstående gäller
Debian-paketen `perl` och `zlib`, där ingen fixversion anges. De följs som
rest-risk tills basimagen kan uppdateras.

## GitHub Actions

`Application Checks` kör tester och Docker-build på feature-branches och PR
utan publicering eller deployment. Senaste körningen lyckades på 18 sekunder:

- [Application Checks 36404525054](https://github.com/itsx25-team2/company-website/actions/runs/36404525054)

`actions/checkout` och `actions/setup-python` uppdaterades till version 7
efter GitHubs varning om utfasad Node.js 20.

## Spårbarhet

- `f26903e`: integrering av utbildarens Workshop 4-version.
- `fecfc53`: första härdning av autentisering och e-postförhandsvisning.
- `47eb0bb`: sessions-, CSRF-, dependency- och branchhärdning.
- `d237f53`: uppdatering av centrala GitHub Actions.

Branchen är pushad och grön men ännu inte mergad. `main` och aktiv deployment
är därför oförändrade.

## Nästa steg

1. Skapa PR från `workshop4/instructor-sync` till `main`.
2. Invänta minst två godkännanden.
3. Merga och följ deployment-workflowen.
4. Verifiera rollout, `/healthz`, SBOM-attestering och Cosign-signatur.
5. Sätt backlogpunkterna till `Done` först efter verifierad deployment.
